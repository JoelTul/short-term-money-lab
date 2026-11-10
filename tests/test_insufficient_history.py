import pandas as pd
import pytest

from short_term_money.backtest import evaluate_strategy
from short_term_money.config import WindowSpec


@pytest.mark.parametrize("count", [1, 3])
def test_insufficient_history_has_clear_error(count):
    wealth = pd.Series(
        [100.0] * count,
        index=pd.date_range("2020-01-31", periods=count, freq="ME"),
    )
    with pytest.raises(ValueError, match="No complete rolling windows"):
        evaluate_strategy(wealth, [WindowSpec("3 months", 3, 3)])


def test_minimum_valid_history_produces_one_observation():
    wealth = pd.Series(
        [100.0, 101.0, 102.0, 103.0],
        index=pd.date_range("2020-01-31", periods=4, freq="ME"),
    )
    result = evaluate_strategy(wealth, [WindowSpec("3 months", 3, 3)])
    assert result.loc["3 months", "observations"] == 1
    assert result.loc["3 months", "median_end_return"] == pytest.approx(0.03)
