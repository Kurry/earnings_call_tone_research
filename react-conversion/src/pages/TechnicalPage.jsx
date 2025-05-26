import React from 'react';
import { Link, Outlet } from 'react-router-dom';
// CodeBlock import removed as it's not used directly on this overview page.

const TechnicalPage = () => {
  const subNavItems = [
    { path: '/technical/project-structure', label: 'Project Structure' },
    { path: '/technical/core-modules', label: 'Core Modules' },
    { path: '/technical/testing-framework', label: 'Testing Framework' },
    { path: '/technical/data-pipeline', label: 'Data Pipeline' },
    { path: '/technical/deployment-execution', label: 'Deployment & Execution' },
    { path: '/technical/performance-optimizations', label: 'Performance Optimizations' },
    { path: '/technical/error-handling', label: 'Error Handling & Logging' },
    { path: '/technical/development-guidelines', label: 'Development Guidelines' },
  ];

  return (
    <div className="space-y-8"> {/* Reduced overall spacing, sub-pages will have their own */}
      <header className="text-center pt-8 pb-4"> {/* Adjusted padding */}
        <h1 className="text-4xl md:text-5xl font-bold text-gray-800">Technical Documentation</h1>
      </header>

      {/* Code Architecture section remains here as part of the overview */}
      <section aria-labelledby="code-architecture-title" className="px-4">
        <h2 id="code-architecture-title" className="text-3xl font-semibold text-gray-700 mb-4">Code Architecture</h2>
        <p className="text-lg text-gray-600 leading-relaxed">
          The earnings call tone research framework is built with modularity, testability, and reproducibility in mind. This overview provides a guide to the technical sections available.
        </p>
        <p className="text-lg text-gray-600 leading-relaxed mt-4">
          Please use the navigation below to explore detailed documentation for each technical area.
        </p>
      </section>

      {/* Sub-navigation menu */}
      <nav className="px-4 py-4 border-t border-b border-gray-200">
        <ul className="flex flex-wrap gap-x-6 gap-y-2 justify-center">
          {subNavItems.map(item => (
            <li key={item.path}>
              <Link 
                to={item.path} 
                className="text-blue-600 hover:text-blue-800 hover:underline font-medium"
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      {/* Outlet for nested routes (the sub-page content) */}
      <div className="px-4 py-8">
        <Outlet />
      </div>
    </div>
  );
};

export default TechnicalPage;
