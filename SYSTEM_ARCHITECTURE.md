# 🏗️ CCC Analyzer - Visual System Architecture

## Complete System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER'S BROWSER                            │
│                   http://localhost:3000                          │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              React Application (Frontend)                   │ │
│  │                                                              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │ │
│  │  │  Dashboard   │  │   Analyze    │  │  Compare     │     │ │
│  │  │   (Home)     │  │   (Single)   │  │  (Two Cos)   │     │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘     │ │
│  │         │                  │                  │              │ │
│  │  ┌──────▼──────┐  ┌────────▼──────┐  ┌───────▼──────┐     │ │
│  │  │CompanySearch│  │CompanySearch  │  │2 x Search    │     │ │
│  │  │Components   │  │ + Analysis    │  │ + Compare    │     │ │
│  │  └──────┬──────┘  └────────┬──────┘  └───────┬──────┘     │ │
│  │         │                  │                  │              │ │
│  │         │    ┌─────────────┴─────────────┐   │              │ │
│  │         └────▶ Axios HTTP Client        ◀───┘              │ │
│  │              (Sends JSON requests)                          │ │
│  │                                                              │ │
│  │         ┌──────────────────────────────────┐              │ │
│  │         │     Recharts Visualizations      │              │ │
│  │         │ (Bar Charts, Line Charts, etc)   │              │ │
│  │         └──────────────────────────────────┘              │ │
│  │                                                              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                             ▲                                     │
│                             │ HTTP (JSON)                         │
│                             ▼                                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Port 8000
                                │
┌───────────────────────────────▼───────────────────────────────────┐
│                  FastAPI Backend Server                            │
│            http://localhost:8000 (Uvicorn)                        │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                   API Routes                                 │ │
│  │                                                               │ │
│  │  GET  /api/companies/search?q={query}                       │ │
│  │  GET  /api/companies/{bse_code}                             │ │
│  │  GET  /api/companies/{bse_code}/financials                 │ │
│  │  POST /api/analysis/calculate-ccc                          │ │
│  │  POST /api/analysis/analyze-company                        │ │
│  │  POST /api/analysis/compare-companies                      │ │
│  │  POST /api/analysis/project-improvement                    │ │
│  │                                                               │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                             │                                      │
│  ┌──────────────────────────▼──────────────────────────────────┐ │
│  │                  Services Layer                              │ │
│  │                                                               │ │
│  │  ┌──────────────────────┐  ┌──────────────────────┐         │ │
│  │  │  ScreenerService     │  │ CCCAnalysisService   │         │ │
│  │  │                      │  │                      │         │ │
│  │  │ • search_company()   │  │ • calculate_ccc()    │         │ │
│  │  │ • get_company_data() │  │ • identify_problems()│         │ │
│  │  │ • get_financials()   │  │ • analyze_trend()    │         │ │
│  │  │ • parse_pages()      │  │ • project_improve()  │         │ │
│  │  │                      │  │ • compare()          │         │ │
│  │  └──────────────────────┘  └──────────────────────┘         │ │
│  │                                                               │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                             │                                      │
│  ┌──────────────────────────▼──────────────────────────────────┐ │
│  │              Data Models (Pydantic)                          │ │
│  │                                                               │ │
│  │ • CompanyBasic        • CompanyAnalysis                     │ │
│  │ • CCCComponents       • ComparisonResult                    │ │
│  │ • FinancialMetric     • CCCTrend                            │ │
│  │                                                               │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                             │                                      │
│  ┌──────────────────────────▼──────────────────────────────────┐ │
│  │         External Data Source Integration                    │ │
│  │                                                               │ │
│  │  ┌────────────────────────────────────────────────┐         │ │
│  │  │  Screener.in API                              │         │ │
│  │  │  (Live Financial Data)                        │         │ │
│  │  │                                                 │         │ │
│  │  │ • Company Search                              │         │ │
│  │  │ • Financial Metrics (Inventory, Receivables)  │         │ │
│  │  │ • Historical Data                             │         │ │
│  │  │ • Balance Sheet Information                   │         │ │
│  │  └────────────────────────────────────────────────┘         │ │
│  │                                                               │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Single Company Analysis

