# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause

# IMPORTANT NOT ON ORIGIN OF PARTS OF COMMENTS/DOCS:
#   EVERYTHING PREFIXED WITH `SPEC:` AND BACK-TICK-QUOTED TEXT IS TAKEN ON 2025-11-22 DIRECTLY FROM 
#   [Qingping MQTT Protocol](https://developer.qingping.co/private/communication-protocols/public-mqtt-json)
#   WHICH IS OFFICIAL DOCUMENTATION PUBLISHED BY QINGPING. EVEN THEY ARE NOT 100% SURE.

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, time, timezone

from enum import Enum, IntEnum, StrEnum
from typing import Optional
import typing

from .base import (
  SensorReading,
  SensorReadingType,
  SensorReadingsContext,
  SensorType,
  SensorReadingStatus
)

import logging
logger = logging.getLogger(__name__)


class JsonField():
  """Abstract base class for JSON protocol field value."""
  value: typing.Any
  def qp_json_encode(self) -> object:
    """encode to format used in JSON protocol messages"""
    raise NotImplementedError("Not implemented yet")
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonField:
    """decode from format used in JSON protocol messages"""
    raise NotImplementedError("Not implemented yet")

@dataclass(init=False)
class JsonDurationSeconds(JsonField):
  seconds: int
  duration: timedelta
  def __init__(self, seconds: int) -> None:
    self.seconds = seconds
    self.duration = timedelta(seconds=seconds)
  @staticmethod
  def from_timedelta(duration: timedelta) -> JsonDurationSeconds:
    seconds = int(duration.total_seconds())
    return JsonDurationSeconds(seconds)
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonDurationSeconds:
    if not isinstance(data, int):
      raise ValueError("Invalid data type for JsonDurationSeconds")
    return JsonDurationSeconds(data)
  def qp_json_encode(self) -> int:
    """encode to format used in JSON protocol messages"""
    return self.seconds

@dataclass(init=False)
class JsonTime:
  minutes_from_midnight: int
  time: time
  def __init__(self, minutes_from_midnight: int) -> None:
    self.minutes_from_midnight = minutes_from_midnight
    if not (0 <= minutes_from_midnight < 24 * 60):
      raise ValueError("Invalid number of minutes from midnight")
    hours = minutes_from_midnight // 60
    minutes = minutes_from_midnight % 60
    self.time = time(hour=hours, minute=minutes)
  @staticmethod
  def from_time(t: time) -> JsonTime:
    minutes_from_midnight = t.hour * 60 + t.minute
    return JsonTime(minutes_from_midnight)
  def qp_json_encode(self) -> int:
    """encode to format used in JSON protocol messages"""
    return self.minutes_from_midnight

@dataclass(init=False)
class JsonTimestamp(JsonField):
  timestamp: int
  dt: datetime
  def __init__(self, timestamp: int) -> None:
    self.timestamp = timestamp
    self.dt = datetime.fromtimestamp(self.timestamp, timezone.utc)
  @staticmethod
  def from_datetime(dt: datetime) -> JsonTimestamp:
    timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())
    return JsonTimestamp(timestamp)
  def qp_json_encode(self) -> int:
    """encode to format used in JSON protocol messages"""
    return self.timestamp
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonTimestamp:
    if not isinstance(data, int):
      raise ValueError("Invalid data type for JsonTimestamp")
    return JsonTimestamp(data)


class JsonResult(IntEnum):
  """JSON protocol result codes.
  
  JSON Protocol spec: 2.2.5 "Result Code of Command List"
  """
  SUCCESS = 1
  CONNECTION_TIMEOUT = -1
  BLUETOOTH_BUSY = -2
  WRITE_DATA_FAILED = -3
  READ_DATA_FAILED = -4
  OPEN_BLE_NOTIFICATION_FAILED = -5
  CLOSE_BLE_NOTIFICATION_FAILED = -6
  UNBINDING_DEVICE = -7
  CONNECT_EXCEPTION = -8
  DEVICE_OFFLINE = -9
  SPARROW_UNBINDING = -10
class JsonFieldResult(JsonField):
  result: JsonResult
  def __init__(self, result: JsonResult) -> None:
    self.result = result
  def qp_json_encode(self) -> int:
    return self.result.value
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonFieldResult:
    if not isinstance(data, int):
      raise ValueError("Invalid data type for JsonFieldResult")
    try:
      result = JsonResult(data)
    except ValueError:
      raise ValueError("Invalid result value for JsonFieldResult")
    return JsonFieldResult(result)

