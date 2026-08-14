# 🎯 CCC Analyzer - Copy & Paste Quick Start

## ⚡ Start Backend (Copy & Paste - Terminal 1)

```bash
cd /Users/krut/ccc-analyzer/backend && /Users/krut/ccc-analyzer/backend/venv/bin/python3 main.py
```

**Expected Result:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ **Backend Ready:** http://localhost:8000

---

## ⚡ Start Frontend (Copy & Paste - Terminal 2)

```bash
cd /Users/krut/ccc-analyzer/frontend && npm install && npm start
```

**Expected Result:**
```
Compiled successfully!

You can now view ccc-analyzer in the browser.
Local: http://localhost:3000
```

✅ **Frontend Ready:** http://localhost:3000

---

## 🌐 Open in Browser

```
http://localhost:3000
```

Click on "Single Company Analysis" or "Compare Companies"

---

## 🧪 Test the API (Optional)

While backend is running, open a new terminal:

```bash
# Test health
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs

# Search for a company
curl "http://localhost:8000/api/companies/search?q=TCS"

# Test analysis endpoint
curl -X POST http://localhost:8000/api/analysis/analyze-company \
  -H "Content-Type: application/json" \
  -d '{"bse_code": "532540", "sector": "manufacturing"}'
```

---

## 📁 Directory Location

All files are in:
```
/Users/krut/ccc-analyzer/
```

---

## 🚨 Troubleshooting

### Backend fails to start
```bash
# Try this instead:
cd /Users/krut/ccc-analyzer/backend
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 main.py
```

### Frontend fails to compile
```bash
# Try this:
cd /Users/krut/ccc-analyzer/frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
npm start
```

### Ports already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

---

## ✅ You're All Set!

Run the backend and frontend commands above in separate terminals.  
Then open http://localhost:3000 in your browser.

**Everything is ready to use!** 🚀
