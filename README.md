# Short-Term Money Lab

**Research question:** Where should money be held when it may be needed within
1 to 36 months?

This project compares cash-like and risky assets using rolling historical
holding periods. The goal is not to find the asset with the highest average
return. It is to find when additional expected return has historically been
large enough to justify the probability and severity of being short of money
when the bill comes due.

## The key distinction

There are two different liability types:

1. **Fixed-date need:** the money is needed at a known date, such as exactly
   12 months from now.
2. **Withdrawal window:** the money could be needed at any point in a range,
   such as 6–9 months from now.

For a withdrawal window, the project evaluates both the return at the end of
the window and the **worst return observed anywhere inside it**. The latter is
the more conservative and usually more relevant measure.

## Holding-period buckets

| Bucket | Earliest use | Latest use |
|---|---:|---:|
| 1–3 months | 1 | 3 |
| 3–6 months | 3 | 6 |
| 6–9 months | 6 | 9 |
| 9–12 months | 9 | 12 |
| 12–18 months | 12 | 18 |
| 18–24 months | 18 | 24 |
| 24–36 months | 24 | 36 |

Exact horizons of 1, 3, 6, 9, 12, 18, 24, and 36 months will also be tested.

## Initial strategies

| Group | Strategy | Role in the test |
|---|---|---|
| Cash | Modeled high-yield savings account | Principal-stable benchmark |
| Cash | 3-month Treasury bills / T-bill proxy | Government-backed cash alternative |
| Cash | Treasury-bill ETF | Tradable cash-like implementation |
| Bonds | 1–3 year Treasury ETF | Modest duration risk |
| Bonds | Broad bond ETF | Diversified bond exposure |
| Stocks | U.S. total-market or S&P 500 ETF | Main risky alternative |
| Mixed | 10/90, 20/80, and 40/60 stock/cash | Risk-budgeted alternatives |
| Alternatives | Gold | Diversifier / inflation sensitivity |
| Alternatives | Bitcoin | High-volatility stress case, not a cash substitute |

I Bonds and bank CDs need separate treatment because early-withdrawal rules,
penalties, purchase limits, and lockups make them different from liquid assets.

## Primary metrics

For every strategy and horizon:

- number of rolling historical observations;
- mean and median cumulative return;
- 5th-percentile and worst cumulative return;
- probability of a nominal loss;
- probability of a real loss after CPI inflation;
- 5% expected shortfall (average result in the worst 5% of cases);
- worst result during a withdrawal window;
- opportunity cost or advantage relative to the cash benchmark.

Later versions will add after-tax results for a Pennsylvania investor,
including ordinary income versus short- and long-term capital-gains treatment
and the state-tax exemption for direct Treasury interest.

## Important research safeguards

- Use adjusted prices or total-return indices so dividends are included.
- Do not use today's HYSA rate across history. A HYSA proxy must vary with the
  prevailing rate environment and be shown under multiple spread assumptions.
- Do not treat ETF price history as representative before the ETF existed.
- Keep overlapping rolling windows for the main visualization, but report
  non-overlapping and block-bootstrap robustness checks because adjacent
  windows are not independent.
- Lag any information used to classify a starting market regime so the model
  cannot see data that had not yet been published.
- Separate nominal principal safety from purchasing-power safety.
- Never call Bitcoin, gold, bond funds, or stock funds “cash equivalents.”

## Decision framework

The eventual recommendation table will be constraint-based:

1. Set the date certainty: fixed date or withdrawal window.
2. Set the acceptable chance and size of a shortfall.
3. Eliminate strategies that violated that risk budget historically.
4. Among the survivors, compare median real after-tax return and liquidity.

This prevents a small improvement in average return from disguising an
unacceptable left-tail outcome.

## Repository layout

```text
short-term-money-lab/
├── .github/
│   └── workflows/
│       └── tests.yml
├── .gitignore
├── README.md
├── pyproject.toml
├── requirements.txt
├── src/
│   └── short_term_money/
│       ├── __init__.py
│       ├── backtest.py
│       ├── config.py
│       └── data.py
└── tests/
    └── test_backtest.py
```

## Quick start

Python 3.11 or 3.12 is recommended. Joel's existing Python 3.12 installation
is compatible.

### Windows PowerShell

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pytest -q
```

Expected result: `7 passed`.

If PowerShell blocks virtual-environment activation, run this once in the
current terminal and then activate it again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pytest -q
```

## Publish the repository to GitHub

Create an empty GitHub repository named `short-term-money-lab`. Do not add a
README, `.gitignore`, or license on GitHub because those files can conflict
with the local versions. Then run these commands from the project folder:

```bash
git init
git add .
git status
git commit -m "Initialize short-term money analysis"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/short-term-money-lab.git
git push -u origin main
```

Before committing, `git status` should not show `.venv`, `__pycache__`,
`.pytest_cache`, raw data, processed data, or `.env` files.

Every push and pull request will run the test suite automatically through
GitHub Actions on Python 3.11 and 3.12.

## Current scope and limitations

- The rolling-window engine and synthetic test cases are working.
- The project does not yet produce the final asset comparison report; the
  production data-source mapping is the next milestone.
- Market downloads use Yahoo Finance through `yfinance`. The service can rate
  limit requests, so failed downloads do not necessarily indicate broken
  analysis code.
- The HYSA series is intentionally modeled from a time-varying reference rate;
  it is not historical performance from one specific bank.
- Taxes and Pennsylvania-specific after-tax comparisons are planned but are
  not implemented yet.

The current starter implements and tests the core rolling-window calculations.
The next milestone is to freeze the data-source mapping and generate the first
comparison tables.
