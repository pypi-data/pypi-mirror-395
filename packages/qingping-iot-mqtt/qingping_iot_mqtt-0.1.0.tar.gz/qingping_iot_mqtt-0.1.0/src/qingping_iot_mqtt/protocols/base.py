# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional, Protocol as TypingProtocol, Mapping, Any
from enum import Enum, IntEnum, auto
from datetime import datetime, timedelta, time
from qingping_iot_mqtt.protocols.common_spec import SensorType

class SensorReadingType(Enum):
  REALTIME = auto()
  HISTORICAL = auto()
  EVENT = auto()
class ProtocolMessageDirection(Enum):
  DEVICE_TO_SERVER = auto()
  SERVER_TO_DEVICE = auto()
class ProtocolMessageCategory(Enum):
  READINGS = auto()
  SETTINGS = auto()
  REPROVISION = auto() # WiFi and MQTT change
  HANDSHAKE = auto()
  COMMAND = auto() # generic
  # TODO: implement others as needed



class SensorReadingStatus(IntEnum):
  NORMAL = 0
  ABNORMAL = 1
  INITIALIZE = 2

@dataclass
class SensorReading:
  """Single sensor reading data point."""
  sensor: SensorType
  value: float # FIXME: use Decimal?
  unit: str # either self-repoted or fixed per sensor type # TODO: this should be an Enum
  level: Optional[int] = None
  status: SensorReadingStatus = SensorReadingStatus.NORMAL
  status_duration: Optional[int] = None
  status_start_time: Optional[int] = None
  def format_status(self, simple: bool = True) -> str:
    if self.status == SensorReadingStatus.NORMAL:
      return "ok"
    elif self.status == SensorReadingStatus.ABNORMAL:
      if self.level is not None:
        if self.value > self.level:
          if simple:
            return "higher"
          else:
            return f"abnormal: >{self.level}{self.unit}"
        else:
          if simple:
            return "lower"
          else:
            return f"abnormal: <{self.level}{self.unit}"
      else:
        return "abnormal"
    elif self.status == SensorReadingStatus.INITIALIZE:
      return "init"
    else:
      return "unknown"
  def __str__(self) -> str:
    return f"SensorReading(sensor={self.sensor.name}, value={self.value}, unit={self.unit}, status='{self.format_status(simple=False)}')"


@dataclass(frozen=True)
class SensorReadingsContext:
  """Context for SensorReading.
  
  This is useful for readings that share common timestamp and origin, especially payloads that merge multiple readings.
  """
  origin: SensorReadingType
  timestamp: int # FIXME: use datetime?
  readings: Iterable[SensorReading]
  
  def __str__(self) -> str:
    return f"SensorReadingsContext(origin={self.origin.name}, timestamp={self.timestamp}, local_date='{datetime.fromtimestamp(self.timestamp)}', readings_count={len(list(self.readings))})"
  
  def dump(self) -> str:
    msg = self.__str__()
    for reading in self.readings:
      msg += f"\n    - {reading}"
    return msg

@dataclass(frozen=True)
class DeviceInfoWiFi:
  ssid: str
  """WiFi SSID"""
  bssid: str
  """WiFi BSSID (MAC Address)"""
  channel: int
  """WiFi AP channel"""
  signal_strength: int
  """WiFi Signal strength (RSSI) - dBm"""

@dataclass(frozen=True)
class TemporaryRapidReporting:
  """Container for temporary rapid reporting settings."""
  enabled: bool
  """Whether temporary rapid reporting is enabled."""
  interval: Optional[timedelta] = None
  """Interval between rapid reports."""
  duration: Optional[timedelta] = None
  """Total duration of rapid reporting."""

