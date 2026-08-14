import React from 'react';
import { Link } from 'react-router-dom';
import './Navigation.css';

function Navigation() {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          <span className="logo-icon">📊</span> CCC Analyzer
        </Link>
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/" className="nav-link">Dashboard</Link>
          </li>
          <li className="nav-item">
            <Link to="/analyze" className="nav-link">Single Analysis</Link>
          </li>
          <li className="nav-item">
            <Link to="/compare" className="nav-link">Compare Companies</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navigation;
