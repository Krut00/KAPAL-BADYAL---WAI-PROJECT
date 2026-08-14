import React, { useState } from 'react';
import axios from 'axios';
import './CompanySearch.css';

function CompanySearch({ onCompanySelect, placeholder = "Enter company name or BSE code" }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const handleSearch = async (e) => {
    const value = e.target.value;
    setSearchQuery(value);

    if (value.length < 2) {
      setResults([]);
      setShowResults(false);
      return;
    }

    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/api/companies/search`, {
        params: { q: value }
      });
      setResults(response.data.results || []);
      setShowResults(true);
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectCompany = (company) => {
    onCompanySelect(company);
    setSearchQuery('');
    setResults([]);
    setShowResults(false);
  };

  return (
    <div className="company-search">
      <input
        type="text"
        value={searchQuery}
        onChange={handleSearch}
        placeholder={placeholder}
        className="search-input"
        onFocus={() => searchQuery.length >= 2 && setShowResults(true)}
      />
      
      {loading && <div className="search-loading">Loading...</div>}
      
      {showResults && results.length > 0 && (
        <ul className="search-results">
          {results.map((company, index) => (
            <li key={index} onClick={() => handleSelectCompany(company)} className="result-item">
              <div className="result-name">{company.name || company.company_name}</div>
              <div className="result-code">{company.bse_code || company.code || company.id}</div>
            </li>
          ))}
        </ul>
      )}
      
      {showResults && results.length === 0 && !loading && searchQuery && (
        <div className="no-results">No companies found</div>
      )}
    </div>
  );
}

export default CompanySearch;
