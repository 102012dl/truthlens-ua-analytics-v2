# TruthLens UA Analytics - PowerShell Start Script (Windows)

Write-Host "====================================" -ForegroundColor Green
Write-Host "TruthLens UA Analytics - Quick Start" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

Write-Host "[1/4] Checking Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found. Please install Python 3.10+" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[2/4] Setting up environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
}

& "venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "[3/4] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
if (Test-Path "dashboard\requirements.txt") {
    pip install -r dashboard\requirements.txt
}

Write-Host ""
Write-Host "[4/4] Starting services..." -ForegroundColor Yellow
Write-Host "Starting API server in background..." -ForegroundColor Cyan
$repoPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$apiProcess = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000" -WorkingDirectory $repoPath -PassThru

Write-Host "Waiting for API to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

Write-Host "Starting Dashboard (dashboard/Home.py)..." -ForegroundColor Cyan
try {
    streamlit run (Join-Path $repoPath "dashboard\Home.py") --server.port 8501
} finally {
    Stop-Process -Id $apiProcess.Id -Force -ErrorAction SilentlyContinue
}
