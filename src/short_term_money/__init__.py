"""Tools for evaluating short-term savings and investment strategies."""

from .backtest import evaluate_strategy, evaluate_universe
from .config import EXACT_HORIZONS, WINDOW_BUCKETS, WindowSpec

__all__ = [
    "EXACT_HORIZONS",
    "WINDOW_BUCKETS",
    "WindowSpec",
    "evaluate_strategy",
    "evaluate_universe",
]

