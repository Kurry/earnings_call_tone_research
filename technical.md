---
layout: default
title: "Technical Documentation"
permalink: /technical/
---

# Technical Documentation

## Code Architecture

The earnings call tone research framework is built with modularity, testability, and reproducibility in mind. This page provides technical details for researchers and practitioners who want to understand or extend the implementation.

## Project Structure

```
earnings_call_tone_research/
├── data/                          # Raw data files
│   ├── ff5_daily.parquet         # Fama-French 5 factors
│   ├── stock_prices.parquet      # Daily stock prices
│   └── tone_dispersion.parquet   # Earnings call data
├── src/                          # Core source code
│   ├── __init__.py
│   ├── factor_build.py           # Factor construction
│   ├── load.py                   # Data loading utilities
│   ├── neutralise.py             # Risk factor neutralization
│   ├── portfolio.py              # Portfolio construction
│   └── report.py                 # Performance analysis
├── tests/                        # Comprehensive test suite
│   ├── test_integration.py       # End-to-end testing
│   ├── test_pipeline.py          # Unit tests
│   └── test_backtest_integration.py # Backtest validation
├── outputs/                      # Generated results
├── docs/                         # GitHub Pages documentation
├── run_backtest.py              # Main execution script
└── requirements.txt             # Python dependencies
```

## Core Modules

### 1. Data Loading (`src/load.py`)

**Purpose**: Centralized data access with validation and preprocessing

```python
def prices() -> pd.DataFrame:
    """Load and pivot stock prices to wide format"""
    
def ff_factors() -> pd.DataFrame:
    """Load Fama-French factor returns"""
    
def tone_calls() -> pd.DataFrame:
    """Load earnings call tone dispersion data"""
```

**Features**:
- Git LFS detection and error handling
- Automatic data type conversion
- Index standardization
- Missing value validation

### 2. Factor Construction (`src/factor_build.py`)

**Purpose**: Transform raw tone data into tradeable factor signals

```python
def build_daily_factor() -> pd.Series:
    """
    Convert quarterly earnings calls to daily factor signals
    
    Steps:
    1. Parse call timestamps and map to trading dates
    2. Aggregate multiple calls per symbol-date
    3. Apply economic sign convention (negate dispersion)
    4. Cross-sectional normalization (z-score)
    
    Returns:
    --------
    pd.Series: Factor values indexed by (date, symbol)
    """
```

**Key Implementation Details**:
- **Date Mapping**: `call_date + BDay(1)` for next business day signal
- **Factor Inversion**: `-tone_dispersion` for correct economic interpretation
- **Z-Score Normalization**: Market-neutral factor construction
- **Missing Data Handling**: Robust aggregation and filtering

### 3. Risk Factor Neutralization (`src/neutralise.py`)

**Purpose**: Remove systematic risk exposures from factor signals

```python
def neutralise(factor: pd.Series) -> pd.Series:
    """
    Neutralize factor against Fama-French factors
    
    Regression: factor_t = α + β₁*MktRF + β₂*SMB + β₃*HML + β₄*RMW + β₅*CMA + ε_t
    
    Returns: ε_t (residual factor)
    """
```

**Statistical Approach**:
- **Daily Regression**: Cross-sectional neutralization each day
- **Robust Estimation**: Handles missing values and outliers
- **Factor Coverage**: Market, size, value, profitability, investment
- **Residual Extraction**: Pure alpha signal extraction

### 4. Portfolio Construction (`src/portfolio.py`)

**Purpose**: Convert factor signals into implementable portfolio weights

#### Core Functions

```python
def build_weights(signal: pd.Series, gross: float = 1.0, 
                 smoothing: float = 0.75) -> pd.DataFrame:
    """
    Advanced portfolio construction with turnover control
    
    Features:
    - Nonlinear signal transformation
    - Adaptive smoothing for turnover reduction
    - Market neutrality enforcement
    - Gross exposure control
    """

def calculate_turnover(weights: pd.DataFrame) -> pd.Series:
    """Calculate daily portfolio turnover"""

def pnl(weights: pd.DataFrame, horizon: int = 5) -> pd.Series:
    """Calculate portfolio P&L from weights and forward returns"""
```

