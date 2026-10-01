# Short-Term Money Lab

[![Tests](https://github.com/JoelTul/short-term-money-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/JoelTul/short-term-money-lab/actions/workflows/tests.yml)

A Python backtesting project for comparing where to hold money that will be needed within the next 1 to 36 months.

## Overview

Short-term money presents a tradeoff: cash protects principal, while assets such as stocks and bonds may offer better returns at the cost of being down when the money is needed.

This project measures that tradeoff across different holding periods and market conditions. Instead of ranking strategies only by average return, it focuses on the questions that matter when an upcoming expense has to be funded:

- How often did the strategy lose money?
- How severe were the worst outcomes?
- Did returns keep pace with inflation?
- How did the strategy compare with a cash benchmark?
- At what horizon, if any, did taking additional risk become worthwhile?

## Fixed Dates vs. Withdrawal Windows

The analysis separates two common situations:

- **Fixed-date need:** The money is required on a known date, such as exactly 12 months from now.
- **Withdrawal window:** The money may be required at any point in a range, such as 6–9 months from now.

For withdrawal windows, the backtest measures both the return at the end of the window and the worst result available during the window. This captures cases where an investment eventually recovered but was still underwater when the money could have been needed.

## Holding Periods

| Window | Earliest withdrawal | Latest withdrawal |
|---|---:|---:|
| 1–3 months | 1 month | 3 months |
| 3–6 months | 3 months | 6 months |
| 6–9 months | 6 months | 9 months |
| 9–12 months | 9 months | 12 months |
| 12–18 months | 12 months | 18 months |
| 18–24 months | 18 months | 24 months |
| 24–36 months | 24 months | 36 months |

The project also supports exact horizons of 1, 3, 6, 9, 12, 18, 24, and 36 months.

## Strategies

The planned comparison includes:

| Category | Strategy |
|---|---|
| Cash | Modeled high-yield savings account |
| Cash | 3-month Treasury bills and Treasury-bill ETFs |
| Bonds | Short-term Treasury and broad bond ETFs |
| Stocks | U.S. total-market and S&P 500 ETFs |
| Mixed portfolios | 10/90, 20/80, and 40/60 stock/cash allocations |
| Alternatives | Gold and Bitcoin as high-volatility comparison cases |

CDs and I Bonds require separate analysis because their penalties, lockups, purchase limits, and redemption rules are different from fully liquid assets.

## Metrics

Each strategy is evaluated using rolling historical windows and the following metrics:

- Mean and median cumulative return
- 5th-percentile and worst cumulative return
- Probability of a nominal loss
- Probability of a real loss after inflation
- 5% expected shortfall
- Worst return available during a withdrawal window
- Performance relative to the cash benchmark

## Methodology

- Adjusted prices or total-return indices are used so distributions are included.
- Inflation-adjusted results use CPI data.
- The high-yield savings benchmark is modeled with a time-varying reference rate rather than applying a current savings rate to the past.
- Assets are not backfilled into periods before they or their selected proxies existed.
- Market-regime variables will be lagged to prevent look-ahead bias.
- Overlapping rolling windows will be supplemented with robustness checks because adjacent observations are not independent.

## Current Status

The core analysis package currently supports:

- Fixed-horizon and withdrawal-window backtests
- Nominal and inflation-adjusted returns
- Downside-risk and expected-shortfall calculations
- Constant-weight stock/cash portfolios
- Automated tests on Python 3.11 and 3.12

The production data pipeline, final comparison tables, visualizations, and after-tax analysis are under development.

## Installation

Python 3.11 or 3.12 is recommended.

```bash
git clone https://github.com/JoelTul/short-term-money-lab.git
cd short-term-money-lab
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Or activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the project and run the tests:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
```

## Project Structure

```text
short-term-money-lab/
├── .github/workflows/tests.yml
├── src/short_term_money/
│   ├── __init__.py
│   ├── backtest.py
│   ├── config.py
│   └── data.py
├── tests/test_backtest.py
├── pyproject.toml
└── requirements.txt
```

## Roadmap

- Finalize the historical data sources and cash-rate assumptions.
- Generate comparison tables for every holding period.
- Add after-tax scenarios for savings interest, Treasury interest, and capital gains.
- Add charts for loss probability, expected shortfall, and real returns.
- Produce a decision table linking time horizon and risk tolerance to eligible strategies.

## Disclaimer

This project is for research and educational purposes and does not constitute personalized financial advice.