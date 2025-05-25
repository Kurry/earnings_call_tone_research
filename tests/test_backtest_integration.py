# tests/test_backtest_integration.py
"""
Comprehensive integration tests for the full backtest pipeline.
Tests the end-to-end execution of run_backtest.py functionality.
"""
import os
import subprocess
import tempfile
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import pytest

import src.factor_build as fb
import src.neutralise as nz
import src.portfolio as pf
import src.report as report
from src.load import ff_factors, prices, tone_calls

# Use non-interactive backend for tests
matplotlib.use('Agg')

REQ = [
    Path("data/ff5_daily.parquet"),
    Path("data/stock_prices.parquet"),
    Path("data/tone_dispersion.parquet"),
]


def _have_all_files():
    """Check if all required parquet files are available and not LFS pointers."""
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
# Full Backtest Pipeline Integration Tests
###############################################################################
@pytest.mark.skipif(not _have_all_files(), reason="research parquets missing")
class TestBacktestPipeline:
    """Test the complete backtest pipeline execution."""
    
    def test_full_pipeline_execution(self):
        """Test complete execution of the backtest pipeline."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            outputs_dir = Path(tmp_dir) / "outputs"
            outputs_dir.mkdir()
            
            original_cwd = os.getcwd()
            try:
                os.chdir(tmp_dir)
                
                # Execute the full pipeline
                factor_raw = fb.build_daily_factor()
                
                if factor_raw.empty:
                    pytest.skip("Empty factor - cannot test full pipeline")
                
                # Step 1: Factor neutralization
                factor_neut = nz.neutralise(factor_raw)
                assert isinstance(factor_neut, pd.Series), "Neutralized factor should be Series"
                assert not factor_neut.empty, "Neutralized factor should not be empty"
                
                # Step 2: Portfolio construction with smoothing
                weights = pf.build_weights(factor_neut, smoothing=0.75)
                assert isinstance(weights, pd.DataFrame), "Weights should be DataFrame"
                assert not weights.empty, "Weights should not be empty"
                
                # Step 3: PnL calculation
                pnl = pf.pnl(weights)
                assert isinstance(pnl, pd.Series), "PnL should be Series"
                assert not pnl.empty, "PnL should not be empty"
                
                # Step 4: Turnover calculation
                turnover = pf.calculate_turnover(weights)
                assert isinstance(turnover, pd.Series), "Turnover should be Series"
                
                # Step 5: Enhanced metrics calculation
                metrics = report.calculate_metrics(pnl)
                assert isinstance(metrics, dict), "Metrics should be dictionary"
                assert len(metrics) > 0, "Should have calculated metrics"
                
                # Verify outputs can be saved
                weights.to_parquet(outputs_dir / "weights.parquet")
                factor_neut.to_frame().to_parquet(outputs_dir / "factor_panel.parquet")
                
                assert (outputs_dir / "weights.parquet").exists()
                assert (outputs_dir / "factor_panel.parquet").exists()
                
            finally:
                os.chdir(original_cwd)
    
    def test_enhanced_tearsheet_generation(self):
        """Test generation of enhanced tearsheet plots."""
        # Create synthetic data for testing
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=100, freq='B')
        returns = pd.Series(np.random.normal(0.001, 0.02, len(dates)), index=dates)
        turnover = pd.Series(np.random.uniform(0.01, 0.1, len(dates)), index=dates)
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            save_path = Path(tmp_dir) / "test_tearsheet.png"
            
            # Test enhanced tearsheet generation
            fig = report.plot_enhanced_tearsheet(
                returns=returns,
                turnover=turnover,
                title="Test Portfolio Performance",
                save_path=str(save_path)
            )
            
            assert save_path.exists(), "Tearsheet plot should be saved"
            assert fig is not None, "Should return matplotlib figure"
    
    def test_factor_exposure_pipeline(self):
        """Test factor exposure analysis with real FF factors."""
        if not _have_all_files():
            pytest.skip("Missing data files")
        
        # Get real FF factors
        ff = ff_factors()
        
        # Create synthetic portfolio returns aligned with FF dates
        overlap_dates = ff.index[-100:]  # Use last 100 dates
        np.random.seed(42)
        portfolio_returns = pd.Series(
            np.random.normal(0.0005, 0.015, len(overlap_dates)), 
            index=overlap_dates
        )
        
        # Test factor exposure analysis
        try:
            betas, r2 = report.analyze_factor_exposures(
                portfolio_returns, 
                ff[["mktrf", "smb", "hml", "rmw", "cma"]].loc[overlap_dates],
                rolling_window=30
            )
            
            assert isinstance(betas, pd.DataFrame), "Betas should be DataFrame"
            assert isinstance(r2, pd.Series), "R-squared should be Series"
            assert len(betas) > 0, "Should have beta estimates"
            
        except ImportError as e:
            pytest.skip(f"Skipping factor exposure test due to missing dependency: {e}")
    
    def test_conditional_metrics_pipeline(self):
        """Test conditional performance metrics calculation."""
        if not _have_all_files():
            pytest.skip("Missing data files")
        
        # Get real FF factors for market conditioning
        ff = ff_factors()
        
        # Create synthetic portfolio returns
        overlap_dates = ff.index[-252:]  # Use last year
        np.random.seed(42)
        portfolio_returns = pd.Series(
            np.random.normal(0.0005, 0.015, len(overlap_dates)), 
            index=overlap_dates
        )
        
        # Test conditional metrics
        conditional_metrics = report.calculate_conditional_metrics(
            portfolio_returns,
            ff["mktrf"].loc[overlap_dates]
        )
        
        assert isinstance(conditional_metrics, dict), "Should return dictionary"
        assert "high_regime" in conditional_metrics, "Should have high regime metrics"
        assert "low_regime" in conditional_metrics, "Should have low regime metrics"
        assert "all_periods" in conditional_metrics, "Should have all periods metrics"


###############################################################################
# Performance Regression Tests
###############################################################################
@pytest.mark.skipif(not _have_all_files(), reason="research parquets missing")
class TestPerformanceRegression:
    """Test that performance characteristics remain stable."""
    
    def test_smoothing_reduces_turnover(self):
        """Regression test: smoothing should reduce turnover."""
        factor = fb.build_daily_factor()
        
        if factor.empty:
            pytest.skip("Empty factor - cannot test smoothing regression")
        
        resid = nz.neutralise(factor)
        
        # Test different smoothing levels
        smoothing_levels = [0.0, 0.5, 0.75, 0.9]
        turnovers = []
        
        for smooth in smoothing_levels:
            weights = pf.build_weights(resid, smoothing=smooth)
            turnover = pf.calculate_turnover(weights)
            turnovers.append(turnover.mean())
        
        # Higher smoothing should generally reduce turnover
        # (allowing for some noise in the data)
        for i in range(1, len(turnovers)):
            if turnovers[i] > turnovers[i-1]:
                # Allow small increases due to data noise
                increase_ratio = turnovers[i] / turnovers[i-1]
                assert increase_ratio < 1.1, f"Smoothing={smoothing_levels[i]} increased turnover too much"
    
    def test_market_neutrality_maintained(self):
        """Regression test: portfolios should remain market neutral."""
        factor = fb.build_daily_factor()
        
        if factor.empty:
            pytest.skip("Empty factor - cannot test market neutrality")
        
        resid = nz.neutralise(factor)
        weights = pf.build_weights(resid, smoothing=0.75)
        
        # Check market neutrality (weights sum to zero)
        weight_sums = weights.sum(axis=1)
        max_deviation = weight_sums.abs().max()
        
        assert max_deviation < 1e-8, f"Market neutrality violated: max deviation {max_deviation}"
    
    def test_gross_exposure_control(self):
        """Regression test: gross exposure should be controlled to target."""
        factor = fb.build_daily_factor()
        
        if factor.empty:
            pytest.skip("Empty factor - cannot test gross exposure")
        
        resid = nz.neutralise(factor)
        
        # Test different gross exposure targets
        for target_gross in [0.5, 1.0, 1.5]:
            weights = pf.build_weights(resid, gross=target_gross, smoothing=0.75)
            actual_gross = weights.abs().sum(axis=1)
            
            # Should be close to target (within 1%)
            max_deviation = (actual_gross - target_gross).abs().max()
            assert max_deviation < 0.01, f"Gross exposure control failed for target {target_gross}"


###############################################################################
# Data Consistency Regression Tests  
###############################################################################
@pytest.mark.skipif(not _have_all_files(), reason="research parquets missing")
class TestDataConsistency:
    """Test that data relationships remain consistent."""
    
    def test_factor_symbol_coverage(self):
        """Test that factor has reasonable symbol coverage in price data."""
        factor = fb.build_daily_factor()
        px = prices()
        
        if factor.empty:
            pytest.skip("Empty factor - cannot test symbol coverage")
        
        # Get symbols from factor
        factor_symbols = set(factor.index.get_level_values(1).unique())
        price_symbols = set(px.columns)
        
        # Check overlap
        overlap = factor_symbols.intersection(price_symbols)
        overlap_ratio = len(overlap) / len(factor_symbols)
        
        # Should have good coverage (at least 70%)
        assert overlap_ratio > 0.7, f"Poor symbol coverage: {overlap_ratio:.2%}"
    
    def test_temporal_coverage(self):
        """Test that factor has reasonable temporal coverage."""
        factor = fb.build_daily_factor()
        px = prices()
        
        if factor.empty:
            pytest.skip("Empty factor - cannot test temporal coverage")
        
        # Get date ranges
        factor_dates = factor.index.get_level_values(0).unique()
        price_dates = px.index
        
        # Check overlap
        overlap = factor_dates.intersection(price_dates)
        
        # Should have substantial overlap
        assert len(overlap) > len(factor_dates) * 0.8, "Poor temporal coverage"
        
        # Factor dates should be within price date range
        assert factor_dates.min() >= price_dates.min(), "Factor dates before price data"
        assert factor_dates.max() <= price_dates.max(), "Factor dates after price data"


###############################################################################
# Output File Validation Tests
###############################################################################
@pytest.mark.skipif(not _have_all_files(), reason="research parquets missing")
def test_output_file_integrity():
    """Test that output files can be generated and have correct structure."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        outputs_dir = Path(tmp_dir) / "outputs"
        outputs_dir.mkdir()
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_dir)
            
            # Run pipeline and generate outputs
            factor = fb.build_daily_factor()
            
            if not factor.empty:
                resid = nz.neutralise(factor)
                weights = pf.build_weights(resid, smoothing=0.75)
                pnl = pf.pnl(weights)
                turnover = pf.calculate_turnover(weights)
                
                # Save outputs
                factor_file = outputs_dir / "factor_panel.parquet"
                weights_file = outputs_dir / "weights.parquet"
                
                if isinstance(resid, pd.Series):
                    resid.to_frame().to_parquet(factor_file)
                else:
                    resid.to_parquet(factor_file)
                
                weights.to_parquet(weights_file)
                
                # Verify files exist and can be read
                assert factor_file.exists(), "Factor panel file should exist"
                assert weights_file.exists(), "Weights file should exist"
                
                # Test round-trip
                factor_loaded = pd.read_parquet(factor_file)
                weights_loaded = pd.read_parquet(weights_file)
                
                assert not factor_loaded.empty, "Loaded factor should not be empty"
                assert not weights_loaded.empty, "Loaded weights should not be empty"
                
                # Verify structure is preserved
                pd.testing.assert_frame_equal(weights, weights_loaded)
        
        finally:
            os.chdir(original_cwd)


###############################################################################
# Run Command Integration Test
###############################################################################
@pytest.mark.skipif(not _have_all_files(), reason="research parquets missing")
@pytest.mark.slow
def test_run_backtest_script():
    """Test that run_backtest.py executes without errors."""
    # This is a slow test that actually runs the full script
    with tempfile.TemporaryDirectory() as tmp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_dir)
            
            # Copy the script to temporary directory and run it
            script_path = Path(original_cwd) / "run_backtest.py"
            
            if script_path.exists():
                # Run with timeout to prevent hanging
                result = subprocess.run(
                    ["python", str(script_path)], 
                    capture_output=True, 
                    text=True, 
                    timeout=300,  # 5 minute timeout
                    cwd=original_cwd
                )
                
                # Should complete without error
                assert result.returncode == 0, f"Script failed with error: {result.stderr}"
                
                # Should produce some output
                assert len(result.stdout) > 0, "Script should produce output"
                
        except subprocess.TimeoutExpired:
            pytest.fail("Script execution timed out")
        except FileNotFoundError:
            pytest.skip("run_backtest.py not found")
        finally:
            os.chdir(original_cwd)