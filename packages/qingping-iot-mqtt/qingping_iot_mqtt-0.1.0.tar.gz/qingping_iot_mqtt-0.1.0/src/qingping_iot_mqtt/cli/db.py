# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause
from peewee import Model, DateTimeField, CharField, FloatField, DatabaseProxy, Database, BlobField, SqliteDatabase
from qingping_iot_mqtt.config.schema import LoggingDatabase, DeviceConfig
from qingping_iot_mqtt.protocols.base import SensorReadingsContext
import datetime
import logging
logger = logging.getLogger(__name__)

_db: Database | None = None
_db_proxy= DatabaseProxy()
_ignore_db: bool = True
_device_mac: dict[str, DeviceConfig] = {}
_device_topic: dict[str, DeviceConfig] = {}

class LoggedSensorReading(Model):
  timestamp = DateTimeField()
  mac = CharField()
  name = CharField()
  sensor = CharField()
  value = FloatField()
  unit = CharField()
  status = CharField()

  class Meta:
    database = _db_proxy
    table_name = "sensor_readings"
    
class LoggedRawPayload(Model):
  timestamp = DateTimeField()
  topic = CharField()
  payload = BlobField()

  class Meta:
    database = _db_proxy
    table_name = "raw_payloads"

def initialize_db(db_config: LoggingDatabase, devices: list[DeviceConfig]) -> None:
  """Initialize the database connection and create tables if they do not exist."""
  global _db, _db_proxy, _device_mac, _device_topic, _ignore_db
  
  if db_config is None or not db_config.enabled:
    _ignore_db = True
    logging.debug("Database logging is disabled.")
    return
  else:
    _ignore_db = False
    logging.debug(f"Initializing database at {db_config.sqlite_path}...")

  _db = SqliteDatabase(db_config.sqlite_path)
  _db.connect()
  _db_proxy.initialize(_db)
  _db.create_tables([LoggedSensorReading, LoggedRawPayload], safe=True)
  
  _device_mac = {}
  _device_topic = {}
  for device in devices:
    _device_mac[device.mac] = device
    _device_topic[device.topic_up] = device
    _device_topic[device.topic_down] = device

def log_sensor_reading(topic: str, ctx: SensorReadingsContext) -> None:
  """Log a sensor reading context entries to the database."""
  global _db, _device_topic, _ignore_db
  if _ignore_db:
    return
  if _db is None:
    raise RuntimeError("Database not initialized")
  
  device = _device_topic.get(topic)
  if device is None:
    raise ValueError(f"Unknown device for topic {topic}")

  
  for r in ctx.readings:
    if r.sensor not in device.model.device_model_info.sensors:
      logger.debug(f"Sensor {r.sensor.name} not supported by device model {device.model.value}, skipping logging.")
      continue
    LoggedSensorReading.create(
      timestamp=datetime.datetime.fromtimestamp(ctx.timestamp, datetime.timezone.utc),
      mac=device.mac,
      name=device.alias,
      sensor=r.sensor.name,
      value=r.value,
      unit=r.unit,
      status=r.format_status(simple=True)
    )
def log_raw_payload(topic: str, payload: bytes) -> None:
  """Log a raw payload to the database."""
  global _db, _ignore_db
  if _ignore_db:
    return
  if _db is None:
    raise RuntimeError("Database not initialized")
  
  LoggedRawPayload.create(
    timestamp=datetime.datetime.now(datetime.timezone.utc),
    topic=topic,
    payload=payload
  )
