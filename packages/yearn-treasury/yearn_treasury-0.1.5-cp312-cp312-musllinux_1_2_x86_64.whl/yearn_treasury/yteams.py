# This is a loose copy of an old script and will not likely be refactored into something pretty
import os
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from functools import lru_cache
from logging import getLogger
from typing import Any, Dict, Final, List, Set, Tuple

import a_sync
from brownie import chain
from eth_portfolio.structs import TokenTransfer
from eth_portfolio._ydb.token_transfers import InboundTokenTransfers
from pandas import DataFrame, MultiIndex
from y import Contract, Network, get_block_at_timestamp
from y.exceptions import ContractNotVerified

from yearn_treasury.constants import ZERO_ADDRESS


DATA_FOLDER: Final = os.path.join(".", "data")
OUTPUT_FILE: Final = os.path.join(DATA_FOLDER, f"teams_revenue_{chain.id}.csv")
NUMBER_OF_MONTHS_TO_INCLUDE_IN_REPORT: Final = 36

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


# TODO: maybe move this into constants for reuse
yteams_addresses = {
    Network.Mainnet: {
        "v3": {
            "ms": "0x33333333D5eFb92f19a5F94a43456b3cec2797AE",
            "splits": {"0x2A12CAA2c13Af03c117D836CA3811a5Ca946133B": 12.5},
        },
        "dinobots": {
            "ms": "0x2C01B4AD51a67E2d8F02208F54dF9aC4c0B778B6",
            "splits": {"0xC4f238633A85A854C4702d2c66264771D1fa7904": 17.5},
        },
        "ylockers": {
            "ms": "0x4444AAAACDBa5580282365e25b16309Bd770ce4a",
            "splits": {
                "0xac580302548FCCBBf00020de20C3A8AA516821AD": 2.5,
                "0x794f80E899c772de9E326eC83cCfD8D94e208B49": 6.25,
                "0x5FF0f87b05806ce89967638CA727Af8309d92A89": 12.5,
                "0x5A7575368797695BefD785f546C6b8B7e9D37f8c": 15.625,
            },
        },
        # "ylockers others": {"ms": "0x4444AAAACDBa5580282365e25b16309Bd770ce4a","splits":{"0x5FF0f87b05806ce89967638CA727Af8309d92A89":12.5, "0x5A7575368797695BefD785f546C6b8B7e9D37f8c":15.625}},
        "yaudit": {
            "ms": "0x8973B848775a87a0D5bcf262C555859b87E6F7dA",
            "splits": {
                "0xd7A1DBe236A38528D54317415a530b2326068373": 35,
                "0xF104F38592287e25868BD8C3dcCCa1a311916f88": 35,
                "0x1a9D272C3b7fE427639702A332D51348213B0bC1": 20,
            },
        },
        "yeth": {
            "ms": "0xeEEEEeeeEe274C3CCe13f77C85d8eBd9F7fd4479",
            "splits": {"0x14EFe6390C6758E3fE4379A14e3B329274b1b072": 25},
        },
        "yfarm": {
            "ms": "0x55157997cb324a374cCd7c40914ff879Fd9D515C",
            "splits": {"0x0B3cCe59E038373F6008D9266B6D6eB4d21689b1": 50},
        },
        "sms": {
            "ms": "0x16388463d60FFE0661Cf7F1f31a7D658aC790ff7",
            "splits": {"0xd6748776CF06a80EbE36cd83D325B31bb916bf54": 25},
        },
    }
}[Network(chain.id)]


logger: Final = getLogger(__name__)

_not_verified: Final[Set[str]] = set()
_warned: Final[Set[TokenTransfer]] = set()

_known_tokens_without_prices: Final = frozenset({"SAFE", "vCOW"})
"""When there is a PriceError for these tokens, no logs will be emitted."""


@lru_cache(maxsize=None)
def transfers_for(wallet: str) -> InboundTokenTransfers:
    return InboundTokenTransfers(wallet, 0, load_prices=True)  # type: ignore [arg-type]


