import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import MethodologyPage from './pages/MethodologyPage';
import ResultsPage from './pages/ResultsPage';
import TechnicalPage from './pages/TechnicalPage'; // Parent for technical section
import NotFoundPage from './pages/NotFoundPage';

// New imports for technical sub-pages
import TechnicalProjectStructurePage from './pages/technical/ProjectStructurePage.jsx';
import TechnicalCoreModulesPage from './pages/technical/CoreModulesPage.jsx';
import TechnicalTestingFrameworkPage from './pages/technical/TestingFrameworkPage.jsx';
import TechnicalDataPipelinePage from './pages/technical/DataPipelinePage.jsx';
import TechnicalDeploymentExecutionPage from './pages/technical/DeploymentExecutionPage.jsx';
import TechnicalPerformanceOptimizationsPage from './pages/technical/PerformanceOptimizationsPage.jsx';
import TechnicalErrorHandlingPage from './pages/technical/ErrorHandlingPage.jsx';
import TechnicalDevelopmentGuidelinesPage from './pages/technical/DevelopmentGuidelinesPage.jsx';

function App() {
  const basename = import.meta.env.DEV ? "/" : "/earnings_call_tone_research/";

  return (
    <BrowserRouter basename={basename}>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="methodology" element={<MethodologyPage />} />
          <Route path="results" element={<ResultsPage />} />
          
          <Route path="technical" element={<TechnicalPage />}>
            {/* If TechnicalPage itself shows content (e.g. Code Architecture), 
                it could have an index route. For now, let's assume it's primarily a layout 
                with sub-navigation and an Outlet. An index route can be added later if needed.
                Or, the first sub-page could be the default.
                For simplicity, let's make "Project Structure" the default/index for /technical.
            */}
            <Route index element={<TechnicalProjectStructurePage />} /> 
            <Route path="project-structure" element={<TechnicalProjectStructurePage />} />
            <Route path="core-modules" element={<TechnicalCoreModulesPage />} />
            <Route path="testing-framework" element={<TechnicalTestingFrameworkPage />} />
            <Route path="data-pipeline" element={<TechnicalDataPipelinePage />} />
            <Route path="deployment-execution" element={<TechnicalDeploymentExecutionPage />} />
            <Route path="performance-optimizations" element={<TechnicalPerformanceOptimizationsPage />} />
            <Route path="error-handling" element={<TechnicalErrorHandlingPage />} />
            <Route path="development-guidelines" element={<TechnicalDevelopmentGuidelinesPage />} />
          </Route>
          
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