#### Advanced Features

**Nonlinear Signal Enhancement**:
```python
# Enhance signal distinction in tails
enhanced_signal = np.sign(centered_ranks) * np.abs(centered_ranks) ** 0.75
```

**Adaptive Smoothing Algorithm**:
```python
# Reduce smoothing for significant signal changes
signal_change = abs(target_weights - previous_weights)
significant_threshold = signal_change.quantile(0.75)
adaptive_smoothing = smoothing - 0.25 if significant_change else smoothing
```

**Constraint Enforcement**:
- Market Neutrality: `sum(weights) = 0`
- Gross Exposure: `sum(|weights|) = target_gross`
- Proportional Adjustment: Maintain relative weight relationships

### 5. Performance Analysis (`src/report.py`)

**Purpose**: Comprehensive factor and portfolio analysis

#### Alphalens Integration

```python
def make_tearsheet(factor: pd.Series, out: str = "outputs/tearsheet.png"):
    """
    Generate Alphalens tearsheet with custom forward return calculation
    
    Custom Features:
    - Patched forward return computation for irregular frequencies
    - Silent execution for automated workflows
    - Comprehensive factor analysis
    """
```

#### Enhanced Metrics

```python
def calculate_metrics(returns: pd.Series) -> Dict[str, float]:
    """
    Calculate advanced performance metrics:
    - Sharpe, Sortino, Calmar ratios
    - Maximum drawdown analysis
    - Win rate and profit ratio
    - Monthly consistency measures
    """

def analyze_factor_exposures(returns: pd.Series, 
                           factor_returns: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Rolling factor exposure analysis using sklearn regression"""

def calculate_conditional_metrics(returns: pd.Series, 
                                condition_series: pd.Series) -> Dict[str, Dict[str, float]]:
    """Performance analysis conditional on market regimes"""
```

## Testing Framework

### 1. Integration Tests (`tests/test_integration.py`)

**Comprehensive End-to-End Validation**:

```python
class TestParquetDataIntegrity:
    """Validate data file structure and quality"""
    
class TestDataAlignment:
    """Test cross-file date and symbol consistency"""
    
class TestEnhancedPipeline:
    """Validate enhanced features like smoothing and metrics"""
    
class TestDataLoading:
    """Test robust data loading and transformation"""
```

**Coverage Areas**:
- ✅ Parquet file validation and LFS detection
- ✅ Data type and value range checking
- ✅ Cross-file date and symbol alignment
- ✅ Factor construction validation
- ✅ Portfolio constraint verification
- ✅ Performance metric calculation
- ✅ Enhanced feature testing (smoothing, advanced metrics)

### 2. Backtest Integration Tests (`tests/test_backtest_integration.py`)

**Full Pipeline Validation**:

```python
class TestBacktestPipeline:
    """Test complete backtest execution"""
    
class TestPerformanceRegression:
    """Ensure performance characteristics remain stable"""
    
class TestDataConsistency:
    """Validate data relationships over time"""
```

**Regression Testing**:
- Factor sign and performance consistency
- Turnover reduction with smoothing
- Market neutrality maintenance
- Gross exposure control
- Symbol and temporal coverage

### 3. Performance Testing

**Benchmarks and Timing**:
- Factor construction: ~1.5s for 32K observations
- Portfolio optimization: ~40s for 2.6K dates × 684 symbols
- Performance analysis: ~2s for 6K PnL observations
- Memory usage: <2GB for full dataset

## Data Pipeline

### Input Data Requirements

#### Stock Prices (`stock_prices.parquet`)
```python
# Required columns
['date', 'symbol', 'adjClose', 'open', 'high', 'low', 'close', 'volume']

# Expected format
- Long format: One row per date-symbol
- Date range: 2000-2024 (6,290 days)
- Symbols: 677 unique tickers
- Missing data: Handled via forward-fill and dropna
```