class JsonCommand(StrEnum):
  """JSON protocol command identifiers. Some of them are bi-directional.
  
  JSON Protocol spec: section 2.2.4 "Command Type Support List"
  Spec says `Integer`, but in practice it's always string.
  """
  BLE_CONNECTION_REQUEST = "1"
  BLE_DISCONNECTION_REQUEST = "2"
  BLE_OPEN_NOTIFICATION_REQUEST = "3"
  BLE_CLOSE_NOTIFICATION_REQUEST = "4"
  BLE_NOTIFICATION_RESPONSE = "5"
  BLE_DATA_TRANSMISSION_EXPECT_RESPONSE = "6"
  BLE_DATA_TRANSMISSION_IGNORE_RESPONSE = "15"
  BLE_DATA_RECEIPT = "7"
  BLE_DATA_RESPONSE = "8"
  BLE_DATA_BROADCAST = "9"
  
  DEVICE_LIST_REQUEST = "10"
  DEVICE_LIST_NAMED_REQUEST = "25"
  DEVICE_LIST_RESPONSE = "11"
  DEVICE_LIST_NAMED_RESPONSE = "26"
  
  REALTIME_DATA = "12"
  """Either real-time data sent by device, or request for temporary rapid reporting sent to device."""
  HISTORICAL_DATA_OR_SETTINGS = "17"
  """Either historical data sent by device, or request to set configuration sent to device."""
  DATA_ACK = "18"
  """Acknowledgment of data receipt - historical or events."""
  
  HEARTBEAT = "13"
  
  MQTT_RECONNECT = "14"
  MQTT_RECONFIGURE = "16"
  
  DEVICE_REPORT_LOG = "19"
  
  BINDING_STATUS = "20"
  BINDING_STATUS_EXTERNAL = "27"
  
  OTA_COMMAND = "23"
  OTA_RESPONSE = "24"
  
  SETTINGS_REPORT = "28"
  """Request and report of current device settings."""
  
  NOTIFICATION = "32"
  """Scene/alert notifications sent by device or their settings sent to device. This is not mentioned in table."""
  ALARM = "40"
  """Alarms for alarm clocks. This is not mentioned in table."""

class JsonCommandContainer(JsonField):
  command: JsonCommand
  value: JsonCommand
  def __init__(self, command: JsonCommand) -> None:
    self.command = command
    self.value = command
  def qp_json_encode(self) -> str:
    return self.command.value
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonCommandContainer:
    if not isinstance(data, str):
      raise ValueError("Invalid data type for JsonCommandContainer")
    try:
      command = JsonCommand(data)
    except ValueError:
      raise ValueError("Invalid command value for JsonCommandContainer")
    return JsonCommandContainer(command)

@dataclass
class JsonDeviceNamed:
  mac: str
  name: str
  def qp_json_encode(self) -> dict[str, str]:
    """encode to format used in JSON protocol messages"""
    return asdict(self)
@dataclass
class JsonMqttConfig(JsonField):
  host: str
  port: int
  usrname: str
  """this is originaly typoed as 'usrname' in Qingping spec, cannot confirm validity"""
  password: str
  clientid: str
  subscribe_topic: str
  publish_topic: str
  def qp_json_encode(self) -> dict[str, object]:
    """encode to format used in JSON protocol messages"""
    return asdict(self)
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonMqttConfig:
    if not isinstance(data, dict):
      raise ValueError("Invalid data type for JsonMqttConfig")
    try:
      host = str(data["host"])
      port = int(data["port"])
      usrname = str(data["usrname"])
      password = str(data["password"])
      clientid = str(data["clientid"])
      subscribe_topic = str(data["subscribe_topic"])
      publish_topic = str(data["publish_topic"])
    except KeyError as e:
      raise ValueError(f"Missing key in JsonMqttConfig: {e}")
    except (TypeError, ValueError) as e:
      raise ValueError(f"Invalid value type in JsonMqttConfig: {e}")
    return JsonMqttConfig(
      host=host,
      port=port,
      usrname=usrname,
      password=password,
      clientid=clientid,
      subscribe_topic=subscribe_topic,
      publish_topic=publish_topic
    )
@dataclass
class JsonWifiConfig(JsonField):
  SSID: str
  PASSWORD: str
  def qp_json_encode(self) -> dict[str, str]:
    return asdict(self)
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonWifiConfig:
    if not isinstance(data, dict):
      raise ValueError("Invalid data type for JsonWifiConfig")
    try:
      ssid = str(data["SSID"])
      password = str(data["PASSWORD"])
    except KeyError as e:
      raise ValueError(f"Missing key in JsonWifiConfig: {e}")
    except (TypeError, ValueError) as e:
      raise ValueError(f"Invalid value type in JsonWifiConfig: {e}")
    return JsonWifiConfig(
      SSID=ssid,
      PASSWORD=password
    )

