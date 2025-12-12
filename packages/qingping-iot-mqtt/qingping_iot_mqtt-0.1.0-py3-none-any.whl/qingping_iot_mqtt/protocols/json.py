# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause

# IMPORTANT NOT ON ORIGIN OF PARTS OF COMMENTS/DOCS:
#   EVERYTHING PREFIXED WITH `SPEC:` AND BACK-TICK-QUOTED TEXT IS TAKEN ON 2025-11-22 DIRECTLY FROM 
#   [Qingping MQTT Protocol](https://developer.qingping.co/private/communication-protocols/public-mqtt-json)
#   WHICH IS OFFICIAL DOCUMENTATION PUBLISHED BY QINGPING. EVEN THEY ARE NOT 100% SURE.

from __future__ import annotations

# TODO: when using types from JsonFieldFormats, check if they contain method qp_json_encode for formatting and run it


import json
from dataclasses import dataclass
from typing import Iterable, Mapping
import logging
import typing
logger = logging.getLogger(__name__)

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
from .json_spec import (
  JsonFieldFormats,
  JsonDurationSeconds,
  JsonTime,
  JsonTimestamp,
  JsonResult,
  JsonCommand,
  JsonDeviceNamed,
  JsonMqttConfig,
  JsonWifiConfig,
  JsonSensorDataSubEntry,
  JsonSensorData,
  JsonWiFiInfo,
  JsonLedThresholds,
  JsonSettings,
  JsonBindingStatus,
  JsonOtaType,
  JsonAction,
  JsonFieldFormats,
  JsonKey
)
from qingping_iot_mqtt.protocols.common_spec import ProtocolName
logger = logging.getLogger(__name__)

class JsonFrameError(Exception):
  """Exception raised on JSON frame parsing errors."""
  pass
class JsonFrame:
  """A single JSON frame as sent/received over MQTT.
  """
  magic = "{"
  frame: bytes
  decoded = {}
  known = {}
  unknown = {}

  def __init__(self, raw: bytes) -> None:
    self.frame = raw
    if not raw.startswith(self.magic.encode("utf-8")):
      raise JsonFrameError("Not a valid JSON frame")
    try:
      self.decoded = json.loads(raw)
    except json.JSONDecodeError as e:
      raise JsonFrameError("Not a valid JSON frame") from e
    self.known = {}
    for key, value in self.decoded.items():
      if not isinstance(key, str):
        raise JsonFrameError("Not a valid JSON frame: key is not a string")
      try:
        decoded_key = JsonKey(key)
      except ValueError:
        self.unknown[key] = value
        logger.debug("Unknown JSON key: %s", key)
        continue
      decoded_value = None
      fmt = decoded_key.fmt
      try:
        decoded_field = fmt.field_type().qp_json_decode(value)
        decoded_value = decoded_field.value if hasattr(decoded_field, "value") else decoded_field
      except Exception as e:
        logger.warning("Failed to decode JSON key %s: %s", key, e)
        self.unknown[key] = value
        continue
      self.known[decoded_key] = decoded_value
  @classmethod
  def construct_frame(cls, cmd: JsonCommand, fields: Mapping[JsonKey, typing.Any]) -> JsonFrame:
    body = {}
    body[JsonKey.TYPE.value] = cmd.value
    for key_raw, value in fields.items():
      key=JsonKey(key_raw)
      if not isinstance(value, key.fmt.expected_type.__class__):
        raise ValueError(f"Value for {key.name} must be of type {key.fmt.expected_type.__class__.__name__}")
      if hasattr(value, "qp_json_encode") and callable(getattr(value, "qp_json_encode")):
        body[key.value] = value.qp_json_encode()  # pyright: ignore[reportAttributeAccessIssue]
    raise NotImplementedError("Not implemented yet")
  def __str__(self) -> str:
    return json.dumps(self.decoded, indent=2)
  def dump(self) -> str:
    return str(self) # FIXME

