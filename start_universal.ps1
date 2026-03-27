# TruthLens UA Analytics - Universal Start Script v3.0 (PowerShell)

$dockerCmd = Get-Command docker -ErrorAction SilentlyContinue
$dockerComposeCmd = Get-Command docker-compose -ErrorAction SilentlyContinue
$repoPath = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "TruthLens UA Analytics - Starting..." -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

if (($null -ne $dockerCmd) -and ($null -ne $dockerComposeCmd)) {
    Write-Host "Docker found - checking daemon..." -ForegroundColor Cyan
    docker info *> $null
    if ($LASTEXITCODE -eq 0) {
        docker-compose up --build -d
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "Services started:" -ForegroundColor Green
            Write-Host "  Dashboard: http://localhost:8501" -ForegroundColor White
            Write-Host "  API: http://localhost:8000" -ForegroundColor White
            Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White
            Write-Host ""
            Write-Host "Logs: docker-compose logs -f" -ForegroundColor Yellow
            Write-Host "Stop: docker-compose down" -ForegroundColor Red
            exit 0
        }
    }
    Write-Host "Docker daemon unavailable or compose failed - falling back to local mode" -ForegroundColor Yellow
} else {
    Write-Host "Docker not found - using local mode" -ForegroundColor Yellow
}

Write-Host "Starting API server..." -ForegroundColor Cyan
$apiProcess = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000" -WorkingDirectory $repoPath -PassThru

Start-Sleep -Seconds 3

Write-Host "Starting Dashboard (dashboard/Home.py)..." -ForegroundColor Cyan
$homePy = Join-Path $repoPath "dashboard\Home.py"
$dashboardProcess = Start-Process -FilePath "streamlit" -ArgumentList "run", $homePy, "--server.port", "8501" -WorkingDirectory $repoPath -PassThru

Write-Host ""
Write-Host "Services started:" -ForegroundColor Green
Write-Host "  Dashboard: http://localhost:8501" -ForegroundColor White
Write-Host "  API: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "Stop: close this window or stop the spawned processes" -ForegroundColor Red

try {
    Wait-Process -Id $apiProcess.Id -ErrorAction SilentlyContinue
    Wait-Process -Id $dashboardProcess.Id -ErrorAction SilentlyContinue
} finally {
    Stop-Process -Id $apiProcess.Id -Force -ErrorAction SilentlyContinue
    Stop-Process -Id $dashboardProcess.Id -Force -ErrorAction SilentlyContinue
}
