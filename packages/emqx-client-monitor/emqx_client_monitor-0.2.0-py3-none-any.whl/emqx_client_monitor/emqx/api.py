# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause

from emqx_client_monitor.config.schema import EmqxConfig, MonitoredClientConfig
from emqx_client_monitor.emqx.client_info import ClientInfo
import requests


def parse_clients_list(data: list[dict], monitored_clients: list[MonitoredClientConfig]) -> dict[str, ClientInfo]:
  monitored_client_aliases = {mc.client_id: mc.alias for mc in monitored_clients}
  skip_filtering = len(monitored_client_aliases) == 0
  clients = {}
  for item in data:
    client_id = item.get("clientid", "undefined")
    if skip_filtering:
      clients[client_id] = ClientInfo.from_dict(item)
    elif client_id in monitored_client_aliases:
      clients[monitored_client_aliases[client_id]] = ClientInfo.from_dict(item)
  return clients


def get_current_clients(
  emqx_config: EmqxConfig, monitored_clients: list[MonitoredClientConfig]
) -> dict[str, ClientInfo]:
  # FIXME: pagination handling
  url = f"{emqx_config.api_url}/v5/clients?page=1&limit=10000&fields=all"
  for mc in monitored_clients:
    url += f"&clientid={mc.client_id}"  # this is safe string, because of ClientId constraints
  for attempt in range(emqx_config.attempts):
    try:
      resp = requests.get(
        url,
        auth=(emqx_config.api_key, emqx_config.api_secret),
        timeout=emqx_config.timeout_seconds,
        verify=emqx_config.ssl,
      )
      resp.raise_for_status()
      data = resp.json()
      clients_data = data.get("data", [])
      return parse_clients_list(clients_data, monitored_clients)
    except (requests.RequestException, ValueError) as e:
      if attempt + 1 == emqx_config.attempts:
        raise e
  raise RuntimeError("Unreachable code reached in get_current_clients")
