"""Run a small backtest with illustrative data (not historical returns)."""

import numpy as np
import pandas as pd

from short_term_money import WINDOW_BUCKETS, evaluate_universe


def main():
    dates = pd.date_range("2020-01-31", periods=61, freq="ME")
    months = np.arange(len(dates))

    # Repeat a made-up year with both gains and a sharp decline.
    stock_returns = np.tile(
        [0.03, 0.02, 0.01, -0.18, -0.07, 0.08,
         0.06, 0.04, 0.03, 0.02, 0.01, 0.03],
        5,
    )

    cash = pd.Series(100 * (1.0025 ** months), index=dates)
    stocks = pd.Series(
        np.r_[100, 100 * np.cumprod(1 + stock_returns)],
        index=dates,
    )
    inflation = pd.Series(100 * (1.002 ** months), index=dates)

    results = evaluate_universe(
        {"Cash (synthetic)": cash, "Stocks (synthetic)": stocks},
        WINDOW_BUCKETS,
        inflation_index=inflation,
    )

    columns = [
        "strategy",
        "window",
        "observations",
        "median_end_return",
        "p05_end_return",
        "nominal_loss_probability",
        "real_loss_probability",
        "window_loss_probability",
    ]

    for column in columns[3:]:
        results[column] = results[column].map(lambda value: f"{value:.1%}")

    print("SYNTHETIC DEMO — illustrative values, not historical market data")
    print(results[columns].to_string(index=False))


if __name__ == "__main__":
    main()