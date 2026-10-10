# Short-Term Money Lab

[![Tests](https://github.com/JoelTul/short-term-money-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/JoelTul/short-term-money-lab/actions/workflows/tests.yml)

Where should you keep money you’ll need in the next 1 to 36 months?

This project uses historical data to compare the return you might earn with the risk of having less money when it’s time to withdraw. It looks at both fixed withdrawal dates and ranges, such as needing the money sometime between 6 and 9 months from now.

## What you can run now

The historical example compares six strategies over the same months:

- S&P 500 ETF (SPY)
- Treasury bill ETF (BIL)
- 1–3 year Treasury bond ETF (SHY)
- Monthly rebalanced mixes of 10%, 20%, or 40% SPY, with the rest in BIL

It evaluates each strategy across seven withdrawal windows: 1–3, 3–6, 6–9, 9–12, 12–18, 18–24, and 24–36 months.

BIL is an ETF comparison, not a historical high-yield savings account. The historical results are before taxes and inflation.

## Run the project

Python 3.11 or 3.12 is recommended. From the project folder, create an environment and install the dependencies.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe examples\historical_etf_comparison.py
```

These commands use the environment’s Python directly, so you don’t need to activate it or change PowerShell’s execution policy.

**macOS or Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python examples/historical_etf_comparison.py
```

The historical example downloads market data, prints a comparison table, and writes numeric results to `outputs/historical_etf_comparison.csv`. That file is generated locally and is ignored by Git.

To plot those results, run `examples/plot_historical_results.py` with the same Python environment. It saves `outputs/historical_etf_comparison.png`.

To run the tests, use `.\.venv\Scripts\python.exe -m pytest -q` on Windows, or `python -m pytest -q` with the environment activated on macOS or Linux.

There is also an offline example at `examples/synthetic_comparison.py`. Its data is made up to demonstrate the calculations; it is not a historical result.

## Reading the results

| Column | Meaning |
|---|---|
| `median_end_return` | Typical return if you withdraw at the end of the range |
| `p05_end_return` | Fifth-percentile return at the end of the range |
| `nominal_loss_probability` | Share of historical starting months that ended with a loss |
| `window_loss_probability` | Share that had a loss at some point within the withdrawal range |
| `observations` | Number of historical starting months evaluated |

The CSV includes additional metrics and the shared sample dates. Returns and probabilities are stored as decimals: `0.05` means 5%.

Each starting month creates a rolling observation. Nearby observations overlap, so they should not be treated as independent trials or as predictions of future odds.

## How the comparison works

All strategies use the same available months, starting with data requested from January 2008. The script excludes the current, potentially unfinished month and checks for gaps in the monthly data. It uses adjusted ETF prices when the data provider supplies them, so distributions can be reflected in returns.

For a withdrawal window, the analysis checks the return at the latest possible withdrawal month and the worst return between the earliest and latest withdrawal months. The mixed SPY/BIL strategies are rebalanced monthly.

## What’s next

The broader question still needs more than an ETF comparison. Planned work includes:

- A historical, time-varying high-yield savings model
- Inflation-adjusted historical results
- After-tax comparisons
- More assets and checks across different market periods
- Charts that make downside risk easier to compare

CDs and I Bonds would need separate treatment for their withdrawal rules, limits, and penalties.

This is a research project, not a recommendation to put money needed soon into any particular asset.