@dataclass
class JsonSensorDataSubEntry:
  """Single sensor data entry in device sensor information.
  
  JSON Protocol spec: section 2.2.2 "Device Sensor Data Format - Sub-Structure format"
  """
  value: float | int
  """spec says `Integer` but it's sometimes foat and even spec contradicts itself"""
  status: Optional[SensorReadingStatus] = SensorReadingStatus.NORMAL
  level: Optional[int] = None
  """SPEC: `Sensor data level(only for some kind of sensors)`"""
  unit: Optional[str] = None
  status_duration: Optional[int] = None
  status_start_time: Optional[int] = None
  
  @classmethod
  def qp_json_decode(cls, data: dict[str, object], sensor: JsonSensorDataKeys) -> JsonSensorDataSubEntry:
    value = data.get("value")
    if value is None:
      raise ValueError("Missing 'value' key in JsonSensorDataSubEntry")
    if not isinstance(value, (int, float)):
      raise ValueError("Invalid 'value' type in JsonSensorDataSubEntry: expected int or float")
    level = data.get("level")
    if level is not None and not isinstance(level, int):
      raise ValueError("Invalid 'level' type in JsonSensorDataSubEntry: expected int")
    status_duration = data.get("status_duration")
    if status_duration is not None and not isinstance(status_duration, int):
      raise ValueError("Invalid 'status_duration' type in JsonSensorDataSubEntry: expected int")
    status_start_time = data.get("status_start_time")
    if status_start_time is not None and not isinstance(status_start_time, int):
      raise ValueError("Invalid 'status_start_time' type in JsonSensorDataSubEntry: expected int")
      
    return cls(
      value=value,
      status=SensorReadingStatus(data.get("status")) if "status" in data else SensorReadingStatus.NORMAL,
      level=level,
      unit=str(data.get("unit")) if "unit" in data else sensor.default_unit,
      status_duration=status_duration,
      status_start_time=status_start_time
    )
  
  def qp_json_encode(self) -> dict[str, object]:
    """encode to format used in JSON protocol messages (omit None fields)"""
    data = {k: v for k, v in asdict(self).items() if v is not None}
    return data
  
  
@dataclass
class JsonSensorData:
  """Device sensor information in device list named response.
  
  JSON Protocol spec: section 2.2.1 "Device Sensor Data Format"
  """
  timestamp: JsonSensorDataSubEntry
  battery: Optional[JsonSensorDataSubEntry] = None
  temperature: Optional[JsonSensorDataSubEntry] = None
  humidity: Optional[JsonSensorDataSubEntry] = None
  pm1: Optional[JsonSensorDataSubEntry] = None
  pm25: Optional[JsonSensorDataSubEntry] = None
  pm10: Optional[JsonSensorDataSubEntry] = None
  co2: Optional[JsonSensorDataSubEntry] = None
  tvoc: Optional[JsonSensorDataSubEntry] = None
  radon: Optional[JsonSensorDataSubEntry] = None
  
  def qp_json_encode(self) -> dict[str, object]:
    """nested encode to format used in JSON protocol messages (omit None fields)"""
    data = {k: v.encode() for k, v in asdict(self).items() if v is not None}
    return data
  
  @classmethod
  def qp_json_decode(cls, data: dict[str, object]) -> JsonSensorData:
    """construct JsonSensorData from dictionary (e.g. parsed from JSON)"""
    fields = {}
    for key, value in data.items():
      if not isinstance(value, dict):
        raise ValueError(f"Invalid value for JsonSensorData field {key}: expected dict, got {type(value)}")
      fields[key] = JsonSensorDataSubEntry.qp_json_decode(value, JsonSensorDataKeys(key))
    return cls(**fields)
  def to_context(self, origin: SensorReadingType) -> SensorReadingsContext:
    ctx: SensorReadingsContext
    timestamp = self.timestamp.value
    readings_entries = asdict(self)
    readings: list[SensorReading] = []
    for sensor_data_key, reading in readings_entries.items():
      try:
        sensor_type = JsonSensorDataKeys(sensor_data_key)
      except Exception:
        continue
      if sensor_type is not None and reading is not None:
        sd: JsonSensorDataSubEntry = JsonSensorDataSubEntry.qp_json_decode(reading, JsonSensorDataKeys(sensor_data_key))
        unit = sd.unit
        if unit is None or unit == str(None):
          unit = sensor_type.default_unit
        readings.append(SensorReading(sensor=sensor_type.associated_sensor,
                                      value=sd.value,
                                      unit=unit,
                                      status=sd.status or SensorReadingStatus.NORMAL,
                                      level=sd.level,
                                      status_duration=sd.status_duration,
                                      status_start_time=sd.status_start_time
                                     ))
    ctx = SensorReadingsContext(
      origin=origin,
      timestamp=int(timestamp),
      readings=readings
    )
    return ctx

  def dump(self) -> str:
    msg = "JsonSensorData:"
    for key, value in asdict(self).items():
      if value is not None:
        msg += f"\n  - {key}: {value}"
    return msg
    

@dataclass
class JsonWiFiInfo(JsonField):
  """WiFi information structure.
  
  JSON Protocol spec: section 3.13 "Heartbeat Package"
  """
  ssid: str
  rssi: int
  channel: int
  bssid: str
  @classmethod
  def qp_json_decode(cls, data) -> JsonWiFiInfo:
    if not isinstance(data, str):
      raise ValueError("Invalid data type for JsonWiFiInfo")
    fields = data.split(",")
    ssid: str
    rssi: int
    channel: int
    bssid: str
    if len(fields) != 4:
      raise ValueError("Invalid WiFi info format")
    ssid = fields[0]
    try:
      rssi = int(fields[1])
    except ValueError:
      raise ValueError("Invalid RSSI value in WiFi info")
    try:
      channel = int(fields[2])
    except ValueError:
      raise ValueError("Invalid channel value in WiFi info")
    bssid = fields[3]
    return cls(ssid=ssid, rssi=rssi, channel=channel, bssid=bssid)
    
  def qp_json_encode(self) -> str:
    """encode to format used in JSON protocol messages (omit None fields)"""
    return f"{self.ssid},{self.rssi},{self.channel},{self.bssid}"


