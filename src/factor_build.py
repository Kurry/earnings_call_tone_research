import pandas as pd
import pandas_market_calendars as mcal
from pandas.tseries.offsets import BDay

from .load import tone_calls

nyse = mcal.get_calendar("NYSE")


def _next_nyse_open(ts: pd.Timestamp) -> pd.Timestamp | None:
    """
    Return the date of the NEXT NYSE session (00:00)
    strictly after `ts`.  Works with any pandas-market-calendars
    version because it uses `valid_days`.
    """
    ts = pd.Timestamp(ts)
    # start search the day *after* the call
    start = (ts + pd.Timedelta(days=1)).normalize()
    # grab the next calendar open within one week window
    days = nyse.valid_days(start, start + pd.Timedelta(days=7))
    return days[0].tz_localize(None) if len(days) else None


def build_daily_factor() -> pd.Series:
    """Return z-scored tone‐dispersion indexed by trade_date + ticker."""
    calls = tone_calls()

    # robust datetime parse
    calls["call_ts"] = pd.to_datetime(calls["date"], errors="coerce")

    # drop bad rows early
    calls = calls.dropna(subset=["call_ts"])

    # trade date = *next NYSE business day* (simple BDay)
    calls["trade_date"] = calls["call_ts"].dt.normalize() + BDay(1)

    factor = calls.set_index(["trade_date", "symbol"])["tone_dispersion"].rename(
        "tone_var"
    )

    # z-score cross-section
    factor = (
        factor.groupby(level=0, group_keys=False)
        .transform(lambda s: (s - s.mean()) / s.std(ddof=0))
        .dropna()
    )
    return factor
