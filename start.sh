#!/bin/bash

# CCC Analyzer - Development Startup Script

echo "🚀 Starting CCC Analyzer Development Environment..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null
then
    echo "❌ Node.js is not installed"
    exit 1
fi

# Setup Backend
echo "📦 Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing backend dependencies..."
pip install -q -r requirements.txt

echo "✅ Backend ready"
echo ""

# Start Backend in background
echo "🔧 Starting FastAPI server (port 8000)..."
python main.py &
BACKEND_PID=$!
sleep 2

echo "✅ Backend running (PID: $BACKEND_PID)"
echo ""

# Setup Frontend
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install -q
fi

echo "✅ Frontend dependencies ready"
echo ""

# Start Frontend
echo "🎨 Starting React dev server (port 3000)..."
npm start &
FRONTEND_PID=$!

echo ""
echo "═════════════════════════════════════════════════════════════"
echo "✨ CCC Analyzer is running!"
echo "═════════════════════════════════════════════════════════════"
echo ""
echo "📊 Frontend:  http://localhost:3000"
echo "🔧 Backend:   http://localhost:8000"
echo "📚 API Docs:  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "═════════════════════════════════════════════════════════════"
echo ""

# Cleanup on exit
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Done!';" EXIT

wait