#### Earnings Calls (`tone_dispersion.parquet`)
```python
# Required columns  
['symbol', 'date', 'tone_dispersion', 'year', 'quarter', 'company_id', 'call_key']

# Expected format
- Quarterly frequency: One row per earnings call
- Date range: 2005-2025 (33,362 calls)  
- Tone dispersion: Float values [0, 1] range
- Multiple calls per symbol-quarter: Aggregated by mean
```

#### Fama-French Factors (`ff5_daily.parquet`)
```python
# Required columns
['mktrf', 'smb', 'hml', 'rmw', 'cma', 'umd', 'rf']

# Expected format
- Daily frequency with DatetimeIndex
- Date range: 1963-2024 (business days only)
- Values: Daily returns in decimal format
- Used for: Factor neutralization and performance attribution
```

### Output Generation

#### Factor Panel (`outputs/factor_panel.parquet`)
- Neutralized factor values by date and symbol
- Used for: Portfolio construction and analysis

#### Portfolio Weights (`outputs/weights.parquet`)
- Daily portfolio weights with smoothing applied
- Constraints: Market neutral, gross exposure = 1.0

#### Visualizations
- `tearsheet.png`: Alphalens factor analysis
- `turnover.png`: Portfolio turnover time series
- `enhanced_tearsheet.png`: Advanced performance metrics

## Deployment and Execution

### Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Data requirements (with Git LFS)
git lfs install
git lfs pull
```

### Execution Workflow

```bash
# Run full backtest
python run_backtest.py

# Run specific tests
pytest tests/test_integration.py -v
pytest tests/test_backtest_integration.py::TestBacktestPipeline -v

# Generate documentation
cd docs/
jekyll serve  # For local development
```

### Configuration Options

**Smoothing Parameters**:
```python
SMOOTHING = 0.75  # 75% weight retention
# Range: [0.0, 1.0]
# 0.0 = No smoothing (100% turnover)
# 1.0 = Maximum smoothing (no turnover)
```

**Portfolio Parameters**:
```python
GROSS_EXPOSURE = 1.0  # 100% gross exposure
HORIZON = 5          # 5-day forward returns
```

## Performance Optimizations

### Computational Efficiency

1. **Vectorized Operations**: Pandas/NumPy for all calculations
2. **Memory Management**: Chunked processing for large datasets
3. **Caching**: Intermediate results stored as parquet files
4. **Parallel Processing**: Multi-core support for rolling calculations

### Scalability Considerations

- **Data Size**: Current implementation handles ~30K factor observations
- **Symbol Universe**: Tested with 677 symbols, scalable to thousands
- **Time Series**: 25-year daily frequency with no performance issues
- **Memory Footprint**: <2GB RAM for full dataset

## Error Handling and Logging

### Data Validation
- Missing file detection with informative error messages
- Git LFS pointer file detection and user guidance
- Data type validation and automatic conversion
- Date range and overlap validation

### Robust Execution
- Graceful handling of missing data points
- Fallback mechanisms for edge cases
- Comprehensive warning and error logging
- Automatic constraint enforcement

---

## Development Guidelines

### Code Standards
- **Type Hints**: All functions have type annotations
- **Docstrings**: Comprehensive documentation for all modules
- **Testing**: >90% test coverage for core functionality
- **Formatting**: Black code formatting with line length 88

### Contributing
1. Fork the repository
2. Create feature branch
3. Add comprehensive tests
4. Update documentation
5. Submit pull request with clear description

### Research Extensions
- Alternative tone metrics (sentiment, uncertainty, etc.)
- Different smoothing algorithms
- Sector-neutral implementations
- International market applications
- Real-time signal generation

---

*For questions about the technical implementation, please refer to the code documentation or submit an issue in the GitHub repository.*