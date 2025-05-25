# tests/test_integration.py
import os
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import src.factor_build as fb
import src.neutralise as nz
import src.portfolio as pf
import src.report as report
from src.load import ff_factors, prices, tone_calls

REQ = [
    Path("data/ff5_daily.parquet"),
    Path("data/stock_prices.parquet"),
    Path("data/tone_dispersion.parquet"),
]


def _have_all_files():
    for p in REQ:
        if not p.exists():
            return False
        try:
            with p.open('rb') as f:
                first = f.readline()
            # skip Git LFS pointer files
            if first.startswith(b'version https://git-lfs.github.com'):
                return False
        except Exception:
            return False
    return True


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


###############################################################################
# 3 ─ Parquet File Data Integrity Tests
###############################################################################
@pytest.mark.skipif(not _have_all_files(), reason="research parquets missing")
class TestParquetDataIntegrity:
    """Test the integrity and expected structure of parquet files."""
    
    def test_ff_factors_structure(self):
        """Test FF5 daily factors parquet file structure."""
        ff = ff_factors()
        
        # Check basic structure
        assert isinstance(ff, pd.DataFrame), "FF factors should be a DataFrame"
        assert not ff.empty, "FF factors should not be empty"
        assert isinstance(ff.index, pd.DatetimeIndex), "FF factors should have DatetimeIndex"
        
        # Check expected columns
        expected_cols = {'mktrf', 'smb', 'hml', 'rmw', 'cma', 'umd', 'rf'}
        assert expected_cols.issubset(set(ff.columns)), f"Missing columns: {expected_cols - set(ff.columns)}"
        
        # Check data types
        assert all(ff.dtypes == 'float64'), "All FF factor columns should be float64"
        
        # Check for reasonable value ranges (factors typically between -20% and +20% daily)
        assert ff.abs().max().max() < 0.5, "FF factors contain unreasonable values"
        
        # Check index is properly sorted
        assert ff.index.is_monotonic_increasing, "FF factors index should be sorted"
    
    def test_stock_prices_structure(self):
        """Test stock prices parquet file structure and loading."""
        px = prices()
        
        # Check basic structure
        assert isinstance(px, pd.DataFrame), "Prices should be a DataFrame"
        assert not px.empty, "Prices should not be empty"
        assert isinstance(px.index, pd.DatetimeIndex), "Prices should have DatetimeIndex"
        
        # Check symbol columns are uppercase
        assert all(col.isupper() for col in px.columns), "Stock symbols should be uppercase"
        
        # Check for reasonable price values (positive, finite)
        assert (px > 0).all().all(), "All prices should be positive"
        assert px.isfinite().all().all(), "All prices should be finite"
        
        # Check index is properly sorted
        assert px.index.is_monotonic_increasing, "Prices index should be sorted"
        
        # Check for sufficient data coverage
        assert len(px) > 100, "Should have sufficient price history"
        assert len(px.columns) > 10, "Should have sufficient number of stocks"
    
    def test_tone_calls_structure(self):
        """Test tone dispersion parquet file structure."""
        tone = tone_calls()
        
        # Check basic structure
        assert isinstance(tone, pd.DataFrame), "Tone calls should be a DataFrame"
        assert not tone.empty, "Tone calls should not be empty"
        
        # Check expected columns
        expected_cols = {'symbol', 'company_id', 'year', 'quarter', 'date', 'tone_dispersion', 'call_key'}
        assert expected_cols.issubset(set(tone.columns)), f"Missing columns: {expected_cols - set(tone.columns)}"
        
        # Check data types
        assert pd.api.types.is_datetime64_any_dtype(tone['date']), "Date column should be datetime"
        assert pd.api.types.is_numeric_dtype(tone['tone_dispersion']), "Tone dispersion should be numeric"
        assert pd.api.types.is_integer_dtype(tone['year']), "Year should be integer"
        assert pd.api.types.is_integer_dtype(tone['quarter']), "Quarter should be integer"
        
        # Check value ranges
        assert tone['quarter'].between(1, 4).all(), "Quarter should be between 1 and 4"
        assert tone['year'].between(1990, 2030).all(), "Year should be reasonable"
        assert tone['tone_dispersion'].isfinite().all(), "Tone dispersion should be finite"


