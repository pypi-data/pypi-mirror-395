# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause

import sys

if __name__ == "__main__":
  from emqx_client_monitor.cli import emqx_client_monitor

  sys.exit(emqx_client_monitor())
