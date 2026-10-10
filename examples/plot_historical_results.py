"""Plot the historical comparison saved by historical_etf_comparison.py."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import pandas as pd

from short_term_money import WINDOW_BUCKETS


def main():
    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / "outputs" / "historical_etf_comparison.csv"
    chart_path = project_root / "outputs" / "historical_etf_comparison.png"

    if not csv_path.exists():
        raise SystemExit(
            "Run examples/historical_etf_comparison.py to create the CSV first."
        )

    results = pd.read_csv(csv_path)
    required = {
        "strategy",
        "window",
        "median_end_return",
        "window_loss_probability",
    }
    missing = required - set(results.columns)
    if missing:
        raise SystemExit(f"CSV is missing columns: {', '.join(sorted(missing))}")

    windows = [window.label for window in WINDOW_BUCKETS]
    positions = list(range(len(windows)))
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for strategy, rows in results.groupby("strategy", sort=False):
        ordered = rows.set_index("window").reindex(windows)
        metrics = ordered[
            ["median_end_return", "window_loss_probability"]
        ]
        if metrics.isna().any().any():
            raise SystemExit(f"Missing window results for {strategy}")

        axes[0].plot(
            positions,
            ordered["median_end_return"],
            marker="o",
            label=strategy,
        )
        axes[1].plot(
            positions,
            ordered["window_loss_probability"],
            marker="o",
            label=strategy,
        )

    axes[0].set_title("Median return at the end of the window")
    axes[1].set_title("Historical share with a loss during the window")
    axes[1].set_ylim(bottom=0)

    for axis in axes:
        axis.set_xticks(positions, windows, rotation=35, ha="right")
        axis.yaxis.set_major_formatter(PercentFormatter(xmax=1))
        axis.grid(axis="y", alpha=0.3)
        axis.set_xlabel("Withdrawal window")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.01),
        ncol=2,
        frameon=False,
    )
    fig.suptitle("Historical ETF outcomes by withdrawal window")
    fig.subplots_adjust(bottom=0.34, top=0.86, wspace=0.25)

    fig.savefig(chart_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved chart to {chart_path}")


if __name__ == "__main__":
    main()