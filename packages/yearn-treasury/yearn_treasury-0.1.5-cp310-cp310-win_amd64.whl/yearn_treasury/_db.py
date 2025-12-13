"""
Database labeling utility for Yearn Treasury.

This module provides a helper function to set up address nicknames
in the database, mapping key Yearn Treasury addresses to human-readable
labels. It is used during database preparation to ensure that wallet
addresses are clearly labeled in analytics and reporting.

When Yearn Treasury is imported, this module maps important addresses
to descriptive nicknames within the DAO Treasury database entity system
for improved data clarity and prettification of reports.
"""

# mypy: disable-error-code="arg-type"
import time

import dao_treasury._docker
from dao_treasury.db import Address, init_db
from y import Network
from y.constants import CHAINID

from yearn_treasury import constants


def prepare_db() -> None:
    """
    Set up address nicknames in the Yearn Treasury database.

    Maps key Yearn Treasury addresses to human-readable labels for improved
    clarity in analytics and reporting. This function is typically called
    during database preparation to ensure wallet addresses are labeled
    within the DAO Treasury database entity system.
    """
    # We need to start the postgres container earlier than dao-treasury does
    dao_treasury._docker.up("postgres")

    time.sleep(5)

    init_db()

    chad = {Network.Mainnet: "y", Network.Fantom: "f"}[CHAINID]  # type: ignore [index]

    labels = {
        constants.TREASURY_MULTISIG: "Yearn Treasury",
        constants.YCHAD_MULTISIG: f"Yearn {chad}Chad Multisig",
        # constants.STRATEGIST_MULTISIG: "Yearn Strategist Multisig",
        # This wallet is an EOA that has been used to assist in bridging tokens across chains.
        "0x5FcdC32DfC361a32e9d5AB9A384b890C62D0b8AC": "Bridge Assistooor EOA",
    }

    Address.set_nicknames(labels)