@dataclass(init=False)
class JsonLedThresholds:
  """LED thresholds represented as comma-separated string of integers."""
  # TODO: implement conversion to LED colors (some lists are 3, some 5 values long and maybe others as well)
  thresholds: list[int]
  @staticmethod
  def from_list(values: list[int]) -> JsonLedThresholds:
    # TODO: support direct creation from list of sensors, not magicaly scaled ints
    obj = JsonLedThresholds.__new__(JsonLedThresholds)
    obj.thresholds = values
    return obj
  def qp_json_encode(self) -> str:
    """encode to format used in JSON protocol messages (omit None fields)"""
    return ",".join(str(v) for v in self.thresholds)
  def __init__(self, csv: str) -> None:
    self.thresholds = []
    for part in csv.split(","):
      try:
        value = int(part)
      except ValueError:
        raise ValueError(f"Invalid LED threshold value: {part}")
      self.thresholds.append(value)

@dataclass(init=False)
class JsonSettings(JsonField):
  """JSON protocol device settings.
  
  JSON Protocol spec: section 2.2.3 Device Setting Format Specification
  This is based on mix of official docs and reverse engineering, so may be incomplete.
  All fields are optional as devices may support different settings and setting requests may contain only subset of them.
  Only exception is `raw_settings` which contains all settings as received in JSON message for future reference.
  """
  
  raw_settings: dict[str, object]
  """Raw settings dictionary as received in JSON message"""
  
  # officially documented settings
  report_interval: Optional[int] = None
  """official SPEC: `Sensor data report interval`"""
  collect_interval: Optional[int] = None
  """official SPEC: `Sensor data acquisition interval`"""
  co2_sampling_interval: Optional[int] = None
  """official SPEC: `CO2 sensor acquisition interval`"""
  pm_sampling_interval: Optional[int] = None
  """official SPEC: `PM2.5 PM10 sensor acquisition interval`"""
  temperature_unit: Optional[str] = None
  """official SPEC: `temperature unit setting`
  
  observed as 'C' or 'F'"""
  night_mode_start_time: Optional[int] = None
  """official SPEC: `start time for night mode(minutes from 00:00)`"""
  night_mode_end_time: Optional[int] = None
  """official SPEC: `end time fro night mode(minutes from 00:00)`"""
  
  # other settings observed in real devices but not documented in official Qingping docs
  power_off_time: Optional[int] = None
  """observed on battery-powered devices: time after which device powers off automatically when not connected"""
  display_off_time: Optional[int] = None
  """observed on OLED devices: time after which display switches to screensaver"""
  auto_slideing_time: Optional[int] = None
  """observed on OLED devices: time after which display auto-slides to next screen"""
  screensaver_type: Optional[int] = None # TODO: reverse engineer enum
  """observed on OLED devices: some form of IntEnum
  
  observed values:
  - 1 - current reading bounces around like old DVD logo
  """
  page_sequence: Optional[str] = None # TODO: implement better structure
  """observed on OLED devices: comma-separated list of screen IDs indicating order of screens to display
  
  last item must be equal to first one to form loop; example `pm25,pm10,co2,temp,pm25`
  """
  
  temp_led_th: Optional[JsonLedThresholds] = None
  """observed on LED enabled devices: temperature LED threshold levels as list of integers with values x100
  
  example: `2300,2650,2800` means thresholds at 23.00°C (green?), 26.50°C (yellow), 28.00°C (red)
  """
  humi_led_th: Optional[JsonLedThresholds] = None
  """observed on LED enabled devices: humidity LED threshold levels as list of integers with values x100
  
  example: `2000,4000,6000` means thresholds at 20.00% (?), 40.00% (?), 60.00% (?)
  """
  co2_led_th: Optional[JsonLedThresholds] = None
  """observed on LED enabled devices: CO2 LED threshold levels as list of integers in ppm
  
  example: `1000,2000,3000` means thresholds at 1000ppm (green), 2000ppm (yellow), 3000ppm (red)
  """
  pm25_led_th: Optional[JsonLedThresholds] = None
  """observed on LED enabled devices: PM2.5 LED threshold levels as list of integers in µg/m³
  
  example: `35,75,115,150,250` means thresholds at 35µg/m³ (green?), 75µg/m³ (yellow?), 115µg/m³ (orange?), 150µg/m³ (red?), 250µg/m³ (purple?)
  """
  pm10_led_th: Optional[JsonLedThresholds] = None
  """observed on LED enabled devices: PM10 LED threshold levels as list of integers in µg/m³
  
  example: `50,150,250,350,450` means thresholds at 50µg/m³ (green?), 150µg/m³ (yellow?), 250µg/m³ (orange?), 350µg/m³ (red?), 450µg/m³ (purple?)
  """
  
  timezone: Optional[int] = None # TODO: reverse engineer enum
  """observed: some form of IntEnum
  
  observed values:
  - 80 - CET (but device was bootstrapped during CEST)
  """
  is_12_hour_mode: Optional[int] = None
  """observed: True if time is displayed in 12-hour mode, False for 24-hour mode (default)"""
  
  
  pm25_standard: Optional[int] = None # TODO: reverse engineer enum
  """observed on PM capable devices: some form of IntEnum
  
  observed values:
  - 0 - ???
  """
  pm25_offset: Optional[int] = None # TODO: reverse engineer
  """observed on PM capable devices: PM2.5 sensor offset (but unclear if absolute or relative)"""
  pm25_zoom: Optional[int] = None # TODO: reverse engineer
  """observed on PM capable devices: unclear what this does"""
  pm25_calib_mode: Optional[int] = None # TODO: reverse engineer
  """observed on PM capable devices: unclear what this does"""
  pm10_offset: Optional[int] = None # TODO: reverse engineer
  """observed on PM capable devices: PM10 sensor offset (but unclear if absolute or relative)"""
  pm10_zoom: Optional[int] = None # TODO: reverse engineer
  """observed on PM capable devices: unclear what this does"""
  
  co2_asc: Optional[int] = None
  """observed on CO2 capable devices: True if automatic self-calibration is enabled, False otherwise"""
  co2_offset: Optional[int] = None # TODO: reverse engineer
  """observed on CO2 capable devices: CO2 sensor offset (but unclear if absolute or relative)"""
  co2_zoom: Optional[int] = None # TODO: reverse engineer
  """observed on CO2 capable devices: unclear what this does"""
  
  temperature_offset: Optional[int] = None
  """observed on temperature capable devices: temperature sensor offset (but unclear if absolute or relative)"""
  temperature_zoom: Optional[int] = None
  """observed on temperature capable devices: unclear what this does"""
  humidity_offset: Optional[int] = None
  """observed on humidity capable devices: humidity sensor offset (but unclear if absolute or relative)"""
  humidity_zoom: Optional[int] = None
  """observed on humidity capable devices: unclear what this does"""
  
  need_ack: Optional[int] = None # FIXME: confirm suspicions, this is important for continous operation
  """observed: very likely indicates whether device needs acknowledgment of historical data receipt
  
  very likely related to JsonKey.HISTORICAL_DATA_ACK
  """
  def qp_json_encode(self) -> dict[str, object]:
    """encode to format used in JSON protocol messages (omit None fields)"""
    data = {k: v for k, v in asdict(self).items() if v is not None}
    return data
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonSettings:
    if not isinstance(data, dict):
      raise ValueError("Invalid data type for JsonSettings")
    obj = JsonSettings.__new__(JsonSettings)
    obj.raw_settings = data
    for key, value in data.items():
      if hasattr(obj, key):
        setattr(obj, key, value)
    return obj

