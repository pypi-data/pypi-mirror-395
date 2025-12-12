# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause
from qingping_iot_mqtt.config.schema import VictoriaMetricsConfig, DeviceConfig
from qingping_iot_mqtt.protocols.base import SensorReadingsContext, SensorReadingType
import datetime
import logging
import json
from qingping_iot_mqtt.protocols.common_spec import SensorType
import qingping_iot_mqtt.const as const
import requests
logger = logging.getLogger(__name__)

_vm_config: VictoriaMetricsConfig | None = None
_verify = True
_ignore_vm: bool = True
_device_topic: dict[str, DeviceConfig] = {}

def vm_metric_name(sensor: SensorType) -> str:
  """Get the Victoria Metrics metric name for a given sensor."""
  if _vm_config is None or _vm_config.metrics_prefix is None:
    prefix = "qingping_iot_"
  else:
    prefix = _vm_config.metrics_prefix
  if prefix and not prefix.endswith("_"):
    prefix += "_"
  sensor_name = sensor.name.lower()
  return f"{prefix}{sensor_name}"
def initialize_vm(vm_config: VictoriaMetricsConfig, devices: list[DeviceConfig]) -> None:
  """Initialize the Victoria Metrics connection."""
  global _vm_config, _device_mac, _device_topic, _ignore_vm, _verify
  
  if vm_config is None or not vm_config.enabled:
    _ignore_vm = True
    logging.debug("Victoria Metrics logging is disabled.")
    return
  else:
    _vm_config = vm_config
    _ignore_vm = False
    logging.debug(f"Initializing Victoria Metrics logging to {vm_config.import_endpoint}...")
    _device_topic = {}
    for device in devices:
      _device_topic[device.topic_up] = device # TODO: move to mqtt main code
    
    _verify = True
    if _vm_config.ignore_ssl_errors:
      _verify = False
    if _vm_config.custom_ca_certs_path:
      _verify = _vm_config.custom_ca_certs_path

    # TODO: test connection?
def log_sensor_reading(topic: str, ctx: SensorReadingsContext) -> None:
  """Log a sensor reading context entries to the VictoriaMetrics."""
  if _ignore_vm or _vm_config is None:
    return
  device = _device_topic.get(topic)
  if device is None:
    logger.debug(f"Device for topic {topic} not found, skipping VM logging.")
    return
  payload = ""
  for r in ctx.readings:
    if r.sensor not in device.model.device_model_info.sensors:
      #logger.debug(f"Sensor {r.sensor.name} not supported by device model {device.model.value}, skipping VM logging.")
      continue
    entry = {
      "timestamps": [int(ctx.timestamp * 1_000)],  # milliseconds - as required by VM
      "values": [r.value],
      "metric": {
        "__name__": vm_metric_name(r.sensor),
        "device_mac": device.mac.replace(":", "").upper(),
        "device_name": device.alias,
        "sensor": r.sensor.name.lower(),
        "unit": r.unit,
        "device_model": device.model.value,
        "device_protocol": device.protocol.value,
      }
    }
    payload += json.dumps(entry) + "\n"
  if not payload:
    return
  
  attempt = 0
  while attempt < _vm_config.retry_attempts if _vm_config.retry_attempts else const.DEFAULT_RETRY_ATTEMPTS:
    attempt += 1
    try:
      response = requests.post(
        url=_vm_config.import_endpoint,
        data=payload,
        auth=( _vm_config.user, _vm_config.password ),
        headers={ "Content-Type": "application/json" },
        verify=_verify,
        timeout=5
      )
      if response.status_code not in [200, 204]:
        logger.error(f"Failed to log to Victoria Metrics, status code {response.status_code}: {response.text}")
      else:
        logger.debug(f"Successfully logged sensor readings to Victoria Metrics for device {device.alias} ({device.mac}).")
        return
    except Exception as e:
      logger.error(f"Error logging to Victoria Metrics: {e}")
  logger.error(f"Exceeded maximum retry attempts ({_vm_config.retry_attempts}) for Victoria Metrics logging.")
  