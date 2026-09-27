"""Project configuration that is safe to import from notebooks and scripts."""

from dataclasses import dataclass


@dataclass(frozen=True)
class WindowSpec:
    """A range of months in which a withdrawal may occur."""

    label: str
    earliest_month: int
    latest_month: int

    def __post_init__(self) -> None:
        if self.earliest_month < 1:
            raise ValueError("earliest_month must be at least 1")
        if self.latest_month < self.earliest_month:
            raise ValueError("latest_month must be >= earliest_month")


WINDOW_BUCKETS = (
    WindowSpec("1-3 months", 1, 3),
    WindowSpec("3-6 months", 3, 6),
    WindowSpec("6-9 months", 6, 9),
    WindowSpec("9-12 months", 9, 12),
    WindowSpec("12-18 months", 12, 18),
    WindowSpec("18-24 months", 18, 24),
    WindowSpec("24-36 months", 24, 36),
)

EXACT_HORIZONS = (1, 3, 6, 9, 12, 18, 24, 36)


DEFAULT_TICKERS = {
    "US stocks": "SPY",
    "Treasury bill ETF": "BIL",
    "1-3 year Treasuries": "SHY",
    "Broad bonds": "BND",
    "Gold": "GLD",
    "Bitcoin": "BTC-USD",
}

