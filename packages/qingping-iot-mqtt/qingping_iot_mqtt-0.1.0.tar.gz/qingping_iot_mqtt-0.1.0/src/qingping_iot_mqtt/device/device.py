# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause
from abc import abstractmethod
from collections.abc import Iterable
from enum import StrEnum
import platform
from typing import Optional
from pydantic import BaseModel
from qingping_iot_mqtt.protocols.base import DeviceCommand, ProtocolMessage, ProtocolMessageDirection, DeviceSettings
from qingping_iot_mqtt.protocols.common_spec import ProtocolName, DeviceModel
import qingping_iot_mqtt.const as const
from qingping_iot_mqtt.config.schema import DeviceConfig, BrokerConfig
from qingping_iot_mqtt.protocols.json import JsonCommandRequestSettings, JsonProtocol, JsonProtocolMesssage
from qingping_iot_mqtt.protocols.hex import HexCommandRequestSettings, HexProtocol, HexFrame, HexProtocolMesssage
from paho.mqtt import client as paho_mqtt_client
from typing import Protocol, Awaitable, Callable, Any
from qingping_iot_mqtt.protocols.base import SensorReadingsContext, ProtocolMessage
import asyncio


import logging
logger = logging.getLogger(__name__)

class QingpingParseError(Exception):
  """Exception raised on Qingping device payload parsing errors."""
  pass
class QingpingCommandStatus(StrEnum):
  UNKNOWN = "unknown"
  SENT = "sent"
  ACKNOWLEDGED = "acknowledged"
  SUCCEEDED = "succeeded"
  FAILED = "failed"
class QingpingDeviceBackend:
  async def publish(self, payload: bytes) -> None:
    pass
  async def pass_sensor_readings(self, readings: Iterable[SensorReadingsContext]) -> None:
    pass
  async def log_message(self, raw: bytes, normalized: str, processed: ProtocolMessage) -> None:
    pass
  
class QingpingDevice:
  """Wrapper for Qingping IoT device instance to be used with external MQTT backend (QingpingDeviceBackend).
  
  Class exposes methods to directly but asynchronously interact with device and react to messages from device.
  """
  dev_cfg: DeviceConfig
  backend: QingpingDeviceBackend
  #settings: DeviceSettings = DeviceSettings()
  
  _pending_command: Optional[DeviceCommand] = None
  _pending_fut: Optional[asyncio.Future[ProtocolMessage]]
  _request_lock: asyncio.Lock
  _loop: asyncio.AbstractEventLoop
  
  def __init__(self, dev_cfg: DeviceConfig, mqtt_cfg: BrokerConfig, loop: asyncio.AbstractEventLoop | None = None) -> None:
    self.dev_cfg = dev_cfg
    self.mqtt_cfg = mqtt_cfg
    self.mqtt_client_id = f"{mqtt_cfg.client_id}-{dev_cfg.mac.replace(':','')}"
    self._request_lock = asyncio.Lock()
    self._loop = loop or asyncio.get_event_loop()
    self._pending_fut: Optional[asyncio.Future[ProtocolMessage]] = None
  
  def consume_message(self, payload: bytes, topic: str) -> None:
    """Handle incoming message from device."""
    pass
  async def send_command(self, cmd: DeviceCommand, expect_response: bool, timeout: int = 10) -> Any:
    if not expect_response:
      await self.backend.publish(cmd.encode())
      return True
    
    async with self._request_lock:
      if self._pending_command is not None:
        logger.warning("Another command is pending, cannot send get_device_settings request.")
        return None
      self._pending_command = cmd
      fut: asyncio.Future[ProtocolMessage] = self._loop.create_future()
      self._pending_fut = fut
      await self.backend.publish(cmd.encode())
      try:
        resp = await asyncio.wait_for(fut, timeout)
        return resp
      finally:
        self._pending_fut = None
        self._pending_command = None
  async def get_device_settings(self) -> Optional[DeviceSettings]:
    raise NotImplementedError()
  async def set_device_settings(self, settings: DeviceSettings) -> bool:
    raise NotImplementedError()