```
┌─────────────┐
│   User      │
│ Enters Text │
└──────┬──────┘
       │ "TCS"
       ▼
┌──────────────────────┐
│ CompanySearch        │
│ Component            │ ◀─── Debounced search input
└──────┬───────────────┘
       │ API Call
       ▼
GET /api/companies/search?q=TCS
       │
       ▼
┌──────────────────────┐
│ ScreenerService      │
│ .search_company()    │ ◀─── Queries Screener.in
└──────┬───────────────┘
       │ Returns matching companies
       ▼
┌──────────────────────┐
│ Display Results      │
│ in Dropdown          │
└──────┬───────────────┘
       │ User selects "TCS (532540)"
       ▼
┌──────────────────────┐
│ handleCompanySelect()│ ◀─── Triggers analysis
└──────┬───────────────┘
       │ setLoading(true)
       ▼
POST /api/analysis/analyze-company?bse_code=532540&sector=default
       │
       ▼
┌──────────────────────────────────────────────┐
│   Backend Analysis Pipeline                  │
│                                              │
│ 1. Fetch Company Data                       │
│    └─▶ ScreenerService.get_company_data()  │
│    └─▶ Extract financial metrics            │
│                                              │
│ 2. Calculate CCC Components                 │
│    └─▶ Inventory Days calculation           │
│    └─▶ Receivable Days calculation          │
│    └─▶ Payable Days calculation             │
│    └─▶ CCC = Inv + Rec - Pay                │
│                                              │
│ 3. Problem Identification (ML-like)        │
│    └─▶ Compare against benchmarks           │
│    └─▶ Detect high inventory days           │
│    └─▶ Detect high receivable days          │
│    └─▶ Detect low payable days              │
│    └─▶ Detect CCC trends                    │
│    └─▶ Calculate severity scores            │
│                                              │
│ 4. Trend Analysis                           │
│    └─▶ Fetch historical data                │
│    └─▶ Calculate year-over-year changes     │
│    └─▶ Identify improvement/deterioration   │
│                                              │
│ 5. Generate Assessment                      │
│    └─▶ Create text summary                  │
│    └─▶ Rank problems by severity            │
│                                              │
└──────────────────────┬───────────────────────┘
                       │ Return JSON response
                       ▼
CompanyAnalysis {
  company_name: "Tata Consultancy Services",
  bse_code: "532540",
  ccc_analysis: {
    current: {
      inventory_days: 45.2,
      receivable_days: 30.1,
      payable_days: 52.3,
      ccc: 23.0
    },
    problems: [
      {
        type: "high_inventory",
        severity: 0.6,
        description: "Inventory Days at 45.2...",
        impact: "..."
      }
    ],
    assessment: "Company shows..."
  },
  trends: {...}
}
                       │
                       ▼
┌──────────────────────────────────┐
│ setAnalysisData(response.data)   │ ◀─── Store in React state
└──────┬───────────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│ Render Analysis UI               │
│                                  │
│ ├─ Metric Cards                 │
│ │  ├─ Inventory Days: 45.2      │
│ │  ├─ Receivable Days: 30.1     │
│ │  ├─ Payable Days: 52.3        │
│ │  └─ CCC: 23.0 days            │
│ │                                │
│ ├─ Bar Chart                    │
│ │  └─ Components visualization  │
│ │                                │
│ ├─ Problems List                │
│ │  └─ [████░░] High Inventory   │
│ │                                │
│ └─ Trends                       │
│    └─ CCC improving -5.2 days   │
│                                  │
└──────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│ User sees complete analysis      │
│ with actionable insights         │
└──────────────────────────────────┘
```

