#!/bin/bash
# TruthLens UA Analytics - Universal Start Script (Linux/Mac)

echo "===================================="
echo "TruthLens UA Analytics - Quick Start"
echo "===================================="
echo

cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1

echo "[1/4] Checking Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python3 not found. Please install Python 3.10+"
    exit 1
fi

echo
echo "[2/4] Setting up environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

echo
echo "[3/4] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
if [ -f "dashboard/requirements.txt" ]; then
    pip install -r dashboard/requirements.txt
fi

echo
echo "[4/4] Starting services..."
echo "Starting API server in background..."
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 &
API_PID=$!
cleanup() { kill $API_PID 2>/dev/null; }
trap cleanup EXIT INT TERM

echo "Waiting for API to start..."
sleep 3

echo "Starting Dashboard (entry: dashboard/Home.py)..."
streamlit run dashboard/Home.py --server.port 8501 --server.address 127.0.0.1
