# SPDX-FileCopyrightText: 2025-present Daniel Skowroński <daniel@skowron.ski>
#
# SPDX-License-Identifier: BSD-3-Clause

import click
from rich.console import Console
from emqx_client_monitor.cli.table import render_clients_table

from emqx_client_monitor.__about__ import __version__
from emqx_client_monitor.config.schema import AgentConfig
from emqx_client_monitor.config.load import load_cli_config
from emqx_client_monitor.emqx.api import get_current_clients
from emqx_client_monitor.prom.exporter import run_exporter


@click.group(
  context_settings={"help_option_names": ["-h", "--help"]},
  invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="emqx-client-monitor")
@click.option(
  "--cfg",
  default="~/.config/emqx-client-monitor/config.yaml",
  type=click.Path(dir_okay=False),
  help="Path to configuration file.",
  show_default=True,
)
@click.pass_context
def emqx_client_monitor(ctx: click.Context, cfg: str):
  click.echo(f"EMQX Client Monitor version {__version__}")
  config = load_cli_config(cfg)
  ctx.ensure_object(dict)
  ctx.obj["cfg"] = cfg
  ctx.obj["config"] = config
  if ctx.invoked_subcommand is None:
    click.echo(ctx.get_help())


@emqx_client_monitor.command("check", help="One-time check of monitored clients' connection status.")
@click.option(
  "--all",
  is_flag=True,
  default=False,
  help="Check all clients, not only the monitored ones.",
)
@click.pass_context
def check_command(ctx: click.Context, all: bool):
  config: AgentConfig = ctx.obj["config"]
  emqx_config = config.emqx
  monitored_clients = config.monitored_clients if not all else []
  try:
    clients = get_current_clients(emqx_config, monitored_clients)
    if len(clients) == 0:
      if all:
        click.echo("No clients are currently connected.")
      else:
        click.echo("No monitored clients are currently connected.")
    else:
      table = render_clients_table(clients, all)
      console = Console()
      console.print(table)
  except Exception as e:
    click.echo(f"Error while fetching clients: {e}", err=True)
    ctx.exit(1)


@emqx_client_monitor.command("prometheus", help="Prometheus exporter")
@click.pass_context
def prometheus_command(ctx: click.Context):
  config: AgentConfig = ctx.obj["config"]
  run_exporter(config)
