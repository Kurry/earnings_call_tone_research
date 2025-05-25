import warnings
from typing import Dict, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .load import prices


def make_tearsheet(factor: pd.Series, out="outputs/tearsheet.png"):
    try:
        import alphalens as al
    except ImportError:
        print(
            "alphalens not installed; please install alpahalens-reloaded to generate tear sheet"
        )
        return

    # Get access to the utility functions we need
    from alphalens.utils import (
        NonMatchingTimezoneError,
        diff_custom_calendar_timedeltas,
        mode,
        timedelta_to_string,
    )

    # Define our own version of compute_forward_returns that doesn't set the freq
    def patched_compute_forward_returns(
        factor,
        prices,
        periods=(1, 5, 10),
        filter_zscore=None,
        cumulative_returns=True,
    ):
        """
        Finds the N period forward returns (as percent change) for each asset
        provided. Modified version that doesn't set a frequency on the index.
        """
        factor_dateindex = factor.index.levels[0]
        if factor_dateindex.tz != prices.index.tz:
            raise NonMatchingTimezoneError(
                "The timezone of 'factor' is not the "
                "same as the timezone of 'prices'. See "
                "the pandas methods tz_localize and "
                "tz_convert."
            )

        # Use generic business day frequency for custom calendar calculations.
        # We avoid attaching this frequency to the index (which would fail
        # when the prices index has irregular spacing) but still provide a
        # valid pandas offset object so that diff_custom_calendar_timedeltas
        # can compute period lengths without raising.
        from pandas.tseries.offsets import BusinessDay as _BDay

        freq = _BDay()

        factor_dateindex = factor_dateindex.intersection(prices.index)

        if len(factor_dateindex) == 0:
            raise ValueError(
                "Factor and prices indices don't match: make sure "
                "they have the same convention in terms of datetimes "
                "and symbol-names"
            )

        # chop prices down to only the assets we care about
        prices = prices.filter(items=factor.index.levels[1])

        raw_values_dict = {}
        column_list = []

        for period in sorted(periods):
            if cumulative_returns:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", FutureWarning)
                    returns = prices.pct_change(period, fill_method=None)
            else:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", FutureWarning)
                    returns = prices.pct_change(fill_method=None)

            forward_returns = returns.shift(-period).reindex(factor_dateindex)

            if filter_zscore is not None:
                mask = abs(forward_returns - forward_returns.mean()) > (
                    filter_zscore * forward_returns.std()
                )
                forward_returns[mask] = np.nan

            # Process period length for column name
            days_diffs = []
            for i in range(30):
                if i >= len(forward_returns.index):
                    break
                p_idx = prices.index.get_loc(forward_returns.index[i])
                if p_idx is None or p_idx < 0 or (p_idx + period) >= len(prices.index):
                    continue
                start = prices.index[p_idx]
                end = prices.index[p_idx + period]
                period_len = diff_custom_calendar_timedeltas(start, end, freq)
                days_diffs.append(period_len.components.days)

            if len(days_diffs) > 0:
                delta_days = (
                    period_len.components.days - mode(days_diffs, keepdims=True).mode[0]
                )
                period_len -= pd.Timedelta(days=delta_days)
            else:
                # Fallback if we couldn't calculate
                period_len = pd.Timedelta(days=period)

            label = timedelta_to_string(period_len)
            column_list.append(label)
            raw_values_dict[label] = np.concatenate(forward_returns.values)

        df = pd.DataFrame.from_dict(raw_values_dict)
        df.set_index(
            pd.MultiIndex.from_product(
                [factor_dateindex, prices.columns], names=["date", "asset"]
            ),
            inplace=True,
        )
        df = df.reindex(factor.index)

        # Set the columns correctly
        df = df[column_list]

        # **** KEY DIFFERENCE: Don't set .freq ****
        # df.index.levels[0].freq = freq

        df.index.set_names(["date", "asset"], inplace=True)
        return df

    # Save the original function and replace it with our patched version
    original_compute_forward_returns = al.utils.compute_forward_returns
    al.utils.compute_forward_returns = patched_compute_forward_returns

    try:
        # Prepare clean factor data
        fac = factor.copy()
        if isinstance(fac.index, pd.MultiIndex):
            lvl0 = fac.index.levels[0]
            dates = pd.DatetimeIndex(lvl0.values)
            fac.index = fac.index.set_levels([dates, fac.index.levels[1]])
        else:
            fac.index = pd.DatetimeIndex(fac.index.values)

        # Suppress warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            # Build clean factor+forward returns DataFrame
            fd = al.utils.get_clean_factor_and_forward_returns(
                fac, prices(), periods=[5, 10], quantiles=5
            )

            # Use a non-interactive backend and capture the figure instead of
            # popping up a GUI window (which would block execution when this
            # script is run from the CLI / CI).
            import matplotlib

            matplotlib.use("Agg", force=True)
            import matplotlib.pyplot as _plt

            _original_show = _plt.show

            def _silent_show(*_args, **_kwargs):
                # Save the latest figure to the requested output path, if any
                if out is not None:
                    try:
                        _plt.gcf().savefig(out, bbox_inches="tight")
                    except Exception:
                        pass
                # Always close to free memory and avoid leaks
                _plt.close("all")

            # Monkey-patch plt.show while the tear sheet is being built
            _plt.show = _silent_show

            try:
                al.tears.create_full_tear_sheet(fd, long_short=True)
                if out is not None:
                    print(f"✓ tear-sheet image saved to {out}")
            finally:
                _plt.show = _original_show
    finally:
        # Restore original compute_forward_returns implementation
        al.utils.compute_forward_returns = original_compute_forward_returns


