"""Compare historical SPY and BIL returns across withdrawal windows."""

import pandas as pd

from short_term_money import WINDOW_BUCKETS, evaluate_universe
from short_term_money.data import download_adjusted_prices, mix_indices


def main():
    try:
        prices = download_adjusted_prices(
            ["SPY", "BIL"],
            start="2008-01-01",
        )
    except Exception as exc:
        raise SystemExit(f"Market data download failed: {exc}") from exc

    # Compare both funds over the same months.
    prices = prices[["SPY", "BIL"]].dropna()

    # Exclude the current month, which may not be finished.
    last_complete_month = (
        pd.Timestamp.now(tz="UTC").tz_localize(None).to_period("M") - 1
    )
    prices = prices[prices.index.to_period("M") <= last_complete_month]

    if len(prices) < 37:
        raise SystemExit("At least 37 complete months of shared data are needed.")

    expected_months = pd.date_range(
        prices.index[0], prices.index[-1], freq="ME"
    )
    if not prices.index.equals(expected_months):
        raise SystemExit("The downloaded prices contain missing months.")

    strategies = {
        "S&P 500 ETF (SPY)": prices["SPY"],
        "Treasury bill ETF (BIL)": prices["BIL"],
    }

    for stock_weight in (0.10, 0.20, 0.40):
        label = f"{stock_weight:.0%} SPY / {1 - stock_weight:.0%} BIL"
        strategies[label] = mix_indices(
            prices["SPY"],
            prices["BIL"],
            risky_weight=stock_weight,
        )

    results = evaluate_universe(strategies, WINDOW_BUCKETS)

    columns = [
        "strategy",
        "window",
        "observations",
        "median_end_return",
        "p05_end_return",
        "nominal_loss_probability",
        "window_loss_probability",
    ]

    results["observations"] = results["observations"].astype(int)
    for column in columns[3:]:
        results[column] = results[column].map(lambda value: f"{value:.1%}")

    print(
        f"Shared sample: {prices.index[0]:%Y-%m} through "
        f"{prices.index[-1]:%Y-%m}"
    )
    print("Adjusted ETF prices; before taxes and inflation.")
    print(results[columns].to_string(index=False))


if __name__ == "__main__":
    main()