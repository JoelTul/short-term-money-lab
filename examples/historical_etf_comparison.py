"""Compare historical SPY and BIL returns across withdrawal windows."""

from pathlib import Path

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

    # Compare both funds over the same complete months.
    prices = prices[["SPY", "BIL"]].dropna()
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
    results["observations"] = results["observations"].astype(int)
    results.insert(0, "sample_start", prices.index[0].strftime("%Y-%m"))
    results.insert(1, "sample_end", prices.index[-1].strftime("%Y-%m"))

    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "outputs" / "historical_etf_comparison.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False)

    columns = [
        "strategy",
        "window",
        "observations",
        "median_end_return",
        "p05_end_return",
        "nominal_loss_probability",
        "window_loss_probability",
    ]

    display = results[columns].copy()
    for column in columns[3:]:
        display[column] = display[column].map(lambda value: f"{value:.1%}")

    print(
        f"Shared sample: {prices.index[0]:%Y-%m} through "
        f"{prices.index[-1]:%Y-%m}"
    )
    print("Adjusted ETF prices; before taxes and inflation.")
    print(display.to_string(index=False))
    print(f"Saved numeric results to {output_path}")


if __name__ == "__main__":
    main()