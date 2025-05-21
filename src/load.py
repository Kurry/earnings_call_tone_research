from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"


def ff_factors() -> pd.DataFrame:
    return pd.read_parquet(DATA / "ff5_daily.parquet")


# src/load.py
def prices():
    px = pd.read_parquet(DATA / "stock_prices.parquet")

    # long form → wide: adjClose, upper-case symbols
    px = px.pivot(index="date", columns="symbol", values="adjClose").sort_index()
    px.columns = px.columns.str.upper()
    return px


def tone_calls() -> pd.DataFrame:
    return pd.read_parquet(DATA / "tone_dispersion.parquet")
    return pd.read_parquet(DATA / "tone_dispersion.parquet")
