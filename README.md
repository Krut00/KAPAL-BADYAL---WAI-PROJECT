# CCC Analyzer - Cash Conversion Cycle Analysis Platform

A comprehensive web application for analyzing and comparing companies' working capital efficiency using the Cash Conversion Cycle (CCC) metric.

## 📋 Project Overview

The CCC Analyzer helps identify working-capital efficiency problems in companies by analyzing:

- **Inventory Days** - Average time inventory remains before being sold
- **Receivable Days** - Average time taken to collect payments from customers
- **Payable Days** - Average time taken to pay suppliers
- **Cash Conversion Cycle (CCC)** - Overall working capital efficiency metric

### Formula
```
CCC = Inventory Days + Receivable Days − Payable Days
```

## ✨ Features

### Current Features
✅ **Single Company Analysis**
- Fetch live financial data from Screener.in
- Calculate CCC components and metrics
- Identify working capital efficiency problems using pattern recognition
- Analyze trends over time
- Visualize CCC metrics with charts

✅ **Company Comparison**
- Compare CCC metrics between two companies
- Side-by-side visualization
- Generate comparative insights
- Identify relative strengths and weaknesses

✅ **Problem Identification**
- Automatic detection of high inventory days
- Identification of slow customer collections
- Detection of quick supplier payments
- Trend analysis for CCC deterioration

### Future Features (Foundation Ready)
🚀 **AI-Powered Analysis** (Claude API Integration)
- Automated pattern recognition
- Natural language insights
- Scenario analysis recommendations
- Cash flow optimization suggestions

🚀 **Scenario Modeling**
- Project CCC improvements
- What-if analysis
- Financial impact modeling

## 🏗️ Project Structure

```
ccc-analyzer/
├── frontend/                    # React application
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navigation.js
│   │   │   ├── Navigation.css
│   │   │   ├── CompanySearch.js
│   │   │   ├── CompanySearch.css
│   │   │   ├── CCCChart.js
│   │   │   └── CCCChart.css
│   │   ├── pages/
│   │   │   ├── Dashboard.js
│   │   │   ├── Dashboard.css
│   │   │   ├── SingleAnalysis.js
│   │   │   ├── SingleAnalysis.css
│   │   │   ├── Comparison.js
│   │   │   └── Comparison.css
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
│
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── companies.py
│   │   │   └── analysis.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── screener.py
│   │   │   └── ccc_analysis.py
│   │   ├── models.py
│   │   └── __init__.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Node.js 14+ and npm
- Python 3.8+
- pip (Python package manager)

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
- The `.env` file is already configured for local development
- Adjust settings as needed

5. **Run the backend server:**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start development server:**
```bash
npm start
```

The application will open at `http://localhost:3000`

## 📊 API Endpoints

### Companies
- `GET /api/companies/search?q=<query>` - Search companies
- `GET /api/companies/{bse_code}` - Get company details
- `GET /api/companies/{bse_code}/financials` - Get financial data

### Analysis
- `POST /api/analysis/calculate-ccc` - Calculate CCC components
- `POST /api/analysis/analyze-company` - Analyze single company
- `POST /api/analysis/compare-companies` - Compare two companies
- `POST /api/analysis/project-improvement` - Project CCC improvements

## 📈 How to Use

### Analyze a Single Company
1. Go to "Single Company Analysis"
2. Search for a company by name or BSE code
3. Select the company
4. View detailed CCC analysis, problems, and trends

### Compare Two Companies
1. Go to "Compare Companies"
2. Select two companies
3. Click "Compare Companies"
4. View side-by-side comparison and insights

## 🔍 Understanding Results

### Working Capital Problems Identified

**High Inventory Days (>30% above benchmark)**
- Indicates slow inventory movement
- May suggest overstocking or low sales
- Recommendation: Improve inventory management

**High Receivable Days (>30% above benchmark)**
- Indicates slow customer collections
- Creates cash flow pressure
- Recommendation: Improve credit policies, follow-up procedures

