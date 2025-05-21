# tests/test_integration.py
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import src.factor_build as fb
import src.neutralise as nz
import src.portfolio as pf
from src.load import prices

REQ = [
    Path("data/ff5_daily.parquet"),
    Path("data/stock_prices.parquet"),
    Path("data/tone_dispersion.parquet"),
]


def _have_all_files():
    return all(p.exists() for p in REQ)


###############################################################################
# 1 ─ Raw parquet smoke check
###############################################################################
@pytest.mark.skipif(not _have_all_files(), reason="research parquets missing")
@pytest.mark.parametrize("fp", REQ)
def test_parquet_not_empty(fp):
    tbl = pd.read_parquet(fp, columns=None)[:5]
    assert len(tbl) > 0, f"{fp} appears empty"


###############################################################################
# 2 ─ Full pipeline (xfail if factor empty)
###############################################################################
@pytest.mark.skipif(not _have_all_files(), reason="research parquets missing")
def test_pipeline_end_to_end(tmp_path):
    factor = fb.build_daily_factor()

    if factor.empty:
        pytest.xfail(
            "tone_dispersion → factor panel produced 0 rows; "
            "check date mapping or parquet contents."
        )

    resid = nz.neutralise(factor)
    weights = pf.build_weights(resid)
    pnl = pf.pnl(weights)

    # basic sanity
    assert isinstance(weights, pd.DataFrame) and not weights.empty
    assert np.allclose(weights.abs().sum(axis=1), 1.0, atol=1e-6)
    assert isinstance(pnl, pd.Series) and not pnl.empty

    # write a tiny artefact to be sure parquet round-trip works
    out = tmp_path / "weights_head.parquet"
    weights.head().to_parquet(out)
    assert out.exists()


# ------------------------------------------------------------------ #
# 5 ─ factor dates must exist in price index
# ------------------------------------------------------------------ #
@pytest.mark.skipif(not _have_all_files(), reason="research parquets missing")
def test_factor_dates_overlap_prices():
    """
    Ensure that at least one trade_date created in build_daily_factor()
    is present in the price table.  Catches silent empty-factor issues.
    """
    factor = fb.build_daily_factor()
    assert not factor.empty, "build_daily_factor() returned 0 rows"

    price_idx = prices().index
    overlap = factor.index.get_level_values(0).unique().intersection(price_idx)
    assert len(overlap) > 0, (
        "No trade_date from factor panel exists in stock_prices index — "
        "check date alignment or BDay mapping."
    )