@dataclass(frozen=False)
class DeviceStatus:
  """Container for device status information, as self-reported by proprties.
  
  Non-frozen to allow multi-stage data ingestion.
  """
  
  co2_calibration_ongoing: Optional[bool] = None
  """Is CO2 sensor calibration ongoing?"""
  charger_plugged_in: Optional[bool] = None
  """Is charger/USB power plugged in?"""
  battery_percentage: Optional[int] = None
  """Battery charge level - percentage."""
  signal_strength: Optional[int] = None
  """Generic signal strength (RSSI) - dBm."""
  wifi_info: Optional[DeviceInfoWiFi] = None
  """WiFi-specific device information, if applicable."""
  
  all_data_sent: Optional[bool] = None
  """Whether device has sent all recorded historical data to server. Reported before disconnection."""
  next_upload_time: Optional[datetime] = None
  
  ntp_enabled: Optional[bool] = None
  """Whether NTP time synchronization is enabled on device."""
  ntp_server: Optional[str] = None
  """NTP server address configured on device."""
  
  ble_info: Optional[DeviceInfoBLE] = None
  """BLE-specific device information, if applicable."""
  temporary_rapid_reporting: Optional[TemporaryRapidReporting] = None
  """Temporary rapid reporting settings."""
  
  bound_device_list: Iterable[str] = field(default_factory=list)
  """List of bound devices (e.g. for gateways)."""

class TimeFormat(Enum):
  """Time format used on device display."""
  H24 = auto()
  H12 = auto()
class TemperatureUnit(Enum):
  """Temperature unit used on device display."""
  CELSIUS = auto()
  FAHRENHEIT = auto()
class SensorDisplayRangedColor(Enum):
  """Colors used for sensor value ranges on device display (traffic lights)."""
  GREEN = auto()
  YELLOW = auto()
  RED = auto()
  UNDEFINED = auto()
class SensorEventTriggerConditionType(Enum):
  ABOVE = auto()
  BELOW = auto()
class SensorEventTriggerRepeat(Enum):
  ONCE = auto()
  DAILY = auto()
@dataclass()
class SensorEventTriggerCondition():
  sensor: SensorType
  """Sensor type for which the event trigger condition is defined."""
  condition_type: SensorEventTriggerConditionType
  """Type of condition to trigger the event - above or below limit."""
  threshold_value: int # FIXME: use Decimal?
  """Threshold value for triggering the event."""
  monitoring_start_time: Optional[time] = None
  """Start of daily window when monitoring is active."""
  monitoring_end_time: Optional[time] = None
  """End of daily window when monitoring is active."""
  monitoring_repeat: Optional[SensorEventTriggerRepeat] = None
  """Whether the event trigger condition is one-time or daily repeated."""
  

@dataclass(frozen=True)
class SensorDisplayRange:
  """Container for ranges of sensor values for display purposes. Traffic-lights on devices.
  
  By design, this is sensor-type agnostic and forced to float values, since this is only supported format.
  """
  # FIXME: Decimal?
  def color(self, value: float) -> SensorDisplayRangedColor:
    """Get color for given sensor value."""
    return SensorDisplayRangedColor.UNDEFINED
@dataclass(frozen=False)
class SensorOffsetConfiguration:
  """Container for sensor offset configuration.
  
  By design, this is sensor-type agnostic and forced to float values, since this is only supported format.
  """
  # FIXME: Decimal?
  offset_value: float
  offset_permille: int

@dataclass(frozen=True)
class EncryptionSettings:
  """Container for encryption settings."""
  
  enabled: bool
  """Whether encryption is enabled."""
  key: Optional[bytes] = None
  """Encryption key, if applicable."""

