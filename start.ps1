Write-Host "Starting Assessly Application..." -ForegroundColor Green

$backend = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    Write-Host "Starting Backend (FastAPI)..." -ForegroundColor Cyan
    uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
}

$frontend = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    Write-Host "Starting Frontend (Streamlit)..." -ForegroundColor Cyan
    streamlit run src/frontend.py
}

Write-Host "`nBoth services are starting..." -ForegroundColor Yellow
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:8501" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop both services" -ForegroundColor Yellow

try {
    while ($true) {
        Receive-Job -Job $backend
        Receive-Job -Job $frontend
        Start-Sleep -Milliseconds 500
    }
}
finally {
    Write-Host "`nStopping services..." -ForegroundColor Red
    Stop-Job -Job $backend, $frontend
    Remove-Job -Job $backend, $frontend
    Write-Host "Services stopped." -ForegroundColor Green
}
