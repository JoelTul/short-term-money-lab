"""Compare historical ETF returns across withdrawal windows."""

from pathlib import Path

import pandas as pd

from short_term_money import WINDOW_BUCKETS, evaluate_universe
from short_term_money.backtest import rolling_window_outcomes
from short_term_money.data import download_adjusted_prices, mix_indices


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

    strategies = {
        "S&P 500 ETF (SPY)": prices["SPY"],
        "Treasury bill ETF (BIL)": prices["BIL"],
        "1-3 year Treasury bond ETF (SHY)": prices["SHY"],
    }

    for stock_weight in (0.10, 0.20, 0.40):
        label = f"{stock_weight:.0%} SPY / {1 - stock_weight:.0%} BIL"
        strategies[label] = mix_indices(
            prices["SPY"],
            prices["BIL"],
            risky_weight=stock_weight,
        )

    results = evaluate_universe(strategies, WINDOW_BUCKETS)

    # Pair each result with BIL from the same starting and ending months.
    comparisons = []
    for window in WINDOW_BUCKETS:
        bil_outcomes = rolling_window_outcomes(prices["BIL"], window)[
            ["start_date", "end_date", "end_return"]
        ].rename(columns={"end_return": "bil_end_return"})

        for strategy_name, wealth_index in strategies.items():
            outcomes = rolling_window_outcomes(wealth_index, window)
            paired = outcomes.merge(
                bil_outcomes,
                on=["start_date", "end_date"],
                validate="one_to_one",
            )
            if len(paired) != len(outcomes):
                raise SystemExit("Could not align all results with BIL.")

            excess = paired["end_return"] - paired["bil_end_return"]
            comparisons.append(
                {
                    "strategy": strategy_name,
                    "window": window.label,
                    "median_excess_end_return_vs_bil": float(excess.median()),
                    "probability_below_bil": float((excess < 0).mean()),
                }
            )

    results = results.merge(
        pd.DataFrame(comparisons),
        on=["strategy", "window"],
        validate="one_to_one",
    )
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
        "median_excess_end_return_vs_bil",
        "probability_below_bil",
    ]

    display = results[columns].copy()
    for column in columns[3:]:
        display[column] = display[column].map(lambda value: f"{value:.1%}")

    print(
        f"Shared sample: {prices.index[0]:%Y-%m} through "
        f"{prices.index[-1]:%Y-%m}"
    )
    print("Adjusted ETF prices; before taxes and inflation.")
    print("Excess return is measured in percentage points versus BIL.")
    print(display.to_string(index=False))
    print(f"Saved numeric results to {output_path}")


if __name__ == "__main__":
    main()