@dataclass(frozen=False)
class DeviceSettings:
  """Container for device settings information.
  
  Either self-reported by device, or requested by server. 
  
  All fields are Optional to only set what user wants to change.
  
  Non-frozen to allow multi-stage data ingestion.
  """
  
  record_interval: Optional[timedelta] = None
  """How often device should record sensor readings.
  
  Those are later uploaded every upload_interval (more than 1 if record_interval < upload_interval)."""
  record_co2_interval: Optional[timedelta] = None
  """How often device should record CO2 sensor readings."""
  record_pm_interval: Optional[timedelta] = None
  """How often device should record PM sensor readings."""
  upload_interval: Optional[timedelta] = None
  """How often device should connect to network and upload recorded sensor readings.
  
  Every upload_interval device will upload real-time data + hostorical data if needed."""
  alert_repeat_interval: Optional[timedelta] = None
  """How often device should repeat alert notifications when sensor readings are outside configured thresholds."""
  alert_delay_interval: Optional[timedelta] = None
  """How long device should wait before sending alert notification when sensor readings are outside configured thresholds."""

  ranges: Mapping[SensorType, SensorDisplayRange] = field(default_factory=dict)
  """Mapping of sensor types to display ranges for traffic-light representation on device display."""
  offsets: Mapping[SensorType, SensorOffsetConfiguration] = field(default_factory=dict)
  """Mapping of sensor types to offset configurations."""
  event_triggers: Iterable[SensorEventTriggerCondition] = field(default_factory=list)
  """List of sensor event trigger conditions. It seems like multiple conditions can be set per sensor."""
  
  auto_poweroff_delay: Optional[timedelta] = None
  """Duration after which device goes to sleep when on battery power."""
  
  device_display_time_format: Optional[TimeFormat] = None
  """Time format used on device display."""
  device_display_temperature_unit: Optional[TemperatureUnit] = None
  """Temperature unit used on device display."""
  
  device_display_show_tvoc: Optional[bool] = None
  """Whether device display should show TVOC readings."""
  device_display_use_led: Optional[bool] = None
  """Whether device display should use LED indicators."""
  device_nighttime_start: Optional[time] = None
  """Start of nighttime period on device (for dimming display)."""
  device_nighttime_end: Optional[time] = None
  """End of nighttime period on device (for dimming display)."""
  device_screensaver_timeout: Optional[timedelta] = None
  """Duration of inactivity after which device display goes to screensaver mode."""
  device_screensaver_type: Optional[int] = None
  """Type of screensaver used on device display."""
  
  auto_co2_calibration: Optional[bool] = None
  """Whether device should perform automatic CO2 sensor calibration."""
  
  encryption: Optional[EncryptionSettings] = None
  """Encryption settings."""
  
  nbiot_splicing_command: Optional[bytes] = None
  """NB-IoT splicing command data."""
  nbiot_protocol_byte_replacement: Optional[bytes] = None
  """NB-IoT protocol byte replacement data."""
  
  connection_timeout: Optional[timedelta] = None
  """Network connection timeout duration."""

@dataclass(frozen=False)
class DeviceCommand:
  """Container for device command information."""
  command: Any
  parameters: Mapping = field(default_factory=dict)
  def encode(self) -> bytes:
    """Encode command into raw bytes to be sent to device."""
    return b""

@dataclass(frozen=True)
class MQTTConfiguration:
  """Container for MQTT configuration payload."""
  broker_address: str
  """MQTT Broker address."""
  broker_port: int
  """MQTT Broker port."""
  username: str
  """MQTT Username."""
  password: str
  """MQTT Password."""
  client_id: str
  """MQTT Client ID."""
  subscribe_topic: str
  """MQTT Topic for device to subscribe to (for commands)."""
  publish_topic: str
  """MQTT Topic for device to publish to (for responses and data upload)."""
@dataclass(frozen=True)
class WiFiConfiguration:
  """Container for WiFi configuration payload."""
  ssid: str
  """WiFi SSID."""
  password: str
  """WiFi Password."""

@dataclass(frozen=True)
class DeviceInfoBLE:
  mac: Optional[str] = None
  """BLE MAC Address"""
  buffer: Optional[str] = None
  """BLE data content"""
  srv_uuid: Optional[str] = None
  """BLE Service UUID"""
  chr_uuid: Optional[str] = None
  """BLE Feature UUID"""
  adv_data: Optional[str] = None
  """BLE broadcast data"""

