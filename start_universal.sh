#!/bin/bash

echo "TruthLens UA Analytics - Starting..."
echo "=================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

if command -v docker >/dev/null 2>&1 && command -v docker-compose >/dev/null 2>&1; then
    echo "Docker found - checking daemon..."
    if docker info >/dev/null 2>&1; then
        docker-compose up --build -d
        if [ $? -eq 0 ]; then
            echo ""
            echo "Services started:"
            echo "  Dashboard: http://localhost:8501"
            echo "  API: http://localhost:8000"
            echo "  API Docs: http://localhost:8000/docs"
            echo ""
            echo "Logs: docker-compose logs -f"
            echo "Stop: docker-compose down"
            exit 0
        fi
    fi
    echo "Docker daemon unavailable or compose failed - falling back to local mode"
else
    echo "Docker not found - using local mode"
fi

echo "Starting API server..."
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 &
API_PID=$!

sleep 3

echo "Starting Dashboard (dashboard/Home.py)..."
streamlit run dashboard/Home.py --server.port 8501 --server.address 127.0.0.1 &
DASHBOARD_PID=$!

echo ""
echo "Services started:"
echo "  Dashboard: http://localhost:8501"
echo "  API: http://localhost:8000"
echo ""
echo "Stop: Ctrl+C"

trap "kill $API_PID $DASHBOARD_PID 2>/dev/null; exit" INT TERM
wait
