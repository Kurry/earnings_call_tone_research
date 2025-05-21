# Tone-Dispersion Factor Research

*Within-call sentiment variance as a market-neutral signal*

---

## Project Layout

```
earnings_call_tone_research/
│
├─ run_backtest.py            # one-shot: build → neutralise → weights → PnL│
├─ src/                       # pure-Python research pipeline
│   ├─ load.py                # reads the three parquet inputs
│   ├─ factor_build.py        # z-scores tone dispersion by trade-date
│   ├─ neutralise.py          # FF5+UMD regression (daily)
│   ├─ portfolio.py           # weight construction & PnL
│   └─ report.py              # quick tear-sheet
│
├─ data/                      # **exactly three parquet files**
│   ├─ tone_dispersion.parquet   # call-level dispersion
│   ├─ stock_prices.parquet      # wide adj-close matrix, index=date
│   └─ ff5_daily.parquet         # daily MKT, SMB, HML, RMW, CMA, UMD, RF
│
└─ tests/                     # pytest suite (unit + integration)
```

---

## Required Inputs

| file                         | expected schema                                                |
| ---------------------------- | -------------------------------------------------------------- |
| **tone\_dispersion.parquet** | Columns: `symbol`, `date`, `tone_dispersion`                   |
| **stock\_prices.parquet**    | Wide table; `index=date`, `columns=tickers`, `values=adjClose` |
| **ff5\_daily.parquet**       | `index=date`; columns `mktrf smb hml rmw cma umd rf`           |

No other data sources or credentials are required.

---

## Tone-Dispersion Calculation  🛈

* **Granularity:** each *speaker-turn* (a continuous block of speech by one speaker) inside the earnings-call transcript.
* **Sentiment score:** a scalar in **\[-1, 1]** produced by a local language-model sentiment head (or any deterministic sentiment function).

  ```text
  sentiment(turn_i)  →  s_i
  ```
* **Dispersion metric:** **population variance** of all scores within the call
  (executive + analyst turns):

  $$
    \text{tone\_dispersion} \;=\;
    \frac{1}{N}\sum_{i=1}^{N} \bigl(s_i-\bar{s}\bigr)^2,
    \qquad \bar{s}=\frac{1}{N}\sum s_i
  $$

  *Requires at least two non-empty turns; otherwise NaN.*

The resulting table written to `data/tone_dispersion.parquet` therefore holds **one row per call**:

| symbol | date (call timestamp) | tone\_dispersion |
| ------ | --------------------- | ---------------- |
| AAPL   | 2024-10-24 16:30:00   | 0.0134           |
| MSFT   | 2024-10-26 17:00:00   | 0.0027           |
| …      | …                     | …                |

During factor construction the script:

1. Shifts `date` to the **next NYSE trading day** (`trade_date`).
2. Z-scores `tone_dispersion` cross-sectionally each `trade_date` to remove level shifts.
3. Feeds the standardized series to the FF5+UMD neutralisation step.

## Quick-Start

```bash
# 1. create environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. drop the three parquet files into data/

# 3. run the pipeline
python run_backtest.py          # writes outputs/weights.parquet & tear-sheet

# 4. run tests
pytest -q                       # sanity-checks factor, alignment and PnL
```

---

## Modifying the Research

| Task                    | Where                        |
| ----------------------- | ---------------------------- |
| Change holding horizon  | `portfolio.pnl(horizon=N)`   |
| Different risk model    | `src/neutralise.py`          |
| Custom weighting scheme | `src/portfolio.py`           |
| Add transaction costs   | debit inside `portfolio.pnl` |

---

## License

MIT – use, adapt, and share.
