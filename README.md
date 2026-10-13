# Short-Term Money Lab

[![Tests](https://github.com/JoelTul/short-term-money-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/JoelTul/short-term-money-lab/actions/workflows/tests.yml)

Where should you keep money you’ll need in the next 1 to 36 months?

This project compares historical investment returns with the risk of having less money when it’s time to withdraw. It evaluates withdrawal ranges, such as needing the money sometime between 6 and 9 months from now.

## Current comparison

Six strategies are evaluated over the same available months:

- S&P 500 ETF (SPY)
- Treasury bill ETF (BIL)
- 1–3 year Treasury bond ETF (SHY)
- Monthly rebalanced mixes of 10%, 20%, or 40% SPY, with the rest in BIL

Each strategy is tested across seven withdrawal windows: 1–3, 3–6, 6–9, 9–12, 12–18, 18–24, and 24–36 months.

The full-sample comparison also measures how often each strategy trails BIL and its median return advantage over BIL.

BIL serves as an ETF benchmark. Historical savings account rates have not been added yet. Historical results are before taxes and inflation.

## Setup

Python 3.11 or 3.12 is recommended. Run these commands from the project folder.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

These commands use the environment’s Python directly, so activation is optional.

**macOS or Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the analysis

**Windows PowerShell:**

```powershell
.\.venv\Scripts\python.exe examples\historical_etf_comparison.py
.\.venv\Scripts\python.exe examples\plot_historical_results.py
.\.venv\Scripts\python.exe examples\period_comparison.py
```

**macOS or Linux, with the environment activated:**

```bash
python examples/historical_etf_comparison.py
python examples/plot_historical_results.py
python examples/period_comparison.py
```

The plotting script reads the CSV created by the historical comparison.

| Output | Contents |
|---|---|
| `outputs/historical_etf_comparison.csv` | Full-sample metrics, including comparisons against BIL |
| `outputs/historical_etf_comparison.png` | Median return and withdrawal-window loss rate |
| `outputs/historical_period_comparison.csv` | Return and loss metrics for separate historical periods |

Generated outputs are ignored by Git.

The period comparison separates 2008–2014, 2015–2019, and 2020 onward. Every rolling window must start and finish within its selected period. Longer horizons therefore have fewer observations.

For an offline demonstration with made-up data, run `examples/synthetic_comparison.py` using the same Python environment.

## Reading the results

| Column | Meaning |
|---|---|
| `median_end_return` | Median cumulative return at the latest withdrawal month |
| `p05_end_return` | Fifth-percentile cumulative return at that month |
| `nominal_loss_probability` | Share of starting months that ended with a loss |
| `window_loss_probability` | Share that had a loss during the withdrawal range |
| `median_excess_end_return_vs_bil` | Median difference between strategy and BIL returns for matching start and end dates |
| `probability_below_bil` | Share of matching observations where the strategy returned less than BIL |
| `observations` | Number of historical starting months evaluated |

The BIL comparison columns are included in the full-sample CSV.

CSV values remain numeric. A return or probability of `0.05` means 5%; an excess return of `0.05` means an advantage of 5 percentage points over BIL.

## Methodology

Data is requested from January 2008 and converted to month-end prices. The examples use shared available months, exclude the current month, and reject gaps in the monthly sample.

Adjusted prices are used when supplied by the data provider, allowing distributions to be reflected in returns.

For each withdrawal range, the backtest calculates both the return at its end and the worst return between its earliest and latest withdrawal months. Stock/BIL mixes are rebalanced monthly.

Rolling observations overlap. Their loss rates describe the historical sample and should not be treated as independent trials or predictions of future odds. Comparisons between periods also use different sample sizes.

## Tests

**Windows PowerShell:**

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

**macOS or Linux:**

```bash
python -m pytest -q
```

Tests cover return calculations, withdrawal-window losses, inflation adjustments, portfolio rebalancing, and the historical example’s CSV export and BIL comparisons. Market downloads are replaced with synthetic data during testing.

## Next steps

- Add a historical, time-varying savings account model
- Include inflation in the historical comparisons
- Compare after-tax outcomes
- Expand the asset universe and robustness checks

CDs and I Bonds would need separate treatment for withdrawal restrictions and penalties.

This project is for research and educational purposes and does not provide personalized financial advice.

## Rust report tool

The optional Rust tool reads the full-sample comparison CSV and prints results for a selected withdrawal window. Install Rust, then run these commands from the project root:

```powershell
cargo run --manifest-path rust-report/Cargo.toml -- outputs/historical_etf_comparison.csv "6-9 months"
```

Replace `"6-9 months"` with another window, such as `"12-18 months"`. Generate the CSV with `examples/historical_etf_comparison.py` first.