"""Compare ETF outcomes across separate historical periods."""

from pathlib import Path

import pandas as pd

from short_term_money import WINDOW_BUCKETS, evaluate_universe
from short_term_money.data import download_adjusted_prices, mix_indices


PERIODS = {
    "2008-2014": ("2008-01-01", "2014-12-31"),
    "2015-2019": ("2015-01-01", "2019-12-31"),
    "2020 onward": ("2020-01-01", None),
}


def main():
    tickers = ["SPY", "BIL", "SHY"]

    try:
        prices = download_adjusted_prices(tickers, start="2008-01-01")
    except Exception as exc:
        raise SystemExit(f"Market data download failed: {exc}") from exc

    prices = prices[tickers].dropna()
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

    columns = [
        "strategy",
        "window",
        "observations",
        "median_end_return",
        "p05_end_return",
        "nominal_loss_probability",
        "window_loss_probability",
    ]
    all_results = []

    for period, (start, end) in PERIODS.items():
        sample = prices.loc[start:end]

        if len(sample) < 37:
            raise SystemExit(f"{period} needs at least 37 shared monthly prices.")

        strategies = {
            "S&P 500 ETF (SPY)": sample["SPY"],
            "Treasury bill ETF (BIL)": sample["BIL"],
            "1-3 year Treasury bond ETF (SHY)": sample["SHY"],
        }

        for stock_weight in (0.10, 0.20, 0.40):
            label = f"{stock_weight:.0%} SPY / {1 - stock_weight:.0%} BIL"
            strategies[label] = mix_indices(
                sample["SPY"],
                sample["BIL"],
                risky_weight=stock_weight,
            )

        # Every rolling window must start and finish inside this period.
        results = evaluate_universe(strategies, WINDOW_BUCKETS)
        results["observations"] = results["observations"].astype(int)
        results.insert(0, "period", period)
        results.insert(1, "sample_start", sample.index[0].strftime("%Y-%m"))
        results.insert(2, "sample_end", sample.index[-1].strftime("%Y-%m"))
        all_results.append(results)

        display = results[columns].copy()
        for column in columns[3:]:
            display[column] = display[column].map(lambda value: f"{value:.1%}")

        print(
            f"\n{period}: {sample.index[0]:%Y-%m} through "
            f"{sample.index[-1]:%Y-%m}"
        )
        print(display.to_string(index=False))

    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "outputs" / "historical_period_comparison.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.concat(all_results, ignore_index=True).to_csv(output_path, index=False)

    print("\nBefore taxes and inflation; overlapping observations.")
    print("Periods contain different numbers of observations.")
    print(f"Saved numeric results to {output_path}")


if __name__ == "__main__":
    main()