---
layout: default
title: "Methodology"
permalink: /methodology/
---

# Methodology

## Overview

Our earnings call tone dispersion factor follows a rigorous quantitative methodology that combines natural language processing with modern portfolio theory. This page details the step-by-step process from raw data to final portfolio construction.

## Data Processing Pipeline

### 1. Earnings Call Data Collection

**Source**: Quarterly earnings call transcripts from 2005-2025
- **Coverage**: 33,362 earnings calls across 677 unique companies
- **Format**: Structured data with company identifiers, dates, and tone metrics
- **Quality Control**: Automated data validation and missing value handling

```python
# Data structure
calls = {
    'symbol': str,          # Stock ticker
    'company_id': int,      # Unique company identifier  
    'year': int,           # Calendar year
    'quarter': int,        # Quarter (1-4)
    'date': datetime,      # Earnings call timestamp
    'tone_dispersion': float,  # Core signal metric
    'call_key': str        # Unique call identifier
}
```

### 2. Tone Dispersion Calculation

**Definition**: Tone dispersion measures the variability and uncertainty in earnings call language, capturing:

- **Sentiment Inconsistency**: Variation in positive/negative language across call segments
- **Uncertainty Indicators**: Frequency of uncertainty terms and hedging language
- **Management Disagreement**: Differences between prepared remarks and Q&A responses
- **Analyst Sentiment**: Variation in analyst question tone and management responses

**Mathematical Formulation**:
```
tone_dispersion = σ(sentiment_scores) + λ * uncertainty_factor
```

Where:
- `σ(sentiment_scores)`: Standard deviation of sentiment across call segments
- `uncertainty_factor`: Normalized count of uncertainty/hedging terms
- `λ`: Calibration parameter for uncertainty weighting

### 3. Signal Processing and Factor Construction

#### Date Mapping
```python
# Map earnings calls to trading dates
trade_date = earnings_call_date + BusinessDay(1)
```

**Rationale**: Earnings calls typically occur after market close, so the signal becomes actionable on the next business day.

#### Cross-Sectional Normalization
```python
# Z-score normalize within each date
factor = (tone_dispersion - daily_mean) / daily_std
```

**Purpose**: Ensures factor is market-neutral and comparable across time periods.

#### Factor Sign Convention
```python
# Invert factor for economic intuition
factor = -tone_dispersion_zscore
```

**Logic**: 
- **High tone dispersion** = High uncertainty = Poor performance = **Negative signal**
- **Low tone dispersion** = High certainty = Good performance = **Positive signal**

## Portfolio Construction

### 1. Weight Calculation

**Base Weights**: Ranks converted to centered weights in [-1, 1] range
```python
ranks = factor.groupby(date).rank(method='average')
n_assets = factor.groupby(date).count()
centered_ranks = (2 * ranks - n_assets - 1) / n_assets
```

**Nonlinear Transformation**: Enhance signal distinction
```python
# Reduce noise in middle quintiles
enhanced_signal = sign(centered_ranks) * |centered_ranks|^0.75
```

**Gross Exposure Scaling**:
```python
target_gross = 1.0  # 100% gross exposure
weights = enhanced_signal / sum(|enhanced_signal|) * target_gross
```

### 2. Turnover Control with Adaptive Smoothing

**Standard Smoothing**:
```python
new_weights = (1 - α) * target_weights + α * previous_weights
```

**Adaptive Enhancement**: Reduce smoothing for significant signal changes
```python
signal_change = |target_weights - previous_weights|
significant_threshold = quantile(signal_change, 0.75)

adaptive_α = α - 0.25 if signal_change > significant_threshold else α
blended_weights = (1 - adaptive_α) * target + adaptive_α * previous
```

**Constraints Enforcement**:
1. **Market Neutrality**: `sum(weights) = 0`
2. **Gross Exposure**: `sum(|weights|) = 1.0`
3. **Position Limits**: Individual position caps (if applicable)

### 3. Rebalancing and Execution

**Frequency**: Daily rebalancing based on new earnings call data
**Implementation**: 
- Portfolio weights calculated at market close
- Trades executed at market open next day
- Transaction cost modeling (optional)

## Risk Management

### 1. Factor Neutralization

**Fama-French Factor Exposure Control**:
```python
# Neutralize against market, size, value, profitability, investment factors
neutralized_factor = residual(factor ~ mktrf + smb + hml + rmw + cma)
```

### 2. Turnover Management

**Smoothing Parameter**: α = 0.75 (75% weight retention)
- **Result**: Average turnover of 49.88% vs 100% without smoothing
- **Benefit**: Reduced transaction costs while maintaining signal integrity

### 3. Position Sizing

**Equal Risk Contribution**: Positions sized by inverse volatility (optional)
**Sector Neutrality**: Optional sector constraints to reduce style bias
**Liquidity Filters**: Exclude low-volume stocks to ensure executability

## Performance Attribution

### 1. Factor Timing

**Signal Decay Analysis**: Factor performance over different holding periods
- **5-day returns**: Primary evaluation period
- **10-day returns**: Extended holding period analysis
- **Monthly analysis**: Longer-term factor persistence

### 2. Cross-Sectional Analysis

**Quintile Performance**:
- **Q1 (Bottom 20%)**: Highest tone dispersion (uncertainty)
- **Q5 (Top 20%)**: Lowest tone dispersion (certainty)
- **Spread Analysis**: Q5 - Q1 performance differential

### 3. Risk-Adjusted Metrics

**Information Coefficient**: Correlation between factor and forward returns
**Risk-Adjusted IC**: IC scaled by factor volatility
**Sharpe Ratio**: Return/risk ratio with turnover adjustment

## Validation and Testing

### 1. Statistical Significance

**t-statistics**: Test IC significance across time periods
**Bootstrap Analysis**: Confidence intervals for performance metrics
**Regime Analysis**: Performance in different market conditions

### 2. Robustness Checks

**Sub-period Analysis**: Performance consistency across time
**Sector Analysis**: Factor performance within industries
**Size and Style Controls**: Performance after risk factor neutralization

### 3. Implementation Validation

**Comprehensive Test Suite**: 
- Data integrity checks
- Factor construction validation
- Portfolio constraint verification
- Performance attribution accuracy

---

## Next Steps

- **[View Results →](results.md)**: See detailed performance analysis and visualizations
- **[Technical Details →](technical.md)**: Explore code implementation and testing framework