async def calculate_teams_revenue_expenses() -> None:
    logger.info("Starting process to calculate teams revenues and expenses")
    timestamps = get_timestamps_for_report()

    async def get_coros_for_timestamp(dt: datetime) -> Dict[str, Dict[str, Decimal]]:
        return await a_sync.gather(
            {
                label: total(label, wallet_info, dt)
                for label, wallet_info in yteams_addresses.items()
            }
        )

    all_data = await a_sync.gather({dt: get_coros_for_timestamp(dt) for dt in timestamps})

    result = {
        (dt, teams, movement): values
        for dt, data in all_data.items()
        for teams, info in data.items()
        for movement, values in info.items()
    }
    df = DataFrame.from_dict(result, orient="index")
    print("------------")
    # print(df.index)
    # print(df.head(10))
    df.index = MultiIndex.from_tuples(df.index)
    print("********")
    # print(df.index)
    df.reset_index(inplace=True)
    df.columns = ["datetime", "team", "label", "value"]
    df.to_csv(OUTPUT_FILE)
    logger.info(
        f"Finished processing yteams calculations and saved file to {os.path.abspath(OUTPUT_FILE)}"
    )


def get_timestamps_for_report() -> List[datetime]:
    now = datetime.now(tz=timezone.utc)
    prev_month_end = datetime(
        year=now.year,
        month=now.month,
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=timezone.utc,
    ) - timedelta(microseconds=1)
    datetimes = []
    print("Exporting report for timestamps:")
    for _ in range(NUMBER_OF_MONTHS_TO_INCLUDE_IN_REPORT):
        print(f" - {prev_month_end}")
        datetimes.append(prev_month_end)
        prev_month_end -= timedelta(days=prev_month_end.day)
    return datetimes


async def total(label: str, wallet_info: Dict[str, Any], timestamp: datetime) -> Dict[str, Decimal]:
    rev = await sum_revenue_transfers.sum(wallet_info["splits"].items(), timestamp=timestamp)
    grants = await sum_grants_received(wallet_info["ms"], timestamp)
    if rev > 10_000_000:
        raise ValueError(rev)
    if grants > 10_000_000:
        raise ValueError(grants)
    net = rev - grants
    if label == "yaudit":
        logger.info("--- %s thru %s ---", label, timestamp)
        logger.info("inbound  %s", rev)
        logger.info("grants  -%s", grants)
        logger.info("net      %s", net)
    return {"revenue": rev, "grants": grants, "total": net}


@a_sync.a_sync(default="async")
async def sum_revenue_transfers(params: Tuple[str, Decimal], timestamp: datetime) -> Decimal:
    wallet, rev_share = params
    block = await get_block_at_timestamp(timestamp)
    total = Decimal(0)
    async for transfer in transfers_for(wallet).yield_thru_block(block):
        transfer = await transfer
        if transfer is None:
            # failed to decode, probably shitcoin
            continue
        if not transfer.value:
            # zero value transfer
            continue
        if transfer.price:
            total += transfer.value * transfer.price
        elif transfer not in _warned and transfer.token not in _known_tokens_without_prices:
            logger.warning(f"BAD: {transfer}")
            _warned.add(transfer)
    return round(total * Decimal((100 - rev_share) / 100), 8)


async def sum_grants_received(wallet: str, timestamp: datetime) -> Decimal:
    grants = Decimal(0)
    block = await get_block_at_timestamp(timestamp)
    async for transfer in transfers_for(wallet).yield_thru_block(block):
        transfer = await transfer
        if transfer is None:
            # failed to decode, probably shitcoin
            continue
        if not transfer.value:
            # zero value transfer
            continue
        if transfer.price:
            if transfer.from_address != ZERO_ADDRESS:
                try:
                    contract = await Contract.coroutine(transfer.from_address)
                    if (
                        hasattr(contract, "recipient") and await contract.recipient == wallet
                    ) or transfer.from_address == "0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52":
                        grants += transfer.value * transfer.price
                except ContractNotVerified as e:
                    if str(e) not in _not_verified:
                        _not_verified.add(str(e))
                        logger.debug(f"{e.__class__.__name__}: {e}")
                except Exception as e:
                    logger.warning(f"{e.__class__.__name__}: {e}")
        elif transfer not in _warned and transfer.token not in _known_tokens_without_prices:
            logger.warning(f"BAD: {transfer}")
            _warned.add(transfer)
    return round(grants, 8)