def calculate_metrics(
    returns: pd.Series, risk_free_rate: Optional[pd.Series] = None
) -> Dict[str, float]:
    """
    Calculate enhanced performance metrics for a return series.

    Parameters:
    -----------
    returns : pd.Series
        Daily portfolio returns
    risk_free_rate : pd.Series, optional
        Daily risk-free rate, if None assumes zero

    Returns:
    --------
    Dict[str, float]
        Dictionary of performance metrics
    """
    if risk_free_rate is not None:
        # Align risk-free rate with returns
        excess_returns = returns - risk_free_rate.reindex(returns.index).fillna(0)
    else:
        excess_returns = returns

    # Annualization factor (assuming daily returns)
    ann_factor = 252

    # Basic metrics
    total_return = (1 + returns).prod() - 1
    ann_return = (1 + total_return) ** (ann_factor / len(returns)) - 1
    ann_volatility = returns.std() * np.sqrt(ann_factor)
    sharpe = (
        np.mean(excess_returns) / returns.std() * np.sqrt(ann_factor)
        if returns.std() > 0
        else 0
    )

    # Drawdown analysis
    cum_returns = (1 + returns).cumprod()
    running_max = cum_returns.cummax()
    drawdown = (cum_returns / running_max) - 1
    max_drawdown = drawdown.min()

    # Advanced metrics
    # Sortino ratio - downside risk only
    downside_returns = returns[returns < 0]
    downside_deviation = (
        downside_returns.std() * np.sqrt(ann_factor) if len(downside_returns) > 0 else 0
    )
    sortino = (
        np.mean(excess_returns) / downside_deviation * np.sqrt(ann_factor)
        if downside_deviation > 0
        else 0
    )

    # Calmar ratio - return / max drawdown
    calmar = abs(ann_return / max_drawdown) if max_drawdown < 0 else 0

    # Win rate and profit ratio
    win_rate = (returns > 0).sum() / len(returns) if len(returns) > 0 else 0

    avg_win = returns[returns > 0].mean() if len(returns[returns > 0]) > 0 else 0
    avg_loss = returns[returns < 0].mean() if len(returns[returns < 0]) > 0 else 0
    profit_ratio = abs(avg_win / avg_loss) if avg_loss < 0 else 0

    # Calculate monthly returns for month-to-month consistency
    monthly_returns = returns.resample("M").apply(lambda x: (1 + x).prod() - 1)
    consistency = (
        (monthly_returns > 0).sum() / len(monthly_returns)
        if len(monthly_returns) > 0
        else 0
    )

    return {
        "total_return": total_return,
        "annualized_return": ann_return,
        "annualized_volatility": ann_volatility,
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino,
        "calmar_ratio": calmar,
        "max_drawdown": max_drawdown,
        "win_rate": win_rate,
        "profit_ratio": profit_ratio,
        "monthly_consistency": consistency,
    }


