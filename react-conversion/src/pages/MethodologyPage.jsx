import React from 'react';
import CodeBlock from '../components/CodeBlock'; // Assuming CodeBlock is ready

const MethodologyPage = () => {
  return (
    <div className="space-y-12">
      <header className="text-center py-8">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-800">Methodology</h1>
      </header>

      <section aria-labelledby="overview-title">
        <h2 id="overview-title" className="text-3xl font-semibold text-gray-700 mb-4">Overview</h2>
        <p className="text-lg text-gray-600 leading-relaxed">
          Our earnings call tone dispersion factor follows a rigorous quantitative methodology that combines natural language processing with modern portfolio theory. This page details the step-by-step process from raw data to final portfolio construction.
        </p>
      </section>

      <section aria-labelledby="data-processing-title">
        <h2 id="data-processing-title" className="text-3xl font-semibold text-gray-700 mb-6">Data Processing Pipeline</h2>
        <div className="space-y-8">
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h3 className="text-2xl font-medium text-gray-700 mb-3">1. Earnings Call Data Collection</h3>
            <p className="text-lg text-gray-600 mb-2"><strong>Source</strong>: Quarterly earnings call transcripts from 2005-2025</p>
            <ul className="list-disc list-inside text-lg text-gray-600 leading-relaxed space-y-1 mb-4">
              <li><strong>Coverage</strong>: 33,362 earnings calls across 677 unique companies</li>
              <li><strong>Format</strong>: Structured data with company identifiers, dates, and tone metrics</li>
              <li><strong>Quality Control</strong>: Automated data validation and missing value handling</li>
            </ul>
            <CodeBlock language="python">
{`calls = {
    'symbol': str,          # Stock ticker
    'company_id': int,      # Unique company identifier  
    'year': int,           # Calendar year
    'quarter': int,        # Quarter (1-4)
    'date': datetime,      # Earnings call timestamp
    'tone_dispersion': float,  # Core signal metric
    'call_key': str        # Unique call identifier
}`}
            </CodeBlock>
          </div>

          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h3 className="text-2xl font-medium text-gray-700 mb-3">2. Tone Dispersion Calculation</h3>
            <p className="text-lg text-gray-600 mb-2"><strong>Definition</strong>: Tone dispersion measures the variability and uncertainty in earnings call language, capturing:</p>
            <ul className="list-disc list-inside text-lg text-gray-600 leading-relaxed space-y-1 mb-4">
              <li><strong>Sentiment Inconsistency</strong>: Variation in positive/negative language across call segments</li>
              <li><strong>Uncertainty Indicators</strong>: Frequency of uncertainty terms and hedging language</li>
              <li><strong>Management Disagreement</strong>: Differences between prepared remarks and Q&A responses</li>
              <li><strong>Analyst Sentiment</strong>: Variation in analyst question tone and management responses</li>
            </ul>
            <p className="text-lg text-gray-600 font-semibold mb-2">Mathematical Formulation:</p>
            <div className="p-3 bg-white border border-gray-300 rounded-md text-center">
              <code className="text-lg text-gray-700">tone_dispersion = σ(sentiment_scores) + λ * uncertainty_factor</code>
            </div>
            <p className="text-lg text-gray-600 mt-3">Where:</p>
            <ul className="list-disc list-inside text-lg text-gray-600 leading-relaxed space-y-1">
              <li><code className="bg-gray-200 p-1 rounded">σ(sentiment_scores)</code>: Standard deviation of sentiment across call segments</li>
              <li><code className="bg-gray-200 p-1 rounded">uncertainty_factor</code>: Normalized count of uncertainty/hedging terms</li>
              <li><code className="bg-gray-200 p-1 rounded">λ</code>: Calibration parameter for uncertainty weighting</li>
            </ul>
          </div>
        </div>
      </section>

      <section aria-labelledby="signal-processing-title">
        <h2 id="signal-processing-title" className="text-3xl font-semibold text-gray-700 mb-6">Signal Processing and Factor Construction</h2>
        <div className="space-y-8">
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h4 className="text-xl font-medium text-gray-700 mb-2">Date Mapping</h4>
            <CodeBlock language="python">
{`# Map earnings calls to trading dates
trade_date = earnings_call_date + BusinessDay(1)`}
            </CodeBlock>
            <p className="text-lg text-gray-600 mt-2"><strong>Rationale</strong>: Earnings calls typically occur after market close, so the signal becomes actionable on the next business day.</p>
          </div>
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h4 className="text-xl font-medium text-gray-700 mb-2">Cross-Sectional Normalization</h4>
            <CodeBlock language="python">
{`# Z-score normalize within each date
factor = (tone_dispersion - daily_mean) / daily_std`}
            </CodeBlock>
            <p className="text-lg text-gray-600 mt-2"><strong>Purpose</strong>: Ensures factor is market-neutral and comparable across time periods.</p>
          </div>
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h4 className="text-xl font-medium text-gray-700 mb-2">Factor Sign Convention</h4>
            <CodeBlock language="python">
{`# Invert factor for economic intuition
factor = -tone_dispersion_zscore`}
            </CodeBlock>
            <p className="text-lg text-gray-600 mt-2"><strong>Logic</strong>:</p>
            <ul className="list-disc list-inside text-lg text-gray-600 leading-relaxed">
              <li><strong>High tone dispersion</strong> = High uncertainty = Poor performance = <strong>Negative signal</strong></li>
              <li><strong>Low tone dispersion</strong> = High certainty = Good performance = <strong>Positive signal</strong></li>
            </ul>
          </div>
        </div>
      </section>

      <section aria-labelledby="portfolio-construction-title">
        <h2 id="portfolio-construction-title" className="text-3xl font-semibold text-gray-700 mb-6">Portfolio Construction</h2>
        <div className="space-y-8">
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h3 className="text-2xl font-medium text-gray-700 mb-3">1. Weight Calculation</h3>
            <p className="text-lg text-gray-600 mb-2"><strong>Base Weights</strong>: Ranks converted to centered weights in [-1, 1] range</p>
            <CodeBlock language="python">
{`ranks = factor.groupby(date).rank(method='average')
n_assets = factor.groupby(date).count()
centered_ranks = (2 * ranks - n_assets - 1) / n_assets`}
            </CodeBlock>
            <p className="text-lg text-gray-600 my-2"><strong>Nonlinear Transformation</strong>: Enhance signal distinction</p>
            <CodeBlock language="python">
{`# Reduce noise in middle quintiles
enhanced_signal = sign(centered_ranks) * |centered_ranks|^0.75`}
            </CodeBlock>
            <p className="text-lg text-gray-600 my-2"><strong>Gross Exposure Scaling</strong>:</p>
            <CodeBlock language="python">
{`target_gross = 1.0  # 100% gross exposure
weights = enhanced_signal / sum(|enhanced_signal|) * target_gross`}
            </CodeBlock>
          </div>
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h3 className="text-2xl font-medium text-gray-700 mb-3">2. Turnover Control with Adaptive Smoothing</h3>
            <p className="text-lg text-gray-600 mb-2"><strong>Standard Smoothing</strong>:</p>
            <CodeBlock language="python">
{`new_weights = (1 - α) * target_weights + α * previous_weights`}
            </CodeBlock>
            <p className="text-lg text-gray-600 my-2"><strong>Adaptive Enhancement</strong>: Reduce smoothing for significant signal changes</p>
            <CodeBlock language="python">
{`signal_change = |target_weights - previous_weights|
significant_threshold = quantile(signal_change, 0.75)

adaptive_α = α - 0.25 if signal_change > significant_threshold else α
blended_weights = (1 - adaptive_α) * target + adaptive_α * previous`}
            </CodeBlock>
            <p className="text-lg text-gray-600 font-semibold mt-3 mb-1">Constraints Enforcement:</p>
            <ol className="list-decimal list-inside text-lg text-gray-600 leading-relaxed">
              <li><strong>Market Neutrality</strong>: <code className="bg-gray-200 p-1 rounded">sum(weights) = 0</code></li>
              <li><strong>Gross Exposure</strong>: <code className="bg-gray-200 p-1 rounded">sum(|weights|) = 1.0</code></li>
              <li><strong>Position Limits</strong>: Individual position caps (if applicable)</li>
            </ol>
          </div>
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h3 className="text-2xl font-medium text-gray-700 mb-3">3. Rebalancing and Execution</h3>
            <p className="text-lg text-gray-600 mb-2"><strong>Frequency</strong>: Daily rebalancing based on new earnings call data</p>
            <p className="text-lg text-gray-600 font-semibold mb-1">Implementation:</p>
            <ul className="list-disc list-inside text-lg text-gray-600 leading-relaxed">
              <li>Portfolio weights calculated at market close</li>
              <li>Trades executed at market open next day</li>
              <li>Transaction cost modeling (optional)</li>
            </ul>
          </div>
        </div>
      </section>

      <section aria-labelledby="risk-management-title">
        <h2 id="risk-management-title" className="text-3xl font-semibold text-gray-700 mb-6">Risk Management</h2>
         <div className="space-y-8">
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h3 className="text-2xl font-medium text-gray-700 mb-3">1. Factor Neutralization</h3>
            <p className="text-lg text-gray-600 mb-2"><strong>Fama-French Factor Exposure Control</strong>:</p>
            <CodeBlock language="python">
{`# Neutralize against market, size, value, profitability, investment factors
neutralized_factor = residual(factor ~ mktrf + smb + hml + rmw + cma)`}
            </CodeBlock>
          </div>
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h3 className="text-2xl font-medium text-gray-700 mb-3">2. Turnover Management</h3>
            <p className="text-lg text-gray-600 mb-2"><strong>Smoothing Parameter</strong>: α = 0.75 (75% weight retention)</p>
            <ul className="list-disc list-inside text-lg text-gray-600 leading-relaxed">
              <li><strong>Result</strong>: Average turnover of 49.88% vs 100% without smoothing</li>
              <li><strong>Benefit</strong>: Reduced transaction costs while maintaining signal integrity</li>
            </ul>
          </div>
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h3 className="text-2xl font-medium text-gray-700 mb-3">3. Position Sizing</h3>
            <ul className="list-disc list-inside text-lg text-gray-600 leading-relaxed">
              <li><strong>Equal Risk Contribution</strong>: Positions sized by inverse volatility (optional)</li>
              <li><strong>Sector Neutrality</strong>: Optional sector constraints to reduce style bias</li>
              <li><strong>Liquidity Filters</strong>: Exclude low-volume stocks to ensure executability</li>
            </ul>
          </div>
        </div>
      </section>

      <section aria-labelledby="performance-attribution-title">
        <h2 id="performance-attribution-title" className="text-3xl font-semibold text-gray-700 mb-6">Performance Attribution</h2>
        {/* Content for Factor Timing, Cross-Sectional Analysis, Risk-Adjusted Metrics */}
        <p className="text-lg text-gray-600 leading-relaxed">
          Detailed content for Factor Timing, Cross-Sectional Analysis (Quintile Performance), and Risk-Adjusted Metrics (Information Coefficient, Sharpe Ratio) will be populated here. This section typically involves tables and explanations of how factor performance is measured and attributed.
        </p>
      </section>
      
      <section aria-labelledby="validation-testing-title">
        <h2 id="validation-testing-title" className="text-3xl font-semibold text-gray-700 mb-6">Validation and Testing</h2>
        {/* Content for Statistical Significance, Robustness Checks, Implementation Validation */}
        <p className="text-lg text-gray-600 leading-relaxed">
          Information on Statistical Significance (t-statistics, bootstrap), Robustness Checks (sub-period, sector analysis), and Implementation Validation (test suite details) will be included in this section.
        </p>
      </section>

      {/* Navigation links are in Header.jsx */}
    </div>
  );
};

export default MethodologyPage;
