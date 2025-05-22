#!/usr/bin/env python
# Improved backtest script using portfolio smoothing
import time

import pandas as pd
import portfolio_improved as portfolio

from src import factor_build, neutralise, report

# Set smoothing parameter
SMOOTHING = 0.75  # 0.75 provides good balance of turnover reduction and performance

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
    w.to_parquet("outputs/weights_improved.parquet")
else:  # single-date case → Series
    w.to_frame().to_parquet("outputs/weights_improved.parquet")

print("[4/4] Computing PnL…")
start = time.time()
pnl = portfolio.pnl(w)
ir = pnl.mean() / pnl.std() * 252**0.5
print(f"    IR(5-day): {ir:.3f} in {time.time()-start:.1f}s")

print("Generating tear-sheet…")
report.make_tearsheet(factor_neut, out="outputs/tearsheet_improved.html")

import matplotlib.dates as mdates

# Create turnover plot
import matplotlib.pyplot as plt

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
plt.savefig("outputs/turnover_improved.png")

print("✓ Improved backtest complete")
print(f"  IR(5-day): {ir:.3f}")
print(f"  Avg Turnover: {avg_turnover:.4f}")
print(f"  Sharpe Ratio (IR/(1+turnover)): {ir/(1+avg_turnover):.4f}")
