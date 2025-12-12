# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause
import sys

if __name__ == "__main__":
    from qingping_iot_mqtt.cli import qingping_iot_mqtt

    sys.exit(qingping_iot_mqtt())
