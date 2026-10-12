"""Check the historical example without downloading market data."""

import importlib.util
from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def historical_example(tmp_path, monkeypatch):
    script_path = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "historical_etf_comparison.py"
    )
    spec = importlib.util.spec_from_file_location("historical_example", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Redirect the example's output into pytest's temporary directory.
    monkeypatch.setattr(
        module,
        "__file__",
        str(tmp_path / "examples" / "historical_etf_comparison.py"),
    )
    return module


@pytest.fixture
def monthly_prices():
    current_month = (
        pd.Timestamp.now(tz="UTC").tz_localize(None).to_period("M")
    )
    dates = pd.date_range(
        end=current_month.to_timestamp("M"),
        periods=49,
        freq="ME",
    )
    return pd.DataFrame(
        {
            "SPY": [100 * 1.01 ** month for month in range(49)],
            "BIL": [100 * 1.002 ** month for month in range(49)],
            "SHY": [100 * 0.995 ** month for month in range(49)],
        },
        index=dates,
    )


def test_historical_csv_contains_correct_returns(
    historical_example, monthly_prices, monkeypatch, tmp_path
):
    monkeypatch.setattr(
        historical_example,
        "download_adjusted_prices",
        lambda tickers, start: monthly_prices.copy(),
    )
    historical_example.main()

    results = pd.read_csv(
        tmp_path / "outputs" / "historical_etf_comparison.csv"
    )
    assert len(results) == 42
    assert not results.duplicated(["strategy", "window"]).any()
    assert set(results["sample_end"]) == {
        monthly_prices.index[-2].strftime("%Y-%m")
    }

    for _, row in results.iterrows():
        horizon = int(row["latest_month"])
        assert row["observations"] == 48 - horizon

        if row["strategy"] == "Treasury bill ETF (BIL)":
            assert row["median_excess_end_return_vs_bil"] == pytest.approx(0)
            assert row["probability_below_bil"] == pytest.approx(0)

        elif row["strategy"] == "S&P 500 ETF (SPY)":
            expected_excess = 1.01 ** horizon - 1.002 ** horizon
            assert row["median_excess_end_return_vs_bil"] == pytest.approx(
                expected_excess
            )
            assert row["probability_below_bil"] == pytest.approx(0)

        elif row["strategy"] == "1-3 year Treasury bond ETF (SHY)":
            assert row["nominal_loss_probability"] == pytest.approx(1)
            assert row["probability_below_bil"] == pytest.approx(1)

        elif row["strategy"] == "20% SPY / 80% BIL":
            assert row["median_end_return"] == pytest.approx(
                1.0036 ** horizon - 1
            )


def test_historical_example_rejects_missing_months(
    historical_example, monthly_prices, monkeypatch, tmp_path
):
    incomplete = monthly_prices.drop(monthly_prices.index[20])
    monkeypatch.setattr(
        historical_example,
        "download_adjusted_prices",
        lambda tickers, start: incomplete.copy(),
    )

    with pytest.raises(SystemExit, match="missing months"):
        historical_example.main()

    assert not (tmp_path / "outputs" / "historical_etf_comparison.csv").exists()