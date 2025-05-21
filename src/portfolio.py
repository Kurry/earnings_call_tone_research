# src/portfolio.py
import numpy as np
import pandas as pd

from .load import prices


def _date(idx):
    return idx.get_level_values(0) if isinstance(idx, pd.MultiIndex) else idx


def build_weights(signal: pd.Series, gross: float = 1.0) -> pd.DataFrame:
    """
    Long–short weights with ∑|w| = gross and ∑w = 0 inside each day,
    even if only two securities are present.
    """
    dlevel = _date(signal.index)

    # centred rank in [-1,1]  :  (2*rank-1)/n
    r = signal.groupby(dlevel).rank(method="first").astype(float)
    n = signal.groupby(dlevel).transform("count")
    centred = (2 * r - 1) / n

    scaled = centred / centred.abs().groupby(dlevel).transform("sum") * gross

    # guarantee DataFrame even if single date or ticker
    return scaled.unstack(fill_value=0.0).astype(float)


def pnl(weights: pd.DataFrame, horizon: int = 5) -> pd.Series:
    px = prices()
    common = weights.columns.intersection(px.columns)
    if common.empty:
        raise ValueError("weights vs price columns have no overlap")

    fwd = px[common].pct_change(horizon).shift(-horizon)
    wl = weights[common].shift(1).reindex(fwd.index).fillna(0.0)

    return (wl * fwd).sum(axis=1).dropna()
