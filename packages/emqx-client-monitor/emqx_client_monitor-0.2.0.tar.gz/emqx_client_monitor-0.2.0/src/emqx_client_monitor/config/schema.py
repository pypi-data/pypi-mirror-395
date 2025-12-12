# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause

from typing import Annotated
from pydantic import BaseModel, Field, StringConstraints


class EmqxConfig(BaseModel):
  api_key: str
  api_secret: str
  api_url: str
  ssl: bool | str = True
  alias: str
  timeout_seconds: int = 5
  attempts: int = 3


ClientId = Annotated[
  str,
  StringConstraints(
    min_length=1,
    max_length=65535,
    pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]*$",
  ),
]
"""While MQTT 5 (and EMQX) allows client ID to be any UTF-8 string up to 65535 bytes, even empty,
this application restricts client IDs to a more manageable subset for configuration purposes
and ensure API query safety. This also ensures Prometheus metric labels are safe."""


class MonitoredClientConfig(BaseModel):
  alias: ClientId
  client_id: ClientId


class PrometheusConfig(BaseModel):
  port: int = 9671
  address: str = "0.0.0.0"
  ttl_seconds: int = 15

  enable_processed_counters: bool = True
  """expose processed message counters"""
  enable_qos_split: bool = False
  """expose per-QoS message counters (ignored if enable_processed_counters is False)"""

  enable_dropped_counters: bool = False
  """expose dropped message counters"""
  enable_reason_split: bool = False
  """expose per-reason dropped message counters (ignored if enable_dropped_counters is False)"""

  enable_bytes_metrics: bool = True
  """expose raw bytes (octets) counters (pub/sub)"""
  enable_packet_metrics: bool = True
  """expose MQTT packets counters (pub/sub)"""

  enable_dates: bool = False
  """expose created_at and connnected_at"""
  enable_inflight_metrics: bool = True
  """expose inflight message counters"""
  enable_subscription_count: bool = True
  """expose subscription count gauge"""
  # enable_connection_states: bool = True
  # """expose is_expired and clean_start flags as 0/1 gauges"""


class AgentConfig(BaseModel):
  emqx: EmqxConfig
  monitored_clients: list[MonitoredClientConfig]
  prometheus: PrometheusConfig = PrometheusConfig()