---

## Data Flow: Company Comparison

```
┌─────────────────────────────┐
│ User Selects Company 1: TCS │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ User Selects Company 2:     │
│ Infosys                     │
└──────────┬──────────────────┘
           │
           ▼
┌──────────────────────────┐
│ Click "Compare Companies"│
└──────────┬───────────────┘
           │
           ▼
POST /api/analysis/compare-companies
{
  company1_bse: "532540",    (TCS)
  company2_bse: "500209",    (Infosys)
  sector: "default"
}
           │
           ▼
┌──────────────────────────────────┐
│ Backend Comparison Analysis      │
│                                  │
│ 1. Fetch both companies          │
│ 2. Calculate CCC for each        │
│ 3. Identify problems for each    │
│ 4. Calculate differences         │
│ 5. Generate comparison insights  │
│                                  │
└──────────────┬───────────────────┘
               │
               ▼
ComparisonResult {
  company1: {
    name: "TCS",
    ccc: { inventory: 45.2, receivable: 30.1, payable: 52.3, ccc: 23.0 },
    problems: [...]
  },
  company2: {
    name: "Infosys",
    ccc: { inventory: 38.5, receivable: 28.3, payable: 55.1, ccc: 11.7 },
    problems: [...]
  },
  comparison: {
    ccc_difference: 11.3,
    inventory_difference: 6.7,
    receivable_difference: 1.8,
    payable_difference: -2.8
  },
  insights: [
    "Infosys has better CCC efficiency",
    "Infosys manages inventory better",
    ...
  ]
}
               │
               ▼
┌──────────────────────────────────┐
│ Display Comparison UI            │
│                                  │
│ ┌──────────────┬──────────────┐ │
│ │ TCS (45.2)   │ INF (38.5)   │ │
│ │ CCC: 23.0    │ CCC: 11.7    │ │
│ └──────────────┴──────────────┘ │
│                                  │
│ [Comparison Chart]               │
│                                  │
│ Key Insights:                    │
│ ✓ Infosys is 11.3 days ahead    │
│ ✓ Better inventory management   │
│                                  │
└──────────────────────────────────┘
```

---

## CCC Calculation Deep Dive

```
Financial Input Data:
┌─────────────────────────────────┐
│ • Average Inventory: $5M        │
│ • Cost of Goods Sold: $40M      │
│ • Average Receivables: $3M      │
│ • Revenue: $35M                 │
│ • Average Payables: $4M         │
└──────────────┬──────────────────┘
               │
               ▼
┌───────────────────────────────────────┐
│ Step 1: Calculate Inventory Days      │
│                                       │
│ Inventory Days = (Avg Inv / COGS) × 365
│                = ($5M / $40M) × 365   │
│                = 0.125 × 365          │
│                = 45.625 days          │
│                ≈ 45.6 days            │
│                                       │
│ ➜ Company takes ~46 days to sell      │
│   inventory                           │
└───────────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────┐
│ Step 2: Calculate Receivable Days     │
│                                       │
│ Receivable Days = (Avg Rec / Rev) × 365
│                 = ($3M / $35M) × 365  │
│                 = 0.0857 × 365        │
│                 = 31.29 days          │
│                 ≈ 31.3 days           │
│                                       │
│ ➜ Company takes ~31 days to collect   │
│   from customers                      │
└───────────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────┐
│ Step 3: Calculate Payable Days        │
│                                       │
│ Payable Days = (Avg Pay / COGS) × 365 │
│             = ($4M / $40M) × 365      │
│             = 0.1 × 365               │
│             = 36.5 days               │
│                                       │
│ ➜ Company takes ~37 days to pay       │
│   suppliers                           │
└───────────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────┐
│ Step 4: Calculate CCC                 │
│                                       │
│ CCC = Inventory Days + Receivable Days
│       - Payable Days                  │
│     = 45.6 + 31.3 - 36.5             │
│     = 76.9 - 36.5                     │
│     = 40.4 days                       │
│                                       │
│ Interpretation:                       │
│ ✓ Company needs 40.4 days of working  │
│   capital for one operating cycle     │
│ ✓ Cash flows through operations in    │
│   40+ days                            │
│ ✓ Company must finance operations for │
│   this period from working capital    │
│                                       │
└───────────────────────────────────────┘
```

