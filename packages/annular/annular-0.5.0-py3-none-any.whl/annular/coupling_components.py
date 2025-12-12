"""coupling_components.py: Utilities for coupling using MUSCLE3."""

import logging

import numpy as np
import pandas as pd
from libmuscle import Grid, Message
from ymmsl import Component, Conduit, Model, Ports

logger = logging.getLogger(__name__)


def compact_market_info_to_msg(
    price: np.ndarray | None, scheduled_demand: np.ndarray | None, timestamp: float
) -> Message:
    """Compact market information to a message.

    Args:
        price: A numpy array with market prices.
        scheduled_demand: A numpy array with the demand scheduled for a satellite.
        timestamp: Floating point value to serve as timestamp for model coordination.

    Returns:
        A muscle3 message where the data attribute is a dictionary with keys
        "price" and "scheduled_demand".
    """
    if price is None and scheduled_demand is None:
        return Message(timestamp=timestamp, data={"price": None, "scheduled_demand": None})

    price = Grid(price)
    scheduled_demand = Grid(scheduled_demand)
    data_dict = {
        "price": price,
        "scheduled_demand": scheduled_demand,
    }
    return Message(timestamp=timestamp, data=data_dict)


def extract_market_info_from_msg(msg: Message) -> tuple[np.ndarray | None, np.ndarray | None, float]:
    """Extract the market information message.

    Args:
        msg: muscle3 Message containing a dictionary with keys "price" and
            "scheduled_demand" for a single satellite.

    Returns:
        tuple: the market price, scheduled demand as numpy arrays, and the timestamp.
    """
    if not isinstance(msg.data["price"], Grid):
        return None, None, msg.timestamp

    # messages are read-only, and we modify them later
    price = msg.data["price"].array.copy()
    demand_met = msg.data["scheduled_demand"].array.copy()

    return price, demand_met, msg.timestamp


def compact_bids_to_msg(demand_bids: pd.DataFrame, timestamp: float) -> Message:
    """Compact a DataFrame of (block) bids columns into a MUSCLE3 Message.

    This takes bids in the following format:

    +--------------------+------------------+-----------+----------+-------+
    | exclusive_group_id | profile_block_id | timestamp | quantity | price |
    +--------------------+------------------+-----------+----------+-------+
    | ...                | ...              | ...       | ...      | ...   |
    +--------------------+------------------+-----------+----------+-------+

    where:

    - `exclusive_group_id`: ID of which exclusive group this bid belongs to
    - `profile_block_id`: ID of which profile block this bid belongs to
    - `timestamp`: timestamp for this bid
    - `quantity`: quantity for this bid
    - `price`: price for this bid

    and (exclusive_group_id, profile_block_id, timestamp) are its Index.

    Every bid must have a `profile_block_id` and `exclusive_group_id`. If a bid
    does not make use of profile block or exclusive group functionality, the
    `exclusive_group_id` must be unique, while `profile_block_id` can be any value.

    The resulting message contains the dataframe converted to a dictionary where

        - column and index names become dictionary keys
        - column and index values become dictionary values.

    Args:
        demand_bids: Dataframe table of the bids from a satellite model.
        timestamp: Floating point value to serve as timestamp for model coordination.

    Returns:
        MUSCLE3 message object containing the bids table information in a
        dictionary.
    """
    demand_bids_dict = {col: Grid(demand_bids[col].to_numpy(), None) for col in demand_bids.columns}
    # add indices
    for level in demand_bids.index.names:
        level_values = demand_bids.index.get_level_values(level)
        if level == "timestamp":
            # `.astype(int) / 1e9` is equivalent to calling `.timestamp()`, but works on whole array
            level_values = level_values.astype(np.int64) / 1e9

        demand_bids_dict[level] = Grid(level_values.to_numpy(), None)

    msg = Message(timestamp, data=demand_bids_dict)
    return msg


def extract_bids_from_msg(msg: Message) -> pd.DataFrame:
    """Reconstruct a DataFrame of (block) bids from a MUSCLE3 Message.

    The `.data` attribute of the incoming message should be a dictionary
    with the following keys: price, quantity, exclusive_group_id, profile_block_id,
    timestamp.

    From this data, a DataFrame in the following format is created:

    +--------------------+------------------+-----------+----------+-------+
    | exclusive_group_id | profile_block_id | timestamp | quantity | price |
    +--------------------+------------------+-----------+----------+-------+
    | ...                | ...              | ...       | ...      | ...   |
    +--------------------+------------------+-----------+----------+-------+

    where:

    - `exclusive_group_id`: ID of which exclusive group this bid belongs to
    - `profile_block_id`: ID of which profile block this bid belongs to
    - `timestamp`: timestamp for this bid
    - `quantity`: quantity for this bid
    - `price`: price for this bid

    and (exclusive_group_id, profile_block_id, timestamp) are its Index.

    Every bid must have a `profile_block_id` and `exclusive_group_id`. If a bid
    does not make use of profile block or exclusive group functionality, the
    `exclusive_group_id` must be unique, while `profile_block_id` can be any value.

    Args:
        msg: MUSCLE3 message object containing the bids table information as
            a dictionary.

    Returns:
        Dataframe table of the bids from a satellite model.
    """
    demand_bids = pd.DataFrame()
    logger.debug("msg.data is %s", msg.data)
    logger.debug("msg.data[quantity] is %s", msg.data["quantity"].array)
    data_cols = ["quantity", "price"]
    for col in data_cols:
        demand_bids[col] = msg.data[col].array

    timestamps = [pd.Timestamp.utcfromtimestamp(t) for t in msg.data["timestamp"].array]
    demand_bids.index = pd.MultiIndex.from_arrays(
        [msg.data["exclusive_group_id"].array, msg.data["profile_block_id"].array, timestamps],
        names=["exclusive_group_id", "profile_block_id", "timestamp"],
    )
    return demand_bids


def get_coupling_setup(config_name: str, number_of_satellites: int) -> Model:
    """Create the MUSCLE3 coupling configuration for the energy system network.

    Args:
        config_name: name of this run to be used as model name
        number_of_satellites: number of satellites to spin up

    Returns:
        MUSCLE3 Model object with the standard coupling configuration
    """
    components = [
        Component("central", "central", None, Ports(o_i=["market_info_out"], s=["bids_in"])),
        Component("satellite", "satellite", [number_of_satellites], Ports(f_init=["market_info_in"], o_f=["bids_out"])),
    ]

    conduits = [
        Conduit("central.market_info_out", "satellite.market_info_in"),
        Conduit("satellite.bids_out", "central.bids_in"),
    ]

    model = Model(config_name, components, conduits)
    return model
