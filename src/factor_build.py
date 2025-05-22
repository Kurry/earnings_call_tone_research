import pandas as pd
from pandas.tseries.offsets import BDay

from .load import tone_calls





def build_daily_factor() -> pd.Series:
    """Return z-scored tone‐dispersion indexed by trade_date + ticker."""
    calls = tone_calls()

    # robust datetime parse from 'date' or 'trade_date'
    if "date" in calls.columns:
        calls["call_ts"] = pd.to_datetime(calls["date"], errors="coerce")
    elif "trade_date" in calls.columns:
        calls["call_ts"] = pd.to_datetime(calls["trade_date"], errors="coerce")
    else:
        raise KeyError("tone_calls() must provide 'date' or 'trade_date' column")

    # drop bad rows early
    calls = calls.dropna(subset=["call_ts"])

    # trade date = *next NYSE business day* (simple BDay)
    calls["trade_date"] = calls["call_ts"].dt.normalize() + BDay(1)

    # aggregate multiple calls per symbol-date by mean dispersion
    calls = (
        calls.groupby(["trade_date", "symbol"], as_index=False)["tone_dispersion"]
        .mean()
    )
    factor = calls.set_index(["trade_date", "symbol"])["tone_dispersion"].rename("tone_var")

    # z-score cross-section
    factor = (
        factor.groupby(level=0, group_keys=False)
        .transform(lambda s: (s - s.mean()) / s.std(ddof=0))
        .dropna()
    )
    return factor
