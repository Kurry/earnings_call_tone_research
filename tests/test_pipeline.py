# tests/test_pipeline.py
import numpy as np
import pandas as pd
import pytest

import src.factor_build as fb
import src.neutralise as nz
import src.portfolio as pf
from src.load import prices


# ------------------------------------------------------------------ #
# tiny synthetic fixtures
# ------------------------------------------------------------------ #
@pytest.fixture(scope="module")
def tiny_calls():
    dates = pd.date_range("2025-01-02", periods=3, freq="B")
    ix = pd.MultiIndex.from_product(
        [dates, ["AAA", "BBB"]],
        names=["trade_date", "symbol"],
    )
    rng = np.random.default_rng(0)
    return pd.Series(rng.normal(size=len(ix)), index=ix, name="tone_dispersion")


@pytest.fixture(scope="module")
def tiny_prices():
    dates = pd.date_range("2025-01-02", periods=10, freq="B")
    data = {"AAA": np.linspace(100, 109, 10), "BBB": np.linspace(50, 59, 10)}
    return pd.DataFrame(data, index=dates)


# ------------------------------------------------------------------ #
# 1. factor build
# ------------------------------------------------------------------ #
def test_factor_build_structure(tiny_calls, monkeypatch):
    # Supply tiny_calls when real parquet absent
    monkeypatch.setattr(fb, "tone_calls", lambda: tiny_calls.reset_index())

    fac = fb.build_daily_factor()
    assert isinstance(fac, pd.Series)
    assert fac.index.names == ["trade_date", "symbol"]
    assert abs(fac.groupby("trade_date").mean()).max() < 1e-8


# ------------------------------------------------------------------ #
# 2. neutralise
# ------------------------------------------------------------------ #
def test_neutralise_zero_cov(monkeypatch):
    dates = pd.date_range("2025-01-02", periods=3, freq="B")
    dummy_ff = pd.DataFrame(
        dict(mktrf=[0.01, -0.02, 0.005], smb=0, hml=0, rmw=0, cma=0, umd=0, rf=0),
        index=dates,
    )
    dummy_ff.index.name = "trade_date"
    monkeypatch.setattr(nz, "FF", dummy_ff)

    ix = pd.MultiIndex.from_product(
        [dates, ["AAA", "BBB"]], names=["trade_date", "symbol"]
    )
    rng = np.random.default_rng(1)
    raw = pd.Series(rng.normal(len(ix)), index=ix)

    resid = nz.neutralise(raw)
    assert resid.index.equals(raw.index)
    assert abs(resid.groupby("trade_date").mean()).max() < 1e-8


# ------------------------------------------------------------------ #
# 3. weights & pnl
# ------------------------------------------------------------------ #
def test_weights_and_pnl(tiny_calls, tiny_prices, monkeypatch):
    monkeypatch.setattr(pf, "prices", lambda: tiny_prices)

    w = pf.build_weights(tiny_calls)
    assert isinstance(w, pd.DataFrame)
    assert np.allclose(w.sum(axis=1), 0.0)

    pnl = pf.pnl(w, horizon=2)
    assert isinstance(pnl, pd.Series) and len(pnl) > 0