@dataclass(frozen=False)
class DeviceInfo:
  """Container for semi-permanent device information, as self-reported by proprties.
  
  Non-frozen to allow multi-stage data ingestion.
  """

  user_id: Optional[str] = None
  """User-assigned device ID."""
  
  sn: Optional[str] = None
  """Unique, permamanent serial number of the device."""
  product_id: Optional[int] = None
  """Product identifier."""
  hw_revision: Optional[int] = None
  """Hardware revision."""
  pm_sn: Optional[str] = None
  """Permanent PM module serial number."""
  
  fw_version_general: Optional[str] = None
  """Unified firmware version string."""
  fw_version_wifi: Optional[str] = None
  """WiFi module firmware version string."""
  fw_version_mcu: Optional[str] = None
  """MCU firmware version string."""
  
  sim_number: Optional[str] = None
  """SIM card number (for cellular devices)."""
  
  unknown_properties: Mapping = field(default_factory=dict)
  """Container for unknown/unparsed properties, for future analysis.
  
  Protocol dependent implementation and presentation, but should be human-readable.
  """
  

class ProtocolMessage:
  """Abstract representation of message using Protocol."""
  
  direction: ProtocolMessageDirection
  """Metadata coming from lower layers.
  
  It is required, because some messages types are not safely inferable from message body alone.
  """
  
  category: ProtocolMessageCategory
  """Category of message, comparable to endpoint.
  
  Parts of converation should be in the same category, e.g. config request and response, sensor reading and ack, etc.
  """
  
  body: bytes
  """Unprocessed raw message transported using lower layer protocols.
  
  It can always be represented as bytes.
  """
  def __str__(self) -> str:
    return f"<{self.__class__.__name__} direction={self.direction.name} category={self.category.name} body_len={len(self.body)} bytes>"
  def dump(self) -> str:
    """Dump message content for debugging purposes."""
    return f"ProtocolMessage(direction={self.direction.name}, category={self.category.name}, body_len={len(self.body)} bytes>"
  def needs_ack(self) -> bool:
    """Check if this message requires an acknowledgment."""
    return False
  def is_this_response(self, response: ProtocolMessage) -> bool:
    """Check if given ProtocolMessage is a response to this intsance."""
    return False


class SensorReadingsContainer():
  """Container for sensor reading reports, independent of protocol.
  
  There are 3 types of sensor readings, all carry list of timestamp to reading data entries:
  - real-time (initiated by device in intervals set by configuration),
    this message usually contains just one entry for latest reading data (of multiple sensors);
    however, documentation examples show multiple entries in single message as well (expected for retransmissions)
  - events/alerts (initiated by device when reading thresholds are outside limits set by configuration)
    nearly identical to real-time messages, but additionaly contain information on readings that triggered the event
    to abstract protocols, alert flag is carried in SensorReading.status field
  - historical (initiated by server when requesting past data stored on device)
    dynamic number of entries depending on how many readings were stored in requested period
  """
  readings: Iterable[SensorReadingsContext] = field(default_factory=list)
  category: ProtocolMessageCategory = field(
    default=ProtocolMessageCategory.READINGS
  )
  def get_reading_contexts(self) -> Iterable[SensorReadingsContext]:
    return self.readings
  def __init__(self, message: ProtocolMessage):
    pass
  def dump(self) -> str:
    msg = f"SensorReadingsContainer(category={self.category.name}, readings_count={len(list(self.readings))})"
    for context in self.readings:
      msg += f"\n  - {context.dump()}"
    return msg
  # TODO: define common interfaces for getting SensorReading data from combined view - readings may contain duplicates
@dataclass(frozen=True)
class SettingsContainer():
  """Container for settings messages (read and writes), independent of protocol."""
  # TODO: implement this


class Protocol(TypingProtocol):
  """Abstract transport contract shared by JSON/HEX variants. This can be understood as Layer 4 in OSI model."""

  name: str
  version: str
  
  def decode_message(self, message: bytes, direction: ProtocolMessageDirection) -> ProtocolMessage:
    """Decode raw message bytes into a ProtocolMessage instance."""
    return ProtocolMessage()
  @classmethod
  def encode_message(cls, message: ProtocolMessage) -> bytes:
    """Encode a ProtocolMessage instance into raw message bytes."""
    return b""
