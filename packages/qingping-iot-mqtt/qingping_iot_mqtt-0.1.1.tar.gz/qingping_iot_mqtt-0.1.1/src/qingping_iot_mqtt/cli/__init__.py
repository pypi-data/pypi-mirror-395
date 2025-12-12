# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause
import click

from qingping_iot_mqtt.__about__ import __version__
from qingping_iot_mqtt.protocols.base import ProtocolMessageDirection, ProtocolMessageCategory
from qingping_iot_mqtt.protocols.hex import HexProtocol, HexFrame, HexSensorReadingMessage
from qingping_iot_mqtt.config.load import load_cli_config
from qingping_iot_mqtt.cli.mqtt import run_mqtt_loop
from qingping_iot_mqtt.cli.db import initialize_db
from qingping_iot_mqtt.cli.vm import initialize_vm

import coloredlogs
import logging

from qingping_iot_mqtt.protocols.json import JsonProtocol
logger = logging.getLogger(__name__)


def _parse_hex_string(label: str, value: str, *, allow_empty: bool = False) -> bytes:
  cleaned = "".join(ch for ch in value if not ch.isspace())
  if not cleaned:
    if allow_empty:
      return b""
    raise click.BadParameter(f"{label} cannot be empty.")
  if len(cleaned) % 2 != 0:
    raise click.BadParameter(f"{label} must have an even number of hex digits.")
  try:
    return bytes.fromhex(cleaned)
  except ValueError as exc:
    raise click.BadParameter(f"Invalid {label}: {exc}") from exc


def _resolve_direction(requested, default):
  return requested or default


def _ensure_hex_proto(proto: str):
  if proto in {"hex", "auto"}:
    return
  raise click.ClickException(f"Protocol '{proto}' is not supported yet.")


def _decode_hex_payload(raw: bytes, direction: ProtocolMessageDirection):
  if raw.startswith(b'{'):
    click.echo("Detected JSON protocol frame. Use appropriate tool to decode JSON frames.")
    return
  protocol = HexProtocol()
  click.echo("HEX protocol detected.")
  message = protocol.decode_message(raw, direction)
  click.echo(message.dump())
  if message.category == ProtocolMessageCategory.READINGS:
    click.echo(HexSensorReadingMessage(message).dump())
def _decode_json_payload(payload: str, direction: ProtocolMessageDirection):
  if not payload.startswith('{') or not payload.endswith('}'):
    click.echo("Detected non-JSON protocol frame. Use appropriate tool to decode HEX frames.")
    return
  protocol = JsonProtocol()
  click.echo("JSON protocol detected.")
  message = protocol.decode_message(payload.encode('utf-8'), direction)
  click.echo(message.dump())

@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.option("--cfg", default="~/.config/qingping/qingping-mqtt.yaml", type=click.Path(dir_okay=False), help="Path to configuration file.", show_default=True)
@click.option("--verbosity", "-v", count=True, help="Increase output verbosity (can be used multiple times).")
@click.version_option(version=__version__, prog_name="qingping-iot-mqtt")
@click.pass_context
def qingping_iot_mqtt(ctx: click.Context, cfg: str, verbosity: int) -> None:
  """Qingping IoT MQTT utilities."""
  ctx.ensure_object(dict)
  ctx.obj["cfg"] = cfg
  if ctx.invoked_subcommand is None:
    click.echo(ctx.get_help())
  
  lvl = logging.INFO
  if verbosity := ctx.params.get("verbosity", 0):
    if verbosity == 1:
      lvl=logging.DEBUG
  coloredlogs.install(fmt="[%(asctime)s] %(message)s", level=lvl)
  logging.info(f"Qingping IoT MQTT CLI v{__version__}")


@qingping_iot_mqtt.command("subscribe")
# TODO: consider logging directly to time-series DB like InfluxDB (HA and Prometheus do not support importing past events)
@click.pass_context
def subscribe(ctx: click.Context):
  """Subscribe to Qingping IoT MQTT broker and process live messages."""
  cfg_path = ctx.obj["cfg"]
  cfg=load_cli_config(cfg_path)
  if cfg.logging_db:
    initialize_db(cfg.logging_db, cfg.devices)
  if cfg.victoria_metrics:
    initialize_vm(cfg.victoria_metrics, cfg.devices)
  run_mqtt_loop(cfg)


@qingping_iot_mqtt.group("manual")
@click.option("--proto", type=click.Choice(["auto", "hex", "json"]), default="auto", show_default=True, help="Protocol to use.")
@click.option("--to-device", is_flag=True, default=False, help="Treat payload as message to device.")
@click.option("--from-device", is_flag=True, default=False, help="Treat payload as message from device.")
@click.pass_context
def manual_group(ctx: click.Context, proto: str, to_device: bool, from_device: bool):
  """Manual protocol helpers."""
  if to_device and from_device:
    raise click.BadParameter("Choose only one of --to-device/--from-device.")
  direction = None
  if to_device:
    direction = ProtocolMessageDirection.SERVER_TO_DEVICE
  elif from_device:
    direction = ProtocolMessageDirection.DEVICE_TO_SERVER
  ctx.ensure_object(dict)
  ctx.obj["manual"] = {"proto": proto, "direction": direction}

@manual_group.command("decode")
@click.option("--payload", "payload", required=True, help="Raw frame as hex string (spaces allowed) or as quoted string.")
@click.pass_context
def manual_decode(ctx: click.Context, payload: str):
  """Decode payload coming from a protocol frame."""
  settings = ctx.obj.get("manual", {})
  proto = settings.get("proto", "auto")
  direction = _resolve_direction(settings.get("direction"), ProtocolMessageDirection.DEVICE_TO_SERVER)
  click.echo(f"Direction: {direction.name}")
  if proto == "auto":
    if payload.startswith('{') and payload.endswith('}'):
      proto = "json"
    else:
      proto = "hex"
  if proto == "json":
    _decode_json_payload(payload, direction)
    return
  if proto == "hex":
    raw = _parse_hex_string("payload", payload)
    _decode_hex_payload(raw, direction)
    return

@manual_group.command("encode")
@click.option("--raw-cmd", "raw_cmd_hex", required=True, help="HEX command byte (e.g. 31).")
@click.option("--payload", "payload_hex", default="", help="Payload as hex string (spaces allowed).")
@click.pass_context
def manual_encode(ctx: click.Context, raw_cmd_hex: str, payload_hex: str):
  """Encode payload into protocol frame."""
  settings = ctx.obj.get("manual", {})
  proto = settings.get("proto", "auto")
  direction = _resolve_direction(settings.get("direction"), ProtocolMessageDirection.SERVER_TO_DEVICE)
  _ensure_hex_proto(proto)
  cmd_bytes = _parse_hex_string("raw-cmd", raw_cmd_hex)
  if len(cmd_bytes) != 1:
    raise click.BadParameter("raw-cmd must describe exactly one byte.")
  payload_bytes = _parse_hex_string("payload", payload_hex, allow_empty=True)
  frame = HexFrame.construct_frame(cmd_bytes[0], payload_bytes)
  click.echo("Protocol: HEX")
  click.echo(f"Direction: {direction.name}")
  click.echo(f"Frame: {frame.frame.hex()}")
