# Short-Term Money Lab

[![Python tests](https://github.com/JoelTul/short-term-money-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/JoelTul/short-term-money-lab/actions/workflows/tests.yml)
[![Rust checks](https://github.com/JoelTul/short-term-money-lab/actions/workflows/rust.yml/badge.svg)](https://github.com/JoelTul/short-term-money-lab/actions/workflows/rust.yml)

Where should you keep money you’ll need in the next 1 to 36 months?

Short-Term Money Lab compares historical investment returns with the risk of having less money when it’s time to withdraw. Python handles the backtests and charts. An optional Rust command-line tool reads the exported results for a selected withdrawal window.

## Preliminary findings

**Sample: January 2008-September 2026.** The figures below summarize the published nominal comparison, before taxes, inflation, and transaction costs. Selected historical subperiod checks have also been reviewed. Inflation-adjusted findings remain pending because the inflation CSV is not present in the published snapshot.

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

### Historical periods changed downside risk

The full-sample results hide substantial differences between historical periods.

For SPY's 18-24 month withdrawal window:

| Period | Starting months tested | Fifth-percentile return at month 24 | Loss at month 24 | Loss during months 18-24 |
|---|---:|---:|---:|---:|
| 2008-2014 | 60 | -14.5% | 13.3% | 16.7% |
| 2015-2019 | 36 | 18.1% | 0.0% | 0.0% |
| January 2020-September 2026 | 57 | 2.7% | 1.8% | 28.1% |

In the full sample, SPY's fifth-percentile return at month 24 was positive
at 2.5%. Within 2008-2014, it was negative at -14.5%. The choice of historical
period materially changes the picture of downside risk.

The more recent period also illustrates withdrawal timing risk: only 1.8%
of eligible observations ended below the initial balance at month 24,
but 28.1% fell below it at some month-end during months 18-24.

Every observation starts and finishes inside its selected period.
These subsets omit windows crossing period boundaries, so their observation
counts do not add up to the full-sample count.

### SHY also experienced losses over longer windows

For SHY in January 2020-September 2026, 37.8% of the 45 eligible observations
ended with a nominal loss at month 36. During months 24-36, 53.3% experienced
at least one month-end balance below the initial investment.

The worst ending return at month 36 in that subset was approximately -3.6%.
A short-term Treasury bond ETF therefore did not consistently preserve the
initial dollar balance in this sample.

### Updated working conclusion

The findings so far identify three important tradeoffs:

- SPY offered substantial upside, alongside shortfalls at possible withdrawal dates.
- Small SPY/BIL allocations reduced several downside measures while giving up upside.
- BIL's small negative outcomes and SHY's larger losses show why loss frequency
  needs to be considered alongside loss size.

A positive fifth-percentile return is not a minimum return or a guarantee.
Likewise, observing no losses at a particular horizon does not establish
that future losses are impossible.

The study has not established one best allocation for every short-term goal.
Historical savings accounts, CDs, crypto, and after-tax outcomes have not been
compared in these published results. Inflation-adjusted conclusions remain
pending because the inflation CSV is still missing from the published snapshot.

Returns above are cumulative and nominal. Rolling observations overlap,
and their historical loss frequencies are not forecasts. The sample also
excludes starting dates at the 2000 and 2007 market peaks.

Source: [October 19 results snapshot](reports/2026-10-19-232051/),
including the full-sample nominal and historical-period comparison tables.

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

The nominal results snapshot and chart are published. Selected subperiod
findings are now summarized above.

The remaining work for version 1 is:

- Generate, validate, and publish the inflation-adjusted results.
- Review where nominal gains failed to preserve purchasing power.
- Complete the final writeup using the published evidence.

Savings account models, additional assets, and tax scenarios can be
separate follow-up studies.

This project is for research and educational purposes and does not provide
personalized financial advice.

## Published results

Dated result tables and charts are available in [reports](reports/).

The current snapshot contains nominal and historical-period results. Its inflation comparison remains incomplete. Published tables preserve the outputs used to review the findings.

## Data availability

Historical examples download data from external services. A temporary outage
or maintenance page can prevent an analysis from completing.

If a download fails, stop before copying results into a published report.
An existing CSV may belong to an earlier run.

A results snapshot is complete only when every listed file is present and
its sample dates are recorded. Inflation-adjusted conclusions remain pending
until the corresponding results have been generated and reviewed.
## What a withdrawal window means

Each observation starts with one investment. A withdrawal window describes
when that money might be needed.

For example, the 12–18 month window checks:

- The return at month 18.
- Whether the balance fell below the initial investment at any sampled
  month-end from month 12 through month 18.

The analysis does not simulate taking money out every month. A loss during
the window means at least one possible withdrawal date had a shortfall,
even if the investment recovered by the final month.

Nominal losses measure dollars. Inflation-adjusted losses measure
purchasing power.
