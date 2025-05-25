import os
import time

import matplotlib.pyplot as plt
import pandas as pd

from src import factor_build, neutralise, portfolio, report
from src.load import ff_factors

# Create outputs directory if it doesn't exist
os.makedirs("outputs", exist_ok=True)

# Set smoothing parameter - 0.75 provides good balance of turnover reduction and performance
SMOOTHING = 0.75

print("[1/5] Building raw factor…")
start = time.time()
factor_raw = factor_build.build_daily_factor()
print(f"    Raw factor: {len(factor_raw)} rows in {time.time()-start:.1f}s")

print("[2/5] Neutralising factor…")
start = time.time()
factor_neut = neutralise.neutralise(factor_raw)
print(f"    Neutralised factor: {len(factor_neut)} rows in {time.time()-start:.1f}s")
if isinstance(factor_neut, pd.Series):
    factor_neut.to_frame().to_parquet("outputs/factor_panel.parquet")
else:
    factor_neut.to_parquet("outputs/factor_panel.parquet")
print("    Saved outputs/factor_panel.parquet")

# 3) weights & pnl
print(f"[3/5] Building weights with smoothing={SMOOTHING}…")
start = time.time()
w = portfolio.build_weights(factor_neut, smoothing=SMOOTHING)
print(f"    Weights matrix: {w.shape} in {time.time()-start:.1f}s")

# Calculate turnover statistics
turnover = portfolio.calculate_turnover(w)
avg_turnover = turnover.mean()
max_turnover = turnover.max()
print(f"    Turnover: avg={avg_turnover:.4f}, max={max_turnover:.4f}")

if isinstance(w, pd.DataFrame):
    w.to_parquet("outputs/weights.parquet")
else:  # single-date case → Series
    w.to_frame().to_parquet("outputs/weights.parquet")

print("[4/5] Computing PnL…")
start = time.time()
pnl = portfolio.pnl(w)
ir = pnl.mean() / pnl.std() * 252**0.5
print(f"    IR(5-day): {ir:.3f} in {time.time()-start:.1f}s")
print(f"    Sharpe Ratio (IR/(1+turnover)): {ir/(1+avg_turnover):.4f}")

print("[5/5] Generating enhanced visualizations…")
# Standard tearsheet
report.make_tearsheet(factor_neut)

# Enhanced tearsheet using our improved metrics
try:
    # Get Fama-French factors for additional analysis
    ff = ff_factors()
    # Align dates between PnL and FF factors
    common_dates = pnl.index.intersection(ff.index)
    ff_returns = ff.loc[common_dates].copy()
    pnl_aligned = pnl.loc[common_dates].copy()

    # Create enhanced tearsheet
    report.plot_enhanced_tearsheet(
        returns=pnl_aligned,
        turnover=turnover.loc[common_dates] if len(common_dates) > 0 else turnover,
        title="Tone-Dispersion Factor Performance",
        save_path="outputs/enhanced_tearsheet.png",
    )
    print("✓ Enhanced tearsheet saved to outputs/enhanced_tearsheet.png")

    # Calculate and display enhanced metrics
    performance_metrics = report.calculate_metrics(pnl_aligned)
    print("\nEnhanced Performance Metrics:")
    for metric, value in performance_metrics.items():
        if "ratio" in metric:
            print(f"  {metric.replace('_', ' ').title()}: {value:.4f}")
        else:
            print(f"  {metric.replace('_', ' ').title()}: {value:.4%}")

    # Analyze factor exposures
    try:
        if len(pnl_aligned) > 60:  # Need sufficient data for rolling analysis
            betas, r2 = report.analyze_factor_exposures(
                returns=pnl_aligned,
                factor_returns=ff_returns[["mktrf", "smb", "hml", "rmw", "cma"]],
                rolling_window=min(
                    60, len(pnl_aligned) // 2
                ),  # Use half the data or 60 days, whichever is smaller
            )

            # Plot factor exposures
            plt.figure(figsize=(12, 8))
            betas.plot(subplots=True, layout=(3, 2), figsize=(12, 10), grid=True)
            plt.suptitle("Rolling Factor Exposures", fontsize=16)
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            plt.savefig("outputs/factor_exposures.png", dpi=300, bbox_inches="tight")
            print("✓ Factor exposures plot saved to outputs/factor_exposures.png")
        else:
            print("Insufficient data for factor exposure analysis")

        # Calculate conditional performance based on market returns
        if len(pnl_aligned) > 20:  # Need sufficient data for conditioning
            market_conditional = report.calculate_conditional_metrics(
                returns=pnl_aligned, condition_series=ff_returns["mktrf"]
            )

            print("\nConditional Performance:")
            print("  In Up Markets:")
            print(
                f"    Sharpe Ratio: {market_conditional['high_regime']['sharpe_ratio']:.4f}"
            )
            print(f"    Win Rate: {market_conditional['high_regime']['win_rate']:.4%}")
            print("  In Down Markets:")
            print(
                f"    Sharpe Ratio: {market_conditional['low_regime']['sharpe_ratio']:.4f}"
            )
            print(f"    Win Rate: {market_conditional['low_regime']['win_rate']:.4%}")
        else:
            print("Insufficient data for conditional performance analysis")
    except Exception as e:
        print(f"Note: Skipping factor exposure analysis due to: {e}")

except Exception as e:
    print(f"Note: Basic tearsheet generated. Enhanced metrics error: {e}")

# Create turnover plot
plt.figure(figsize=(12, 6))
turnover.iloc[-100:].plot()  # Last 100 days for clarity
plt.axhline(
    y=avg_turnover, color="r", linestyle="--", label=f"Average: {avg_turnover:.4f}"
)
plt.title(f"Daily Turnover with Smoothing={SMOOTHING}")
plt.ylabel("Turnover")
plt.xlabel("Date")
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig("outputs/turnover.png")
print("✓ Turnover plot saved to outputs/turnover.png")

print("\n✓ Backtest complete")
print(f"  IR(5-day): {ir:.3f}")
print(f"  Avg Turnover: {avg_turnover:.4f}")
print(f"  Sharpe Ratio (IR/(1+turnover)): {ir/(1+avg_turnover):.4f}")