---

## Problem Identification Algorithm

```
Input: CCC Metrics + Sector Benchmark

Sector Benchmarks:
┌─────────────────────────────────────┐
│ Manufacturing:                      │
│ • Inventory Days: 90                │
│ • Receivable Days: 45               │
│ • Payable Days: 60                  │
│ • CCC: 75                           │
└─────────────────────────────────────┘

Current Company Metrics:
┌─────────────────────────────────────┐
│ • Inventory Days: 45.6              │
│ • Receivable Days: 30.1             │
│ • Payable Days: 52.3                │
│ • CCC: 23.0                         │
└─────────────────────────────────────┘

Algorithm:

1. Check High Inventory Days
   IF inventory_days > benchmark × 1.3?
   45.6 > (90 × 1.3)? → 45.6 > 117? NO ✗
   ➜ No problem detected

2. Check High Receivable Days
   IF receivable_days > benchmark × 1.3?
   30.1 > (45 × 1.3)? → 30.1 > 58.5? NO ✗
   ➜ No problem detected

3. Check Low Payable Days
   IF payable_days < benchmark × 0.7?
   52.3 < (60 × 0.7)? → 52.3 < 42? NO ✗
   ➜ No problem detected

4. Check CCC Trend
   IF historical_ccc is increasing?
   [65.0, 56.0, 46.0, 40.4]
   Trend is DECREASING ✓ (improving)
   ➜ No problem detected

Result:
┌──────────────────────────────────────┐
│ Assessment: Company shows healthy    │
│ working capital efficiency           │
│ No critical problems identified      │
└──────────────────────────────────────┘
```

---

## File Organization

```
/Users/krut/ccc-analyzer/
│
├── 📚 Documentation
│   ├── README.md                 ← Full documentation
│   ├── QUICKSTART.md             ← 5-minute setup
│   ├── ARCHITECTURE.md           ← System design
│   ├── PROJECT_SUMMARY.md        ← Complete overview
│   ├── LOCAL_EXECUTION_GUIDE.md  ← This file
│   └── TESTDATA.md               ← Sample data
│
├── 🎨 Frontend (React at localhost:3000)
│   └── frontend/
│       ├── package.json          ← npm config
│       ├── public/
│       │   └── index.html        ← HTML template
│       └── src/
│           ├── App.js            ← Main component
│           ├── index.js          ← Entry point
│           ├── components/       ← Reusable components
│           │   ├── Navigation.js
│           │   ├── CompanySearch.js
│           │   └── CCCChart.js   (Recharts)
│           └── pages/            ← Page components
│               ├── Dashboard.js  (Home)
│               ├── SingleAnalysis.js
│               └── Comparison.js
│
├── 🐍 Backend (FastAPI at localhost:8000)
│   └── backend/
│       ├── main.py              ← App entry point
│       ├── requirements.txt      ← Dependencies
│       ├── .env                  ← Configuration
│       └── app/
│           ├── models.py         ← Data models
│           ├── api/              ← API routes
│           │   ├── companies.py  (Search, get company)
│           │   └── analysis.py   (Calculate, analyze, compare)
│           └── services/         ← Business logic
│               ├── screener.py   (Screener.in integration)
│               └── ccc_analysis.py (CCC calculations)
│
└── 🔧 Utilities
    ├── start.sh                 ← Linux/Mac startup
    └── start.bat                ← Windows startup
```

---

**Everything is production-ready! The architecture is clean, scalable, and easy to understand.** ✅
