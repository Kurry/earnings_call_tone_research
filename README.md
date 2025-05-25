# Tone-Dispersion Factor Research

*Within-call sentiment variance as a market-neutral signal*

---

## Project Layout

```
earnings_call_tone_research/
│
├─ run_backtest.py            # one-shot: build → neutralise → weights → PnL
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
| **tone_dispersion.parquet**  | Columns: `symbol`, `date`, `tone_dispersion`                   |
| **stock_prices.parquet**     | Wide table; `index=date`, `columns=tickers`, `values=adjClose` |
| **ff5_daily.parquet**        | `index=date`; columns `mktrf smb hml rmw cma umd rf`           |

No other data sources or credentials are required.

### Transcript Data for Sentiment Analysis
The sentiment analysis component of this research relies on earnings call transcripts. The specific dataset used for building or applying the sentiment models can be found at:
- [Kurry's S&P 500 Earnings Transcripts on Hugging Face](https://huggingface.co/datasets/kurry/sp500_earnings_transcripts)

---

## Tone-Dispersion Calculation 🛈

* **Granularity:** Each *speaker-turn* (a continuous block of speech by one speaker) inside the earnings-call transcript is scored.
* **Sentiment score:** Each turn receives a scalar in **[-1, 1]** from a local language-model sentiment head (or any deterministic sentiment function):

  ```text
  sentiment(turn_i) → s_i
  ```
* **Dispersion metric:** The **population variance** of all sentiment scores within the call (including both executive and analyst turns):

  $$
  \text{tone_dispersion} = \frac{1}{N} \sum_{i=1}^{N} (s_i - \bar{s})^2, \qquad \bar{s} = \frac{1}{N} \sum_{i=1}^{N} s_i
  $$

  *Requires at least two non-empty turns; otherwise, the value is NaN.*
  
  *Note: This formula requires a Markdown viewer that supports LaTeX math rendering. For reference, in plain code:*
  
  ```python
  mean = sum(scores) / len(scores)
  variance = sum((s - mean) ** 2 for s in scores) / len(scores)
  ```

The resulting table written to `data/tone_dispersion.parquet` therefore holds **one row per call**:

| symbol | date (call timestamp) | tone_dispersion |
| ------ | --------------------- | --------------- |
| AAPL   | 2024-10-24 16:30:00   | 0.0134          |
| MSFT   | 2024-10-26 17:00:00   | 0.0027          |
| ...    | ...                   | ...             |

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
| Add transaction costs   | modify logic inside `portfolio.pnl` |

## GitHub Pages

You can host the backtest results and tear sheet using GitHub Pages:

1. Run `python run_backtest.py` to generate the `outputs/tearsheet.html` file.
2. Commit and push the `outputs/` directory to your repository.
3. In your GitHub repository settings, enable Pages with:
   - Source: *main* branch
   - Folder: */ (root)*
4. Navigate to `https://kurry.github.io/earnings_call_tone_research/outputs/tearsheet.html` to view the tear sheet.

---
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
