# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause

# IMPORTANT NOT ON ORIGIN OF PARTS OF COMMENTS/DOCS:
#   EVERYTHING PREFIXED WITH `SPEC:` AND BACK-TICK-QUOTED TEXT IS TAKEN ON 2025-11-16 DIRECTLY FROM 
#   [Qingping Products Data Reporting Protocol](https://qingping.feishu.cn/docx/BlYOdJVRQobV0ox6SNZcV8V6nZT)
#   WHICH IS OFFICIAL DOCUMENTATION PUBLISHED BY QINGPING. EVEN THEY ARE NOT 100% SURE.

# FIXME: implement `New Protocol V2 Sensor Data Format Description`

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .base import (
  Protocol,
  ProtocolMessage,
  ProtocolMessageDirection,
  ProtocolMessageCategory,
  SensorReading,
  SensorReadingsContainer,
  SensorReadingType,
  SensorReadingsContext,
  SensorType,
  SensorReadingStatus,
  DeviceCommand
)
from .hex_spec import (
  HexFieldFormats,
  HexCommand,
  HexKey
)
from qingping_iot_mqtt.protocols.common_spec import ProtocolName


@dataclass
class HexPayloadEntry:
  """Representation of single TLV entry in HEX protocol payload."""
  key:    HexKey
  key_raw: int
  length: int
  value:  bytes
  
  def __str__(self) -> str:
    return f"HexPayloadEntry(key=0x{self.key_raw:02X}, alias={self.key.name}, length={self.length}, value=0x{self.value.hex()})"
  def dump(self) -> str:
    msg = self.__str__()
    if self.key.fmt == HexFieldFormats.LV_STRING:
      try:
        str_value = self.value.decode('utf-8')
        msg += f" -> (string='{str_value}')"
      except UnicodeDecodeError:
        msg += " -> (invalid UTF-8 string)"
    elif self.key.fmt == HexFieldFormats.MINUTES:
      msg += f" ->  (int={int.from_bytes(self.value, 'little', signed=False)} minutes)"
    elif self.key.fmt == HexFieldFormats.SECONDS:
      msg += f" ->  (int={int.from_bytes(self.value, 'little', signed=False)} seconds)"
    # FIXME: add more formats as needed # FIXME: move to HexKey formatter/extractor or somewhere else?
    return msg

@dataclass
class HexPayload():
  """Representation of decoded HEX protocol payload, which is series of TLVs.
  
  HEX Protocol spec: section 2 "Protocol DefinitionFormat" - "PAYLOAD FORMAT" table
  Spec guanrantees TLV: 1B Key + 2B Length + Length B Value, so no extra parsing is needed beyond that.
  Responsibility of interpreting values is on higher-level logic.
  """
  entries: Iterable[HexPayloadEntry]
  def __init__(self, raw: bytes):
    self.entries = []
    offset = 0
    while offset < len(raw):
      key = HexKey.UNKNOWN
      try:
        key = HexKey(raw[offset])
      except ValueError:
        key = HexKey.UNKNOWN
      length = int.from_bytes(raw[offset+1:offset+3], 'little')
      value = raw[offset+3:offset+3+length]
      
      entry = HexPayloadEntry(key=key, key_raw=raw[offset], length=length, value=value)
      self.entries.append(entry)
      
      offset += 3 + length
  
  @staticmethod
  def construct_payload(entries: Iterable[HexPayloadEntry]) -> bytes:
    """Constructs HEX payload from TLV entries."""
    body = bytearray()
    for entry in entries:
      body.append(entry.key.value)
      body += entry.length.to_bytes(2, 'little')
      body += entry.value
    return bytes(body)

class HexFrameError(Exception):
  """Exception raised on HEX frame parsing errors."""
  pass
