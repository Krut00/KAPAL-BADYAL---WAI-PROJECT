import React, { useState } from 'react';
import axios from 'axios';
import CompanySearch from '../components/CompanySearch';
import { CCCComponentsChart, CCCTrendChart } from '../components/CCCChart';
import API_URL from '../api';
import './SingleAnalysis.css';

function getErrorMessage(error, fallback) {
  const detail = error?.response?.data?.detail;
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || String(item)).join(', ');
  }
  if (detail && typeof detail === 'object') {
    return detail.msg || JSON.stringify(detail);
  }
  return fallback;
}

function getCompanyIdentifier(company) {
  return company.bse_code
    || company.code
    || company.url?.match(/\/company\/([^/]+)/)?.[1]
    || company.id;
}

function SingleAnalysis() {
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCompanySelect = async (company) => {
    setLoading(true);
    setError(null);

    try {
      const bseCode = getCompanyIdentifier(company);
      const response = await axios.post(
        `${API_URL}/api/analysis/analyze-company`,
        null,
        {
          params: {
            bse_code: bseCode
          }
        }
      );

      if (response.data.status === 'success') {
        setAnalysisData(response.data);
      } else {
        setError('Failed to fetch analysis data');
      }
    } catch (err) {
      setError(getErrorMessage(err, 'Error fetching company analysis'));
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="single-analysis">
      {/* Header */}
      <div className="page-header">
        <h1>🔍 Company Analysis</h1>
        <p>Search any company to see its working capital metrics</p>
      </div>

      {/* Search Section */}
      <div className="search-section">
        <div className="search-container">
          <CompanySearch
            onCompanySelect={handleCompanySelect}
            placeholder="Type company name or BSE code..."
          />
        </div>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
        </div>
      )}

      {analysisData && !loading && (
        <div className="analysis-results">
          <div className="company-header card">
            <h2>{analysisData.company.name}</h2>
            <div className="company-meta">
              <span>BSE Code: <strong>{analysisData.company.bse_code}</strong></span>
            </div>
          </div>

          <div className="metrics-section">
            <h2>CCC Metrics</h2>
            <div className="metrics-grid">
              <div className="metric-card">
                <div className="metric-label">Inventory Days</div>
                <div className="metric-value">{analysisData.ccc_analysis.current.inventory_days}</div>
                <div className="metric-unit">days</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Receivable Days</div>
                <div className="metric-value">{analysisData.ccc_analysis.current.receivable_days}</div>
                <div className="metric-unit">days</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Payable Days</div>
                <div className="metric-value">{analysisData.ccc_analysis.current.payable_days}</div>
                <div className="metric-unit">days</div>
              </div>
              <div className="metric-card metric-ccc">
                <div className="metric-label">Cash Conversion Cycle</div>
                <div className="metric-value">{analysisData.ccc_analysis.current.ccc}</div>
                <div className="metric-unit">days</div>
              </div>
            </div>
          </div>

          {analysisData.ccc_analysis.current && (
            <CCCComponentsChart data={analysisData.ccc_analysis.current} />
          )}

          {analysisData.historical_ccc && analysisData.historical_ccc.length > 1 && (
            <CCCTrendChart data={analysisData.historical_ccc} />
          )}

          <div className="assessment-section card">
            <h2>Working Capital Assessment</h2>
            {analysisData.benchmark && (
              <div className="benchmark-note">
                <strong>Industry reference:</strong> CCC benchmark {analysisData.benchmark.ccc} days; 
                inventory {analysisData.benchmark.inventory_days} days, receivables {analysisData.benchmark.receivable_days} days, 
                and payables {analysisData.benchmark.payable_days} days. {analysisData.benchmark.source}.
              </div>
            )}
            <div className={`assessment ${analysisData.ccc_analysis.problems.length === 0 ? 'healthy' : 'warning'}`}>
              <p>{analysisData.ccc_analysis.assessment}</p>
            </div>

            {analysisData.ccc_analysis.problems.length > 0 && (
              <div className="problems-list">
                <h3>Identified Problems:</h3>
                {analysisData.ccc_analysis.problems.map((problem, index) => (
                  <div key={index} className="problem-item" style={{ borderLeftColor: `rgba(255, 107, 107, ${0.3 + problem.severity * 0.7})` }}>
                    <div className="problem-header">
                      <h4>{problem.type.replace(/_/g, ' ').toUpperCase()}</h4>
                      <div className="severity-bar">
                        <div className="severity-fill" style={{ width: `${problem.severity * 100}%` }}></div>
                      </div>
                    </div>
                    <p className="problem-description">{problem.description}</p>
                    <p className="problem-impact"><strong>Impact:</strong> {problem.impact}</p>
                  </div>
                ))}
              </div>
            )}

            {analysisData.data_quality && (
              <div className="analysis-data-note">
                <strong>Data used:</strong> {analysisData.data_quality.source}. 
                Periods: {(analysisData.data_quality.periods_used || []).join(', ')}. 
                {analysisData.data_quality.cogs_note}
              </div>
            )}
          </div>

          {analysisData.trends && Object.keys(analysisData.trends).length > 0 && (
            <div className="trends-section card">
              <h2>Trend Analysis</h2>
              <div className="trends-grid">
                <div className="trend-item">
                  <span>CCC Trend:</span>
                  <strong>{analysisData.trends.ccc_trend}</strong>
                </div>
                <div className="trend-item">
                  <span>CCC Total Change:</span>
                  <strong>{analysisData.trends.ccc_total_change} days</strong>
                </div>
                <div className="trend-item">
                  <span>Inventory Trend:</span>
                  <strong>{analysisData.trends.inventory_trend} days</strong>
                </div>
                <div className="trend-item">
                  <span>Receivable Trend:</span>
                  <strong>{analysisData.trends.receivable_trend} days</strong>
                </div>
                <div className="trend-item">
                  <span>Payable Trend:</span>
                  <strong>{analysisData.trends.payable_trend} days</strong>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

          {analysisData && analysisData.investor_insights && analysisData.investor_insights.length > 0 && (
            <div className="investor-insights-section card">
              <h2>Investor Perspective</h2>
              <ul className="investor-insights-list">
                {analysisData.investor_insights.map((insight, index) => (
                  <li key={index}>{insight}</li>
                ))}
              </ul>
            </div>
          )}

    </div>
  );
}

export default SingleAnalysis;