class JsonBindingStatus(IntEnum):
  """JSON protocol binding status codes.
  
  JSON Protocol spec: section 3.20 Server Sends Binding Status
  """
  BINDING = 1
  UNBINDING = 2
class JsonFieldBindingStatus(JsonField):
  status: JsonBindingStatus
  def __init__(self, status: JsonBindingStatus) -> None:
    self.status = status
  def qp_json_encode(self) -> int:
    return self.status.value
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonFieldBindingStatus:
    if not isinstance(data, int):
      raise ValueError("Invalid data type for JsonFieldBindingStatus")
    try:
      status = JsonBindingStatus(data)
    except ValueError:
      raise ValueError("Invalid binding status value for JsonFieldBindingStatus")
    return JsonFieldBindingStatus(status)
class JsonOtaType(IntEnum):
  """JSON protocol OTA update types.
  
  JSON Protocol spec: section 3.21 Server Sends OTA Command
  """
  WIFI = 0
  MCU = 1
class JsonFieldOtaType(JsonField):
  ota_type: JsonOtaType
  def __init__(self, ota_type: JsonOtaType) -> None:
    self.ota_type = ota_type
  def qp_json_encode(self) -> int:
    return self.ota_type.value
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonFieldOtaType:
    if not isinstance(data, int):
      raise ValueError("Invalid data type for JsonFieldOtaType")
    try:
      ota_type = JsonOtaType(data)
    except ValueError:
      raise ValueError("Invalid OTA type value for JsonFieldOtaType")
    return JsonFieldOtaType(ota_type)
class JsonAction(StrEnum):
  """JSON protocol action strings. This may be used for different actions.
  
  JSON Protocol spec: section 3.29 Alarm Settings
  """
  SYNC = "alarmSync"
  QUERY = "alarmQuery"
