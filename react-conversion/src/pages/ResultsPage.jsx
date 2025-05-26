import React from 'react';
import QuintileChart from '../components/QuintileChart'; // Placeholder component
import SortableTable from '../components/SortableTable';   // Placeholder component

// It's good practice to manage image paths better, but for now, direct paths.
// These will be updated when assets are moved.
const imagePath = (name) => `/docs/assets/images/${name}`; // Helper for now

const ResultsPage = () => {
  // Placeholder data for tables - in a real app, this might come from props or state
  const icAnalysisData = [
    { period: '5-Day', ic: '+0.015', riskAdjustedIc: '+0.027', tStat: 'N/A', pValue: 'N/A' },
    { period: '10-Day', ic: '+0.011', riskAdjustedIc: '+0.019', tStat: 'N/A', pValue: 'N/A' },
  ];
  const icColumns = [
    { Header: 'Period', accessor: 'period' },
    { Header: 'IC', accessor: 'ic' },
    { Header: 'Risk-Adjusted IC', accessor: 'riskAdjustedIc' },
    { Header: 't-stat', accessor: 'tStat' },
    { Header: 'p-value', accessor: 'pValue' },
  ];

  // Data for QuintileChart (currently hardcoded in interactive.js, replicate structure)
  const quintileChartData = [
    { quintile: 'Q1', return: 1.683, description: 'Highest Dispersion' },
    { quintile: 'Q2', return: 2.5, description: 'High Dispersion' },
    { quintile: 'Q3', return: 3.0, description: 'Medium Dispersion' },
    { quintile: 'Q4', return: 3.8, description: 'Low Dispersion' },
    { quintile: 'Q5', return: 4.748, description: 'Lowest Dispersion' }
  ];


  return (
    <div className="space-y-12">
      <header className="text-center py-8">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-800">Results and Performance Analysis</h1>
      </header>

      <section aria-labelledby="exec-summary-title">
        <h2 id="exec-summary-title" className="text-3xl font-semibold text-gray-700 mb-4">Executive Summary</h2>
        <p className="text-lg text-gray-600 leading-relaxed">
          The earnings call tone dispersion factor demonstrates <strong>statistically significant predictive power</strong> for future stock returns. Our analysis reveals that companies with low tone dispersion (consistent, certain communication) systematically outperform those with high tone dispersion (uncertain, inconsistent communication).
        </p>
      </section>

      <section aria-labelledby="key-metrics-title">
        <h2 id="key-metrics-title" className="text-3xl font-semibold text-gray-700 mb-6">Key Performance Metrics</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8 text-center">
          {/* These would ideally be dynamic or styled components */}
          <div className="p-4 bg-green-100 rounded-lg shadow"><h3 className="text-2xl font-bold text-green-700">+0.015</h3><p className="text-green-600">Information Coefficient (5D)</p></div>
          <div className="p-4 bg-green-100 rounded-lg shadow"><h3 className="text-2xl font-bold text-green-700">+0.027</h3><p className="text-green-600">Risk-Adjusted IC (5D)</p></div>
          <div className="p-4 bg-green-100 rounded-lg shadow"><h3 className="text-2xl font-bold text-green-700">+3.065</h3><p className="text-green-600">Quintile Spread (bps)</p></div>
          <div className="p-4 bg-green-100 rounded-lg shadow"><h3 className="text-2xl font-bold text-green-700">49.88%</h3><p className="text-green-600">Average Turnover</p></div>
        </div>
        
        <h3 className="text-2xl font-medium text-gray-700 mb-3">Information Coefficient Analysis</h3>
        {/* Replace with SortableTable if ready, or basic table for now */}
        <div className="overflow-x-auto shadow-md rounded-lg mb-6">
          <table className="min-w-full leading-normal">
            <thead className="bg-gray-200">
              <tr>{icColumns.map(col => <th key={col.accessor} className="px-5 py-3 border-b-2 border-gray-300 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">{col.Header}</th>)}</tr>
            </thead>
            <tbody className="bg-white">
              {icAnalysisData.map((row, i) => (
                <tr key={i}>
                  <td className="px-5 py-4 border-b border-gray-200 text-sm"><strong>{row.period}</strong></td>
                  <td className="px-5 py-4 border-b border-gray-200 text-sm"><span className="text-green-600 font-semibold">{row.ic}</span></td>
                  <td className="px-5 py-4 border-b border-gray-200 text-sm"><span className="text-green-600 font-semibold">{row.riskAdjustedIc}</span></td>
                  <td className="px-5 py-4 border-b border-gray-200 text-sm">{row.tStat}</td>
                  <td className="px-5 py-4 border-b border-gray-200 text-sm">{row.pValue}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="p-4 bg-green-50 border-l-4 border-green-500 text-green-700">
          <strong>Interpretation:</strong> Positive IC indicates the factor correctly predicts return direction. Risk-adjusted IC accounts for factor volatility. Values are economically meaningful for institutional strategies.
        </div>
      </section>

      <section aria-labelledby="quintile-performance-title">
        <h2 id="quintile-performance-title" className="text-3xl font-semibold text-gray-700 mb-6">Quintile Performance Analysis</h2>
        <div className="p-6 bg-gray-50 rounded-lg shadow mb-8 text-center">
          <h4 className="text-xl font-medium text-gray-700 mb-2">Interactive Quintile Returns (5-Day)</h4>
          <QuintileChart data={quintileChartData} /> {/* Pass data to the chart */}
          <p className="text-sm text-gray-500 mt-2"><em>Click on quintile bars for detailed information (functionality to be implemented in QuintileChart component)</em></p>
        </div>
        {/* Placeholder for the detailed quintile table from results.md */}
        <p className="text-lg text-gray-600 leading-relaxed mb-4">
          (Detailed Quintile Performance Table will be rendered here, similar to the one in `docs/results.md`, potentially using the `SortableTable` component.)
        </p>
         <h3 className="text-2xl font-medium text-gray-700 mt-6 mb-3">Factor Spread Analysis</h3>
        <ul className="list-disc list-inside text-lg text-gray-600 leading-relaxed space-y-1">
            <li><strong>5-Day Spread (Q5-Q1)</strong>: <span className="font-semibold text-green-600">+3.065 bps</span></li>
            <li><strong>10-Day Spread (Q5-Q1)</strong>: <span className="font-semibold text-red-600">-2.913 bps</span> (note: short-term vs medium-term dynamics)</li>
            <li><strong>Economic Significance</strong>: Clear outperformance of low-dispersion stocks</li>
        </ul>
      </section>

      <section aria-labelledby="portfolio-performance-title">
        <h2 id="portfolio-performance-title" className="text-3xl font-semibold text-gray-700 mb-6">Portfolio Performance</h2>
        {/* Placeholder for Risk-Return Profile and Turnover Analysis tables */}
        <p className="text-lg text-gray-600 leading-relaxed">
          (Tables for Risk-Return Profile and Turnover Analysis will be rendered here.)
        </p>
      </section>

      <section aria-labelledby="visualizations-title">
        <h2 id="visualizations-title" className="text-3xl font-semibold text-gray-700 mb-6">Visualizations</h2>
        <div className="grid md:grid-cols-2 gap-8 items-start">
          <figure className="text-center">
            <h3 className="text-xl font-medium text-gray-700 mb-2">Factor Performance Tearsheet</h3>
            <img src={imagePath('tearsheet.png')} alt="Alphalens Tearsheet" className="w-full h-auto rounded-lg shadow-md" />
            <figcaption className="text-sm text-gray-500 mt-2">Key insights: Clear quintile separation, positive IC, consistent performance, low market correlation.</figcaption>
          </figure>
          <figure className="text-center">
            <h3 className="text-xl font-medium text-gray-700 mb-2">Turnover Analysis</h3>
            <img src={imagePath('turnover.png')} alt="Turnover Analysis" className="w-full h-auto rounded-lg shadow-md" />
            <figcaption className="text-sm text-gray-500 mt-2">Turnover characteristics: Stable around 50% with smoothing, no extreme spikes.</figcaption>
          </figure>
        </div>
      </section>

      {/* Other sections from results.md (Factor Statistics, Return Attribution, Risk Analysis, Economic Interpretation, etc.) would follow similar patterns */}
      {/* For brevity, only a few key sections are fully fleshed out here. */}
      <section aria-labelledby="further-sections-title">
        <h2 id="further-sections-title" className="text-3xl font-semibold text-gray-700 mb-4">Further Analysis Sections</h2>
        <p className="text-lg text-gray-600 leading-relaxed">
        This page will also include detailed sections (replicating the content from `docs/results.md`) on:
        </p>
        <ul className="list-disc list-inside text-lg text-gray-600 leading-relaxed space-y-1 mt-2">
            <li>Factor Statistics Deep Dive (Quantile Distribution table)</li>
            <li>Return Attribution (5-Day Return Analysis)</li>
            <li>Risk Analysis (Factor Loadings table, Regime Analysis)</li>
            <li>Economic Interpretation (Behavioral Finance Foundation, Business Cycle Sensitivity)</li>
            <li>Implementation Considerations (Capacity Analysis, Transaction Costs)</li>
            <li>Statistical Validation (Robustness Tests, Significance Testing)</li>
            <li>Comparison to Academic Literature</li>
        </ul>
        <p className="text-lg text-gray-600 leading-relaxed mt-4">
        These sections will involve converting Markdown text, lists, and tables into JSX with appropriate Tailwind CSS styling.
        </p>
      </section>


      {/* Navigation links are in Header.jsx */}
    </div>
  );
};

export default ResultsPage;
