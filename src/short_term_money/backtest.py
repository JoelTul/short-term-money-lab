"""Rolling fixed-horizon and withdrawal-window backtests."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
import pandas as pd

from .config import WindowSpec
from .data import to_monthly_index


def _expected_shortfall(values: pd.Series, probability: float = 0.05) -> float:
    """Return the mean of the worst probability mass of observations."""
    clean = values.dropna().sort_values()
    if clean.empty:
        return np.nan
    count = max(1, int(np.ceil(len(clean) * probability)))
    return float(clean.iloc[:count].mean())


def rolling_window_outcomes(
    wealth_index: pd.Series,
    window: WindowSpec,
    inflation_index: pd.Series | None = None,
) -> pd.DataFrame:
    """Calculate outcomes from every eligible starting month.

    `end_return` assumes withdrawal in the latest month. `worst_window_return`
    assumes the investor may have to withdraw at the least favorable month from
    earliest_month through latest_month.
    """
    wealth = to_monthly_index(wealth_index)
    frame = wealth.rename("wealth").to_frame()
    if inflation_index is not None:
        inflation = to_monthly_index(inflation_index).rename("inflation")
        frame = frame.join(inflation, how="inner").dropna()

    records: list[dict[str, object]] = []
    for start_position in range(0, len(frame) - window.latest_month):
        start = frame.iloc[start_position]
        candidate = frame.iloc[
            start_position + window.earliest_month :
            start_position + window.latest_month + 1
        ]
        end = candidate.iloc[-1]

        path_returns = candidate["wealth"] / start["wealth"] - 1.0
        record: dict[str, object] = {
            "start_date": frame.index[start_position],
            "end_date": candidate.index[-1],
            "end_return": float(end["wealth"] / start["wealth"] - 1.0),
            "worst_window_return": float(path_returns.min()),
        }

        if inflation_index is not None:
            real_path = (
                (candidate["wealth"] / start["wealth"])
                / (candidate["inflation"] / start["inflation"])
                - 1.0
            )
            record["real_end_return"] = float(
                (end["wealth"] / start["wealth"])
                / (end["inflation"] / start["inflation"])
                - 1.0
            )
            record["worst_real_window_return"] = float(real_path.min())
        records.append(record)

    return pd.DataFrame.from_records(records)


def summarize_outcomes(outcomes: pd.DataFrame) -> pd.Series:
    """Summarize the left tail and typical result of rolling outcomes."""
    end_returns = outcomes["end_return"].dropna()
    worst_window = outcomes["worst_window_return"].dropna()
    if end_returns.empty:
        raise ValueError("No complete rolling windows are available")

    metrics: dict[str, float | int] = {
        "observations": int(len(end_returns)),
        "mean_end_return": float(end_returns.mean()),
        "median_end_return": float(end_returns.median()),
        "p05_end_return": float(end_returns.quantile(0.05)),
        "worst_end_return": float(end_returns.min()),
        "nominal_loss_probability": float((end_returns < 0.0).mean()),
        "expected_shortfall_05": _expected_shortfall(end_returns),
        "worst_withdrawal_window_return": float(worst_window.min()),
        "window_loss_probability": float((worst_window < 0.0).mean()),
    }

    if "real_end_return" in outcomes:
        real = outcomes["real_end_return"].dropna()
        real_window = outcomes["worst_real_window_return"].dropna()
        metrics.update(
            {
                "median_real_end_return": float(real.median()),
                "p05_real_end_return": float(real.quantile(0.05)),
                "real_loss_probability": float((real < 0.0).mean()),
                "real_window_loss_probability": float(
                    (real_window < 0.0).mean()
                ),
            }
        )
    return pd.Series(metrics)


def evaluate_strategy(
    wealth_index: pd.Series,
    windows: Sequence[WindowSpec],
    inflation_index: pd.Series | None = None,
) -> pd.DataFrame:
    """Evaluate one strategy across several exact or ranged horizons."""
    rows = []
    for window in windows:
        outcomes = rolling_window_outcomes(
            wealth_index, window, inflation_index=inflation_index
        )
        summary = summarize_outcomes(outcomes)
        summary["window"] = window.label
        summary["earliest_month"] = window.earliest_month
        summary["latest_month"] = window.latest_month
        rows.append(summary)
    return pd.DataFrame(rows).set_index("window")


def evaluate_universe(
    strategies: Mapping[str, pd.Series],
    windows: Sequence[WindowSpec],
    inflation_index: pd.Series | None = None,
) -> pd.DataFrame:
    """Evaluate multiple strategies and return a tidy comparison table."""
    results = []
    for strategy_name, wealth_index in strategies.items():
        result = evaluate_strategy(
            wealth_index,
            windows,
            inflation_index=inflation_index,
        ).reset_index()
        result.insert(0, "strategy", strategy_name)
        results.append(result)
    return pd.concat(results, ignore_index=True)

