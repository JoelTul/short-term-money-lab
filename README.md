# Short-Term Money Lab

[![Python tests](https://github.com/JoelTul/short-term-money-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/JoelTul/short-term-money-lab/actions/workflows/tests.yml)
[![Rust checks](https://github.com/JoelTul/short-term-money-lab/actions/workflows/rust.yml/badge.svg)](https://github.com/JoelTul/short-term-money-lab/actions/workflows/rust.yml)

Where should you keep money you’ll need in the next 1 to 36 months?

Short-Term Money Lab compares historical investment returns with the risk of having less money when it’s time to withdraw. Python handles the backtests and charts. An optional Rust command-line tool reads the exported results for a selected withdrawal window.

## Current comparison

Six strategies are evaluated over the same available months:

- S&P 500 ETF (SPY)
- Treasury bill ETF (BIL)
- 1–3 year Treasury bond ETF (SHY)
- Monthly rebalanced portfolios holding 10%, 20%, or 40% SPY, with the rest in BIL

Each strategy is tested across seven withdrawal windows:

| Window | Earliest withdrawal | Latest withdrawal |
|---|---:|---:|
| 1–3 months | 1 month | 3 months |
| 3–6 months | 3 months | 6 months |
| 6–9 months | 6 months | 9 months |
| 9–12 months | 9 months | 12 months |
| 12–18 months | 12 months | 18 months |
| 18–24 months | 18 months | 24 months |
| 24–36 months | 24 months | 36 months |

The full-sample comparison also measures how often each strategy trails BIL and its median return difference versus BIL.

BIL serves as an ETF benchmark. Historical savings account rates have not been added yet. Historical results are before taxes and inflation.

## Setup

Python 3.11 or 3.12 is recommended. Run the commands below from the project root.

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

The historical examples require internet access to download market data. The plotting script reads the CSV produced by the full-sample comparison.

| Output | Contents |
|---|---|
| `outputs/historical_etf_comparison.csv` | Full-sample metrics and comparisons against BIL |
| `outputs/historical_etf_comparison.png` | Median return and withdrawal-window loss rate |
| `outputs/historical_period_comparison.csv` | Return and loss metrics for separate historical periods |

Generated outputs are ignored by Git.

The period comparison separates 2008–2014, 2015–2019, and 2020 onward. Every rolling window must start and finish within its selected period.

For an offline demonstration using made-up data, run `examples/synthetic_comparison.py` with the same Python environment.

## Rust report tool

The Rust tool reads `historical_etf_comparison.csv` and prints the results for one withdrawal window. It reports the observation count, median return, withdrawal-window loss rate, and frequency of trailing BIL.

Install the current stable toolchain using the [official Rust installer](https://rust-lang.org/tools/install/). On Windows, install the C++ build tools if prompted.

After generating the Python CSV, run:

```bash
cargo run --manifest-path rust-report/Cargo.toml -- outputs/historical_etf_comparison.csv "6-9 months"
```

Replace `"6-9 months"` with another window, such as `"12-18 months"`.

With no arguments, the tool uses `outputs/historical_etf_comparison.csv` and the `6-9 months` window:

```bash
cargo run --manifest-path rust-report/Cargo.toml
```

CSV paths are resolved relative to the directory where you run the command.

## Reading the results

| Column | Meaning |
|---|---|
| `median_end_return` | Median cumulative return at the latest withdrawal month |
| `p05_end_return` | Fifth-percentile cumulative return at that month |
| `nominal_loss_probability` | Share of starting months that ended with a loss |
| `window_loss_probability` | Share that had a loss during the withdrawal range |
| `median_excess_end_return_vs_bil` | Median of the paired strategy-minus-BIL return differences |
| `probability_below_bil` | Share of matching observations where the strategy returned less than BIL |
| `observations` | Number of historical starting months evaluated |

The BIL comparison columns are included in the full-sample CSV. Strategy and benchmark returns are paired using the same starting and ending months.

CSV values remain numeric. A return or probability of `0.05` means 5%; an excess return of `0.05` means 5 percentage points above BIL.

Returns are cumulative over the relevant horizon, not annualized.

## Methodology and limits

- Data is requested from January 2008 and converted to month-end prices.
- The historical examples use shared available months, exclude the current month, and reject gaps in the monthly sample.
- Adjusted prices are used when supplied by the data provider, allowing distributions to be reflected in returns.
- Each withdrawal range is evaluated at its ending month and at its worst month within the range.
- Stock/BIL portfolios are rebalanced monthly.
- Monthly observations do not capture losses between month-end sampling dates.

Rolling observations overlap. Their loss rates describe the historical sample and should not be treated as independent trials or predictions of future odds.

Longer horizons and shorter historical periods provide fewer observations. Results are before taxes, inflation, and transaction costs.

## Tests and automated checks

**Python — Windows PowerShell:**

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

**Python — macOS or Linux, with the environment activated:**

```bash
python -m pytest -q
```

Python tests cover return calculations, withdrawal-window losses, inflation adjustments, portfolio rebalancing, and the historical example’s CSV export and BIL comparisons. Synthetic data replaces market downloads during testing.

**Rust — all platforms:**

```bash
rustup component add rustfmt clippy
cargo fmt --manifest-path rust-report/Cargo.toml -- --check
cargo clippy --locked --manifest-path rust-report/Cargo.toml --all-targets -- -D warnings
cargo test --locked --manifest-path rust-report/Cargo.toml
```

Rust integration tests check window selection, percentage formatting, quoted CSV fields, and rejection of unknown windows and extra arguments.

GitHub Actions runs Python tests on Python 3.11 and 3.12. Rust formatting, Clippy, and tests run on Windows and Linux.

## Next steps

- Add a historical, time-varying savings account model
- Include inflation in the historical comparisons
- Compare after-tax outcomes
- Expand the asset universe and robustness checks

CDs and I Bonds would need separate treatment for withdrawal restrictions and penalties.

This project is for research and educational purposes and does not provide personalized financial advice.