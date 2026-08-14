# 🚀 CCC Analyzer - Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

✅ Backend running at: `http://localhost:8000`
📚 API Docs at: `http://localhost:8000/docs`

## Step 2: Frontend Setup (2 minutes)

In a **new terminal**:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm start
```

✅ Frontend running at: `http://localhost:3000`

## Step 3: Start Using! (1 minute)

1. Open browser to `http://localhost:3000`
2. Go to "Single Company Analysis" or "Compare Companies"
3. Search for an Indian company (e.g., "TCS", "Infosys", "HDFC")
4. View analysis results!

## 🔧 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Try reinstalling dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm start
```

### Port conflicts
- Backend uses port 8000
- Frontend uses port 3000
- If busy, modify port in:
  - Backend: `main.py` (change `port=8000`)
  - Frontend: `package.json` (add `"PORT=3001"` to start script)

## 📊 Next Steps

1. **Single Analysis**: Analyze individual companies
2. **Comparison**: Compare two companies side-by-side
3. **Understand Results**: Read problem descriptions
4. **Explore Features**: Try different sectors

## 📝 Sample Companies to Try

(Once Screener.in integration is live)
- TCS (Tata Consultancy Services)
- Infosys
- HDFC Bank
- Reliance Industries
- ITC Limited

## 🎯 Main Features

| Feature | Status |
|---------|--------|
| Company Search | ✅ Ready |
| Single Analysis | ✅ Ready |
| Comparison | ✅ Ready |
| Charts & Visuals | ✅ Ready |
| Problem Detection | ✅ Ready |
| AI Analysis | 🚀 Coming Soon |
| Scenario Modeling | 🚀 Coming Soon |

## 🔗 Key URLs

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📞 Help

- Check README.md for detailed documentation
- Review API docs at `/docs` endpoint
- Check browser console for errors

---

**Ready? Let's analyze some CCC! 📊**
