# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause

# IMPORTANT NOT ON ORIGIN OF PARTS OF COMMENTS/DOCS:
#   EVERYTHING PREFIXED WITH `SPEC:` AND BACK-TICK-QUOTED TEXT IS TAKEN ON 2025-11-16 DIRECTLY FROM 
#   [Qingping Products Data Reporting Protocol](https://qingping.feishu.cn/docx/BlYOdJVRQobV0ox6SNZcV8V6nZT)
#   WHICH IS OFFICIAL DOCUMENTATION PUBLISHED BY QINGPING. EVEN THEY ARE NOT 100% SURE.

# FIXME: implement `New Protocol V2 Sensor Data Format Description`

from enum import Enum, IntEnum, auto

from .base import (
  ProtocolMessageDirection,
  SensorType
)
class HexFieldFormats(Enum):
  """Types of field formats to be parsed in HEX protocol.

  This is derived from HEX Protocol spec: section 3 "Command Definition" - "KEY Definition", but not explicitly defined there.
  
  ALL numeric values are unsigned integers and in LITTLE ENDIAN format. 
  """
  # LV - always 2 bytes length prefix, type depends on Key
  LV_STRING = auto()       # string
  LV_ENTRIES_6B = auto()   # (length/6) entries of 6 bytes each - SENSORS_GROUP_6B
  LV_ENTRIES_8B = auto()   # (length/8) entries of 8 bytes each - SENSORS_GROUP_8B
  LV_EVENTPAYLOAD = auto() # length is always 12 bytes; TIMESTAMP + 6 bytes sensor data + 2 bytes ("event setting value" OR (for 0x14) 1byte signal stength + 1byte reserved)

  
  # non-LV - just values
  SENSORS_GROUP_6B = auto()   #  6 bytes, SENSOR_TH_3B + SENSOR_2ND_2B + BATTERY_PERC
  SENSOR_TH = auto()          #  3 bytes, "the high 12bit is magnified 10 times and the positive offset is 500, the unit is ℃.; The lower 12bit is the humidity magnified 10 times, the unit is %RH."
  SENSOR_2NDB = auto()        #  2 bytes, "The air pressure is magnified 100 times, and the unit is kPa." OR "Maybe CO2 depends on product"
  SENSOR_AUX_TH = auto()      #  4 bytes, "2 bytes temperature (positive offset 500) + 2 bytes humidity."
  SENSORS_GROUP_8B = auto()   #  8 bytes, SENSORS_GROUP_6B + 2 bytes AUX Temperature (0xFFFF=disconnected)
  MINUTES = auto()            #  2 bytes, unsigned int, minutes
  SECONDS = auto()            #  2 bytes, unsigned int, seconds
  BOOL = auto()               #  1 bytes, boolean
  WIFI = auto()               # XX bytes, `"SSID","PASSOWRD"` string 
  MQTT = auto()               # XX bytes, `URL port username password clientid sub_topic pub_topic` string separated by spaces
  TIMESTAMP = auto()          #  4 bytes, unsigned int, epoch time
  NBIOT_BYTE_REPLACE= auto()  #  3 bytes, replacement for bytes 0x1A then 0x1B then 0x08 (0x43 to unset)
  ENCRYPTION_KEY = auto()     # 16 bytes, AES key, all 0 to disable
  PRESSURE_PRECISE = auto()   #  6 bytes, first 4 bytes are 100*Pa, last 2 bytes are "others"
  PERC = auto()               #  1 bytes, unsigned, percentage 0-100
  BLE_POWER = auto()          #  2 bytes, unknown format
  BLE_NAME = auto()           # 28 bytes, string of max 28 bytes (TBD but likely null-terminated, so need to parse bytes 1 by 1)
  TH_OFFSET = auto()          #  4 bytes, "2 bytes temperature (step is 0.1) + 2 bytes humidity (step is 0.1)."
  PRESSURE_OFFSET = auto()    #  2 bytes, "2 bytes (step is 0.1)."
  RANGE = auto()              #  4 bytes, define boundaries of middle range (yellow) in greed-yellow-red display, 2 bytes for lower bound, 2 bytes for upper bound, unit depends on sensor
  OFFSET_PMIL = auto()        #  2 bytes, (signed?) int16, 0.1% steps
  PPM = auto()                #  2 bytes, int16 (may be signed for offset), parts per million
  DECI_DEGREE = auto()        #  2 bytes, int16 (may be signed for offset), 0.1 degree Celsius (or F when flag 0x19 is set???)
  PERMILLE = auto()           #  2 bytes, int16 (may be signed for offset), 0.1% steps
  UGM3 = auto()               #  2 bytes, uint16, micrograms per cubic meter
  EVENT_ALERT = auto()        #  5 bytes, 1 byte event ID, 4 bytes value
  GENERIC_2B = auto()         #  2 bytes, generic 2 bytes field, unknown format
  FLAG = auto()               #  0 bytes, flag field, no data, just presence indicates flag is set
  
  UNKNOWN = auto()            # XX bytes, unknown format, raw bytes

