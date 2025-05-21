import pandas as pd
import statsmodels.api as sm

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
        y = day_df.iloc[:, 0]
        X = sm.add_constant(day_df[["mktrf", "smb", "hml", "rmw", "cma", "umd"]])
        return sm.OLS(y, X).fit().resid

    resid = (
        df.groupby(_get_date_index(df), group_keys=False)
        .apply(_resid)
        .rename("tone_resid")
    )
    return resid