def plot_enhanced_tearsheet(
    returns: pd.Series,
    turnover: pd.Series = None,
    benchmark_returns: pd.Series = None,
    title: str = "Enhanced Portfolio Performance",
    save_path: str = "outputs/enhanced_tearsheet.png",
) -> plt.Figure:
    """
    Generate an enhanced tear sheet with multiple performance metrics.

    Parameters:
    -----------
    returns : pd.Series
        Daily portfolio returns
    turnover : pd.Series, optional
        Daily portfolio turnover
    benchmark_returns : pd.Series, optional
        Daily benchmark returns for comparison
    title : str
        Plot title
    save_path : str
        Where to save the plot

    Returns:
    --------
    plt.Figure
        The matplotlib figure object
    """
    metrics = calculate_metrics(returns)

    # Create figure with subplots
    fig = plt.figure(figsize=(12, 10))

    # 1. Cumulative returns
    ax1 = plt.subplot2grid((3, 2), (0, 0), colspan=2)
    cum_returns = (1 + returns).cumprod() - 1
    cum_returns.plot(ax=ax1, color="blue", linewidth=2)

    if benchmark_returns is not None:
        cum_bench = (1 + benchmark_returns.reindex(returns.index)).cumprod() - 1
        cum_bench.plot(ax=ax1, color="gray", linestyle="--", linewidth=1, alpha=0.7)
        ax1.legend(["Portfolio", "Benchmark"])

    ax1.set_title("Cumulative Returns")
    ax1.set_ylabel("Return")
    ax1.grid(True, alpha=0.3)

    # 2. Drawdowns
    ax2 = plt.subplot2grid((3, 2), (1, 0), colspan=2)
    running_max = (1 + returns).cumprod().cummax()
    drawdown = ((1 + returns).cumprod() / running_max) - 1
    drawdown.plot(ax=ax2, color="red", linewidth=1.5)
    ax2.set_title("Drawdowns")
    ax2.set_ylabel("Drawdown")
    ax2.grid(True, alpha=0.3)

    # 3. Monthly returns heatmap
    ax3 = plt.subplot2grid((3, 2), (2, 0))
    monthly_returns = returns.resample("M").apply(lambda x: (1 + x).prod() - 1)
    monthly_returns = monthly_returns.to_frame()

    # Create a pivot table for the heatmap
    monthly_pivot = pd.DataFrame(
        {
            "Year": monthly_returns.index.year,
            "Month": monthly_returns.index.month,
            "Returns": monthly_returns.iloc[:, 0].values,
        }
    )
    heatmap_data = monthly_pivot.pivot("Year", "Month", "Returns")

    # Plot heatmap if we have sufficient data
    if not heatmap_data.empty and len(heatmap_data) > 1:
        im = ax3.imshow(heatmap_data, cmap="RdYlGn", aspect="auto", vmin=-0.1, vmax=0.1)
        ax3.set_title("Monthly Returns")

        # Add colorbar
        plt.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)

        # Set x and y ticks
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        ax3.set_xticks(np.arange(len(months)))
        ax3.set_xticklabels(months, rotation=45)
        ax3.set_yticks(np.arange(len(heatmap_data.index)))
        ax3.set_yticklabels(heatmap_data.index)
    else:
        ax3.text(
            0.5,
            0.5,
            "Insufficient data for heatmap",
            horizontalalignment="center",
            verticalalignment="center",
        )

    # 4. Metrics table
    ax4 = plt.subplot2grid((3, 2), (2, 1))
    ax4.axis("off")

    metrics_text = "\n".join(
        [
            f"Annualized Return: {metrics['annualized_return']:.2%}",
            f"Annualized Volatility: {metrics['annualized_volatility']:.2%}",
            f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}",
            f"Sortino Ratio: {metrics['sortino_ratio']:.2f}",
            f"Max Drawdown: {metrics['max_drawdown']:.2%}",
            f"Calmar Ratio: {metrics['calmar_ratio']:.2f}",
            f"Win Rate: {metrics['win_rate']:.2%}",
            f"Profit Ratio: {metrics['profit_ratio']:.2f}",
            f"Monthly Consistency: {metrics['monthly_consistency']:.2%}",
        ]
    )

    if turnover is not None:
        avg_turnover = turnover.mean()
        metrics_text += f"\nAvg. Turnover: {avg_turnover:.2%}"
        metrics_text += f"\nAdj. Sharpe: {metrics['sharpe_ratio']/(1+avg_turnover):.2f}"

    ax4.text(0.1, 0.9, metrics_text, verticalalignment="top", fontsize=10)
    ax4.set_title("Performance Metrics")

    # Add main title
    plt.suptitle(title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Save figure if path is provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


def analyze_factor_exposures(
    returns: pd.Series, factor_returns: pd.DataFrame, rolling_window: int = 60
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Analyze time-varying factor exposures using rolling regression.

    Parameters:
    -----------
    returns : pd.Series
        Portfolio returns
    factor_returns : pd.DataFrame
        Factor returns (e.g., Fama-French factors)
    rolling_window : int
        Window size for rolling regression

    Returns:
    --------
    Tuple[pd.DataFrame, pd.DataFrame]
        Factor betas and R-squared over time
    """
    from sklearn.linear_model import LinearRegression

    # Align data
    aligned_data = pd.concat([returns, factor_returns], axis=1).dropna()

    # Initialize results
    dates = aligned_data.index[rolling_window - 1 :]
    factor_names = factor_returns.columns
    betas = pd.DataFrame(index=dates, columns=factor_names)
    r2 = pd.Series(index=dates)

    # Rolling regression
    for i in range(rolling_window, len(aligned_data) + 1):
        window = aligned_data.iloc[i - rolling_window : i]

        y = window.iloc[:, 0].values
        X = window.iloc[:, 1:].values

        model = LinearRegression().fit(X, y)
        betas.iloc[i - rolling_window] = model.coef_
        r2.iloc[i - rolling_window] = model.score(X, y)

    return betas, r2


def calculate_conditional_metrics(
    returns: pd.Series,
    condition_series: pd.Series,
    condition_threshold: Optional[float] = None,
) -> Dict[str, Dict[str, float]]:
    """
    Calculate performance metrics conditionally based on another series.
    Useful for analyzing performance in different market regimes.

    Parameters:
    -----------
    returns : pd.Series
        Portfolio returns
    condition_series : pd.Series
        Series to condition on (e.g., market returns, volatility)
    condition_threshold : float, optional
        Threshold to split condition_series, if None uses median

    Returns:
    --------
    Dict[str, Dict[str, float]]
        Performance metrics in each regime
    """
    # Align data
    aligned = pd.concat([returns, condition_series], axis=1).dropna()
    ret = aligned.iloc[:, 0]
    cond = aligned.iloc[:, 1]

    # Determine threshold if not provided
    if condition_threshold is None:
        condition_threshold = cond.median()

    # Split returns by condition
    high_regime = ret[cond > condition_threshold]
    low_regime = ret[cond <= condition_threshold]

    # Calculate metrics for each regime
    high_metrics = calculate_metrics(high_regime)
    low_metrics = calculate_metrics(low_regime)
    all_metrics = calculate_metrics(ret)

    return {
        "high_regime": high_metrics,
        "low_regime": low_metrics,
        "all_periods": all_metrics,
    }
