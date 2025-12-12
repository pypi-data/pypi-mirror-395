# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum, Enum, auto

class SensorType(StrEnum):
  TIMESTAMP = auto()
  BATTERY = auto()
  TEMPERATURE = auto()
  TEMPERATURE_AUX = auto()
  PRESSURE = auto()
  HUMIDITY = auto()
  HUMIDITY_AUX = auto()
  PM1 = auto()
  PM25 = auto()
  PM10 = auto()
  CO2 = auto()
  CO2_CONC = auto()
  VOC = auto()
  NOISE = auto()
  LIGHT = auto()
  TVOC = auto()
  RADON = auto()
  SIGNAL_STRENGTH = auto()
  # FIXME: implement field to indicate whether ranges are supported

class ProtocolName(StrEnum):
  HEX = "hex"
  JSON = "json"
  UNKNOWN = "unknown"
  @classmethod
  def identify(cls, data: bytes) -> ProtocolName:
    """Identify ProtocolName from payload, based on magic ID."""
    if data.startswith(b'\x43\x47'):
      return ProtocolName.HEX
    if data.startswith(b'{') and data.endswith(b'}'):
      return ProtocolName.JSON
    return ProtocolName.UNKNOWN

@dataclass
class DeviceModelInfo:
  name: str
  base_protocol: ProtocolName
  sensors: list[SensorType] = field(default_factory=list)
  

class DeviceModel(StrEnum):
  CGDN1 = ("CGDN1", DeviceModelInfo(
    name="Qingping Air Monitor Lite",
    base_protocol=ProtocolName.JSON,
    sensors=[SensorType.SIGNAL_STRENGTH, SensorType.BATTERY, 
             SensorType.TEMPERATURE, SensorType.HUMIDITY, 
             SensorType.PM25, SensorType.PM10, SensorType.CO2],
  ))
  CGP22C = ("CGP22C", DeviceModelInfo(
    name="Qingping CO₂ & Temp & RH Monitor",
    base_protocol=ProtocolName.HEX,
    sensors=[SensorType.SIGNAL_STRENGTH, SensorType.BATTERY, 
             SensorType.TEMPERATURE, SensorType.HUMIDITY, 
             SensorType.CO2],
  ))
  CGP23W = ("CGP23W", DeviceModelInfo(
    name="Qingping Temp & RH Monitor",
    base_protocol=ProtocolName.HEX,
    sensors=[SensorType.SIGNAL_STRENGTH, SensorType.BATTERY, 
             SensorType.TEMPERATURE, SensorType.HUMIDITY, 
             SensorType.PRESSURE],
  ))
  # TODO: add other models
  
  UNKNOWN = ("UNKNOWN", DeviceModelInfo(
    name="Unknown Device Model",
    base_protocol=ProtocolName.UNKNOWN,
    sensors=list(SensorType.__members__.values()),
  ))
  
  device_model_info: DeviceModelInfo
  def __new__(cls, value, dmi: DeviceModelInfo):
    obj = str.__new__(cls, value)
    obj._value_ = value
    obj.device_model_info = dmi
    return obj
