# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause

import asyncio
from asyncio_mqtt import Client, MqttError
from typing import Awaitable, Callable, Optional
from collections.abc import Iterable
from qingping_iot_mqtt.config.schema import BrokerConfig, DeviceConfig
from qingping_iot_mqtt.device.device import QingpingDeviceBackend
from qingping_iot_mqtt.protocols.base import ProtocolMessage, SensorReadingsContext


import logging
logger = logging.getLogger(__name__)

class CliBackend(QingpingDeviceBackend):
  broker_cfg: BrokerConfig
  dev_cfg: DeviceConfig
  on_message: Callable[[str, bytes], Awaitable[None]] | None = None
  
  _client: Optional[Client] = None
  _stopped: asyncio.Event = asyncio.Event()
  _worker_task: asyncio.Task | None = None
  
  def __init__(self, broker_cfg: BrokerConfig, dev_cfg: DeviceConfig) -> None:
    self.broker_cfg = broker_cfg
    self.dev_cfg = dev_cfg
  def set_on_message_callback(self, callback: Callable[[str, bytes], Awaitable[None]]) -> None:
    self.on_message = callback
  def start(self) -> None:
    client = Client(
      hostname=self.broker_cfg.host,
      port=self.broker_cfg.port,
      client_id=self.broker_cfg.client_id+"-cli-backend-"+self.dev_cfg.mac.replace(":",""),
      username=self.broker_cfg.username,
      password=self.broker_cfg.password,
      keepalive=self.broker_cfg.keepalive,
      clean_session=self.broker_cfg.clean_session,
    )
    self._client = client
    self._worker_task = asyncio.create_task(self._loop())

  async def stop(self) -> None:
    self._stopped.set()
    if self._worker_task:
      self._worker_task.cancel()
      try:
        await self._worker_task
      except asyncio.CancelledError:
        pass
      self._worker_task = None
  async def _loop(self) -> None:
    assert self._client is not None
    client = self._client
    try:
      async with client:
        await client.subscribe(self.dev_cfg.topic_up)

        async with client.unfiltered_messages() as messages:
          async for msg in messages:
            if self._stopped.is_set():
              break
            if self.on_message is not None:
              await self.on_message(msg.topic, msg.payload)
    except MqttError as e:
      logger.error(f"MQTT error in backend loop: {e}")

  async def publish(self, payload: bytes) -> None:
    if self._client is None:
      raise RuntimeError("MQTT client not started.")
    await self._client.publish(self.dev_cfg.topic_down, payload)
  async def pass_sensor_readings(self, readings: Iterable[SensorReadingsContext]) -> None:
    for reading in readings:
      logger.info(f"Readings from {self.dev_cfg.alias}: {reading.dump}")
  async def log_message(self, raw: bytes, normalized: str, processed: ProtocolMessage) -> None:
    logger.info(f"Message  from {self.dev_cfg.alias}: {normalized}")
