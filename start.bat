@echo off
echo ====================================
echo TruthLens UA Analytics - Quick Start
echo ====================================
echo.

echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [3/4] Starting API server...
start "API Server" cmd /k "python -m uvicorn app.main:app --reload --port 8000"

echo Waiting for API to start...
timeout /t 3 /nobreak > nul

echo.
echo [4/4] Starting Dashboard...
streamlit run dashboard\Home.py --server.port 8501

pause