class HexFrame:
  """Representation of raw HEX protocol frame split to raw fields.
  
  HEX Protocol spec: section 2 "Protocol Format" - "PROTOCOL FORMAT" table
  """
  
  magic = b'\x43\x47' # 'CG' as per protocol

  frame:        bytes # stores raw frame data
  frame_length: int   # total length of the frame in bytes
  
  # frame split fields 
  sop:             int   # bytes 1-2     "SOP" in spec, must match HexFrame.magic
  cmd:             int   # byte  3,      "CMD" in spec, 
  payload_length:  int   # bytes 4-5,    number of bytes in "PAYLOAD" field
  payload_raw:     bytes # bytes 6-var,  "PAYLOAD" in spec
  checksum:        int   # last 2 bytes, "The sum of all contents from the frame header to the previous byte of the check digit.""
  
  # contents
  payload:         HexPayload  # parsed payload
  
  def __init__(self, raw: bytes):
    self.frame = raw
    self.frame_length = len(raw)
    if len(raw) < 7:
      raise HexFrameError(f"HEX frame too short: expected at least 7 bytes, got {len(raw)} bytes")
    
    self.sop = int.from_bytes(raw[0:2], 'little')
    if self.sop != int.from_bytes(self.magic, 'little'):
      raise HexFrameError(f"Invalid HEX frame magic/SOP: expected {self.magic.hex()}, got {raw[0:2].hex()}")
    
    self.cmd = raw[2]
    
    self.payload_length = int.from_bytes(raw[3:5], 'little')
    if self.payload_length + 7 != len(raw):
      raise HexFrameError(f"HEX frame length mismatch: expected {self.payload_length + 7} bytes, got {len(raw)} bytes")
    
    self.payload_raw = raw[5:5+self.payload_length]
    
    self.checksum = int.from_bytes(raw[5+self.payload_length:7+self.payload_length], 'little')
    checksum_calc = sum(raw[0:5+self.payload_length]) & 0xFFFF
    if self.checksum != checksum_calc:
      raise HexFrameError(f"HEX frame checksum mismatch: expected {self.checksum:04X}, calculated {checksum_calc:04X}")
    
    self.payload = HexPayload(self.payload_raw)
  
  @classmethod
  def construct_frame(cls, cmd: int, payload: bytes) -> HexFrame:
    """Constructs HEX frame from command and payload."""
    body = bytearray()
    body += cls.magic
    body.append(cmd)
    body += len(payload).to_bytes(2, 'little')
    body += payload
    checksum = sum(body) & 0xFFFF
    body += checksum.to_bytes(2, 'little')
    return cls(bytes(body))
  def __str__(self) -> str:
    return f"HexFrame(cmd=0x{self.cmd:02X}, payload_length={self.payload_length}, checksum=0x{self.checksum:04X})"
  def dump(self) -> str:
    msg = self.__str__()
    msg += f"  {self.frame.hex()}"
    return msg
class HexProtocolMesssage(ProtocolMessage):
  """Representation of decoded HEX protocol message."""
  frame: HexFrame
  def __init__(self, direction: ProtocolMessageDirection, body: bytes):
    self.body = body
    self.frame = HexFrame(body)
    self.direction = direction
    if self.frame.cmd in [
      HexCommand.DATA_UPLOADING,
      HexCommand.EVENT_REPORTING,
      HexCommand.REAL_TIME_DATA_UPLOADING,
    ]:
      self.category = ProtocolMessageCategory.READINGS
    
    elif self.frame.cmd in [
      HexCommand.CONFIGURATION_SENDING,
      HexCommand.CONFIGURATION_REPORTING
    ]:
      self.category = ProtocolMessageCategory.SETTINGS
    
    
    elif self.frame.cmd in [
      HexCommand.FIRMWARE_UPGRADE,
    ]:
      self.category = ProtocolMessageCategory.COMMAND
    
    elif self.frame.cmd in [
      HexCommand.NETWORK_ACCESS_SETTING,
    ]:
      self.category = ProtocolMessageCategory.REPROVISION
    
    else:
      raise HexFrameError(f"Unknown HEX command in frame: {self.frame.cmd:02X}")
  def dump(self) -> str:
    msg = f"HexProtocolMessage(direction={self.direction.name}, category={self.category.name}, raw_cmd={self.frame.cmd:2X}, body_len={len(self.body)} bytes>"
    for entry in self.frame.payload.entries:
      msg += f"\n  - {entry.dump()}"
    return msg