class JsonFieldAction(JsonField):
  action: JsonAction
  def __init__(self, action: JsonAction) -> None:
    self.action = action
  def qp_json_encode(self) -> str:
    return self.action.value
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonFieldAction:
    if not isinstance(data, str):
      raise ValueError("Invalid data type for JsonFieldAction")
    try:
      action = JsonAction(data)
    except ValueError:
      raise ValueError("Invalid action value for JsonFieldAction")
    return JsonFieldAction(action)

class JsonFieldInt(JsonField):
  value: int
  def __init__(self, value: int) -> None:
    self.value = value
  def qp_json_encode(self) -> int:
    return self.value
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonFieldInt:
    if not isinstance(data, int):
      raise ValueError("Invalid data type for JsonFieldInt")
    return JsonFieldInt(data)
class JsonFieldListOfInts(JsonField):
  value: list[int]
  def __init__(self, value: list[int]) -> None:
    self.value = value
  def qp_json_encode(self) -> list[int]:
    return self.value
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonFieldListOfInts:
    if not isinstance(data, list) or not all(isinstance(i, int) for i in data):
      raise ValueError("Invalid data type for JsonFieldListOfInts")
    return JsonFieldListOfInts(data)

class JsonFieldString(JsonField):
  value: str
  def __init__(self, value: str) -> None:
    self.value = value
  def qp_json_encode(self) -> str:
    return self.value
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonFieldString:
    if not isinstance(data, str):
      raise ValueError("Invalid data type for JsonFieldString")
    return JsonFieldString(data)
class JsonFieldListOfStrings(JsonField):
  value: list[str]
  def __init__(self, value: list[str]) -> None:
    self.value = value
  def qp_json_encode(self) -> list[str]:
    return self.value
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonFieldListOfStrings:
    if not isinstance(data, list) or not all(isinstance(i, str) for i in data):
      raise ValueError("Invalid data type for JsonFieldListOfStrings")
    return JsonFieldListOfStrings(data)
class JsonFieldListOfNamedDevices(JsonField):
  value: list[JsonDeviceNamed]
  def __init__(self, value: list[JsonDeviceNamed]) -> None:
    self.value = value
  def qp_json_encode(self) -> list[dict[str, str]]:
    return [d.qp_json_encode() for d in self.value]
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonFieldListOfNamedDevices:
    if not isinstance(data, list):
      raise ValueError("Invalid data type for JsonFieldListOfNamedDevices")
    devices = []
    for item in data:
      if not isinstance(item, dict):
        raise ValueError("Invalid item type in JsonFieldListOfNamedDevices: expected dict")
      devices.append(JsonDeviceNamed(
        mac=item.get("mac", ""),
        name=item.get("name", "")
      ))
    return JsonFieldListOfNamedDevices(devices)

class JsonFieldListOfSensorData(JsonField):
  value: list[JsonSensorData]
  def __init__(self, value: list[JsonSensorData]) -> None:
    self.value = value
  def qp_json_encode(self) -> list[dict[str, object]]:
    return [d.qp_json_encode() for d in self.value]
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonFieldListOfSensorData:
    if not isinstance(data, list):
      raise ValueError("Invalid data type for JsonFieldListOfSensorData")
    sensor_data_list = []
    for item in data:
      if not isinstance(item, dict):
        raise ValueError("Invalid item type in JsonFieldListOfSensorData: expected dict")
      sensor_data_list.append(JsonSensorData.qp_json_decode(item))
    return JsonFieldListOfSensorData(sensor_data_list)

class JsonFieldDict(JsonField):
  value: dict[str, object]
  def __init__(self, value: dict[str, object]) -> None:
    self.value = value
  def qp_json_encode(self) -> dict[str, object]:
    return self.value
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonFieldDict:
    if not isinstance(data, dict):
      raise ValueError("Invalid data type for JsonFieldDict")
    return JsonFieldDict(data)
class JsonFieldListOfDicts(JsonField):
  value: list[dict[str, object]]
  def __init__(self, value: list[dict[str, object]]) -> None:
    self.value = value
  def qp_json_encode(self) -> list[dict[str, object]]:
    return self.value
  @classmethod
  def qp_json_decode(cls, data: object) -> JsonFieldListOfDicts:
    if not isinstance(data, list) or not all(isinstance(i, dict) for i in data):
      raise ValueError("Invalid data type for JsonFieldListOfDicts")
    return JsonFieldListOfDicts(data)

