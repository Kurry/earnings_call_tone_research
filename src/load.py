from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"


def ff_factors() -> pd.DataFrame:
    return pd.read_parquet(DATA / "ff5_daily.parquet")


# src/load.py
def prices():
    path = DATA / "stock_prices.parquet"
    # detect Git LFS pointer files and prompt user to fetch real data
    try:
        with open(path, 'rb') as f:
            first = f.readline()
        if first.startswith(b'version https://git-lfs.github.com'):
            raise RuntimeError(
                "data/stock_prices.parquet appears to be a Git LFS pointer.\n"
                "Please run `git lfs install` and `git lfs pull` to fetch the actual data."
            )
    except OSError:
        raise RuntimeError(f"Unable to open {path}")
    px = pd.read_parquet(path)

    # long form → wide: adjClose, upper-case symbols
    px = px.pivot(index="date", columns="symbol", values="adjClose").sort_index()
    px.columns = px.columns.str.upper()
    return px


def tone_calls() -> pd.DataFrame:
    return pd.read_parquet(DATA / "tone_dispersion.parquet")
