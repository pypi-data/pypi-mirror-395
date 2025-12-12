# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause

from datetime import datetime
from datetime import timezone
from emqx_client_monitor.emqx.client_info import ClientInfo
import human_readable
from rich.table import Table
from rich.style import Style
from rich.text import Text


def fmt_count(count: int, is_error: bool = False) -> Text:
  if count == 0:
    return Text(str(count), style=Style(dim=True))
  else:
    if is_error:
      return Text(str(count), style=Style(color="red", bold=True))
    else:
      return Text(str(count))


def fmt_ago(dt: datetime, now: datetime, flag: bool = True) -> Text:
  if dt is None or not flag:
    return Text("never", style=Style(color="red"))
  else:
    delta = now - dt
    return Text(human_readable.time_delta(delta))


def render_clients_table(clients: dict[str, ClientInfo], all: bool) -> Table:
  table = Table(show_header=True, header_style="bold magenta")
  if all:
    table.add_column("Client ID", style=Style(bold=True))
  else:
    table.add_column("Alias", style=Style(bold=True))
  # table.add_column("Client ID")
  table.add_column("Created\n(time ago)", justify="right")
  table.add_column("Keep\nalive", justify="right")
  table.add_column("Connected\n(time ago)", justify="right")
  table.add_column("Sub\nCnt", justify="right")
  table.add_column("MsgIn\nFlght", justify="right")
  table.add_column("RX\nMsg", justify="right")
  table.add_column("RX\nDrop", justify="right")
  table.add_column("TX\nMsg", justify="right")
  table.add_column("TX\nDrop", justify="right")
  now = datetime.now(timezone.utc)
  for client_id, client_info in sorted(clients.items()):
    human_readable.activate("en_ABBR")
    delta = human_readable.time_delta(client_info.keepalive)
    human_readable.deactivate()
    table.add_row(
      client_id,
      # client_info.client_id,
      fmt_ago(client_info.created_at, now),
      delta,
      fmt_ago(client_info.connected_at, now, client_info.is_connected),
      fmt_count(client_info.subscription_count),
      fmt_count(client_info.inflight),
      fmt_count(client_info.rx.msg_processed),
      fmt_count(client_info.rx.msg_dropped, is_error=True),
      fmt_count(client_info.tx.msg_processed),
      fmt_count(client_info.tx.msg_dropped, is_error=True),
    )
  return table