class JsonFieldFormats(StrEnum):
  """JSON protocol message field formats.
  
  JSON Protocol spec: section 2.2 Json Formation Specification and following
  """
  INT = ("INT", JsonFieldInt)
  LIST_OF_INTS = ("LIST_OF_INTS", JsonFieldListOfInts)
  TYPE_FIELD = ("TYPE_FIELD", JsonCommandContainer)
  STRING = ("STRING", JsonFieldString)
  DEVICE_LIST = ("DEVICE_LIST", JsonFieldListOfStrings)
  """list of device MAC addresses as strings"""
  DEVICE_NAMED_LIST = ("DEVICE_NAMED_LIST", JsonFieldListOfNamedDevices)
  """list of named devices"""
  MQTT_CONFIG = ("MQTT_CONFIG", JsonMqttConfig)
  WIFI_CONFIG = ("WIFI_CONFIG", JsonWifiConfig)
  WIFI_INFO = ("WIFI_INFO", JsonWiFiInfo)
  SENSOR_DATA_LIST = ("SENSOR_DATA_LIST", JsonFieldListOfSensorData)
  SETTINGS = ("SETTINGS", JsonSettings)
  TIMESTAMP = ("TIMESTAMP", JsonTimestamp)
  SECONDS = ("SECONDS", JsonDurationSeconds)
  RESULT = ("RESULT", JsonFieldResult)
  BINDING_STATUS = ("BINDING_STATUS", JsonFieldBindingStatus)
  OTA_TYPE = ("OTA_TYPE", JsonFieldOtaType)
  BIND_PARAMS = ("BIND_PARAMS", JsonFieldDict) # TODO: implement better structure
  """binding parameters as key-value dictionary
  
  official example:
  ```
  {
    "type": "bind", //bind unbind
    "company_id": 1
  }
  ```
  """
  SCENES = ("SCENES", JsonFieldDict) # TODO: implement better structure
  """alert notification scenes as key-value dictionary
  
  official example (this is dict with single key 'scenes' mapping to list of scene dicts):
  ```
  {
    "scenes": [
      {
        "id": 328162,
        "cool_down": -1,
        "device_scene": {
          "rules": [
            {
              "sensor_item": 10,
              "operator": 1,
              "threshold_num": 226
            }
          ]
        }
      }
    ]
  }
  ```
  """
  ACTION = ("ACTION", JsonFieldAction)
  ALARMS = ("ALARMS", JsonFieldListOfDicts) # TODO: implement better structure
  """alarm clock alarms as list of alarm dicts
  
  official example:
  ```
  [
    {
      "id": 142,
      "delayable": 0,
      "enabled": 1,
      "hhmmss": 175300,
      "local_id": 3,
      "repeat": "1,2,3,4,5,6,7",
      "ringtone": "6e70b659"
    }
  ]
  ```
  """
  expected_type: JsonField
  def __new__(cls, value, expected_type) -> JsonFieldFormats:
    obj = str.__new__(cls, value)
    obj._value_ = value
    obj.expected_type = expected_type
    return obj
  def field_type(self) -> JsonField:
    return self.expected_type


class JsonSensorDataKeys(StrEnum):
  """JSON protocol sensor data keys with associated sensor types and default units.
  
  Default units are from SPEC in section 2.2.1 "Device Sensor Data Format", usually omitted from payloads.
  """
  # FIXME: unit should probably be Enum as well
  TIMESTAMP = ("timestamp", SensorType.TIMESTAMP, "")
  BATTERY = ("battery", SensorType.BATTERY, "%")
  TEMPERATURE = ("temperature", SensorType.TEMPERATURE, "°C")
  HUMIDITY = ("humidity", SensorType.HUMIDITY, "%")
  PM1 = ("pm1", SensorType.PM1, "µg/m³")
  PM25 = ("pm25", SensorType.PM25, "µg/m³")
  PM10 = ("pm10", SensorType.PM10, "µg/m³")
  CO2 = ("co2", SensorType.CO2, "ppm")
  TVOC = ("tvoc", SensorType.TVOC, "ppb")
  RADON = ("radon", SensorType.RADON, "index")

  associated_sensor: SensorType
  default_unit: str
  def __new__(cls, value, associated_sensor, default_unit: str) -> JsonSensorDataKeys:
    obj = str.__new__(cls, value)
    obj._value_ = value
    obj.associated_sensor = associated_sensor
    obj.default_unit = default_unit
    return obj 