class JsonProtocolMesssage(ProtocolMessage):
  """Representation of decoded JSON protocol message."""
  frame: JsonFrame
  frame_type: JsonCommand
  def __init__(self, direction: ProtocolMessageDirection, body: bytes) -> None:
    self.body = body
    self.frame = JsonFrame(body)
    self.direction = direction
    if self.frame.known.get(JsonKey.TYPE) is None:
      raise JsonFrameError("No type field in JSON frame")
    self.frame_type = self.frame.known[JsonKey.TYPE].value
    if self.frame_type in [
      JsonCommand.BLE_CONNECTION_REQUEST,
      JsonCommand.BLE_DISCONNECTION_REQUEST,
      JsonCommand.BLE_OPEN_NOTIFICATION_REQUEST,
      JsonCommand.BLE_CLOSE_NOTIFICATION_REQUEST,
      JsonCommand.BLE_NOTIFICATION_RESPONSE,
      JsonCommand.BLE_DATA_TRANSMISSION_EXPECT_RESPONSE,
      JsonCommand.BLE_DATA_TRANSMISSION_IGNORE_RESPONSE,
      JsonCommand.BLE_DATA_RECEIPT,
      JsonCommand.BLE_DATA_RESPONSE,
      JsonCommand.BLE_DATA_BROADCAST,
      JsonCommand.DEVICE_REPORT_LOG,
      JsonCommand.BINDING_STATUS,
      JsonCommand.BINDING_STATUS_EXTERNAL,
      JsonCommand.OTA_COMMAND,
      JsonCommand.OTA_RESPONSE,
      
    ]:
      self.category = ProtocolMessageCategory.COMMAND
    elif self.frame_type in [
      JsonCommand.DEVICE_LIST_REQUEST,
      JsonCommand.DEVICE_LIST_NAMED_REQUEST,
      JsonCommand.DEVICE_LIST_RESPONSE,
      JsonCommand.DEVICE_LIST_NAMED_RESPONSE,
      JsonCommand.DATA_ACK,
    ]:
      self.category = ProtocolMessageCategory.HANDSHAKE
    elif self.frame_type in [
      JsonCommand.REALTIME_DATA,
      JsonCommand.NOTIFICATION,
      JsonCommand.HEARTBEAT
    ]:
      self.category = ProtocolMessageCategory.READINGS
    elif self.frame_type in [
      JsonCommand.MQTT_RECONNECT,
      JsonCommand.MQTT_RECONFIGURE,
    ]:
      self.category = ProtocolMessageCategory.REPROVISION
    elif self.frame_type in [
      JsonCommand.SETTINGS_REPORT,
      JsonCommand.ALARM,
    ]:
      self.category = ProtocolMessageCategory.SETTINGS
    elif self.frame_type == JsonCommand.HISTORICAL_DATA_OR_SETTINGS:
      if direction == ProtocolMessageDirection.DEVICE_TO_SERVER:
        self.category = ProtocolMessageCategory.READINGS
      elif direction == ProtocolMessageDirection.SERVER_TO_DEVICE:
        self.category = ProtocolMessageCategory.SETTINGS
    else:
      raise JsonFrameError(f"Unknown JSON frame type: {self.frame_type}")
  def dump(self) -> str:
    msg = f"JsonProtocolMessage(direction={self.direction.name}, category={self.category.name}, type={self.frame_type} fields_cound={len(self.frame.decoded)})>"
    for key, value in self.frame.known.items():
      msg += f"\n  - {key}={value}"
    return msg
  def needs_ack(self) -> bool:
    """Check if this message requires an acknowledgment."""
    return self.frame.known.get(JsonKey.NEED_ACK, False)
  def is_this_response(self, response: ProtocolMessage) -> bool:
    """Check if given ProtocolMessage is a response to this intsance."""
    if not isinstance(response, JsonProtocolMesssage):
      return False
    
    # cannot be response in same direction
    if self.direction == response.direction:
      return False
    
    # if both have ID, they must match
    if self.frame.known.get(JsonKey.ID) is not None and  response.frame.known.get(JsonKey.ID) is not None:
      if self.frame.known.get(JsonKey.ID) != response.frame.known.get(JsonKey.ID):
        return False
    
    if self.frame_type == JsonCommand.DEVICE_LIST_REQUEST and response.frame_type == JsonCommand.DEVICE_LIST_RESPONSE:
      return True
    if self.frame_type == JsonCommand.DEVICE_LIST_NAMED_REQUEST and response.frame_type == JsonCommand.DEVICE_LIST_NAMED_RESPONSE:
      return True

    if self.frame_type in [JsonCommand.REALTIME_DATA, JsonCommand.HISTORICAL_DATA_OR_SETTINGS] and response.frame_type == JsonCommand.DATA_ACK:
      return True
    
    if self.direction == ProtocolMessageDirection.SERVER_TO_DEVICE \
      and self.frame_type == JsonCommand.HISTORICAL_DATA_OR_SETTINGS \
      and response.frame_type == JsonCommand.SETTINGS_REPORT:
        return True
    
    if self.frame_type == JsonCommand.OTA_COMMAND and response.frame_type == JsonCommand.OTA_RESPONSE:
      return True
    
    # TODO: implement temporary rapid reporting flow
    # TODO: implement notification setting flow
    # TODO: implement alarm setting flow
    
    return False
