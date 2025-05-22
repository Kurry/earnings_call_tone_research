import time

import matplotlib.pyplot as plt
import pandas as pd

from src import factor_build, neutralise, portfolio, report

# Set smoothing parameter - 0.75 provides good balance of turnover reduction and performance
SMOOTHING = 0.75

print("[1/4] Building raw factor…")
start = time.time()
factor_raw = factor_build.build_daily_factor()
print(f"    Raw factor: {len(factor_raw)} rows in {time.time()-start:.1f}s")

print("[2/4] Neutralising factor…")
start = time.time()
factor_neut = neutralise.neutralise(factor_raw)
print(f"    Neutralised factor: {len(factor_neut)} rows in {time.time()-start:.1f}s")
if isinstance(factor_neut, pd.Series):
    factor_neut.to_frame().to_parquet("outputs/factor_panel.parquet")
else:
    factor_neut.to_parquet("outputs/factor_panel.parquet")
print("    Saved outputs/factor_panel.parquet")

# 2) weights & pnl
print(f"[3/4] Building weights with smoothing={SMOOTHING}…")
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

print("[4/4] Computing PnL…")
start = time.time()
pnl = portfolio.pnl(w)
ir = pnl.mean() / pnl.std() * 252**0.5
print(f"    IR(5-day): {ir:.3f} in {time.time()-start:.1f}s")
print(f"    Sharpe Ratio (IR/(1+turnover)): {ir/(1+avg_turnover):.4f}")

print("Generating tear-sheet…")
report.make_tearsheet(factor_neut)

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
print("✓ Turnover plot saved to outputs/turnover.png")
