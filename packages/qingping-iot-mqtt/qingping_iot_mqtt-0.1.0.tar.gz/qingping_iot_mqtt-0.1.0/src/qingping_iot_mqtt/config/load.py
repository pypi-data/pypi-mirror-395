# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause
from .schema import CliConfig
import yaml
from pathlib import Path


def load_cli_config(path: str) -> CliConfig:
  path_expanded = Path(path).expanduser()
  with open(path_expanded, "r", encoding="utf-8") as f:
    raw_cfg = yaml.safe_load(f)
  _cli_cfg = CliConfig.model_validate(raw_cfg)
  return _cli_cfg
