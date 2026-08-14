import React, { useState } from 'react';
import axios from 'axios';
import CompanySearch from '../components/CompanySearch';
import { ComparisonChart } from '../components/CCCChart';
import './Comparison.css';

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

function Comparison() {
  const [company1, setCompany1] = useState(null);
  const [company2, setCompany2] = useState(null);
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const performComparison = async () => {
    if (!company1 || !company2) {
      setError('Please select both companies');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(
        `http://localhost:8000/api/analysis/compare-companies`,
        {
          company1_bse: getCompanyIdentifier(company1),
          company2_bse: getCompanyIdentifier(company2)
        }
      );

      if (response.data.status === 'success') {
        setComparisonData(response.data);
      } else {
        setError('Failed to fetch comparison data');
      }
    } catch (err) {
      setError(getErrorMessage(err, 'Error performing comparison'));
      console.error('Comparison error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setCompany1(null);
    setCompany2(null);
    setComparisonData(null);
    setError(null);
  };

  return (
    <div className="comparison">
      <div className="page-header">
        <h1>Compare Two Companies</h1>
        <p>Side-by-side analysis of CCC and working capital efficiency</p>
      </div>

      <div className="selection-section card">
        <h2>Select Companies to Compare</h2>
        
        <div className="company-selection">
          <div className="company-selector">
            <label>Company 1</label>
            {company1 ? (
              <div className="selected-company">
                <div className="company-info">
                  <p className="company-name">{company1.name || company1.company_name}</p>
                  <p className="company-code">{getCompanyIdentifier(company1)}</p>
                </div>
                <button className="btn-clear" onClick={() => setCompany1(null)}>✕</button>
              </div>
            ) : (
              <CompanySearch
                onCompanySelect={setCompany1}
                placeholder="Search for first company..."
              />
            )}
          </div>

          <div className="vs-divider">VS</div>

          <div className="company-selector">
            <label>Company 2</label>
            {company2 ? (
              <div className="selected-company">
                <div className="company-info">
                  <p className="company-name">{company2.name || company2.company_name}</p>
                  <p className="company-code">{getCompanyIdentifier(company2)}</p>
                </div>
                <button className="btn-clear" onClick={() => setCompany2(null)}>✕</button>
              </div>
            ) : (
              <CompanySearch
                onCompanySelect={setCompany2}
                placeholder="Search for second company..."
              />
            )}
          </div>
        </div>

        <div className="controls">
          <button
            className="btn btn-primary"
            onClick={performComparison}
            disabled={!company1 || !company2 || loading}
          >
            {loading ? 'Comparing...' : 'Compare Companies'}
          </button>
          
          {comparisonData && (
            <button className="btn btn-secondary" onClick={handleClear}>
              Clear & Start Over
            </button>
          )}
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

      {comparisonData && !loading && (
        <div className="comparison-results">
          {comparisonData.comparison && (
            <ComparisonChart
              company1={{ name: comparisonData.company1.name, ccc: comparisonData.company1.ccc }}
              company2={{ name: comparisonData.company2.name, ccc: comparisonData.company2.ccc }}
            />
          )}

          <div className="metrics-comparison">
            <h2>CCC Metrics Comparison</h2>
            <div className="comparison-table">
              <div className="comparison-row header">
                <div className="metric-name">Metric</div>
                <div className="company-col">
                  <strong>{comparisonData.company1.name}</strong>
                </div>
                <div className="company-col">
                  <strong>{comparisonData.company2.name}</strong>
                </div>
                <div className="difference-col">
                  <strong>Difference</strong>
                </div>
              </div>

              <div className="comparison-row">
                <div className="metric-name">Inventory Days</div>
                <div className="company-col">{comparisonData.company1.ccc.inventory_days}</div>
                <div className="company-col">{comparisonData.company2.ccc.inventory_days}</div>
                <div className="difference-col">
                  {(comparisonData.company1.ccc.inventory_days - comparisonData.company2.ccc.inventory_days).toFixed(2)}
                </div>
              </div>

              <div className="comparison-row">
                <div className="metric-name">Receivable Days</div>
                <div className="company-col">{comparisonData.company1.ccc.receivable_days}</div>
                <div className="company-col">{comparisonData.company2.ccc.receivable_days}</div>
                <div className="difference-col">
                  {(comparisonData.company1.ccc.receivable_days - comparisonData.company2.ccc.receivable_days).toFixed(2)}
                </div>
              </div>

              <div className="comparison-row">
                <div className="metric-name">Payable Days</div>
                <div className="company-col">{comparisonData.company1.ccc.payable_days}</div>
                <div className="company-col">{comparisonData.company2.ccc.payable_days}</div>
                <div className="difference-col">
                  {(comparisonData.company1.ccc.payable_days - comparisonData.company2.ccc.payable_days).toFixed(2)}
                </div>
              </div>

              <div className="comparison-row highlight">
                <div className="metric-name"><strong>Cash Conversion Cycle</strong></div>
                <div className="company-col"><strong>{comparisonData.company1.ccc.ccc}</strong></div>
                <div className="company-col"><strong>{comparisonData.company2.ccc.ccc}</strong></div>
                <div className="difference-col">
                  <strong>{comparisonData.comparison.ccc_difference}</strong>
                </div>
              </div>
            </div>
          </div>

          <div className="assessment-comparison">
            <div className="assessment-box">
              <h3>{comparisonData.company1.name}</h3>
              <p>{comparisonData.company1.assessment}</p>
            </div>
            <div className="assessment-box">
              <h3>{comparisonData.company2.name}</h3>
              <p>{comparisonData.company2.assessment}</p>
            </div>
          </div>

          <div className="benchmark-note comparison-benchmark-note">
            Benchmarks are selected from each company's Screener.in industry classification and applied as industry reference profiles.
          </div>

          {comparisonData.insights && comparisonData.insights.length > 0 && (
            <div className="insights card">
              <h2>Key Insights</h2>
              <ul className="insights-list">
                {comparisonData.insights.map((insight, index) => (
                  <li key={index}>💡 {insight}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Comparison;