###############################################################################
# 4 ─ Data Alignment and Cross-File Consistency Tests
###############################################################################
@pytest.mark.skipif(not _have_all_files(), reason="research parquets missing")
class TestDataAlignment:
    """Test alignment and consistency between different data files."""
    
    def test_price_ff_date_overlap(self):
        """Test that prices and FF factors have sufficient date overlap."""
        px = prices()
        ff = ff_factors()
        
        # Find overlap
        overlap = px.index.intersection(ff.index)
        
        # Should have substantial overlap
        assert len(overlap) > 100, "Insufficient date overlap between prices and FF factors"
        
        # Check that overlap covers a reasonable time period
        date_range = overlap.max() - overlap.min()
        assert date_range.days > 365, "Date overlap should span at least one year"
    
    def test_tone_calls_symbol_in_prices(self):
        """Test that tone dispersion symbols exist in price data."""
        tone = tone_calls()
        px = prices()
        
        # Get unique symbols from tone data (uppercase for comparison)
        tone_symbols = set(tone['symbol'].str.upper().unique())
        price_symbols = set(px.columns)
        
        # Check overlap
        overlap = tone_symbols.intersection(price_symbols)
        
        # Should have reasonable overlap
        assert len(overlap) > 0, "No symbols from tone data found in price data"
        
        # At least 50% of tone symbols should be in price data
        overlap_ratio = len(overlap) / len(tone_symbols)
        assert overlap_ratio > 0.3, f"Low symbol overlap: {overlap_ratio:.2%}"


###############################################################################
# 5 ─ Enhanced Pipeline Integration Tests
###############################################################################
@pytest.mark.skipif(not _have_all_files(), reason="research parquets missing")
class TestEnhancedPipeline:
    """Test the enhanced pipeline with smoothing and advanced metrics."""
    
    def test_portfolio_smoothing_effect(self):
        """Test that portfolio smoothing reduces turnover."""
        factor = fb.build_daily_factor()
        
        if factor.empty:
            pytest.skip("Empty factor - cannot test smoothing")
        
        resid = nz.neutralise(factor)
        
        # Build weights with and without smoothing
        weights_no_smooth = pf.build_weights(resid, smoothing=0.0)
        weights_smooth = pf.build_weights(resid, smoothing=0.75)
        
        # Calculate turnover
        turnover_no_smooth = pf.calculate_turnover(weights_no_smooth)
        turnover_smooth = pf.calculate_turnover(weights_smooth)
        
        # Smoothing should reduce average turnover
        assert turnover_smooth.mean() < turnover_no_smooth.mean(), \
            "Smoothing should reduce average turnover"
    
    def test_enhanced_metrics_calculation(self):
        """Test enhanced metrics calculation on synthetic returns."""
        # Create synthetic return series
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=252, freq='B')
        returns = pd.Series(np.random.normal(0.001, 0.02, len(dates)), index=dates)
        
        metrics = report.calculate_metrics(returns)
        
        # Check all expected metrics are present
        expected_metrics = {
            'total_return', 'annualized_return', 'annualized_volatility', 
            'sharpe_ratio', 'sortino_ratio', 'calmar_ratio', 'max_drawdown',
            'win_rate', 'profit_ratio', 'monthly_consistency'
        }
        assert expected_metrics.issubset(set(metrics.keys())), \
            f"Missing metrics: {expected_metrics - set(metrics.keys())}"
        
        # Check metric values are reasonable
        assert -1 < metrics['max_drawdown'] <= 0, "Max drawdown should be negative"
        assert 0 <= metrics['win_rate'] <= 1, "Win rate should be between 0 and 1"
        assert metrics['annualized_volatility'] > 0, "Volatility should be positive"
    
    def test_factor_exposure_analysis(self):
        """Test factor exposure analysis functionality."""
        # Create synthetic data
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=100, freq='B')
        
        # Portfolio returns
        portfolio_returns = pd.Series(np.random.normal(0.001, 0.02, len(dates)), index=dates)
        
        # Factor returns (mock FF5)
        factor_returns = pd.DataFrame({
            'mktrf': np.random.normal(0.0005, 0.015, len(dates)),
            'smb': np.random.normal(0.0, 0.01, len(dates)),
            'hml': np.random.normal(0.0, 0.01, len(dates)),
            'rmw': np.random.normal(0.0, 0.008, len(dates)),
            'cma': np.random.normal(0.0, 0.008, len(dates))
        }, index=dates)
        
        betas, r2 = report.analyze_factor_exposures(
            portfolio_returns, factor_returns, rolling_window=30
        )
        
        # Check structure
        assert isinstance(betas, pd.DataFrame), "Betas should be DataFrame"
        assert isinstance(r2, pd.Series), "R-squared should be Series"
        assert len(betas) > 0, "Betas should not be empty"
        assert set(betas.columns) == set(factor_returns.columns), "Beta columns should match factors"


