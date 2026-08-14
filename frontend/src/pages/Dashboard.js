import React from 'react';
import { Link } from 'react-router-dom';
import './Dashboard.css';

function Dashboard() {
  return (
    <div className="dashboard">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">💰 Cash Conversion Cycle</h1>
          <h2 className="hero-subtitle">Analyzer</h2>
          <p className="hero-description">Instantly analyze company working capital efficiency</p>
          
          <div className="features-grid">
            <Link to="/analyze" className="feature-card feature-card-primary">
              <div className="card-glow"></div>
              <div className="card-content">
                <div className="feature-icon">🔍</div>
                <h3>Analyze Company</h3>
                <p>See CCC metrics & problems</p>
              </div>
            </Link>

            <Link to="/compare" className="feature-card feature-card-secondary">
              <div className="card-glow"></div>
              <div className="card-content">
                <div className="feature-icon">⚖️</div>
                <h3>Compare</h3>
                <p>Side-by-side comparison</p>
              </div>
            </Link>
          </div>
        </div>
      </div>

      {/* Info Section */}
      <div className="info-section">
        <h2 className="section-title">How It Works</h2>
        <div className="info-container">
          <div className="info-box info-box-1">
            <div className="box-icon">📊</div>
            <h3>CCC Formula</h3>
            <div className="formula">
              CCC = Inventory + Receivable − Payable
            </div>
            <p>Measures working capital efficiency</p>
          </div>

          <div className="info-box info-box-2">
            <div className="box-icon">⚡</div>
            <h3>Quick Facts</h3>
            <ul>
              <li>Lower CCC = Better efficiency</li>
              <li>Faster cash flow</li>
              <li>Improved operations</li>
            </ul>
          </div>

          <div className="info-box info-box-3">
            <div className="box-icon">🎯</div>
            <h3>Key Metrics</h3>
            <ul>
              <li>Inventory Days (turnover speed)</li>
              <li>Receivable Days (collection time)</li>
              <li>Payable Days (payment terms)</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
