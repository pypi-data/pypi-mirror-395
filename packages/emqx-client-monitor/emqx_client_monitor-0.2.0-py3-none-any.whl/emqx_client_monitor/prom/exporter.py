# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause

import time
import threading
from prometheus_client import start_http_server, REGISTRY
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily
from prometheus_client.registry import Collector
from emqx_client_monitor.config.schema import AgentConfig, EmqxConfig, MonitoredClientConfig, PrometheusConfig
from emqx_client_monitor.emqx.api import get_current_clients
from emqx_client_monitor.emqx.client_info import ClientInfo, QoSLevel, DropReason


class LazyCollector(Collector):
  METRIC_PREFIX: str = "emqx_client_monitor"

  emqx_cfg: EmqxConfig
  prom_cfg: PrometheusConfig
  monitored_clients: list[MonitoredClientConfig]

  _lock: threading.Lock
  _cached_at: float
  ttl_s: int
  _cached: dict[str, ClientInfo]

  def __init__(self, config: AgentConfig):
    self.ttl_s = config.prometheus.ttl_seconds
    self._lock = threading.Lock()
    self._cached = {}
    self._cached_at = 0.0
    self.emqx_cfg = config.emqx
    self.prom_cfg = config.prometheus
    self.monitored_clients = config.monitored_clients

  label_names = ["broker", "alias", "client_id"]

  def get_labels(self, alias: str, client: ClientInfo) -> list[str]:
    return [
      self.emqx_cfg.alias,
      alias,
      client.client_id,
    ]

  def collect(self):
    now = time.time()
    with self._lock:
      if self._cached == {} or (now - self._cached_at) > self.ttl_s:
        try:
          self._cached = get_current_clients(emqx_config=self.emqx_cfg, monitored_clients=self.monitored_clients)
          self._cached_at = now
        except Exception as e:
          print(f"Error while fetching clients for Prometheus exporter: {e}")
      data = self._cached

    connected = GaugeMetricFamily(f"{self.METRIC_PREFIX}_connected", "Is client connected", labels=self.label_names)
    for mc in self.monitored_clients:
      if mc.alias in data:
        v = 1 if data[mc.alias].is_connected else 0
        connected.add_metric([self.emqx_cfg.alias, mc.alias, mc.client_id], v)
      else:
        connected.add_metric([self.emqx_cfg.alias, mc.alias, mc.client_id], 0)
    yield connected

    inflight = GaugeMetricFamily(
      f"{self.METRIC_PREFIX}_inflights", "Number of inflight messages", labels=self.label_names
    )
    sub_count = GaugeMetricFamily(
      f"{self.METRIC_PREFIX}_subscriptions", "Number of subscriptions", labels=self.label_names
    )
    created_at = GaugeMetricFamily(
      f"{self.METRIC_PREFIX}_created_at", "Client creation time (epoch seconds)", labels=self.label_names
    )
    connected_at = GaugeMetricFamily(
      f"{self.METRIC_PREFIX}_connected_at", "Client last connected time (epoch seconds)", labels=self.label_names
    )
    msgs = CounterMetricFamily(
      f"{self.METRIC_PREFIX}_messages_processed",
      "Number of received messages processed (total)",
      labels=self.label_names + ["direction"],
    )
    msgs_qos = CounterMetricFamily(
      f"{self.METRIC_PREFIX}_messages_processed_by_qos",
      "Number of received messages processed split by QoS",
      labels=self.label_names + ["direction", "qos"],
    )
    drops = CounterMetricFamily(
      f"{self.METRIC_PREFIX}_messages_dropped",
      "Number of received messages dropped (total)",
      labels=self.label_names + ["direction"],
    )
    drops_reason = CounterMetricFamily(
      f"{self.METRIC_PREFIX}_messages_dropped_by_reason",
      "Number of received messages dropped split by reason",
      labels=self.label_names + ["direction", "reason"],
    )
    octets = CounterMetricFamily(
      f"{self.METRIC_PREFIX}_bytes", "Number of received raw octets (bytes)", labels=self.label_names + ["direction"]
    )
    packets = CounterMetricFamily(
      f"{self.METRIC_PREFIX}_packets", "Number of received MQTT packets", labels=self.label_names + ["direction"]
    )

    for mc in self.monitored_clients:
      if mc.alias in data:
        client = data[mc.alias]
        inflight.add_metric(self.get_labels(mc.alias, client), client.inflight)
        sub_count.add_metric(self.get_labels(mc.alias, client), client.subscription_count)
        if client.created_at is not None:
          created_at.add_metric(self.get_labels(mc.alias, client), client.created_at.timestamp())
        if client.connected_at is not None:
          connected_at.add_metric(self.get_labels(mc.alias, client), client.connected_at.timestamp())
        msgs.add_metric(self.get_labels(mc.alias, client) + ["rx"], client.rx.msg_processed)
        msgs.add_metric(self.get_labels(mc.alias, client) + ["tx"], client.tx.msg_processed)
        for qos in client.rx.msg_processed_by_qos:
          msgs_qos.add_metric(
            self.get_labels(mc.alias, client) + ["rx", qos.value], client.rx.msg_processed_by_qos[qos]
          )
        for qos in client.tx.msg_processed_by_qos:
          msgs_qos.add_metric(
            self.get_labels(mc.alias, client) + ["tx", qos.value], client.tx.msg_processed_by_qos[qos]
          )
        drops.add_metric(self.get_labels(mc.alias, client) + ["rx"], client.rx.msg_dropped)
        drops.add_metric(self.get_labels(mc.alias, client) + ["tx"], client.tx.msg_dropped)
        for reason in client.rx.msg_dropped_by_reason:
          drops_reason.add_metric(
            self.get_labels(mc.alias, client) + ["rx", reason.value], client.rx.msg_dropped_by_reason[reason]
          )
        for reason in client.tx.msg_dropped_by_reason:
          drops_reason.add_metric(
            self.get_labels(mc.alias, client) + ["tx", reason.value], client.tx.msg_dropped_by_reason[reason]
          )
        octets.add_metric(self.get_labels(mc.alias, client) + ["rx"], client.rx.raw_octets)
        octets.add_metric(self.get_labels(mc.alias, client) + ["tx"], client.tx.raw_octets)
        packets.add_metric(self.get_labels(mc.alias, client) + ["rx"], client.rx.mqtt_packets)
        packets.add_metric(self.get_labels(mc.alias, client) + ["tx"], client.tx.mqtt_packets)

    if self.prom_cfg.enable_subscription_count:
      yield sub_count
    if self.prom_cfg.enable_inflight_metrics:
      yield inflight
    if self.prom_cfg.enable_dates:
      yield created_at
      yield connected_at
    if self.prom_cfg.enable_processed_counters:
      yield msgs
      if self.prom_cfg.enable_qos_split:
        yield msgs_qos
    if self.prom_cfg.enable_dropped_counters:
      yield drops
      if self.prom_cfg.enable_reason_split:
        yield drops_reason
    if self.prom_cfg.enable_bytes_metrics:
      yield octets
    if self.prom_cfg.enable_packet_metrics:
      yield packets


def run_exporter(config: AgentConfig):
  REGISTRY.register(LazyCollector(config))
  start_http_server(config.prometheus.port, addr=config.prometheus.address)
  print(f"Prometheus exporter started on {config.prometheus.address}:{config.prometheus.port}")
  while True:
    threading.Event().wait()
