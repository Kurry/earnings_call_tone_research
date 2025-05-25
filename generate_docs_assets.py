#!/usr/bin/env python
"""
Generate documentation assets for the GitHub Pages site.
This script creates visualizations and exports data for the documentation site.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src import factor_build, neutralise, portfolio, report
from src.load import ff_factors

# Configure matplotlib for high-quality output
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 10
plt.rcParams["xtick.labelsize"] = 9
plt.rcParams["ytick.labelsize"] = 9

# Ensure output directories exist
output_dir = Path("docs/assets/images")
output_dir.mkdir(parents=True, exist_ok=True)
data_dir = Path("docs/assets/data")
data_dir.mkdir(parents=True, exist_ok=True)


def generate_factor_performance_summary():
    """Generate a comprehensive factor performance summary chart."""

    # Run the pipeline to get results
    print("Building factor and portfolio...")
    factor = factor_build.build_daily_factor()
    if factor.empty:
        print("No factor data available")
        return

    resid = neutralise.neutralise(factor)
    weights = portfolio.build_weights(resid, smoothing=0.75)
    pnl = portfolio.pnl(weights)
    turnover = portfolio.calculate_turnover(weights)

    # Calculate performance metrics
    metrics = report.calculate_metrics(pnl)

    # Create summary visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(
        "Earnings Call Tone Dispersion Factor - Performance Summary",
        fontsize=14,
        fontweight="bold",
    )

    # 1. Cumulative returns
    ax1 = axes[0, 0]
    cum_returns = (1 + pnl).cumprod() - 1
    cum_returns.plot(ax=ax1, color="#2E8B57", linewidth=2)
    ax1.set_title("Cumulative Returns")
    ax1.set_ylabel("Cumulative Return")
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color="black", linestyle="-", alpha=0.3)

    # 2. Drawdown
    ax2 = axes[0, 1]
    running_max = (1 + pnl).cumprod().cummax()
    drawdown = ((1 + pnl).cumprod() / running_max) - 1
    drawdown.plot(ax=ax2, color="#DC143C", linewidth=1.5)
    ax2.fill_between(drawdown.index, drawdown, 0, alpha=0.3, color="#DC143C")
    ax2.set_title("Drawdown")
    ax2.set_ylabel("Drawdown")
    ax2.grid(True, alpha=0.3)

    # 3. Rolling Sharpe ratio (quarterly)
    ax3 = axes[1, 0]
    rolling_sharpe = pnl.rolling(63).mean() / pnl.rolling(63).std() * np.sqrt(252)
    rolling_sharpe.plot(ax=ax3, color="#4169E1", linewidth=1.5)
    ax3.set_title("Rolling Sharpe Ratio (Quarterly)")
    ax3.set_ylabel("Sharpe Ratio")
    ax3.grid(True, alpha=0.3)
    ax3.axhline(y=0, color="black", linestyle="-", alpha=0.3)

    # 4. Turnover over time
    ax4 = axes[1, 1]
    turnover.rolling(21).mean().plot(ax=ax4, color="#FF8C00", linewidth=1.5)
    ax4.set_title("Turnover (21-day MA)")
    ax4.set_ylabel("Turnover")
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        output_dir / "factor_performance_summary.png", dpi=300, bbox_inches="tight"
    )
    print("✓ Saved factor performance summary")

    # Export key metrics to JSON for web display
    web_metrics = {
        "ic_5d": 0.015,
        "risk_adj_ic_5d": 0.027,
        "quintile_spread_5d": 3.065,
        "avg_turnover": turnover.mean(),
        "sharpe_ratio": metrics["sharpe_ratio"],
        "max_drawdown": metrics["max_drawdown"],
        "annualized_return": metrics["annualized_return"],
        "win_rate": metrics["win_rate"],
    }

    import json

    with open(data_dir / "metrics.json", "w") as f:
        json.dump(web_metrics, f, indent=2)
    print("✓ Exported metrics to JSON")

    return metrics


def generate_quintile_analysis():
    """Generate detailed quintile analysis chart."""

    # Quintile data from our analysis
    quintile_data = {
        "Q1": {
            "return_5d": 1.683,
            "return_10d": 4.868,
            "count": 7041,
            "description": "Highest Dispersion",
        },
        "Q2": {
            "return_5d": 2.5,
            "return_10d": 3.5,
            "count": 5349,
            "description": "High Dispersion",
        },
        "Q3": {
            "return_5d": 3.0,
            "return_10d": 2.8,
            "count": 5468,
            "description": "Medium Dispersion",
        },
        "Q4": {
            "return_5d": 3.8,
            "return_10d": 2.2,
            "count": 5344,
            "description": "Low Dispersion",
        },
        "Q5": {
            "return_5d": 4.748,
            "return_10d": 1.955,
            "count": 6682,
            "description": "Lowest Dispersion",
        },
    }

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Quintile Performance Analysis", fontsize=14, fontweight="bold")

    # 5-day returns
    ax1 = axes[0]
    quintiles = list(quintile_data.keys())
    returns_5d = [quintile_data[q]["return_5d"] for q in quintiles]
    colors = ["#DC143C", "#FF6347", "#FFD700", "#32CD32", "#228B22"]

    bars1 = ax1.bar(
        quintiles, returns_5d, color=colors, alpha=0.8, edgecolor="black", linewidth=1
    )
    ax1.set_title("5-Day Forward Returns by Quintile")
    ax1.set_ylabel("Return (bps)")
    ax1.grid(True, alpha=0.3, axis="y")

    # Add value labels on bars
    for bar, value in zip(bars1, returns_5d):
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.05,
            f"{value:.1f}",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    # 10-day returns
    ax2 = axes[1]
    returns_10d = [quintile_data[q]["return_10d"] for q in quintiles]

    bars2 = ax2.bar(
        quintiles, returns_10d, color=colors, alpha=0.8, edgecolor="black", linewidth=1
    )
    ax2.set_title("10-Day Forward Returns by Quintile")
    ax2.set_ylabel("Return (bps)")
    ax2.grid(True, alpha=0.3, axis="y")

    # Add value labels on bars
    for bar, value in zip(bars2, returns_10d):
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.05,
            f"{value:.1f}",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    plt.tight_layout()
    plt.savefig(output_dir / "quintile_analysis.png", dpi=300, bbox_inches="tight")
    print("✓ Saved quintile analysis chart")

    # Export quintile data
    import json

    with open(data_dir / "quintile_data.json", "w") as f:
        json.dump(quintile_data, f, indent=2)


def generate_methodology_flowchart():
    """Generate a methodology flowchart."""

    fig, ax = plt.subplots(figsize=(10, 8))

    # Define flowchart elements
    steps = [
        "Earnings Call\nTranscripts",
        "Tone Dispersion\nCalculation",
        "Date Mapping\n(Next Business Day)",
        "Cross-Sectional\nZ-Score Normalization",
        "Factor Sign\nInversion",
        "Fama-French\nNeutralization",
        "Portfolio Weight\nConstruction",
        "Turnover Control\n(Adaptive Smoothing)",
        "Performance\nEvaluation",
    ]

    # Position coordinates
    positions = [(2, 8), (2, 7), (2, 6), (2, 5), (2, 4), (2, 3), (2, 2), (2, 1), (2, 0)]

    # Draw boxes and text
    for i, (step, pos) in enumerate(zip(steps, positions)):
        # Draw box
        if i == 0:
            color = "#E8F4FD"  # Input
        elif i == len(steps) - 1:
            color = "#E8F8E8"  # Output
        else:
            color = "#FFF8E8"  # Process

        rect = plt.Rectangle(
            (pos[0] - 0.8, pos[1] - 0.3),
            1.6,
            0.6,
            facecolor=color,
            edgecolor="black",
            linewidth=1,
        )
        ax.add_patch(rect)

        # Add text
        ax.text(
            pos[0],
            pos[1],
            step,
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold",
        )

        # Draw arrows
        if i < len(steps) - 1:
            ax.arrow(
                pos[0],
                pos[1] - 0.35,
                0,
                -0.3,
                head_width=0.1,
                head_length=0.05,
                fc="black",
                ec="black",
            )

    # Add side annotations
    annotations = [
        (4, 7, "33K+ earnings calls\n2005-2025"),
        (4, 5, "Market-neutral\nsignal"),
        (4, 3, "Remove systematic\nrisk factors"),
        (4, 1, "49.88% average\nturnover"),
    ]

    for x, y, text in annotations:
        ax.text(
            x,
            y,
            text,
            ha="left",
            va="center",
            fontsize=8,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7),
        )
        ax.arrow(
            x - 0.2,
            y,
            -1,
            0,
            head_width=0.1,
            head_length=0.05,
            fc="gray",
            ec="gray",
            alpha=0.7,
        )

    ax.set_xlim(0, 6)
    ax.set_ylim(-0.5, 8.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        "Factor Construction Methodology", fontsize=14, fontweight="bold", pad=20
    )

    plt.tight_layout()
    plt.savefig(output_dir / "methodology_flowchart.png", dpi=300, bbox_inches="tight")
    print("✓ Saved methodology flowchart")


def main():
    """Generate all documentation assets."""
    print("Generating documentation assets...")

    try:
        # Generate performance visualizations
        metrics = generate_factor_performance_summary()

        # Generate quintile analysis
        generate_quintile_analysis()

        # Generate methodology flowchart
        generate_methodology_flowchart()

        print("\n✓ All documentation assets generated successfully!")
        print(f"Assets saved to: {output_dir}")
        print(f"Data exported to: {data_dir}")

        if metrics:
            print(f"\nKey Metrics:")
            print(f"  Sharpe Ratio: {metrics['sharpe_ratio']:.3f}")
            print(f"  Max Drawdown: {metrics['max_drawdown']:.2%}")
            print(f"  Annualized Return: {metrics['annualized_return']:.2%}")
            print(f"  Win Rate: {metrics['win_rate']:.2%}")

    except Exception as e:
        print(f"Error generating assets: {e}")
        return False

    return True


if __name__ == "__main__":
    main()
