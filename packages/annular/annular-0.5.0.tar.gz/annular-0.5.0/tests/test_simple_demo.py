import pandas as pd
import pytest

from annular.coupling import run


def test_simple_demo_bids(simple_demo_bid_strategy):
    """Test bids from a 24h bidding strategy.

    In each time period, we
    - expect a bid at the ceiling price for the flexible demand due in the current bidding window
    - expect a bid for flexible demand in the rest of the look-ahead period at the best expected
      market price within that flexible demand's satisfaction window, plus the strategy's bid margin.
    """
    bids = simple_demo_bid_strategy.determine_bids()
    assert len(bids) == 4
    assert bids["quantity"].iloc[1] == 1
    assert bids["price"].iloc[1] == simple_demo_bid_strategy.ceiling_price
    assert bids["quantity"].iloc[3] == 2
    assert bids["price"].iloc[3] == pytest.approx(6 * (1 + simple_demo_bid_strategy.bid_margin))

    simple_demo_bid_strategy.meet_demand([10] * 4, [0, 1, 0, 0])
    bids = simple_demo_bid_strategy.determine_bids()
    assert len(bids) == 5
    assert bids["quantity"].iloc[3] == 2
    assert bids["price"].iloc[3] == simple_demo_bid_strategy.ceiling_price
    assert bids["quantity"].iloc[4] == 3
    assert bids["price"].iloc[4] == pytest.approx(5 * (1 + simple_demo_bid_strategy.bid_margin))

    simple_demo_bid_strategy.meet_demand([10] * 4, [0, 0, 0, 2])
    bids = simple_demo_bid_strategy.determine_bids()
    assert len(bids) == 4
    assert bids["quantity"].iloc[0] == 3
    assert bids["price"].iloc[0] == simple_demo_bid_strategy.ceiling_price
    assert bids["quantity"].iloc[3] == 4
    assert bids["price"].iloc[3] == pytest.approx(8 * (1 + simple_demo_bid_strategy.bid_margin))

    simple_demo_bid_strategy.meet_demand([10] * 4, [3, 0, 0, 0])
    bids = simple_demo_bid_strategy.determine_bids()
    assert len(bids) == 4
    assert bids["quantity"].iloc[2] == 4
    assert bids["price"].iloc[2] == simple_demo_bid_strategy.ceiling_price


def test_simple_demo_meet_demand(simple_demo_bid_strategy):
    """Test that demand is properly met based on bids."""
    simple_demo_bid_strategy.determine_bids()
    simple_demo_bid_strategy.meet_demand(market_price=[5] * 4, demand_met=[0, 1, 0, 2])
    assert simple_demo_bid_strategy.demands["flex+4"].sum() == 7
    simple_demo_bid_strategy.determine_bids()
    simple_demo_bid_strategy.meet_demand(market_price=[6] * 4, demand_met=[0, 0, 0, 0])
    assert simple_demo_bid_strategy.demands["flex+4"].sum() == 7
    simple_demo_bid_strategy.determine_bids()
    simple_demo_bid_strategy.meet_demand(market_price=[6] * 4, demand_met=[3, 0, 0, 4])
    assert simple_demo_bid_strategy.demands["flex+4"].sum() == 0


@pytest.mark.parametrize(
    ["prices", "demand", "error"],
    [
        ([5] * 4, [0, 10, 0, 2], AssertionError),
        ([5] * 4, [0, 0, 0, 0], ValueError),
        ([50] * 4, [0, 1, 0, 2], AssertionError),
    ],
    ids=["too_much_demand", "too_little_demand", "wrong_price_for_demand"],
)
def test_simple_demo_raises(simple_demo_bid_strategy, prices, demand, error):
    """Test that meet_demand fails if incorrect demand or price is provided."""
    simple_demo_bid_strategy.determine_bids()
    with pytest.raises(error):
        simple_demo_bid_strategy.meet_demand(market_price=prices, demand_met=demand)


@pytest.mark.integration
@pytest.mark.gurobi
def test_simple_demo_full(data_dir, tmp_path):
    """Integration test using the simple demo strategy."""
    config_path = data_dir / "test_multi_hour.ymmsl"
    run(config_path, tmp_path)
    results_dir = next(tmp_path.iterdir())
    results = pd.read_csv(results_dir / "hydrogen/dispatch.csv", index_col=0, parse_dates=True)
    assert len(results) == 3
    assert (results["price"].values == 1).all()
    assert (results["demand"].values == [1, 2, 3]).all()
    assert str(results.index[0]) == "2024-01-01 07:00:00+00:00"
    assert str(results.index[1]) == "2024-01-02 03:00:00+00:00"
    assert str(results.index[2]) == "2024-01-03 17:00:00+00:00"
