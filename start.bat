@echo off
REM CCC Analyzer - Development Startup Script for Windows

echo.
echo 🚀 Starting CCC Analyzer Development Environment...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    exit /b 1
)

REM Setup Backend
echo 📦 Setting up Backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install -q -r requirements.txt

echo ✅ Backend ready
echo.

REM Start Backend in background
echo 🔧 Starting FastAPI server (port 8000)...
start "CCC Backend" python main.py
timeout /t 2 /nobreak

echo ✅ Backend running
echo.

REM Setup Frontend
cd ..\frontend

if not exist "node_modules" (
    echo 📦 Installing frontend dependencies...
    call npm install -q
)

echo ✅ Frontend dependencies ready
echo.

REM Start Frontend
echo 🎨 Starting React dev server (port 3000)...
start "CCC Frontend" cmd /k npm start

echo.
echo ═════════════════════════════════════════════════════════════
echo ✨ CCC Analyzer is running!
echo ═════════════════════════════════════════════════════════════
echo.
echo 📊 Frontend:  http://localhost:3000
echo 🔧 Backend:   http://localhost:8000
echo 📚 API Docs:  http://localhost:8000/docs
echo.
echo Close this window to stop the servers
echo ═════════════════════════════════════════════════════════════
echo.

pause
