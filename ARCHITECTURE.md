# CCC Analyzer - Architecture & Design

## System Overview

The CCC Analyzer is built as a modern full-stack web application with a clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                      User Browser                            │
│                   (React Frontend)                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Dashboard | Analysis | Comparison                       │ │
│  │ • Company Search Component                               │ │
│  │ • CCC Charts & Visualizations                            │ │
│  │ • Analysis Pages                                         │ │
│  └────────────────┬──────────────────────────────────────┐  │
│                   │ HTTP/REST (JSON)                     │   │
└───────────────────┼─────────────────────────────────────┼───┘
                    │                                     │
        ┌───────────▼──────────────────────┐      ┌──────▼─────┐
        │   FastAPI Backend Server          │      │  Screener  │
        │   (http://localhost:8000)         │      │   .in      │
        │                                   │      │  (Live API)│
        │  ┌─────────────────────────────┐ │      └────────────┘
        │  │ API Routes                  │ │
        │  │ • /api/companies/*          │ │
        │  │ • /api/analysis/*           │ │
        │  └──────────┬──────────────────┘ │
        │             │                    │
        │  ┌──────────▼──────────────────┐ │
        │  │ Services Layer              │ │
        │  │ • ScreenerService           │ │
        │  │ • CCCAnalysisService        │ │
        │  └──────────┬──────────────────┘ │
        │             │                    │
        │  ┌──────────▼──────────────────┐ │
        │  │ Data Models                 │ │
        │  │ • CompanyBasic              │ │
        │  │ • CCCComponents             │ │
        │  │ • ComparisonResult          │ │
        │  └─────────────────────────────┘ │
        └─────────────────────────────────┘
```

## Frontend Architecture

### React Application Structure

```
frontend/src/
├── App.js                      # Main app component with routing
├── App.css                     # Global styles
│
├── components/
│   ├── Navigation.js           # Top navigation bar
│   ├── Navigation.css
│   ├── CompanySearch.js        # Company search input component
│   ├── CompanySearch.css
│   ├── CCCChart.js             # Chart components (Recharts)
│   └── CCCChart.css
│
├── pages/
│   ├── Dashboard.js            # Home/info page
│   ├── Dashboard.css
│   ├── SingleAnalysis.js       # Single company analysis page
│   ├── SingleAnalysis.css
│   ├── Comparison.js           # Two-company comparison page
│   └── Comparison.css
│
├── index.js                    # React entry point
└── index.css                   # Global CSS
```

### Component Hierarchy

```
<App>
  <Navigation>
    <nav-links>
  </Navigation>
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/analyze" element={<SingleAnalysis />}>
      <CompanySearch />
      <CCCComponentsChart />
    </Route>
    <Route path="/compare" element={<Comparison />}>
      <CompanySearch /> x2
      <ComparisonChart />
    </Route>
  </Routes>
</App>
```

## Backend Architecture

### FastAPI Application Structure

```
backend/
├── main.py                     # FastAPI app setup, CORS config
├── requirements.txt            # Python dependencies
├── .env                        # Configuration
│
└── app/
    ├── __init__.py
    │
    ├── models.py               # Pydantic data models
    │
    ├── api/
    │   ├── __init__.py
    │   ├── companies.py        # Company routes
    │   │   ├── GET /search - Search companies
    │   │   ├── GET /{bse_code} - Get company details
    │   │   └── GET /{bse_code}/financials - Get financial data
    │   │
    │   └── analysis.py         # Analysis routes
    │       ├── POST /calculate-ccc - Calculate CCC
    │       ├── POST /analyze-company - Single analysis
    │       ├── POST /compare-companies - Comparison
    │       └── POST /project-improvement - Projections
    │
    └── services/
        ├── __init__.py
        │
        ├── screener.py         # Screener.in API integration
        │   ├── search_company()
        │   ├── get_company_data()
        │   ├── get_historical_financials()
        │   └── _parse_company_page()
        │
        └── ccc_analysis.py     # CCC analysis logic
            ├── calculate_ccc_components()
            ├── identify_problems()
            ├── analyze_trend()
            └── project_ccc_improvement()
```

## Data Flow

### Single Company Analysis Flow

```
1. User selects company
   ↓
2. Frontend: CompanySearch → search_query (company name/BSE code)
   ↓
3. Backend: GET /api/companies/search?q={query}
   ↓
4. ScreenerService.search_company() → fetch from Screener.in
   ↓
5. Frontend: Display search results
   ↓
6. User selects company
   ↓
7. Frontend: POST /api/analysis/analyze-company
   ↓
8. Backend:
   - ScreenerService.get_company_data() → fetch financials
   - CCCAnalysisService.calculate_ccc_components() → compute metrics
   - CCCAnalysisService.identify_problems() → pattern recognition
   - CCCAnalysisService.analyze_trend() → historical analysis
   ↓
9. Backend: Return CompanyAnalysis response
   ↓
10. Frontend: Display results
    - Metric cards
    - Charts
    - Problem list
    - Trend analysis
```

### Comparison Flow

```
1. User selects Company 1 and Company 2
   ↓
2. Frontend: POST /api/analysis/compare-companies
   ↓
3. Backend:
   - Fetch data for both companies
   - Calculate CCC for both
   - Identify problems for both
   - Calculate differences
   - Generate insights
   ↓
4. Backend: Return ComparisonResult response
   ↓
5. Frontend: Display
    - Side-by-side metrics table
    - Comparison chart
    - Individual assessments
    - Key insights
```

## CCC Analysis Logic

### Problem Identification Algorithm

```python
def identify_problems(current_ccc, historical_ccc, sector):
    problems = []
    benchmark = SECTOR_BENCHMARKS[sector]
    
    # Check 1: High Inventory Days
    if current_ccc.inventory_days > benchmark.inventory_days * 1.3:
        problems.append("High inventory days")
    
    # Check 2: High Receivable Days
    if current_ccc.receivable_days > benchmark.receivable_days * 1.3:
        problems.append("High receivable days")
    
    # Check 3: Low Payable Days
    if current_ccc.payable_days < benchmark.payable_days * 0.7:
        problems.append("Low payable days")
    
    # Check 4: Increasing CCC Trend
    if trend_is_increasing(historical_ccc):
        problems.append("Increasing CCC")
    
    return problems
```

### Trend Analysis

```python
def analyze_trend(historical_data):
    # Calculate year-over-year changes
    # Determine if improving or deteriorating
    # Calculate average change rate
    # Identify which components are changing most
    
    return {
        "ccc_trend": "improving" | "deteriorating" | "stable",
        "ccc_total_change": float,
        "inventory_trend": float,
        "receivable_trend": float,
        "payable_trend": float
    }
```

## API Response Examples

### Single Analysis Response
```json
{
  "status": "success",
  "company": {
    "name": "TCS",
    "bse_code": "532540",
    "sector": "manufacturing"
  },
  "ccc_analysis": {
    "current": {
      "inventory_days": 45.2,
      "receivable_days": 30.1,
      "payable_days": 52.3,
      "ccc": 23.0
    },
    "problems": [
      {
        "type": "high_inventory",
        "severity": 0.6,
        "description": "...",
        "impact": "..."
      }
    ],
    "assessment": "..."
  },
  "trends": {...},
  "profitability": {...}
}
```

### Comparison Response
```json
{
  "status": "success",
  "company1": {...},
  "company2": {...},
  "comparison": {
    "ccc_difference": 12.5,
    "inventory_difference": 5.2,
    "receivable_difference": -2.1,
    "payable_difference": 3.0
  },
  "insights": [...]
}
```

## Technology Stack Details

### Frontend (React)
- **React 18**: Latest hooks-based architecture
- **React Router**: Client-side routing (SPA)
- **Axios**: HTTP client for API calls
- **Recharts**: Chart library with responsive components
- **CSS3**: Custom styling (no frameworks for simplicity)

### Backend (Python)
- **FastAPI**: Modern async web framework
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server
- **Requests**: HTTP client for Screener.in
- **BeautifulSoup4**: HTML parsing (for scraping)
- **NumPy/Pandas**: Data analysis (prepared for future use)

## Error Handling

### Frontend
- Try-catch around API calls
- User-friendly error messages
- Loading states during API requests
- Validation before submissions

### Backend
- HTTP exception handling
- Try-catch in each endpoint
- Proper error status codes
- Detailed error messages in responses

## Future AI Integration Architecture

```
┌─────────────────────────────────────────────────┐
│   React Frontend                                 │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────▼───────────┐
        │  FastAPI Backend   │
        │                    │
        │  ┌──────────────┐  │
        │  │ New endpoint:│  │
        │  │ /api/ai/*    │  │
        │  └──────┬───────┘  │
        │         │          │
        │  ┌──────▼────────────────┐
        │  │ AIAnalysisService     │
        │  │ (to be created)       │
        │  └──────┬────────────────┘
        │         │
        │  ┌──────▼───────────┐
        │  │ Claude API       │
        │  │ (Anthropic)      │
        │  └──────────────────┘
        │
        └────────────────────┘
```

**Planned AI Features:**
- Pattern recognition and explanation
- Recommendation generation
- Scenario analysis
- Natural language insights
- Benchmark comparisons

## Performance Considerations

### Frontend Optimization
- Code splitting with React Router
- Lazy loading of components
- Memoization of expensive calculations
- Efficient re-render management

### Backend Optimization
- Async/await for non-blocking operations
- Caching of Screener.in data
- Connection pooling for external APIs
- Database indexing (when data is persisted)

### Scalability Path
1. Add data persistence (PostgreSQL)
2. Implement caching layer (Redis)
3. Containerize with Docker
4. Deploy to cloud (AWS/GCP/Azure)
5. Add CDN for static assets

## Security Considerations

### Current (Development)
- CORS configured for localhost
- Environment variables for sensitive config
- Input validation via Pydantic

### Future (Production)
- Rate limiting
- Authentication & authorization
- HTTPS/SSL
- API key management
- Data encryption
- Security headers

---

**This architecture is designed to be scalable, maintainable, and ready for future enhancements.**