class HexCommand(IntEnum):
  """HEX Protocol Command Identifiers, used in frame header ("CMD" field).
  
  HEX Protocol spec: section 3 "Command Definition" - "CMD Definition"
  """
  DATA_UPLOADING =           (0x31, ProtocolMessageDirection.DEVICE_TO_SERVER)
  CONFIGURATION_SENDING =    (0x32, ProtocolMessageDirection.SERVER_TO_DEVICE)
  FIRMWARE_UPGRADE =         (0x33, ProtocolMessageDirection.SERVER_TO_DEVICE)
  EVENT_REPORTING =          (0x34, ProtocolMessageDirection.DEVICE_TO_SERVER)
  CONFIGURATION_REPORTING =  (0x39, ProtocolMessageDirection.DEVICE_TO_SERVER)
  NETWORK_ACCESS_SETTING =   (0x3A, ProtocolMessageDirection.SERVER_TO_DEVICE)
  REAL_TIME_DATA_UPLOADING = (0x3B, ProtocolMessageDirection.DEVICE_TO_SERVER)
  
  
  direction: ProtocolMessageDirection
  def __new__(cls, value, direction):
    obj = int.__new__(cls, value)
    obj._value_ = value
    obj.direction = direction
    return obj
  
class HexKey(IntEnum):
  """HEX Protocol Key Identifiers, used in frame body
  
  HEX Protocol spec: section 3 "Command Definition" - "KEY Definition". 
  
  Official spec is messy mix of TLVs, prefixes and flags. My attempt at structuring them:
  
  - HEADER_* - normal TLVs  marking start of sections of data uplads
  - EVT_* - used both as flags for reports and Type for event configuration (Length cannot be inferred from Key alone because device differs in capabilities)
  - PROP_* - RO properties of the device, reported after server request
  - SETTING_* - RW settings of the device, can be set by server and reported back by device
  - CONNECTION_* - event/flags related to network connection status
  - CMD_* - commands sent by server to device
  - DATA_* - sensor data fields reported by device in various types of reports
  - UNKNOWN_* fields not properly defined in docs
  """
  
  # device properties
  PROP_DEVICE_ID =               (0x01, HexFieldFormats.LV_STRING)
  """`Device ID`
  
  SPEC: It is set by the server and can be used as the AES key for encryption."""
  PROP_DEVICE_SN =               (0x02, HexFieldFormats.LV_STRING)
  """`Device SN`
  
  SPEC: The unique serial number of the device."""
  PROP_FIRMWARE_VERSION =        (0x11, HexFieldFormats.LV_STRING) # TODO: confirm format
  """`Fimware version`"""
  PROP_FIRMWARE_URL_WIFI =       (0x12, HexFieldFormats.LV_STRING) # TODO: confirm format
  """`URL of Wi-Fi module firmware`
  
  SPEC: URL of MCU firmware"""
  PROP_FIRMWARE_URL_MCU =        (0x13, HexFieldFormats.LV_STRING) # TODO: confirm format
  """`URL of MCU firmware`
  
  SPEC: URL of MCU firmware"""
  PROP_SIM_NUMBER =              (0x16, HexFieldFormats.UNKNOWN) # TODO: confirm format
  """`SIM card number`"""
  PROP_DEVICE_REV =              (0x22, HexFieldFormats.LV_STRING)
  """`Hardware version`"""
  PROP_DEVICE_WIRELESS_FW =      (0x34, HexFieldFormats.LV_STRING) # TODO: confirm format
  """`Wireless module firmware version`"""
  PROP_DEVICE_MCU_FW =           (0x35, HexFieldFormats.LV_STRING) # TODO: confirm format
  """`MCU firmware version`"""
  PROP_DEVICE_PRODUCTID =        (0x38, HexFieldFormats.GENERIC_2B)
  """`Product ID`
  
  SPEC: 2 bytes, in addition to the user-defined product ID, which must be same as the BLE product ID."""
  PROP_PM_SN =                   (0x61, HexFieldFormats.LV_STRING)
  """SPEC: PM module serial number
  
  SPEC: When the length is 0, it means that the PM module is not connected."""
  PROP_SNTP_CALIBRATION = (0x44, HexFieldFormats.BOOL) # this is RW prop
  """`Set the SNTP calibration time switch`
  
  SPEC:0: off; 1: on. """
  PROP_SNTP_SERVER = (0x43, HexFieldFormats.LV_STRING) # this is RW prop
  """`Set the SNTP server`
  
  SPEC: Such as: cn.pool.ntp.org ."""
  
  # device status fields
  STATE_CO2_CALIBRATION_ONGOING = (0x4A, HexFieldFormats.BOOL)
  """`CO2 calibration status` - is it ongoing now?
  
  SPEC: 1 byte. 1: being calibrated, 0: not being.
  """
  STATE_USB_PLUGGEDIN = (0x2C, HexFieldFormats.BOOL)
  """`USB plug-in status`
  
  SPEC: Plug-in: 0x01; Pull-out: 0x00"""
  STATE_BATTERY_PERC = (0x64, HexFieldFormats.PERC, SensorType.BATTERY)
  """`Battery percentage` - %
  
  SPEC: 1 byte unsigned."""
  STATE_SIGNAL_STRENGHT = (0x65, HexFieldFormats.GENERIC_2B, SensorType.SIGNAL_STRENGTH)
  """`Signal strength` - dBm???
  
  SPEC: 2 bytes unsigned.
  OBSERVATION: for WiFi it's signed dBm RSSI (so SPEC is wrong)"""
  
  STATE_ALL_DATA_SENT = (0x1D, HexFieldFormats.BOOL)
  """`Disconnect the device` - flag signalling all data has been sent
  
  SPEC: When the data reported or sent by the device is the last piece of content, this KEY can be used to allow the device to enter the low power consumption mode quickly.
  SPEC: - 0x00: There is still data not sent.
  SPEC: - 0x01: All the data has been sent."""
  STATE_NEXT_UPLOAD_TS = (0x24, HexFieldFormats.TIMESTAMP)
  """`Time of next connection`
  
  SPEC: The content is timestamp."""
  
  # section headers
  HEADER_HISTORICAL_DATA_6B = (0x03, HexFieldFormats.LV_ENTRIES_6B)
  """`Historical data` - standard (6-byte groups)"""
  HEADER_REALTIME_DATA = (0x14, HexFieldFormats.LV_EVENTPAYLOAD)
  """`Event of real-time networking`
  
  SPEC: There will be this event every time before the device is connected to the network (except for the over-limit event networking)."""
  HEADER_HISTORICAL_DATA_8B = (0x33, HexFieldFormats.LV_ENTRIES_8B)
  """`Historical data` - extended (8-byte groups)
  
  SPEC: The difference with 0x03 KEY is that the data of this KEY is in a group of 8 bytes, and the last two bytes indicate the AUX humidity, and the others are consistent with 0x03 KEY."""
  HEADER_EVENT_ALERT = (0x66, HexFieldFormats.EVENT_ALERT)
  """`Event alert`
  
  SPEC: 1 byte event ID + 4 byte event value."""
  HEADER_USERDEF = (0xC8, HexFieldFormats.UNKNOWN)
  """`User defined function` - marker
  
  SPEC: Greater than this value can be used for user-defined."""
  
  # setting fields
  SETTING_INTERVAL_UPLOAD_M = (0x04, HexFieldFormats.MINUTES)
  """`Interval of data uploading` in minutes
  
  SPEC: Unit: minutes."""
  SETTING_INTERVAL_RECORD_S = (0x05, HexFieldFormats.SECONDS)
  """`Interval of data recording` in seconds
  
  SPEC: Unit: seconds."""
  SETTING_INTERVAL_ALERT_REPEAT_S = (0x1B, HexFieldFormats.SECONDS)
  """`Interval of event repeat notification`
  
  SPEC: Used to set the device repeat notification frequency (unit: seconds)."""
  SETTING_DELAY_REPORTING_S = (0x37, HexFieldFormats.SECONDS)
  """`Reporting delay time` in seconds
  
  SPEC: 2 bytes, unit is seconds."""
  SETTING_CO2_RANGES = (0x3C, HexFieldFormats.RANGE, SensorType.CO2)
  """`Set the middle range of CO2 level` - ppm
  
  SPEC: 4 bytes, every 2 bytes occupy a demarcation point, the first point is the minimum value (inclusive) and the second point is the maximum value (inclusive)."""
  SETTING_TEMPERATURE_RANGES = (0x4F, HexFieldFormats.RANGE, SensorType.TEMPERATURE)
  """`Set the middle range of temperature level` - deci-degree Celsius
  
  SPEC: 4 bytes, every 2 bytes occupy a demarcation point, the first point is the minimum value of the middle grade, and the second point is the maximum value of the middle grade, with a step of 0.1."""
  SETTING_HUMIDITY_RANGES = (0x50, HexFieldFormats.RANGE, SensorType.HUMIDITY)
  """`Set the middle range of humidity rating standard` - permille
  
  SPEC: 4 bytes, every 2 bytes occupy a demarcation point, the first point is the minimum value of the medium level, the second point is the maximum value of the medium level (inclusive), step 0.1."""
  SETTING_PM25_RANGES = (0x51, HexFieldFormats.RANGE, SensorType.PM25)
  """`Set the middle range of PM2.5 rating standard` - ppm
  
  SPEC: 4 bytes, every 2 bytes occupy a demarcation point, the first point is the minimum value of the medium level, the second point is the maximum value of the medium level (inclusive), step 1."""
  SETTING_PM10_RANGES = (0x52, HexFieldFormats.RANGE, SensorType.PM10)
  """`Set the middle range of PM10 rating standard` - ppm
  
  SPEC: 4 bytes, every 2 bytes occupy a demarcation point, the first point is the minimum value of the medium level, the second point is the maximum value of the medium level (inclusive), step 1."""
  SETTING_TVOC_RANGES = (0x53, HexFieldFormats.RANGE, SensorType.TVOC)
  """`Set the middle range of TVOC rating standard` - (?)
  
  SPEC: 4 bytes, every 2 bytes occupy a demarcation point, the first point is the minimum value of the medium level, the second point is the maximum value of the medium level (inclusive), step 1."""
  SETTING_NOISE_RANGES = (0x54, HexFieldFormats.RANGE, SensorType.NOISE)
  """`Set the middle range of Noise rating standard` - (dB?)
  
  SPEC: 4 bytes, every 2 bytes occupy a demarcation point, the first point is the minimum value of the medium level, the second point is the maximum value of the medium level (inclusive), step 1."""
  SETTING_LIGHT_RANGES = (0x55, HexFieldFormats.RANGE, SensorType.LIGHT)
  """`Set the middle range of Light rating standard` - (lux?)
  
  SPEC: 4 bytes, every 2 bytes occupy a demarcation point, the first point is the minimum value of the medium level, the second point is the maximum value of the medium level (inclusive), step 1."""
  SETTING_POWER_BATTERY_AUTOFF_M = (0x3D, HexFieldFormats.MINUTES)
  """`Set the auto-off time while using battery` - minutes
  
  SPEC: 2 bytes, unit is minutes."""
  SETTING_TEMPERATURE_UNIT_F = (0x19, HexFieldFormats.BOOL)
  """`Unit of temperature` - flag to enable weird units (on display)
  
  SPEC: 0x00: Celsius. 0x01: Fahrenheit."""
  SETTING_CLOCK_12H = (0x3E, HexFieldFormats.BOOL)
  """`12-hour setting` - flag to enable weird time format (on display)
  
  SPEC: 1 byte. 0: 24-hour; 1: 12-hour."""
  SETTING_TVOC_SHOW = (0x62, HexFieldFormats.UNKNOWN)
  """`TVOC reading display`
  
  SPEC: 0: do not display reading, 1: display reading."""
  SETTING_LED_ENABLED = (0x63, HexFieldFormats.UNKNOWN)
  """`LED switch setting`
  
  SPEC: 0: off, 1: on."""
  SETTING_CO2_AUTO_SENSOR_CALIBRATION = (0x40, HexFieldFormats.BOOL)
  """`CO2 ASC switch` - enable or disable automatic self-calibration (ASC) of CO2 sensor
  
  SPEC: 1 byte. 0: off; 1: on."""
  SETTING_CO2_OFFSET_PMIL = (0x3F, HexFieldFormats.PERMILLE, SensorType.CO2)
  """`Offset CO2 by percentage` - permille
  
  SPEC: 2 bytes, percentage, step is 0.1%."""
  SETTING_CO2_OFFSET_PPM = (0x45, HexFieldFormats.PPM, SensorType.CO2)
  """`Offset CO2 by value` - ppm
  
  SPEC: 2 bytes, value, step is 1."""
  SETTING_TEMPERATURE_OFFSET_VALUE_DC = (0x46, HexFieldFormats.DECI_DEGREE, SensorType.TEMPERATURE)
  """`Offset temperature by value` - deci-degree Celsius
  
  SPEC: 2 bytes, value, step is 0.1."""
  SETTING_TEMPERATURE_OFFSET_PMIL = (0x47, HexFieldFormats.PERMILLE, SensorType.TEMPERATURE)
  """`Offset temperature by percentage` - permille
  
  SPEC: 2 bytes, percentage, step is 0.1%."""
  SETTING_HUMIDITY_OFFSET_VALUE_PMIL = (0x48, HexFieldFormats.PERMILLE, SensorType.HUMIDITY)
  """`Offset humidity by value` - permille absolute
  
  SPEC: 2 bytes, percentage, step is 0.1."""
  SETTING_HUMIDITY_OFFSET_PMIL = (0x49, HexFieldFormats.PERMILLE, SensorType.HUMIDITY)
  """`Offset humidity by percentage` - permille relative
  
  SPEC: 2 bytes, percentage, step is 0.1%."""
  SETTING_PM25_OFFSET_VALUE = (0x4B, HexFieldFormats.UGM3, SensorType.PM25)
  """`Offset PM2.5 by value` - ug/m3
  
  SPEC: 2 bytes, value, step is 1."""
  SETTING_PM25_OFFSET_PMIL = (0x4C, HexFieldFormats.PERMILLE, SensorType.PM25)
  """`Offset CO2 by percentage` - permille
  
  SPEC: 2 bytes, percentage, step is 0.1%."""
  SETTING_PM10_OFFSET_VALUE = (0x4D, HexFieldFormats.UGM3, SensorType.PM10)
  """`Offset PM10 by value` - ug/m3
  
  SPEC: 2 bytes, value, step is 1."""
  SETTING_PM10_OFFSET_PMIL = (0x4E, HexFieldFormats.PERMILLE, SensorType.PM10)
  """`Offset PM10 by percentage` - permille
  
  SPEC: 2 bytes, percentage, step is 0.1%."""
  SETTING_INTERVAL_CO2 = (0x3B, HexFieldFormats.UNKNOWN) # FIXME
  
  # event IDs
  EVT_BATTERY_LOW = (0x17, HexFieldFormats.FLAG)
  """`Event of battery low` - low battery, likely last report before shutdown
  
  SPEC: Over-limit event."""
  EVT_TEMPERATURE_HIGHER = (0x07, HexFieldFormats.FLAG, SensorType.TEMPERATURE)
  """`Report when higher than a temperature value`
  
  SPEC: Over-limit event."""
  EVT_TEMPERATURE_LOWER = (0x08, HexFieldFormats.FLAG, SensorType.TEMPERATURE)
  """`Report when lower than a temperature value`
  
  SPEC: Over-limit event."""
  EVT_HUMIDITY_HIGHER = (0x0A, HexFieldFormats.FLAG, SensorType.HUMIDITY)
  """`Report when higher than a humidity value`
  
  SPEC: Over-limit event."""
  EVT_HUMIDITY_LOWER = (0x0B, HexFieldFormats.FLAG, SensorType.HUMIDITY)
  """`Report when lower than a humidity value`
  
  SPEC: Over-limit event."""
  EVT_PRESSURE_HIGHER = (0x0D, HexFieldFormats.FLAG, SensorType.PRESSURE)
  """`Report when higher than an air pressure value`
  
  SPEC: Over-limit event."""
  EVT_PRESSURE_LOWER = (0x0E, HexFieldFormats.FLAG, SensorType.PRESSURE)
  """`Report when lower than an air pressure value`
  
  SPEC: Over-limit event."""
  EVT_AUXTEMP_HIGHER = (0x29, HexFieldFormats.FLAG, SensorType.TEMPERATURE_AUX)
  """`Report when higher than an AUX temperature value`
  
  SPEC: Over-limit event."""
  EVT_AUXTEMPT_LOWER = (0x2A, HexFieldFormats.FLAG, SensorType.TEMPERATURE_AUX)
  """`Report when lower than an AUX temperature value`
  
  SPEC: Over-limit event."""
  EVT_CO2_HIGHER = (0x39, HexFieldFormats.FLAG, SensorType.CO2)
  """`Report when higher than a CO2 value`
  
  SPEC: Over-limit event."""
  EVT_CO2_LOWER = (0x3A, HexFieldFormats.FLAG, SensorType.CO2)
  """`Report when lower than a CO2 value`
  
  SPEC: Over-limit event."""
  EVT_TVOC_HIGHER = (0x57, HexFieldFormats.FLAG, SensorType.TVOC)
  """`Report when higher than a TVOC value`
  
  SPEC: Over-limit event."""
  EVT_TVOC_LOWER = (0x58, HexFieldFormats.FLAG, SensorType.TVOC)
  """`Report when lower than a TVOC value`
  
  SPEC: Over-limit event."""
  EVT_PM25_HIGHER = (0x59, HexFieldFormats.FLAG, SensorType.PM25)
  """`Report when higher than a PM2.5 value`
  
  SPEC: Over-limit event."""
  EVT_PM25_LOWER = (0x5A, HexFieldFormats.FLAG, SensorType.PM25)
  """`Report when lower than a PM2.5 value`
  
  SPEC: Over-limit event."""
  EVT_PM10_HIGHER = (0x5B, HexFieldFormats.FLAG, SensorType.PM10)
  """`Report when higher than a PM10 value`
  
  SPEC: Over-limit event."""
  EVT_PM10_LOWER = (0x5C, HexFieldFormats.FLAG, SensorType.PM10)
  """`Report when lower than a PM10 value`
  
  SPEC: Over-limit event."""
  EVT_NOISE_HIGHER = (0x5D, HexFieldFormats.FLAG, SensorType.NOISE)
  """`Report when higher than a noise value`
  
  SPEC: Over-limit event."""
  EVT_NOISE_LOWER = (0x5E, HexFieldFormats.FLAG, SensorType.NOISE)
  """`Report when lower than a noise value`
  
  SPEC: Over-limit event."""
  EVT_LIGHT_HIGHER = (0x5F, HexFieldFormats.FLAG, SensorType.LIGHT)
  """`Report when higher than a light value`
  
  SPEC: Over-limit event."""
  EVT_LIGHT_LOWER = (0x60, HexFieldFormats.FLAG, SensorType.LIGHT)
  """`Report when lower than a light value`
  
  SPEC: Over-limit event."""
  
  
  # commands
  CMD_FACTORY_RESET = (0x1E, HexFieldFormats.UNKNOWN) # TODO: confirm format
  """`Reset to the factory settings`"""
  CMD_MQTT_WIFI = (0x20, HexFieldFormats.WIFI)
  """`Set Wi-Fi account and password` - only for Wi-Fi/MQTT capable devices
  
  SPEC: The content is: `"SSID","PASSOWRD"`"""
  CMD_MQTT_BROKER = (0x25, HexFieldFormats.MQTT)
  """`MQTT connection` - only for Wi-Fi/MQTT capable devices
  
  SPEC: "The content is (separate with spaces)：`URL port username password clientid sub_topic pub_topic`"""
  CMD_NBIOT_SPLICE = (0x26, HexFieldFormats.UNKNOWN) # TODO: confirm format
  """`Data splicing package command` - NBIoT only
  
  SPEC: It is used for unpacking identification when sending NB-IoT long packets. The content is the total number of packets + packet serial number + packet length, the KEY content needs to be after the "byte replacement" KEY."""
  CMD_NBIOT_REPLACEMENT = (0x27, HexFieldFormats.NBIOT_BYTE_REPLACE)
  """`Protocol byte replacement` - NBIoT only
  
  SPEC: The NB-IoT module cannot send 0x1A/0x1B/0x08, this KEY is used to identify and replace these three bytes. KEY content has 3 bytes, the first is used to replace 0x1A, the second is used to replace 0x1B, the third is used to replace 0x08, if the byte does not need to be replaced, use 0x43 to indicate."""
  CMD_CONNECTION_ENCRYPTION = (0x28, HexFieldFormats.ENCRYPTION_KEY)
  """`Set data encryption` key, empty to disable
  
  SPEC: The content is a 16-byte AES key to indicate encryption, and the content is empty to indicate no encryption."""
  CMD_BLE_POWER = (0x2B, HexFieldFormats.BLE_POWER)
  """`Set Bluetooth broadcast transmission power`"""
  CMD_BLE_NAME = (0x36, HexFieldFormats.BLE_NAME)
  """`Set BLE broadcast name`
  
  SPEC: Length should not exceed 28 bytes."""
  CMD_CO2_CALIBRATE = (0x41, HexFieldFormats.BOOL)
  """`Manual calibration of CO2`
  
  SPEC: 1 byte. 1: perform calibration."""
  
  # sensor data fields
  DATA_PRESSURE_HISTORICAL = (0x2D, HexFieldFormats.PRESSURE_PRECISE, SensorType.PRESSURE)
  """`Historical data reporting (air pressure 0.01 pa)`
  
  SPEC: The air pressure uses 4 bytes, and the others use 2 bytes."""
  DATA_PRESSURE_REALTIME = (0x2E, HexFieldFormats.PRESSURE_PRECISE, SensorType.PRESSURE)
  """`Historical data reporting (air pressure 0.01 pa)`
  
  SPEC: The air pressure uses 4 bytes, and the others use 2 bytes."""
  DATA_MAIN_TH_OFFSET = (0x2F, HexFieldFormats.TH_OFFSET) # TODO: ??
  """`Main body temperature and humidity offset`
  
  SPEC: 2 bytes temperature (step is 0.1) + 2 bytes humidity (step is 0.1)."""
  DATA_AUX_TH_OFFSET = (0x30, HexFieldFormats.TH_OFFSET) # TODO: ??
  """`AUX temperature and humidity offset`
  
  SPEC: 2 bytes temperature (step is 0.1) + 2 bytes humidity (step is 0.1)."""
  DATA_PRESSURE_OFFSET = (0x31, HexFieldFormats.PRESSURE_OFFSET, SensorType.PRESSURE)
  """`Air pressure offset` - 0.1 Pa???
  
  SPEC: 2 bytes (step is 0.1)."""
  DATA_AUX_TH = (0x32, HexFieldFormats.SENSOR_AUX_TH) # TODO: ??
  """`AUX temperature and humidity data`
  
  SPEC: 2 bytes temperature (positive offset 500) + 2 bytes humidity."""
  
  # unknown
  UNKNOWN_TIMESTAMP = (0x15, HexFieldFormats.UNKNOWN)
  """SPEC: Timestamp"""
  UNKNOWN_REALTIME_DATA_REPORTING_S = (0x42, HexFieldFormats.UNKNOWN)
  """SPEC: Real-time data reporting
  
  SPEC: Duration, unit is seconds."""
  
  UNKNOWN = (0xFF, HexFieldFormats.UNKNOWN)
  """Unknown Key, attempt to parse as TLV with raw bytes value"""

  fmt: HexFieldFormats
  associated_sensor: SensorType | None
  def __new__(cls, value, fmt, associated_sensor=None):
    obj = int.__new__(cls, value)
    obj._value_ = value
    obj.fmt = fmt
    obj.associated_sensor = associated_sensor
    return obj
