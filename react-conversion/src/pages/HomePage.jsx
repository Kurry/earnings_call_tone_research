import React from 'react';
import CodeBlock from '../components/CodeBlock'; // Assuming CodeBlock is ready

// It's good practice to manage image paths better, but for now, direct paths.
// These will be updated when assets are moved.
const imagePath = (name) => `/docs/assets/images/${name}`; // Helper for now

const HomePage = () => {
  return (
    <div className="space-y-12">
      <header className="text-center py-8">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-800">Earnings Call Tone Dispersion Research</h1>
      </header>

      <section aria-labelledby="executive-summary-title">
        <h2 id="executive-summary-title" className="text-3xl font-semibold text-gray-700 mb-4">Executive Summary</h2>
        <p className="text-lg text-gray-600 leading-relaxed">
          This research explores the predictive power of <strong>tone dispersion</strong> in earnings calls for future stock returns. Using natural language processing and quantitative finance techniques, we analyze how uncertainty and disagreement in management communication affects subsequent stock performance.
        </p>
        <div className="mt-6 p-4 bg-blue-50 border-l-4 border-blue-500 text-blue-700">
          <h3 className="text-xl font-semibold mb-2">Key Findings</h3>
          <p className="mb-2"><strong>Recent Performance (2020-2024)</strong>:</p>
          <ul className="list-disc list-inside space-y-1">
            <li><strong>Positive Sharpe Ratio</strong>: 0.231 (recent period)</li>
            <li><strong>Annualized Return</strong>: 2.48% (market-neutral alpha)</li>
            <li><strong>Economic Intuition Confirmed</strong>: Low tone dispersion (certainty) predicts outperformance</li>
            <li><strong>Regime Evolution</strong>: Factor effectiveness improved significantly in modern markets</li>
          </ul>
          <p className="mt-3 text-sm">
            <strong>Important Note</strong>: This factor shows strong performance in recent years (2020+) but struggled historically (2005-2019), suggesting the relationship between earnings call tone and returns has strengthened as markets have evolved.
          </p>
        </div>
      </section>

      <section aria-labelledby="what-is-tone-dispersion-title">
        <h2 id="what-is-tone-dispersion-title" className="text-3xl font-semibold text-gray-700 mb-4">What is Tone Dispersion?</h2>
        <p className="text-lg text-gray-600 leading-relaxed mb-2">
          <strong>Tone dispersion</strong> measures the uncertainty and disagreement in earnings call language. It captures:
        </p>
        <ul className="list-disc list-inside text-lg text-gray-600 leading-relaxed space-y-1">
          <li>Variation in sentiment across different parts of the call</li>
          <li>Inconsistency in management messaging</li>
          <li>Uncertainty about future prospects</li>
          <li>Disagreement between management and analysts</li>
        </ul>
        <div className="mt-6 p-4 bg-gray-100 rounded-lg">
          <h3 id="research-hypothesis-title" className="text-2xl font-semibold text-gray-700 mb-2">Research Hypothesis</h3>
          <blockquote className="text-lg text-gray-600 italic border-l-4 border-gray-300 pl-4">
            Companies with <strong>low tone dispersion</strong> (consistent, certain communication) should outperform those with <strong>high tone dispersion</strong> (uncertain, inconsistent communication).
          </blockquote>
        </div>
      </section>

      <section aria-labelledby="factor-performance-summary-title">
        <h2 id="factor-performance-summary-title" className="text-3xl font-semibold text-gray-700 mb-6">Factor Performance Summary</h2>
        <p className="text-lg text-gray-600 mb-4"><strong>Recent Period (2020-2024) - When Factor Works Best</strong>:</p>
        <div className="overflow-x-auto shadow-md rounded-lg">
          <table className="min-w-full leading-normal">
            <thead className="bg-gray-200">
              <tr>
                <th className="px-5 py-3 border-b-2 border-gray-300 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Metric</th>
                <th className="px-5 py-3 border-b-2 border-gray-300 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Value</th>
                <th className="px-5 py-3 border-b-2 border-gray-300 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Interpretation</th>
              </tr>
            </thead>
            <tbody className="bg-white">
              <tr>
                <td className="px-5 py-4 border-b border-gray-200 text-sm"><strong>Sharpe Ratio</strong></td>
                <td className="px-5 py-4 border-b border-gray-200 text-sm">0.231</td>
                <td className="px-5 py-4 border-b border-gray-200 text-sm">Positive risk-adjusted returns</td>
              </tr>
              <tr>
                <td className="px-5 py-4 border-b border-gray-200 text-sm"><strong>Annualized Return</strong></td>
                <td className="px-5 py-4 border-b border-gray-200 text-sm">2.48%</td>
                <td className="px-5 py-4 border-b border-gray-200 text-sm">Market-neutral alpha generation</td>
              </tr>
              <tr>
                <td className="px-5 py-4 border-b border-gray-200 text-sm"><strong>Max Drawdown</strong></td>
                <td className="px-5 py-4 border-b border-gray-200 text-sm">-39.01%</td>
                <td className="px-5 py-4 border-b border-gray-200 text-sm">Moderate downside risk</td>
              </tr>
              <tr>
                <td className="px-5 py-4 border-b border-gray-200 text-sm"><strong>Win Rate</strong></td>
                <td className="px-5 py-4 border-b border-gray-200 text-sm">32.83%</td>
                <td className="px-5 py-4 border-b border-gray-200 text-sm">Reasonable hit rate for factor</td>
              </tr>
              <tr>
                <td className="px-5 py-4 border-b border-gray-200 text-sm"><strong>Average Turnover</strong></td>
                <td className="px-5 py-4 border-b border-gray-200 text-sm">49.88%</td>
                <td className="px-5 py-4 border-b border-gray-200 text-sm">Controlled with 75% smoothing</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="mt-4 text-sm text-gray-600">
          <strong>Historical Context</strong>: The factor struggled in earlier periods (2005-2019) but has shown consistent positive performance since 2020, suggesting increased market efficiency in pricing earnings call sentiment.
        </p>
      </section>

      <section aria-labelledby="data-methodology-title">
        <h2 id="data-methodology-title" className="text-3xl font-semibold text-gray-700 mb-4">Data and Methodology</h2>
        <div className="space-y-4">
          <div>
            <h3 className="text-2xl font-medium text-gray-700 mb-2">Data Sources</h3>
            <ul className="list-disc list-inside text-lg text-gray-600 leading-relaxed">
              <li><strong>Earnings Call Data</strong>: 33,362 quarterly earnings calls (2005-2025)</li>
              <li><strong>Stock Prices</strong>: Daily adjusted prices for 677 stocks (2000-2024)</li>
              <li><strong>Fama-French Factors</strong>: Daily factor returns for risk adjustment</li>
            </ul>
          </div>
          <div>
            <h3 className="text-2xl font-medium text-gray-700 mb-2">Factor Construction</h3>
            <ol className="list-decimal list-inside text-lg text-gray-600 leading-relaxed space-y-1">
              <li><strong>Tone Analysis</strong>: Extract tone dispersion metrics from earnings call transcripts</li>
              <li><strong>Signal Mapping</strong>: Map quarterly calls to next business day trading dates</li>
              <li><strong>Cross-Sectional Ranking</strong>: Z-score normalize within each date</li>
              <li><strong>Portfolio Construction</strong>: Long-short portfolio with controlled turnover</li>
            </ol>
          </div>
        </div>
      </section>

      <section aria-labelledby="performance-visualizations-title">
        <h2 id="performance-visualizations-title" className="text-3xl font-semibold text-gray-700 mb-6">Performance Visualizations</h2>
        <div className="grid md:grid-cols-2 gap-8 items-start">
          <figure>
            <h3 className="text-xl font-medium text-gray-700 mb-2 text-center">Recent Performance Analysis (2020-2024)</h3>
            <img src={imagePath('recent_performance_analysis.png')} alt="Recent Performance Analysis" className="w-full h-auto rounded-lg shadow-md" />
          </figure>
          <figure>
            <h3 className="text-xl font-medium text-gray-700 mb-2 text-center">Regime Comparison Across Time Periods</h3>
            <img src={imagePath('regime_comparison.png')} alt="Regime Comparison" className="w-full h-auto rounded-lg shadow-md" />
          </figure>
        </div>
      </section>
      
      <section aria-labelledby="methodology-overview-title" className="text-center">
        <h2 id="methodology-overview-title" className="text-3xl font-semibold text-gray-700 mb-6">Methodology Overview</h2>
        <img src={imagePath('methodology_flowchart.png')} alt="Methodology Flowchart" className="max-w-2xl mx-auto h-auto rounded-lg shadow-md" />
      </section>

      {/* Navigation links are in Header.jsx, so they are omitted here unless specifically needed for page content */}

      <section aria-labelledby="quick-start-title">
        <h2 id="quick-start-title" className="text-3xl font-semibold text-gray-700 mb-4">Quick Start</h2>
        <p className="text-lg text-gray-600 mb-2">To reproduce these results:</p>
        <CodeBlock language="bash">
{`# Clone the repository
git clone https://github.com/kurry/earnings_call_tone_research.git
cd earnings_call_tone_research

# Install dependencies
pip install -r requirements.txt

# Run the backtest
python run_backtest.py`}
        </CodeBlock>
      </section>

      <section aria-labelledby="author-title" className="text-center py-8 bg-gray-50 rounded-lg">
        <h2 id="author-title" className="text-3xl font-semibold text-gray-700 mb-4">Author</h2>
        <p className="text-lg text-gray-600">
          This research was conducted by <strong>Kurry Tran</strong> using advanced quantitative finance techniques and natural language processing methods. The analysis demonstrates the practical application of behavioral finance principles in systematic trading strategies.
        </p>
        <p className="text-lg text-gray-600 mt-2">
          <strong>Contact</strong>: kurry.tran@gmail.com <br />
          <strong>GitHub</strong>: <a href="https://github.com/kurry" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">github.com/kurry</a>
        </p>
      </section>
      
      {/* 'Last updated' can be added here if needed, e.g., using new Date().toLocaleDateString() */}
    </div>
  );
};

export default HomePage;
