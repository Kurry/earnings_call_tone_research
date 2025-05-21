import pandas as pd

from src import factor_build, neutralise, portfolio, report

# 1) build & save factor
factor_raw = factor_build.build_daily_factor()
factor_neut = neutralise.neutralise(factor_raw)
factor_neut.to_parquet("outputs/factor_panel.parquet")

# 2) weights & pnl
w = portfolio.build_weights(factor_neut)

if isinstance(w, pd.DataFrame):
    w.to_parquet("outputs/weights.parquet")
else:  # single-date case → Series
    w.to_frame().to_parquet("outputs/weights.parquet")

pnl = portfolio.pnl(w)
print("IR(5-day):", pnl.mean() / pnl.std() * 252**0.5)

# 3) Alphalens tear-sheet
report.make_tearsheet(factor_neut)
print("✓ tear-sheet saved to outputs/tearsheet.html")
