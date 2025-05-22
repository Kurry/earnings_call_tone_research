import warnings

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
                    returns = prices.pct_change(period)
            else:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", FutureWarning)
                    returns = prices.pct_change()

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

            def _silent_show(*args, **kwargs):
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
