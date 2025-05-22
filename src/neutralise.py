import pandas as pd
import numpy as np
import statsmodels.api as sm  # only for API consistency, but fallback for small samples

from .load import ff_factors

FF = ff_factors()


def _get_date_index(df: pd.DataFrame) -> pd.Index:
    """Return the first level of the index as a plain date Index."""
    if isinstance(df.index, pd.MultiIndex):
        return df.index.get_level_values(0)
    return df.index


def neutralise(factor: pd.Series) -> pd.Series:
    """
    Regress the raw tone-dispersion signal on daily FF-5 + UMD
    and return the cross-sectional residuals.
    Works whether the index level is called 'date' or 'trade_date'.
    """
    # align factors
    date_level = factor.index.names[0]  # 'trade_date' in our build
    df = (
        factor.to_frame()
        .join(FF, how="left", on=date_level)  # CRSP factors keyed on same date
        .dropna()
    )

    def _resid(day_df: pd.DataFrame):
        y = day_df.iloc[:, 0].values
        cols = ["mktrf", "smb", "hml", "rmw", "cma", "umd"]
        # design matrix with constant term
        X = np.column_stack([np.ones(len(day_df))] + [day_df[c].values for c in cols])
        # solve least squares for speed
        try:
            beta, *_ = np.linalg.lstsq(X, y, rcond=None)
            resid = y - X.dot(beta)
        except Exception:
            # fallback to statsmodels if numpy fails
            X_sm = sm.add_constant(day_df[cols])
            resid = sm.OLS(day_df.iloc[:, 0], X_sm).fit().resid.values
        return pd.Series(resid, index=day_df.index)

    resid = (
        df.groupby(_get_date_index(df), group_keys=False)
        .apply(_resid)
        .rename("tone_resid")
    )
    return resid
