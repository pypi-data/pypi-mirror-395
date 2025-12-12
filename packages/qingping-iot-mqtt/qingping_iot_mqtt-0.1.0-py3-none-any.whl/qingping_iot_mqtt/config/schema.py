# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause
import platform
from typing import Optional
from pydantic import BaseModel
from qingping_iot_mqtt.protocols.common_spec import ProtocolName, DeviceModel
import qingping_iot_mqtt.const as const

class BrokerConfig(BaseModel):
  host: str
  port: int
  username: str
  password: str
  client_id: str = platform.node()
  keepalive: int = 60
  clean_session: bool = True
class DeviceConfig(BaseModel):
  alias: str
  mac: str
  topic_up: str
  topic_down: str
  protocol: ProtocolName
  model: DeviceModel=DeviceModel.UNKNOWN

class LoggingDatabase(BaseModel):
  sqlite_path: str
  enabled: bool = False

class VictoriaMetricsConfig(BaseModel):
  import_endpoint: str
  ignore_ssl_errors: Optional[bool] = False
  custom_ca_certs_path: Optional[str] = None
  user: str
  password: str
  enabled: bool = False
  metrics_prefix: Optional[str] = "qingping_iot_"
  retry_attempts: Optional[int] = const.DEFAULT_RETRY_ATTEMPTS

class CliConfig(BaseModel):
  broker: BrokerConfig
  devices: list[DeviceConfig]
  logging_db: Optional[LoggingDatabase] = None
  victoria_metrics: Optional[VictoriaMetricsConfig] = None
