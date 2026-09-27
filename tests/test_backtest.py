import numpy as np
import pandas as pd
import pytest

from short_term_money.backtest import (
    evaluate_strategy,
    rolling_window_outcomes,
    summarize_outcomes,
)
from short_term_money.config import WindowSpec
from short_term_money.data import mix_indices, modeled_hysa_index


def monthly_series(values, name="test"):
    index = pd.date_range("2020-01-31", periods=len(values), freq="ME")
    return pd.Series(values, index=index, name=name, dtype=float)


def test_fixed_three_month_return():
    wealth = monthly_series([100, 101, 102, 103, 104])
    result = rolling_window_outcomes(
        wealth,
        WindowSpec("3 months", 3, 3),
    )
    assert len(result) == 2
    assert result.iloc[0]["end_return"] == pytest.approx(0.03)
    assert result.iloc[0]["worst_window_return"] == pytest.approx(0.03)


def test_window_uses_worst_possible_withdrawal_month():
    wealth = monthly_series([100, 110, 90, 120, 130])
    result = rolling_window_outcomes(
        wealth,
        WindowSpec("1-3 months", 1, 3),
    )
    first = result.iloc[0]
    assert first["end_return"] == pytest.approx(0.20)
    assert first["worst_window_return"] == pytest.approx(-0.10)


def test_real_returns_use_inflation_index():
    wealth = monthly_series([100, 102, 104, 106])
    inflation = monthly_series([100, 101, 102, 103], name="cpi")
    result = rolling_window_outcomes(
        wealth,
        WindowSpec("3 months", 3, 3),
        inflation_index=inflation,
    )
    expected = (106 / 100) / (103 / 100) - 1
    assert result.iloc[0]["real_end_return"] == pytest.approx(expected)


def test_summary_reports_loss_probabilities():
    outcomes = pd.DataFrame(
        {
            "end_return": [-0.10, 0.05, 0.10, 0.20],
            "worst_window_return": [-0.20, -0.01, 0.02, 0.10],
        }
    )
    summary = summarize_outcomes(outcomes)
    assert summary["nominal_loss_probability"] == pytest.approx(0.25)
    assert summary["window_loss_probability"] == pytest.approx(0.50)
    assert summary["expected_shortfall_05"] == pytest.approx(-0.10)


def test_modeled_hysa_is_non_decreasing_when_rates_are_nonnegative():
    rates = monthly_series([5.0, 5.0, 5.0, 5.0], name="rate")
    wealth = modeled_hysa_index(
        rates,
        spread_bps=50,
        implementation_lag_months=0,
    )
    assert (wealth.pct_change().dropna() >= 0).all()


def test_mixed_index_validates_weight():
    values = monthly_series(np.linspace(100, 110, 6))
    with pytest.raises(ValueError):
        mix_indices(values, values, risky_weight=1.1)


def test_evaluate_strategy_labels_output():
    wealth = monthly_series(np.linspace(100, 120, 10))
    result = evaluate_strategy(
        wealth,
        [WindowSpec("1-3 months", 1, 3)],
    )
    assert list(result.index) == ["1-3 months"]
    assert result.loc["1-3 months", "observations"] == 7

