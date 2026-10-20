# Short-Term Money Lab

[![Python tests](https://github.com/JoelTul/short-term-money-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/JoelTul/short-term-money-lab/actions/workflows/tests.yml)
[![Rust checks](https://github.com/JoelTul/short-term-money-lab/actions/workflows/rust.yml/badge.svg)](https://github.com/JoelTul/short-term-money-lab/actions/workflows/rust.yml)

Where should you keep money you’ll need in the next 1 to 36 months?

Short-Term Money Lab compares historical investment returns with the risk of having less money when it’s time to withdraw. Python handles the backtests and charts. An optional Rust command-line tool reads the exported results for a selected withdrawal window.

## Preliminary findings

**Sample: January 2008–September 2026.** The figures below summarize the nominal comparison, before taxes, inflation, and transaction costs. Inflation-adjusted analysis is implemented, but its results and the historical subperiod comparisons still need review before the final writeup.

### Stocks delivered higher returns, with meaningful withdrawal risk

SPY produced strong median returns in this sample. However, many starting dates left the investor below their initial balance during the months when withdrawal could have been necessary.

| Withdrawal window | Median return at latest month | Fifth-percentile return at latest month | Share with a loss during the window |
|---|---:|---:|---:|
| 1–3 months | 4.1% | -9.2% | 47.7% |
| 3–6 months | 7.9% | -9.8% | 35.2% |
| 6–9 months | 11.2% | -13.4% | 30.1% |
| 9–12 months | 15.9% | -12.6% | 24.9% |
| 12–18 months | 25.5% | -8.4% | 20.8% |
| 18–24 months | 29.7% | 2.5% | 15.9% |
| 24–36 months | 45.4% | 19.4% | 6.9% |

Returns are cumulative, not annualized. The fifth percentile describes a relatively poor outcome; more severe outcomes are possible.

### The withdrawal date changes the conclusion

None of the 189 eligible SPY observations ended with a nominal loss at exactly 36 months. However, 6.9% were below their initial balance at some point during months 24–36.

Waiting until the final month and needing the money earlier are different situations. A favorable result at exactly three years does not establish dependable access throughout the preceding year.

### Small stock allocations changed the tradeoff

For the 12–18 month window:

| Strategy | Median return at month 18 | Fifth-percentile return at month 18 | Share with a loss during months 12–18 |
|---|---:|---:|---:|
| SPY | 25.5% | -8.4% | 20.8% |
| 10% SPY / 90% BIL | 3.2% | 0.2% | 13.5% |

The mixed portfolio gave up substantial upside while improving these downside measures. It still experienced losses, so the results do not establish an allocation suitable for every short-term goal.

### Loss frequency needs a severity measure

BIL sometimes recorded very small negative returns. For the 9–12 month window, its fifth-percentile ending return was approximately -0.1%, compared with -12.6% for SPY.

A tiny loss and a large loss both count toward loss probability. Frequency should therefore be read alongside loss size. BIL is also an ETF, so these results should not be interpreted as historical savings account outcomes.

### Working conclusion

The decision depends on how much shortfall the expense can tolerate and whether withdrawal can be delayed.

For a mandatory expense, the possibility of being underwater matters even when the median return is attractive. For a flexible goal, accepting some stock exposure may be a tradeoff worth evaluating.

The study has not established a universally best allocation or a reliable cutoff at which stocks become suitable for short-term spending.

## Current comparison

Six strategies are evaluated over the same available months:

- S&P 500 ETF (SPY)
- Treasury bill ETF (BIL)
- 1–3 year Treasury bond ETF (SHY)
- Monthly rebalanced portfolios holding 10%, 20%, or 40% SPY, with the rest in BIL

Each strategy is tested across seven withdrawal windows: 1–3, 3–6, 6–9, 9–12, 12–18, 18–24, and 24–36 months.

The full-sample nominal comparison measures returns, downside outcomes, and performance relative to BIL. A separate example adjusts returns for historical inflation.

Historical savings account rates, CDs, and after-tax outcomes have not been compared directly.

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
.\.venv\Scripts\python.exe examples\inflation_comparison.py
```

**macOS or Linux, with the environment activated:**

```bash
python examples/historical_etf_comparison.py
python examples/plot_historical_results.py
python examples/period_comparison.py
python examples/inflation_comparison.py
```

The historical examples require internet access to download data. The plotting script reads the CSV produced by the full-sample nominal comparison.

| Output | Contents |
|---|---|
| `outputs/historical_etf_comparison.csv` | Full-sample nominal metrics and comparisons against BIL |
| `outputs/historical_etf_comparison.png` | Median nominal return and withdrawal-window loss rate |
| `outputs/historical_period_comparison.csv` | Nominal return and loss metrics for separate historical periods |
| `outputs/historical_inflation_comparison.csv` | Nominal and inflation-adjusted return and loss metrics |

Generated outputs are ignored by Git.

For an offline demonstration using made-up data, run `examples/synthetic_comparison.py` with the same Python environment.

### Historical periods

The period comparison separates 2008–2014, 2015–2019, and 2020 onward. Every rolling window must start and finish within its selected period.

Longer horizons and shorter periods provide fewer observations. These calendar periods are comparison groups, not formally defined market regimes.

### Inflation-adjusted returns

The inflation example uses the U.S. Bureau of Labor Statistics’ monthly CPI-U all-items index, not seasonally adjusted: [CPIAUCNS, retrieved from FRED](https://fred.stlouisfed.org/series/CPIAUCNS).

ETF prices and CPI observations are aligned to matching months. The shared sample ends at the latest complete month available in both datasets.

Real returns measure changes in purchasing power:

```text
Real return = (ending wealth / starting wealth)
              / (ending CPI / starting CPI) - 1
```

An investment can gain dollars while losing purchasing power. The inflation comparison measures both nominal and real outcomes over the same sample.

## Rust report tool

The Rust tool reads `historical_etf_comparison.csv` and prints results for one withdrawal window. It reports the observation count, median nominal return, withdrawal-window loss rate, and frequency of trailing BIL.

Install the current stable toolchain using the [official Rust installer](https://rust-lang.org/tools/install/). On Windows, install the C++ build tools if prompted.

After generating the nominal comparison CSV, run:

```bash
cargo run --manifest-path rust-report/Cargo.toml -- outputs/historical_etf_comparison.csv "6-9 months"
```

Replace `"6-9 months"` with another window, such as `"12-18 months"`.

With no arguments, the tool uses `outputs/historical_etf_comparison.csv` and the `6-9 months` window:

```bash
cargo run --manifest-path rust-report/Cargo.toml
```

CSV paths are resolved relative to the directory where you run the command. The current Rust report expects the nominal comparison CSV.

## Reading the results

| Column | Meaning |
|---|---|
| `median_end_return` | Median cumulative nominal return at the latest withdrawal month |
| `p05_end_return` | Fifth-percentile nominal return at that month |
| `nominal_loss_probability` | Share of starting months that ended below the initial dollar balance |
| `window_loss_probability` | Share that fell below the initial dollar balance during the withdrawal range |
| `median_excess_end_return_vs_bil` | Median of the paired strategy-minus-BIL return differences |
| `probability_below_bil` | Share of matching observations where the strategy returned less than BIL |
| `median_real_end_return` | Median inflation-adjusted return at the latest withdrawal month |
| `p05_real_end_return` | Fifth-percentile inflation-adjusted return at that month |
| `real_loss_probability` | Share of starting months that ended with less purchasing power |
| `real_window_loss_probability` | Share with a purchasing-power loss during the withdrawal range |
| `observations` | Number of historical starting months evaluated |

The BIL comparison columns are included in the full-sample nominal CSV. Strategy and benchmark returns are paired using the same starting and ending months.

Real-return columns are included in the inflation comparison CSV.

CSV values remain numeric. A return or probability of `0.05` means 5%; an excess return of `0.05` means 5 percentage points above BIL.

## Methodology and limits

- Data is requested from January 2008 and converted to month-end prices.
- The historical examples use shared available months, exclude the current month, and reject gaps in the monthly sample.
- Adjusted prices are used when supplied by the data provider, allowing distributions to be reflected in returns.
- Each withdrawal range is evaluated at its ending month and at its worst month within the range.
- Stock/BIL portfolios are rebalanced monthly.
- Monthly observations do not capture losses between month-end sampling dates.
- All results are before taxes and transaction costs. Only the inflation comparison adjusts for CPI.

The sample excludes earlier starting dates, including the 2000 market peak and the 2007 pre-crisis peak. Findings may change with a longer history or different starting dates.

Rolling observations overlap and are not independent trials. Their historical loss frequencies should not be treated as forecasts.

The preliminary findings above are a dated snapshot. Refreshed downloads may produce different results, including revisions to historical data.

## Tests and automated checks

**Python — Windows PowerShell:**

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

**Python — macOS or Linux, with the environment activated:**

```bash
python -m pytest -q
```

Python tests cover return calculations, withdrawal-window losses, inflation adjustments, portfolio rebalancing, and the nominal historical example’s CSV export and BIL comparisons. Synthetic data replaces market downloads during testing.

**Rust — all platforms:**

```bash
rustup component add rustfmt clippy
cargo fmt --manifest-path rust-report/Cargo.toml -- --check
cargo clippy --locked --manifest-path rust-report/Cargo.toml --all-targets -- -D warnings
cargo test --locked --manifest-path rust-report/Cargo.toml
```

Rust integration tests check window selection, percentage formatting, quoted CSV fields, and rejection of unknown windows and extra arguments.

GitHub Actions runs Python tests on Python 3.11 and 3.12. Rust formatting, Clippy, and tests run on Windows and Linux.

## Finishing the first study

The remaining work for version 1 is:

- Review the inflation-adjusted results and identify where nominal gains failed to preserve purchasing power.
- Check whether the main findings hold across the existing historical subperiods.
- Publish a dated results snapshot, supporting chart, and final writeup.

Savings account models, additional assets, and tax scenarios can be separate follow-up studies.

This project is for research and educational purposes and does not provide personalized financial advice.

## Published results

Dated result tables and charts are available in [reports](reports/).

Each snapshot identifies its nominal and inflation-adjusted sample dates. These snapshots preserve the outputs used for reviewing the study’s conclusions.