# EMQX Client Monitor

Prometheus-compatible exporter/monitor for watching EMQX MQTT clients.

**This is work in progress.**

[EMQX](https://www.emqx.com) doesn't expose Prometheus endpoint for watching individual client connections and relying on [`SYS` subscribed events](https://docs.emqx.com/en/emqx/latest/observability/mqtt-system-topics.html#client-subscribed-and-unsubscribed-events) may not be reliable in some scenarios. This agent uses [EMQX's REST API](https://docs.emqx.com/en/emqx/latest/admin/api.html) to monitor connection state of configured clients and expose Prometheus-style endpoint for further ingestion.

Primary use-case is monitoring of IoT devices, which connect to network for short periods of time to publish and receive MQTT messages, especially those that do not transmit any heartbeats.

It is intended to be deployed on Kubernetes cluster and automatically ingested to Prometheus. Some manual modes are available for convenience. 

## Important assumptions

### Client (and resulting metric) uniqueness

It is based on following attributes:

- client `alias` from configuration
- MQTT client ID (from config), which must be unique per-broker (so it's also unique per server response)
- MQTT username (from server response)
- broker `alias` from configuration (this allows multiple instances of monitor to be ingested into one Prometheus)

Following fields are ignored for this purpose:

- IP address and port number of client - those may change over time (e.g. from DHCP) and are anyway problematic with NAT; in future, they may get exposed as metric (IP converted to integer)
- EMQX node - it may be random in round-robin cluster; in future, this may get exposed as metric via some mapping coming from agent configuration (right now it's string like `"emqx@emqx-0.emqx-headless.namespace.svc.cluster.local"`)
- all connection attributes like *clean start*, because they are client configurable

---

## Usage

### Prerequisites

- API key and secret from any admin EMQX user

### Configuration

Prepare configuration file based on [`examples/config.yaml`](./examples/config.yaml). By default, this program uses `~/.config/emqx-client-monitor/config.yaml`, but it can be overridden with `--cfg` flag. 

#### `emqx`

```yaml
emqx:
  api_key: "01234567890abcde"
  api_secret: "exampleSecretKey1234567890ABCDEFGHIJKLMNOPQRS"
  api_url: "http://emqx:18083/api/"
  ssl: true  # or path to CA bundle
  alias: LocalEMQX
```

Required:

- `api_key` and `api_secret` are outputs from EMQX itself
- `api_url` must be URL to base EMQX API endpoint (ending with `/api/`)
- `alias` is name for EMQX broker, it should be unique among multiple instances of this program being ingested by single Prometheus DB

Optional:

- `ssl` is parameter passed to `requests` library as `verify` - it's either:
  - default `True` for validation of Root CA certs using whatever your Python trusts
  - `False` is insecure mode (for brave and lazy people)
  - string *path*, which points to CA chain; this is useful for handling private Root CA on systems where Python doesn't use system chains
- `timeout_seconds` is EMQX API connection timeout (default `5`)
- `attempts` allows multiple attempts before failing (default `3`)

#### `monitored_clients`

```yaml
monitored_clients:
  - alias: QingpingCO2_Room1
    client_id: "qingping-DEADBEEF1234"
  - alias: QingpingCO2_Room2
    client_id: "qingping-DEADBEEF5678"
```

It's a list of clients to be monitored. Each entry contains `client_id` for matching MQTT client ID (it's unique on broker) and `alias` used as extra label.

#### `prometheus`

TBD

### Running

#### `check`

This is a sub-command for manually checking connected clients once and printing human-readable table. Flag `--all` can be used to ignore `monitored_clients` and get all clients connected (alias column stores client ID).

Example output:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┳━━━━━┳━━━━━━━┳━━━━━━━━━┳━━━━━━┳━━━━━┳━━━━━━┓
┃                        ┃    Created ┃  Keep ┃  Connected ┃ Sub ┃ MsgIn ┃      RX ┃   RX ┃  TX ┃   TX ┃
┃ Alias                  ┃ (time ago) ┃ alive ┃ (time ago) ┃ Cnt ┃ Flght ┃     Msg ┃ Drop ┃ Msg ┃ Drop ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━╇━━━━━╇━━━━━━━╇━━━━━━━━━╇━━━━━━╇━━━━━╇━━━━━━┩
│ HumidifierWaterRefTerm │   16 hours │   10s │   16 hours │   4 │     0 │   24279 │    0 │  16 │    0 │
│ QingpingIoTMQTT_Client │ 39 minutes │    1m │ 39 minutes │   8 │     0 │       0 │    0 │ 126 │    0 │
│ QingpingCO2_Room1      │   a second │    2m │   a second │   0 │     0 │       0 │    0 │   0 │    0 │
│ QingpingCO2_Room2      │  4 minutes │    2m │  4 minutes │   1 │     0 │       2 │    0 │   0 │    0 │
│ QingpingCO2_Room3      │    13 days │    2m │    13 days │   1 │     0 │   38455 │    0 │  69 │    0 │
│ RTL433_Room1           │    a month │    1m │   23 hours │   0 │     0 │  702456 │    0 │   0 │    0 │
│ RTL433_Room2           │    30 days │    1m │    18 days │   0 │     0 │ 5184897 │    0 │   0 │    0 │
│ ZAMEL                  │     7 days │   32s │     7 days │   0 │     0 │ 6007727 │    0 │   0 │    0 │
└────────────────────────┴────────────┴───────┴────────────┴─────┴───────┴─────────┴──────┴─────┴──────┘
```

#### `prometheus`

TBD
