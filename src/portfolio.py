# src/portfolio.py
import warnings

import numpy as np
import pandas as pd

from .load import prices


def _date(idx):
    return idx.get_level_values(0) if isinstance(idx, pd.MultiIndex) else idx


def build_weights(
    signal: pd.Series, gross: float = 1.0, smoothing: float = 0.75
) -> pd.DataFrame:
    """
    Long–short weights with ∑|w| = gross and ∑w = 0 inside each day,
    with enhanced smoothing between days to control turnover.

    Parameters:
    -----------
    signal : pd.Series
        Factor signal with MultiIndex (date, symbol)
    gross : float
        Target gross exposure (sum of absolute weights)
    smoothing : float
        Weight between 0 and 1 determining how much to retain previous day weights
        0 = no smoothing (complete portfolio turnover each day)
        1 = maximum smoothing (weights never change)
        Default is 0.75 (75% retention of previous day weights)
    """
    if not (0 <= smoothing <= 1):
        raise ValueError("Smoothing parameter must be between 0 and 1")

    dlevel = _date(signal.index)

    # First calculate the target weights without smoothing
    # Use improved ranking with midpoint tie handling
    r = signal.groupby(dlevel).rank(method="average").astype(float)
    n = signal.groupby(dlevel).transform("count")
    centred = (2 * r - n - 1) / n

    # Apply nonlinear transformation to enhance signal distinction
    # This reduces the impact of noise in the middle of the distribution
    centred = np.sign(centred) * np.abs(centred) ** 0.75

    # Scale to desired gross exposure
    scaled = centred / centred.abs().groupby(dlevel).transform("sum") * gross

    # Convert to DataFrame
    target_weights = scaled.unstack(fill_value=0.0).astype(float)

    # If no smoothing requested, return the target weights directly
    if smoothing == 0:
        return target_weights

    # Apply improved weight smoothing between days
    dates = sorted(target_weights.index)
    all_symbols = target_weights.columns

    # Initialize with first day's weights
    smoothed_weights = pd.DataFrame(index=dates, columns=all_symbols, dtype=float)
    smoothed_weights.iloc[0] = target_weights.iloc[0]

    # For each subsequent day, blend previous day's weights with target weights
    for i in range(1, len(dates)):
        prev_date = dates[i - 1]
        curr_date = dates[i]

        # Get previous weights and current target
        prev_weights = smoothed_weights.loc[prev_date]
        target = target_weights.loc[curr_date]

        # Identify symbols with significant signal changes
        signal_change = abs(target - prev_weights)
        # Find symbols with significant changes (top 25%)
        significant_change_threshold = signal_change.quantile(0.75)
        significant_change = signal_change > significant_change_threshold

        # Create a Series for adaptive smoothing factors
        adaptive_smoothing = pd.Series(index=all_symbols, data=smoothing)
        # Reduce smoothing for symbols with significant changes
        adaptive_smoothing[significant_change] = max(0, smoothing - 0.25)

        # Apply weighted blend with adaptive smoothing
        blended = pd.Series(index=all_symbols)
        for sym in all_symbols:
            sym_smoothing = adaptive_smoothing[sym]
            blended[sym] = (1 - sym_smoothing) * target[
                sym
            ] + sym_smoothing * prev_weights[sym]

        # Re-normalize to ensure gross exposure constraint is maintained
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            gross_exposure = blended.abs().sum()
            if gross_exposure > 0:  # Avoid division by zero
                blended = blended * (gross / gross_exposure)

        # Ensure weights sum to zero (market neutral)
        net_exposure = blended.sum()
        if abs(net_exposure) > 1e-10:  # Only adjust if meaningfully different from zero
            # Distribute the net exposure proportionally to weight magnitude
            weight_magnitude = blended.abs()
            total_magnitude = weight_magnitude.sum()

            if total_magnitude > 0:
                adjustment_factor = -net_exposure / total_magnitude
                adjustment = weight_magnitude * adjustment_factor
                blended += adjustment

        smoothed_weights.loc[curr_date] = blended

    return smoothed_weights


def pnl(weights: pd.DataFrame, horizon: int = 5) -> pd.Series:
    """Calculate PnL series from weights and forward returns"""
    px = prices()
    common = weights.columns.intersection(px.columns)
    if common.empty:
        raise ValueError("weights vs price columns have no overlap")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        fwd = px[common].pct_change(horizon, fill_method=None).shift(-horizon)

    wl = weights[common].shift(1).reindex(fwd.index).fillna(0.0)
    return (wl * fwd).sum(axis=1).dropna()


def calculate_turnover(weights: pd.DataFrame) -> pd.Series:
    """
    Calculate the daily portfolio turnover.

    Turnover is defined as the sum of absolute weight changes divided by 2.
    A turnover of 1.0 means complete portfolio replacement.
    """
    weights_shifted = weights.shift(1)
    daily_turnover = (weights - weights_shifted).abs().sum(axis=1).dropna() / 2
    return daily_turnover
