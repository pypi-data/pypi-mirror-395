# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class DropReason(StrEnum):
  QUEUE_FULL = "queue_full"
  EXPIRED = "expired"
  TOO_LARGE = "too_large"
  AWAIT_PUBREL_TIMEOUT = "await_pubrel_timeout"


class QoSLevel(StrEnum):
  QOS0 = "0"
  QOS1 = "1"
  QOS2 = "2"


@dataclass
class ClientStatsSingleDirection:
  mqtt_packets: int
  raw_octets: int
  msg_dropped: int
  msg_dropped_by_reason: dict[DropReason, int]
  msg_processed: int
  msg_processed_by_qos: dict[QoSLevel, int]


@dataclass
class ClientInfo:
  client_id: str
  username: str

  clean_start: bool
  keepalive: int

  created_at: datetime
  is_connected: bool
  connected_at: datetime
  is_expired: bool

  subscription_count: int
  inflight: int

  rx: ClientStatsSingleDirection
  tx: ClientStatsSingleDirection

  @classmethod
  def from_dict(cls, data: dict) -> "ClientInfo":
    # unsupported fields: auth_expire_at, awaiting_rel_cnt, awaiting_rel_max, client_attrs, durable, enable_authn, inflight_max, heap_size, expiry_interval, ip_address (doesn't make sense if behind NAT), is_bridge, is_persistent, keepalive, listener, mailbox_len, mountpoint, mqueue_dropped, mqueue_len, mqueue_max, node, peersni, port, proto_name, proto_ver, recv_cnt, reductions, subscriptions_max

    rx = ClientStatsSingleDirection(
      mqtt_packets=data.get("recv_pkt", 0),
      raw_octets=data.get("recv_oct", 0),
      msg_dropped=data.get("recv_msg.dropped", 0),
      msg_dropped_by_reason={
        DropReason.AWAIT_PUBREL_TIMEOUT: data.get("recv_msg.dropped.await_pubrel_timeout", 0),
      },
      msg_processed=data.get("recv_msg", 0),
      msg_processed_by_qos={
        QoSLevel.QOS0: data.get("recv_msg.qos0", 0),
        QoSLevel.QOS1: data.get("recv_msg.qos1", 0),
        QoSLevel.QOS2: data.get("recv_msg.qos2", 0),
      },
    )
    tx = ClientStatsSingleDirection(
      mqtt_packets=data.get("send_pkt", 0),
      raw_octets=data.get("send_oct", 0),
      msg_dropped=data.get("send_msg.dropped", 0),
      msg_dropped_by_reason={
        DropReason.EXPIRED: data.get("send_msg.dropped.expired", 0),
        DropReason.QUEUE_FULL: data.get("send_msg.dropped.queue_full", 0),
        DropReason.TOO_LARGE: data.get("send_msg.dropped.too_large", 0),
      },
      msg_processed=data.get("send_msg", 0),
      msg_processed_by_qos={
        QoSLevel.QOS0: data.get("send_msg.qos0", 0),
        QoSLevel.QOS1: data.get("send_msg.qos1", 0),
        QoSLevel.QOS2: data.get("send_msg.qos2", 0),
      },
    )

    try:
      created_at = datetime.fromisoformat(data.get("created_at", "1969-01-01T00:00:00+00:00"))
    except ValueError:
      created_at = datetime.fromisoformat("1969-01-01T00:00:00+00:00")
    try:
      connected_at = datetime.fromisoformat(data.get("connected_at", "1969-01-01T00:00:00+00:00"))
    except ValueError:
      connected_at = datetime.fromisoformat("1969-01-01T00:00:00+00:00")

    ci = cls(
      client_id=data.get("clientid", "undefined"),
      username=data.get("username", "undefined"),
      clean_start=data.get("clean_start", False),
      keepalive=data.get("keepalive", 0),
      created_at=created_at,
      connected_at=connected_at,
      is_connected=data.get("connected", False),
      is_expired=data.get("is_expired", False),
      subscription_count=data.get("subscriptions_cnt", 0),
      rx=rx,
      tx=tx,
      inflight=data.get("inflight_cnt", 0),
    )
    return ci