class JsonSensorReadingMessageError(Exception):
  """Exception raised on JSON sensor reading message parsing errors."""
  pass
class JsonSensorReadingMessage(SensorReadingsContainer):
  """Representation of sensor reading container from JSON protocol message."""
  def __init__(self, message: ProtocolMessage) -> None:
    self.category = message.category
    if not isinstance(message, JsonProtocolMesssage):
      raise ValueError("Can only construct JsonSensorReadingMessage from JsonProtocolMesssage")
    self.readings = []
    if message.category != ProtocolMessageCategory.READINGS:
      raise ValueError("JsonSensorReadingMessage can only be constructed from READINGS message")
    if message.direction != ProtocolMessageDirection.DEVICE_TO_SERVER:
      raise ValueError("JsonSensorReadingMessage can only be constructed from DEVICE_TO_SERVER message")
    if message.frame_type == JsonCommand.REALTIME_DATA:
      # TODO: implement after encountering such message
      raise NotImplementedError("REALTIME_DATA message parsing not implemented yet, got {message.frame}")
      pass
    elif message.frame_type == JsonCommand.HISTORICAL_DATA_OR_SETTINGS:
      sensor_data = message.frame.known.get(JsonKey.SENSOR_DATA)
      if sensor_data is None:
        raise JsonSensorReadingMessageError("No sensor data in REALTIME_DATA message")
      if not isinstance(sensor_data, list):
        raise JsonSensorReadingMessageError("Invalid sensor data in HISTORICAL_DATA_OR_SETTINGS message")
      for entry in sensor_data:
        if not isinstance(entry, JsonSensorData):
          raise JsonSensorReadingMessageError("Invalid sensor data entry in HISTORICAL_DATA_OR_SETTINGS message")
        self.readings.append(entry.to_context(origin=SensorReadingType.HISTORICAL))
    elif message.frame_type == JsonCommand.NOTIFICATION:
      # TODO: implement after encountering such message
      raise NotImplementedError("NOTIFICATION message parsing not implemented yet, got {message.frame}")
    elif message.frame_type == JsonCommand.HEARTBEAT:
      if JsonKey.WIFI_INFO not in message.frame.known:
        raise JsonSensorReadingMessageError("No WiFi info in HEARTBEAT message")
      wifi_info: JsonWiFiInfo = message.frame.known.get(JsonKey.WIFI_INFO) # pyright: ignore[reportAssignmentType]
      timestamp: JsonTimestamp = message.frame.known.get(JsonKey.TIMESTAMP) or JsonTimestamp(0)
      try:
        reading = SensorReading(
          sensor=SensorType.SIGNAL_STRENGTH,
          value=wifi_info.rssi,
          unit="dBm"
        )
        ctx = SensorReadingsContext(
          timestamp=timestamp.timestamp,
          origin=SensorReadingType.REALTIME,
          readings=[reading]
        )
        self.readings.append(ctx)
      except JsonFrameError as e:
        raise JsonSensorReadingMessageError("Invalid WiFi info in HEARTBEAT message") from e
    else:
      raise JsonSensorReadingMessageError("JsonSensorReadingMessage can only be constructed from REALTIME_DATA, HISTORICAL_DATA_OR_SETTINGS, NOTIFICATION or HEARTBEAT message")

class JsonRawCommand(DeviceCommand):
  payload: bytes
  def __init__(self, command: JsonCommand, parameters: Mapping[JsonKey, JsonFieldFormats]):
    self.command = command
    for key, value in parameters.items():
      if not isinstance(value, key.fmt.__class__):
        raise ValueError(f"Value for {key.name} must be of type {key.fmt.__class__.__name__}")
    self.parameters=parameters
  def encode(self) -> bytes:
    frame = JsonFrame.construct_frame(self.command, self.parameters)
    return frame.frame
  def dump(self) -> str:
    msg = f"JsonRawCommand(command={self.command}, payload_length={len(self.payload)})"
    msg += f"\n  {self.payload.decode('utf-8')}"
    return msg
class JsonCommandRequestSettings(JsonRawCommand):
  def __init__(self):
    super().__init__(command=JsonCommand.SETTINGS_REPORT, parameters={})


class JsonProtocol(Protocol):#
  name = ProtocolName.JSON.name
  version = "1.0"

  def decode_message(self, message: bytes, direction: ProtocolMessageDirection) -> ProtocolMessage:
    return JsonProtocolMesssage(direction, message)
  
  @classmethod
  def encode_message(cls, message: ProtocolMessage) -> bytes:
    if not isinstance(message, JsonProtocolMesssage):
      raise ValueError("Can only encode JsonProtocolMesssage")
    return message.frame.frame    
