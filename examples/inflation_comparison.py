"""Compare nominal and inflation-adjusted historical ETF returns."""

from pathlib import Path
from urllib.request import urlopen

import pandas as pd

from short_term_money import WINDOW_BUCKETS, evaluate_universe
from short_term_money.data import download_adjusted_prices, mix_indices


CPI_SERIES = "CPIAUCNS"
CPI_URL = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={CPI_SERIES}"


def download_cpi():
    """Load BLS monthly CPI-U from FRED and label observations by month end."""
    with urlopen(CPI_URL, timeout=30) as response:
        data = pd.read_csv(
            response,
            index_col=0,
            parse_dates=[0],
            na_values=".",
        )

    cpi = pd.to_numeric(data[CPI_SERIES], errors="raise")
    cpi = cpi.sort_index().resample("ME").last()
    if cpi.dropna().empty or (cpi.dropna() <= 0).any():
        raise ValueError("CPI data must contain positive index values.")
    return cpi.rename("CPI")


def main():
    tickers = ["SPY", "BIL", "SHY"]
    try:
        prices = download_adjusted_prices(tickers, start="2008-01-01")
        cpi = download_cpi()
    except Exception as exc:
        raise SystemExit(f"Data download failed: {exc}") from exc

    # Use identical complete months for asset prices and inflation.
    shared = prices[tickers].join(cpi, how="inner").dropna()
    last_complete_month = (
        pd.Timestamp.now(tz="UTC").tz_localize(None).to_period("M") - 1
    )
    shared = shared[shared.index.to_period("M") <= last_complete_month]

    if len(shared) < 37:
        raise SystemExit("At least 37 complete months of shared data are needed.")

    expected_months = pd.date_range(
        shared.index[0], shared.index[-1], freq="ME"
    )
    if not shared.index.equals(expected_months):
        raise SystemExit("The shared ETF and CPI data contain missing months.")

    strategies = {
        "S&P 500 ETF (SPY)": shared["SPY"],
        "Treasury bill ETF (BIL)": shared["BIL"],
        "1-3 year Treasury bond ETF (SHY)": shared["SHY"],
    }
    for stock_weight in (0.10, 0.20, 0.40):
        label = f"{stock_weight:.0%} SPY / {1 - stock_weight:.0%} BIL"
        strategies[label] = mix_indices(
            shared["SPY"],
            shared["BIL"],
            risky_weight=stock_weight,
        )

    results = evaluate_universe(
        strategies,
        WINDOW_BUCKETS,
        inflation_index=shared["CPI"],
    )
    results["observations"] = results["observations"].astype(int)
    results.insert(0, "sample_start", shared.index[0].strftime("%Y-%m"))
    results.insert(1, "sample_end", shared.index[-1].strftime("%Y-%m"))
    results.insert(2, "inflation_series", CPI_SERIES)

    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "outputs" / "historical_inflation_comparison.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False)

    columns = [
        "strategy",
        "window",
        "observations",
        "median_end_return",
        "median_real_end_return",
        "p05_real_end_return",
        "real_loss_probability",
        "real_window_loss_probability",
    ]
    display = results[columns].copy()
    for column in columns[3:]:
        display[column] = display[column].map(lambda value: f"{value:.1%}")

    print(
        f"Shared sample: {shared.index[0]:%Y-%m} through "
        f"{shared.index[-1]:%Y-%m}"
    )
    print(f"Real returns use BLS CPI-U ({CPI_SERIES}) from FRED; before taxes.")
    print("Returns are cumulative, not annualized.")
    print(display.to_string(index=False))
    print(f"Saved numeric results to {output_path}")


if __name__ == "__main__":
    main()