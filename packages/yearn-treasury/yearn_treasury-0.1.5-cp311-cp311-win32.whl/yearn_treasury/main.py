"""
Command-line interface for the Yearn Treasury exporter.

This module provides the `yearn-treasury` CLI, which connects to a Brownie network
(based on the `--network` option or the `BROWNIE_NETWORK_ID` environment variable),
periodically snapshots treasury metrics, and pushes them to Victoria Metrics.
It also launches Yearn Treasury's Grafana dashboard and an optional renderer for visual reports.

Example:
    Run export every 12 hours on mainnet:

    .. code-block:: bash

        yearn-treasury run --network mainnet --interval 12h

CLI Options:
    --network         Brownie network identifier (default: mainnet)
    --interval        Time interval between datapoints (default: 12h)
    --concurrency     Max number of historical blocks to export concurrently (default: 30)
    --daemon          Run as a background daemon (currently unsupported)
    --grafana-port    Port for the Grafana dashboard (default: 3004)
    --victoria-port   Port for the Victoria metrics endpoint (default: 8430)
    --start-renderer  Start the Grafana renderer container for dashboard image export
    --renderer-port   Port for the renderer service (default: 8080)
"""

import asyncio
import os
from argparse import ArgumentParser
from typing import Final, final

from yearn_treasury import yteams


parser = ArgumentParser(description="Treasury CLI")
subparsers = parser.add_subparsers(dest="command", required=True)

run_parser = subparsers.add_parser("run", help="Run the treasury export tool")
run_parser.add_argument(
    "--network",
    type=str,
    help="The brownie network identifier for the RPC to use. Overrides BROWNIE_NETWORK_ID env var if unset.",
    default="mainnet",
)
run_parser.add_argument(
    "--interval",
    type=str,
    help="The time interval between datapoints. Default: 12h",
    default="12h",
)
run_parser.add_argument(
    "--concurrency",
    type=int,
    help="The max number of historical blocks to export concurrently. default: 30",
    default=30,
)
run_parser.add_argument(
    "--daemon",
    action="store_true",
    help="Run as a background daemon (currently unsupported).",
)
run_parser.add_argument(
    "--grafana-port",
    type=int,
    help="Port for the Grafana dashboard where you can view your data. Default: 3004",
    default=3004,
)
run_parser.add_argument(
    "--victoria-port",
    type=int,
    help="Port for the Victoria metrics reporting endpoint. Default: 8430",
    default=8430,
)
run_parser.add_argument(
    "--start-renderer",
    action="store_true",
    help="If set, the Grafana renderer container will be started for dashboard image export. By default, only the grafana container is started.",
)
run_parser.add_argument(
    "--renderer-port",
    type=int,
    help="Port for the service that renders visual reports. Default: 8080",
    default=8080,
)
args = run_parser.parse_args()

# Set BROWNIE_NETWORK_ID from --network flag if not already set
os.environ.setdefault("BROWNIE_NETWORK_ID", args.network)
BROWNIE_NETWORK = os.environ["BROWNIE_NETWORK_ID"]


# TODO: run forever arg
def main() -> None:
    """
    Connect to the configured Brownie network, clean up the database, and start the export loop.

    This function is registered as a console script entrypoint under
    ``yearn-treasury``. It performs the following steps:
        1. Reads the ``BROWNIE_NETWORK_ID`` environment variable (populated from
           the ``--network`` option or existing env var).
        2. Connects to the specified Brownie network.
        3. Merges local SHITCOINS into eth_portfolio's config to skip tokens we don't care about.
        4. Drops any shitcoin transactions that might be in the database.
        5. Constructs an immutable Args subclass to pass CLI parameters to
           :func:`dao_treasury.main.export`.
        6. Exports ports for external services into environment variables.
        7. Runs both the DAO Treasury export and Yearn team revenue/expenses calculation concurrently under asyncio.
    """
    import dao_treasury.db
    import eth_portfolio

    from . import constants, rules, shitcoins

    # Merge local SHITCOINS into eth_portfolio's config to skip tokens we don't care about
    eth_portfolio.SHITCOINS[constants.CHAINID].update(shitcoins.SHITCOINS)  # type: ignore [index]

    # Drop any shitcoin txs that might be in the db
    dao_treasury.db._drop_shitcoin_txs()

    @final
    class Args(constants.Args):
        """
        Immutable container of CLI arguments for export and dashboard/renderer configuration.

        Inherits from DAO Treasury's :class:`constants.Args` and is used to pass runtime
        parameters to the DAO Treasury export and related services.
        """

        network: Final[str] = args.network
        """Brownie network to connect to."""

        interval: Final[str] = args.interval
        """Time interval between snapshots."""

        concurrency: Final[int] = args.concurrency
        """The max number of historical blocks to export concurrently."""

        grafana_port: Final[int] = args.grafana_port
        """Grafana port."""

        victoria_port: Final[int] = args.victoria_port
        """Victoria metrics port."""

        start_renderer: Final[bool] = args.start_renderer
        """Boolean indicating whether to start the renderer container."""

        renderer_port: Final[int] = args.renderer_port
        """Report renderer port."""

        daemon: Final[bool] = args.daemon
        """Whether to run in daemon mode."""

    import dao_treasury.main

    # Export ports for external services (must come after import)
    os.environ["DAO_TREASURY_GRAFANA_PORT"] = str(Args.grafana_port)
    os.environ["DAO_TREASURY_RENDERER_PORT"] = str(Args.renderer_port)
    os.environ["VICTORIA_PORT"] = str(Args.victoria_port)

    async def yearn_wrapper():
        """
        Run the DAO Treasury export and Yearn team revenue/expenses calculation concurrently.

        This coroutine gathers:
            - The main DAO Treasury export process (dao_treasury.main.export)
            - The Yearn teams' revenue and expenses calculation (yteams.calculate_teams_revenue_expenses)
        """
        return await asyncio.gather(
            dao_treasury.main.export(Args),
            yteams.calculate_teams_revenue_expenses(),
        )

    # Start the balance export routine
    asyncio.get_event_loop().run_until_complete(yearn_wrapper())

    rules  # I just put this here so the import isn't flagged as unused