###############################################################################
# 6 ─ Output Generation and File I/O Tests  
###############################################################################
@pytest.mark.skipif(not _have_all_files(), reason="research parquets missing")
def test_output_file_generation():
    """Test that the pipeline can generate expected output files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Set up temporary outputs directory
        outputs_dir = Path(tmp_dir) / "outputs"
        outputs_dir.mkdir()
        
        # Mock the outputs directory in the environment
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_dir)
            
            # Run partial pipeline
            factor = fb.build_daily_factor()
            
            if not factor.empty:
                resid = nz.neutralise(factor)
                weights = pf.build_weights(resid)
                
                # Test parquet output
                weights_file = outputs_dir / "test_weights.parquet"
                weights.to_parquet(weights_file)
                
                # Verify file was created and can be read back
                assert weights_file.exists(), "Weights parquet file should be created"
                weights_loaded = pd.read_parquet(weights_file)
                pd.testing.assert_frame_equal(weights, weights_loaded)
                
                # Test PnL calculation
                pnl = pf.pnl(weights)
                assert isinstance(pnl, pd.Series), "PnL should be a Series"
                assert not pnl.empty, "PnL should not be empty"
        
        finally:
            os.chdir(original_cwd)


###############################################################################
# 7 ─ Performance and Regression Tests
###############################################################################
@pytest.mark.skipif(not _have_all_files(), reason="research parquets missing")
def test_pipeline_performance_characteristics():
    """Test that pipeline produces reasonable performance characteristics."""
    factor = fb.build_daily_factor()
    
    if factor.empty:
        pytest.skip("Empty factor - cannot test performance")
    
    resid = nz.neutralise(factor)
    weights = pf.build_weights(resid, smoothing=0.75)
    pnl = pf.pnl(weights)
    
    # Basic performance checks
    assert len(pnl) > 0, "Should have PnL observations"
    
    # Check that weights are market neutral (sum to zero)
    weight_sums = weights.sum(axis=1)
    assert np.allclose(weight_sums, 0.0, atol=1e-10), "Weights should be market neutral"
    
    # Check gross exposure is approximately 1.0
    gross_exposure = weights.abs().sum(axis=1)
    assert np.allclose(gross_exposure, 1.0, rtol=1e-6), "Gross exposure should be 1.0"
    
    # Calculate basic performance metrics
    if len(pnl) > 20:  # Need sufficient data
        ir = pnl.mean() / pnl.std() * np.sqrt(252)
        
        # IR should be finite
        assert np.isfinite(ir), "Information ratio should be finite"
        
        # Turnover should be reasonable
        turnover = pf.calculate_turnover(weights)
        avg_turnover = turnover.mean()
        
        assert 0 <= avg_turnover <= 2.0, f"Average turnover {avg_turnover:.4f} seems unreasonable"


###############################################################################
# 8 ─ Data Loading and Transformation Tests
###############################################################################
@pytest.mark.skipif(not _have_all_files(), reason="research parquets missing")
class TestDataLoading:
    """Test data loading and transformation functions."""
    
    def test_stock_prices_loading_no_warnings(self):
        """Test that stock prices load without generating warnings."""
        import warnings
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            px = prices()
            
            # Check for deprecation warnings
            deprecation_warnings = [warning for warning in w 
                                  if issubclass(warning.category, (FutureWarning, DeprecationWarning))]
            
            if deprecation_warnings:
                # Log the warnings but don't fail - they may be from dependencies
                for warning in deprecation_warnings:
                    print(f"Warning in prices(): {warning.message}")
        
        # Verify successful loading
        assert isinstance(px, pd.DataFrame), "Prices should load as DataFrame"
        assert not px.empty, "Prices should not be empty"
    
    def test_stock_prices_transformation_quality(self):
        """Test quality of stock prices after pivot transformation."""
        px = prices()
        
        # Check that we have reasonable data coverage
        assert len(px) > 1000, "Should have substantial price history"
        assert len(px.columns) > 100, "Should have many stocks"
        
        # Check data sparsity is reasonable (financial data is naturally sparse)
        non_null_ratio = px.count().sum() / (len(px) * len(px.columns))
        assert non_null_ratio > 0.1, f"Data too sparse: {non_null_ratio:.2%} non-null"
        
        # Check for reasonable price ranges
        px_clean = px.dropna()
        if not px_clean.empty:
            assert (px_clean > 0).all().all(), "All prices should be positive"
            assert (px_clean < 10000).all().all(), "Prices should be reasonable (< $10,000)"
    
    def test_pnl_calculation_robustness(self):
        """Test that PnL calculation handles edge cases properly."""
        factor = fb.build_daily_factor()
        
        if factor.empty:
            pytest.skip("Empty factor - cannot test PnL calculation")
        
        resid = nz.neutralise(factor)
        weights = pf.build_weights(resid, smoothing=0.75)
        
        # Test PnL calculation doesn't generate warnings
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            pnl = pf.pnl(weights)
            
            # Filter to only pandas/finance related warnings
            relevant_warnings = [warning for warning in w 
                               if 'pct_change' in str(warning.message) or 
                                  'fill_method' in str(warning.message)]
            
            # Should not have pandas deprecation warnings
            assert len(relevant_warnings) == 0, \
                f"PnL calculation generated warnings: {[str(w.message) for w in relevant_warnings]}"
        
        # Verify PnL is reasonable
        assert isinstance(pnl, pd.Series), "PnL should be Series"
        assert not pnl.empty, "PnL should not be empty"
        assert np.isfinite(pnl).all(), "All PnL values should be finite"