**Low Payable Days (<30% below benchmark)**
- Indicates quick supplier payments
- Drains cash reserves unnecessarily
- Recommendation: Negotiate better payment terms

**Increasing CCC**
- Indicates deteriorating working capital efficiency
- More cash locked into operations
- Recommendation: Address the primary driver

## 🔄 Data Source

Financial data is fetched from **Screener.in**, a popular Indian stock market analysis platform.

**Note:** Live integration with Screener.in API requires proper authentication. Currently, the system is configured for demonstration with mock data structures.

### Future Integration Options:
1. **Screener.in API** - Direct API integration
2. **Screener.in MCP Server** - Custom MCP integration (https://github.com/minhaj3/screener.in-MCP-server)
3. **Web Scraping** - BeautifulSoup-based data extraction

## 🤖 AI Integration (Future Implementation)

The project is ready for Claude API integration:

```python
# In app/services/ai_analysis.py (to be created)
from anthropic import Anthropic

async def analyze_with_ai(company_data, problems):
    """Use Claude for advanced pattern recognition and recommendations"""
    # AI-powered insights generation
    # Natural language problem explanations
    # Scenario analysis and recommendations
```

To enable AI features:
1. Add Claude API key to `.env`
2. Install Anthropic SDK: `pip install anthropic`
3. Implement analysis endpoints using Claude

## 🏢 Sector Benchmarks

The system includes default benchmarks for different sectors:

- **Default**: General benchmark
- **Retail**: Fast inventory turnover, quick collections
- **Manufacturing**: Longer inventory cycles, extended payables
- **Services**: Minimal inventory, focus on receivables

Customize benchmarks in `app/services/ccc_analysis.py`

## 📝 CCC Analysis Questions Addressed

The platform answers 9 key questions:

1. ✅ Is the selected company facing a working-capital efficiency problem?
2. ✅ Which component of its CCC is contributing most to the problem?
3. ✅ What could be the possible reasons for the inefficiency?
4. ✅ What solutions can be developed to address the problem?
5. 🚀 How can AI support the analysis and solution process?
6. 🚀 What are the financial and operational trade-offs of these solutions?
7. 🚀 Which solution is most practical for the company?
8. 🚀 How much could the CCC potentially improve under the proposed scenario?
9. 🚀 Could improved working-capital efficiency potentially support better profitability and cash-flow management?

✅ = Implemented | 🚀 = Future AI-powered features

## 🛠️ Technologies Used

### Frontend
- **React 18** - UI framework
- **React Router** - Navigation
- **Axios** - HTTP client
- **Recharts** - Data visualization
- **CSS3** - Styling

### Backend
- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Requests** - HTTP requests
- **BeautifulSoup4** - Web scraping (future)
- **Anthropic SDK** - AI integration (future)

## 📦 Deployment

### Local Development
Already configured. Run both servers as described in setup.

### GitHub Deployment
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/ccc-analyzer.git
git push -u origin main
```

### Docker Deployment (Future)
Create `Dockerfile` and `docker-compose.yml` for containerized deployment.

## 📚 Additional Resources

- [Screener.in](https://www.screener.in) - Financial data source
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Cash Conversion Cycle Explained](https://www.investopedia.com/terms/c/cashconversioncycle.asp)

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Additional sector benchmarks
- More visualization types
- Mobile app version
- Real-time data updates
- AI-powered recommendations

## 📄 License

This project is open source and available for educational and commercial use.

## 🎯 Future Roadmap

- [ ] Claude API integration for AI analysis
- [ ] Scenario modeling and projections
- [ ] Historical data tracking
- [ ] Export reports (PDF, Excel)
- [ ] Mobile responsive improvements
- [ ] User accounts and saved analyses
- [ ] Real-time data feeds
- [ ] Industry comparison benchmarks
- [ ] Docker containerization
- [ ] Cloud deployment options

## 💬 Questions?

For questions or issues, please refer to the documentation or create an issue in the repository.

---

**Built with ❤️ for working capital management professionals**