class JsonKey(StrEnum):
  """JSON protocol message keys.
  
  JSON Protocol spec: section 2.2 Json Formation Specification
  EXTRA keys as observed in wild
  """
  
  # official keys from spec table 2.2
  TYPE =   ("type",   JsonFieldFormats.TYPE_FIELD)
  MAC =    ("mac",    JsonFieldFormats.STRING)
  BUFFER = ("buffer", JsonFieldFormats.STRING)
  LENGTH = ("length", JsonFieldFormats.INT)
  SRV_UUID = ("srv_uuid", JsonFieldFormats.STRING)
  CHR_UUID = ("chr_uuid", JsonFieldFormats.STRING)
  ADV_DATA = ("adv_data", JsonFieldFormats.STRING)
  RSSI = ("rssi", JsonFieldFormats.INT, SensorType.SIGNAL_STRENGTH)
  TIMEOUT = ("timeout", JsonFieldFormats.SECONDS)
  SW_VERSION = ("sw_version", JsonFieldFormats.STRING)
  WIFI_INFO = ("wifi_info", JsonFieldFormats.WIFI_INFO)
  UP_ITVL = ("up_itvl", JsonFieldFormats.SECONDS)
  """SPEC: `Temporary report interval(second)`"""
  DURATION = ("duration", JsonFieldFormats.SECONDS)
  """SPEC: `Temporary report duration(second)`"""
  DEV_LIST = ("dev_list", JsonFieldFormats.DEVICE_LIST)
  MQTT_CFG = ("mqtt_cfg", JsonFieldFormats.MQTT_CONFIG)
  WIFI_CFG = ("wifi_cfg", JsonFieldFormats.WIFI_CONFIG)
  SENSOR_DATA = ("sensorData", JsonFieldFormats.SENSOR_DATA_LIST)
  """SPEC says `sensor_data` in table, but then uses `sensorData` in examples and this matches observed data"""
  SETTINGS = ("setting", JsonFieldFormats.SETTINGS)
  CO2_SAMPLING_INTERVAL = ("co2_sampling_interval", JsonFieldFormats.SECONDS)
  PM_SAMPLING_INTERVAL = ("pm_sampling_interval", JsonFieldFormats.SECONDS)
  TEMPERATURE_UNIT = ("temperature_unit", JsonFieldFormats.STRING)
  TIMESTAMP = ("timestamp", JsonFieldFormats.TIMESTAMP)
  RESULT = ("result", JsonFieldFormats.RESULT)
  
  # extra keys from other planes in spec
  STATUS = ("status", JsonFieldFormats.BINDING_STATUS)
  """field not from main table in spec, used exclusively in binding status messages"""
  CODE   = ("code",   JsonFieldFormats.INT)
  """field not from main table in spec, only known value is 0"""
  ERROR_CODE = ("error_code", JsonFieldFormats.INT)
  """field not from main table in spec
  
  mentioned in OTA section; values:
  - 0 - success
  - other - failure
  """
  DESC = ("desc", JsonFieldFormats.STRING)
  """field not from main table in spec, usage seems not to make much sense"""
  
  
  NEED_ACK = ("need_ack", JsonFieldFormats.INT)
  """field not from main table in spec, specifies if ack response is needed"""
  ID  =    ("id",      JsonFieldFormats.INT)
  """field not from main table in spec, used in messages requiring response to match requests and responses"""
  ACK_ID = ("ack_id",  JsonFieldFormats.INT)
  """field not from main table in spec, used in responses to match requests and responses, must match ID"""
  SCENE_ID_LIST = ("scene_id_list", JsonFieldFormats.LIST_OF_INTS)
  """field not from main table in spec, same as ACK_ID but for scene IDs"""
  
  OTA_TYPE = ("ota_type", JsonFieldFormats.OTA_TYPE)
  """field not from main table in spec, used in OTA messages to specify type of update"""
  OTA_URL =     ("url",      JsonFieldFormats.STRING)
  """field not from main table in spec, used in OTA messages to specify URL of update file"""
  OTA_PERCENT = ("percent", JsonFieldFormats.INT)
  """field not from main table in spec, used in OTA response messages to specify progress percentage"""
  
  HOMEKIT_DEVICE_LIST = ("homekit_dev_list", JsonFieldFormats.DEVICE_NAMED_LIST)
  """field not from main table in spec, used in device list named request/response messages"""
  BIND_PARAMS = ("params", JsonFieldFormats.BIND_PARAMS)
  """field not from main table in spec, used in binding status messages to specify binding parameters"""
  
  ACTION = ("action", JsonFieldFormats.ACTION)
  """field not from main table in spec, used at least in alarm clock configuration (not to be confused with event alerts)"""
  ALARMS = ("alarms", JsonFieldFormats.ALARMS)
  """field not from main table in spec, used at least in alarm clock configuration (not to be confused with event alerts)"""
  
  # extra fields observed in real messages  
  MODULE_VERSION = ("module_version", JsonFieldFormats.STRING)
  """field not from main table in spec, observed in heartbeat"""
  WIFI_MAC = ("wifi_mac", JsonFieldFormats.STRING)
  """field not from main table in spec, observed in heartbeat and seems to be alias for MAC"""
  HK_SALT = ("hk_salt", JsonFieldFormats.STRING)
  """field not from main table in spec, observed in device list named response, purpose unknown"""
  IOT_PLATFORM = ("iot_platform", JsonFieldFormats.INT)
  """field not from main table in spec, observed in device list named response, likely indicates 1 = Qingping Cloud, 0 = private MQTT broker"""
  TIMEZONE = ("timezone", JsonFieldFormats.INT)
  """field not from main table in spec, observed in settings, match JsonSettings.TIMEZONE"""
  HW_VERSION = ("hw_version", JsonFieldFormats.STRING)
  """field not from main table in spec, observed in heartbeat, indicates hardware version"""
  
  fmt: JsonFieldFormats
  associated_sensor: SensorType | None
  def __new__(cls, value, fmt, associated_sensor=None):
    obj = str.__new__(cls, value) # FIXME: consider case normalization to avoid issues from poor spec
    obj._value_ = value
    obj.fmt = fmt
    obj.associated_sensor = associated_sensor
    return obj 
