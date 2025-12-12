# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause
import platform
from typing import Optional
from pydantic import BaseModel
from qingping_iot_mqtt.protocols.base import ProtocolMessage, ProtocolMessageDirection, DeviceSettings
from qingping_iot_mqtt.protocols.common_spec import ProtocolName, DeviceModel
import qingping_iot_mqtt.const as const
from qingping_iot_mqtt.config.schema import DeviceConfig
from qingping_iot_mqtt.protocols.json import JsonCommandRequestSettings, JsonProtocol, JsonProtocolMesssage
from qingping_iot_mqtt.protocols.hex import HexCommandRequestSettings, HexProtocol, HexFrame, HexProtocolMesssage

class QingpingParseError(Exception):
  """Exception raised on Qingping device payload parsing errors."""
  pass
class QingpingDevice:
  cfg: DeviceConfig
  def __init__(self, cfg: DeviceConfig) -> None:
    self.cfg = cfg
  def parse_payload(self, payload: bytes, topic: str) -> ProtocolMessage:
    proto = ProtocolName.identify(payload)
    if proto == ProtocolName.JSON:
      protocol = JsonProtocol()
    elif proto == ProtocolName.HEX:
      protocol = HexProtocol()
    else:
      raise ValueError("Unknown protocol")
    if proto != self.cfg.protocol:
      raise QingpingParseError("Payload protocol does not match device configuration")
    if topic!=self.cfg.topic_up and topic!=self.cfg.topic_down:
      raise QingpingParseError("Topic does not match device configuration")
    direction = ProtocolMessageDirection.DEVICE_TO_SERVER if topic==self.cfg.topic_up else ProtocolMessageDirection.SERVER_TO_DEVICE
    message = protocol.decode_message(payload, direction)
    return message
  def get_request_for_device_settings(self) -> bytes:
    if self.cfg.protocol == ProtocolName.JSON:
      protocol = JsonProtocol()
      cmd = JsonCommandRequestSettings()
      msg = JsonProtocolMesssage(
        direction=ProtocolMessageDirection.SERVER_TO_DEVICE,
        body=cmd.payload)
      return protocol.encode_message(msg)
    elif self.cfg.protocol == ProtocolName.HEX:
      protocol = HexProtocol()
      cmd = HexCommandRequestSettings()
      msg = HexProtocolMesssage(
        direction=ProtocolMessageDirection.SERVER_TO_DEVICE,
        body=cmd.payload)
      return protocol.encode_message(msg)
    else:
      raise ValueError("Unknown protocol")
    