class HexSensorReadingMessageError(Exception):
  """Exception raised on HEX sensor reading message parsing errors."""
  pass
class HexSensorReadingMessage(SensorReadingsContainer):
  """Representation of sensor reading container from HEX protocol message."""
  
  @staticmethod
  def decode_timestamp(data: bytes) -> int:
    """Decodes 4-byte timestamp to int.
    
    SPEC section 4.4 "Event Reporting" -> "Events that can be reported (not limited to the following items, parsed with the actual KEY):"
    """
    if len(data) < 6:
      raise HexSensorReadingMessageError(f"Invalid payload length: expected at least 6 bytes, got {len(data)} bytes")
    ts = int.from_bytes(data[0:4], byteorder="little")
    return ts
  @staticmethod
  def decode_interval(data: bytes) -> int:
    """Decodes 2-byte interval to int.
    
    SPEC section 4.1 "Data Uploading" -> "Description of historical data content parsing:"
    """
    if len(data) < 6:
      raise HexSensorReadingMessageError(f"Invalid payload length: expected at least 6 bytes, got {len(data)} bytes")
    interval = int.from_bytes(data[4:6], byteorder="little")
    return interval
  
  @staticmethod
  def decode_signal_strength(data: bytes) -> int:
    """Decodes 1-byte `signal strength` to int. This should only be called for TLV HexKey.HEADER_REALTIME_DATA
    
    SPEC section 4.4 "Event Reporting" -> "Events that can be reported (not limited to the following items, parsed with the actual KEY):"
    """
    if len(data) != 12:
      raise HexSensorReadingMessageError(f"Invalid payload length: expected 12 bytes, got {len(data)} bytes")
    signal = int.from_bytes(data[10:11], byteorder="little", signed=True)
    return signal
  
  @staticmethod
  def decode_sensor_data_group(data: bytes, start: int = 4, length: int=6) -> Iterable[SensorReading]:
    """Decodes single sensor data group (6B or 8B) to sensor readings.
    
    SPEC section 4.1 "Data Uploading" -> "Sensor data parsing instructions:"
    """
    readings = []
    if length not in [6, 8]:
      raise HexSensorReadingMessageError(f"Invalid sensor data group length: expected 6 or 8 bytes, got {len(data)} bytes")
    if len(data) < start+length:
      raise HexSensorReadingMessageError(f"Invalid data length: expected at least {start+length} bytes, got {len(data)} bytes")
    packed = int.from_bytes(data[start:start+3], byteorder="little")
    
    humidity_raw = packed & 0x0FFF
    humidity_permille = humidity_raw
    reading_humi = SensorReading(
      sensor=SensorType.HUMIDITY,
      value=humidity_permille / 10.0,
      unit="%"
    )
    readings.append(reading_humi)
    
    
    temperature_raw = (packed >> 12) & 0x0FFF
    temperature_dc = temperature_raw - 500
    reading_temp = SensorReading(
      sensor=SensorType.TEMPERATURE,
      value=temperature_dc / 10.0,
      unit="°C"
    )
    readings.append(reading_temp)
    
    third_sensor_raw = int.from_bytes(data[start+3:start+5], byteorder="little")
    """this fields is one of two:
    1) SPEC: The air pressure is magnified 100 times, and the unit is kPa." 
      -> data stored as raw is in 0.1hPa = daPa
      -> CGP23W states range 30-125kPa = 3000 - 12500 daPa, lowest non-lab recorded pressure on Earth is 870hPa = 8700 daPa
    2) SPEC: Maybe CO2 depends on product
      -> data stored as raw is in ppm
      -> CGP22C states range 400-9999 ppm, 9999 is reported as max value, but all values up to 9999 can be easily generated by user
    
    this cannot be decided on such low level, so higher-level logic must decide which sensor it is based on device model or value ranges
    therefore, both sensors are created here and higher-level logic must pick the correct one
    """
    reading_co2 = SensorReading(
      sensor=SensorType.CO2,
      value=third_sensor_raw,
      unit="ppm"
    )
    readings.append(reading_co2)
    reading_pressure = SensorReading(
      sensor=SensorType.PRESSURE,
      value=third_sensor_raw / 10.0,
      unit="hPa"
    )
    readings.append(reading_pressure)
    
    battery_raw = int.from_bytes(data[start+5:start+6], byteorder="little")
    reading_battery = SensorReading(
      sensor=SensorType.BATTERY,
      value=battery_raw,
      unit="%"  # SPEC: battery percentage
    )
    readings.append(reading_battery)
    
    if length == 8: # SPEC: section 4.1 "Data Uploading" -> "Sensor data parsing instructions:" - `This item is only available for specified products.`
      packed_aux = int.from_bytes(data[start+6:start+8], byteorder="little")
      if packed_aux != 0xFFFF: # SPEC: `The value is 0xFFFF means no external humidity sensor.`
      
        humidity_aux_raw = packed_aux & 0x0FFF
        humidity_aux_permille = humidity_aux_raw
        reading_humi_aux = SensorReading(
          sensor=SensorType.HUMIDITY_AUX,
          value=humidity_aux_permille / 10.0,
          unit="%"
        )
        readings.append(reading_humi_aux)
        
        temperature_aux_raw = (packed_aux >> 12) & 0x0FFF
        temperature_aux_dc = temperature_aux_raw - 500
        reading_temp_aux = SensorReading(
          sensor=SensorType.TEMPERATURE_AUX,
          value=temperature_aux_dc / 10.0,
          unit="°C"
        )
        readings.append(reading_temp_aux)
    return readings
  
  def __init__(self, message: ProtocolMessage):
    self.category = message.category
    if not isinstance(message, HexProtocolMesssage):
      raise ValueError("Can only construct HexSensorReadingMessage from HexProtocolMesssage")
    self.readings = []
    if message.category != ProtocolMessageCategory.READINGS:
      raise ValueError("HexSensorReadingMessage can only be constructed from READINGS message")
    for entry in message.frame.payload.entries:
      if entry.key in [
        HexKey.HEADER_HISTORICAL_DATA_6B,
        HexKey.HEADER_HISTORICAL_DATA_8B
      ]:
        # SPEC section 4.1 "Data Uploading" -> "Description of historical data content parsing:" - as-is
        # SPEC section 4.1 "Data Uploading" -> "Sensor data parsing instructions:" - temp, humidity is fine, co2 vs pressure could be drived from values making sense, but what about other sensors? are they reported only from events?
        length = 6 if entry.key == HexKey.HEADER_HISTORICAL_DATA_6B else 8 
        timestamp = HexSensorReadingMessage.decode_timestamp(entry.value)
        interval  = HexSensorReadingMessage.decode_interval(entry.value) # 
        
        if len(entry.value) != entry.length:
          raise HexSensorReadingMessageError(f"Invalid historical data payload length: expected {entry.value} bytes from TLV, got {len(entry.value)} bytes")
        if (len(entry.value) - 6) % length != 0:
          raise HexSensorReadingMessageError(f"Invalid historical data payload length: expected multiple of {length} bytes for sensor data groups, got {len(entry.value)-6} bytes")
        entry_count = (len(entry.value) - 6) // length
        for entry_index in range(entry_count):
          sensor_data_start = 6 + entry_index * length
          sensor_readings = HexSensorReadingMessage.decode_sensor_data_group(entry.value, start=sensor_data_start, length=length)
          readings_context = SensorReadingsContext(readings=sensor_readings, origin=SensorReadingType.HISTORICAL, timestamp=timestamp+entry_index*interval)
          self.readings.append(readings_context)
      elif entry.key == HexKey.HEADER_EVENT_ALERT:
        # SPEC -> `1 byte event ID + 4 byte event value.` this is kind of duplicate of EVT_*
        event_id = int.from_bytes(entry.value[0:1], byteorder="little")
        event_value = entry.value[1:5]
        raise NotImplementedError(f"Event alert parsing not implemented yet, but found event id=0x{event_id:02X}, event_value=0x{event_value.hex()}")
      elif entry.key in [
        HexKey.EVT_BATTERY_LOW,
        HexKey.EVT_TEMPERATURE_HIGHER,
        HexKey.EVT_TEMPERATURE_LOWER,
        HexKey.EVT_HUMIDITY_HIGHER,
        HexKey.EVT_HUMIDITY_LOWER,
        HexKey.EVT_PRESSURE_HIGHER,
        HexKey.EVT_PRESSURE_LOWER,
        HexKey.EVT_AUXTEMP_HIGHER,
        HexKey.EVT_AUXTEMPT_LOWER,
        HexKey.EVT_CO2_HIGHER,
        HexKey.EVT_CO2_LOWER,
        HexKey.EVT_TVOC_HIGHER,
        HexKey.EVT_TVOC_LOWER,
        HexKey.EVT_PM25_HIGHER,
        HexKey.EVT_PM25_LOWER,
        HexKey.EVT_PM10_HIGHER,
        HexKey.EVT_PM10_LOWER,
        HexKey.EVT_NOISE_HIGHER,
        HexKey.EVT_NOISE_LOWER
      ]:
        # SPEC section 4.4 "Event Reporting" -> "Events that can be reported (not limited to the following items, parsed with the actual KEY):" -> HexKey.EVT_*
        timestamp = HexSensorReadingMessage.decode_timestamp(entry.value)
        event_setting_value = int.from_bytes(entry.value[10:12], byteorder="little")
        sensor_readings = HexSensorReadingMessage.decode_sensor_data_group(entry.value)
        for r in sensor_readings:
          if entry.key.associated_sensor == r.sensor:
            r.status = SensorReadingStatus.ABNORMAL
            r.level = event_setting_value
        readings_context = SensorReadingsContext(readings=sensor_readings, origin=SensorReadingType.EVENT, timestamp=timestamp)
        self.readings.append(readings_context)
      elif entry.key == HexKey.HEADER_REALTIME_DATA:
        # SPEC section 4.4 "Event Reporting" -> "Events that can be reported (not limited to the following items, parsed with the actual KEY):"  -> 0x14
        realtime_readings = list(HexSensorReadingMessage.decode_sensor_data_group(entry.value))
        timestamp = HexSensorReadingMessage.decode_timestamp(entry.value)
        signal_raw = HexSensorReadingMessage.decode_signal_strength(entry.value)
        signal = SensorReading(sensor=SensorType.SIGNAL_STRENGTH, value=signal_raw, unit="dBm") # FIXME: unit?
        realtime_readings.append(signal)
        readings_context = SensorReadingsContext(readings=realtime_readings, origin=SensorReadingType.REALTIME, timestamp=timestamp)
        self.readings.append(readings_context)
      else:
        pass
        #raise HexSensorReadingMessageError(f"Unknown HEX sensor reading entry key: {entry.key}")
    pass

class HexRawCommand(DeviceCommand):
  payload: bytes
  def __init__(self, command: int, parameters: Mapping[str, bytes]):
    self.command = command
    self.payload = parameters.get('payload', b'')
  def encode(self) -> HexFrame:
    frame = HexFrame.construct_frame(cmd=self.command, payload=self.payload)
    return frame
  def dump(self) -> str:
    msg = f"HexRawCommand(command=0x{self.command:02X}, payload_length={len(self.payload)})"
    msg += f"\n  {self.payload.hex()}"
    return msg
class HexCommandRequestSettings(HexRawCommand):
  def __init__(self):
    super().__init__(command=HexCommand.CONFIGURATION_SENDING, parameters={})

class HexProtocol(Protocol):#
  name = ProtocolName.HEX.name
  version = "1.0"

  def decode_message(self, message: bytes, direction: ProtocolMessageDirection) -> ProtocolMessage:
    return HexProtocolMesssage(direction, message)
  
  @classmethod
  def encode_message(cls, message: ProtocolMessage) -> bytes:
    if not isinstance(message, HexProtocolMesssage):
      raise ValueError("Can only encode HexProtocolMesssage")
    return message.frame.frame