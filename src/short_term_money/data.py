"""Data loading and index construction helpers.

All backtests consume month-end wealth indices. A wealth index starts at an
arbitrary positive value and reflects reinvested distributions when the source
series supports them.
"""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd


def to_monthly_index(series: pd.Series) -> pd.Series:
    """Convert a dated daily/weekly wealth index to clean month-end values."""
    if not isinstance(series.index, pd.DatetimeIndex):
        raise TypeError("series must have a DatetimeIndex")
    output = series.sort_index().dropna().resample("ME").last()
    if output.empty or (output <= 0).any():
        raise ValueError("wealth index must contain positive values")
    return output.astype(float)


def download_adjusted_prices(
    tickers: Iterable[str],
    start: str = "1993-01-01",
    end: str | None = None,
) -> pd.DataFrame:
    """Download adjusted market prices and return month-end wealth indices.

    The yfinance dependency is imported lazily so the calculation package and
    its tests can run without making a network request.
    """
    import yfinance as yf

    ticker_list = list(tickers)
    raw = yf.download(
        ticker_list,
        start=start,
        end=end,
        auto_adjust=False,
        actions=False,
        progress=False,
        group_by="column",
    )
    if raw.empty:
        raise RuntimeError("No market-price data were returned")

    adjusted = raw["Adj Close"] if "Adj Close" in raw else raw["Close"]
    if isinstance(adjusted, pd.Series):
        adjusted = adjusted.to_frame(name=ticker_list[0])
    return adjusted.sort_index().resample("ME").last().dropna(how="all")


def modeled_hysa_index(
    annual_rates_percent: pd.Series,
    spread_bps: float = 50.0,
    implementation_lag_months: int = 1,
) -> pd.Series:
    """Create a monthly HYSA wealth index from a time-varying policy rate.

    This is explicitly a model, not a claim about any particular bank account.
    The default assumes the account APY is 50 basis points below the supplied
    annual rate, floored at zero. Multiple spreads should be tested.
    """
    monthly_rate = annual_rates_percent.sort_index().resample("ME").mean()
    if implementation_lag_months:
        monthly_rate = monthly_rate.shift(implementation_lag_months)
    apy = ((monthly_rate - spread_bps / 100.0) / 100.0).clip(lower=0.0)
    monthly_return = np.power(1.0 + apy, 1.0 / 12.0) - 1.0
    wealth = (1.0 + monthly_return.dropna()).cumprod()
    wealth.name = f"Modeled HYSA ({spread_bps:.0f} bp spread)"
    return wealth


def mix_indices(
    risky_index: pd.Series,
    safe_index: pd.Series,
    risky_weight: float,
) -> pd.Series:
    """Build a monthly, constant-weight strategy rebalanced every month."""
    if not 0.0 <= risky_weight <= 1.0:
        raise ValueError("risky_weight must be between 0 and 1")

    aligned = pd.concat(
        [to_monthly_index(risky_index), to_monthly_index(safe_index)],
        axis=1,
        join="inner",
    ).dropna()

    if len(aligned) < 2:
        raise ValueError("At least two shared monthly observations are required")

    returns = aligned.pct_change().dropna()
    mixed_returns = (
        risky_weight * returns.iloc[:, 0]
        + (1.0 - risky_weight) * returns.iloc[:, 1]
    )

    wealth = pd.Series(index=aligned.index, dtype=float)
    wealth.iloc[0] = 1.0
    wealth.iloc[1:] = (1.0 + mixed_returns).cumprod().to_numpy()
    wealth.name = f"{risky_weight:.0%} risky / {1-risky_weight:.0%} safe"
    return wealth

