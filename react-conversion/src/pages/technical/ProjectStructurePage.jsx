import React from 'react';
import CodeBlock from '../../components/CodeBlock'; // Note: path is now '../../components/'

const TechnicalProjectStructurePage = () => {
  return (
    <section aria-labelledby="project-structure-title">
      {/* The h1 that was in the placeholder can be removed if titles are handled by a parent or main content area style.
          Or, it can be kept if each sub-page should have its own prominent H1.
          For consistency with how other pages are being built, let's use a specific H2 for the section content here,
          assuming the overall page title might be part of a banner or layout above the Outlet.
          If TechnicalPage.jsx has an H1 "Technical Documentation", then sub-pages could start with H2.
          Let's re-evaluate if an H1 is needed per sub-page later. For now, an H2 for the content block.
      */}
      <h2 id="project-structure-title" className="text-3xl font-semibold text-gray-700 mb-4">Project Structure</h2>
      <CodeBlock language="bash">
{`earnings_call_tone_research/
├── data/                          # Raw data files
│   ├── ff5_daily.parquet
│   ├── stock_prices.parquet
│   └── tone_dispersion.parquet
├── src/                           # Core source code
│   ├── factor_build.py
│   ├── load.py
│   ├── neutralise.py
│   ├── portfolio.py
│   └── report.py
├── tests/                         # Comprehensive test suite
├── outputs/                       # Generated results
├── docs/                          # GitHub Pages documentation
├── run_backtest.py                # Main execution script
└── requirements.txt               # Python dependencies`}
      </CodeBlock>
      <p className="mt-4 text-sm text-gray-600">
        This structure organizes the project into data, source code, tests, generated outputs, and documentation.
      </p>
    </section>
  );
};

export default TechnicalProjectStructurePage;
