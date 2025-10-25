@echo off
echo Starting Assessly Application...

start "Backend - FastAPI" cmd /k "uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload"
timeout /t 2 /nobreak >nul
start "Frontend - Streamlit" cmd /k "streamlit run src/frontend.py"

echo.
echo Both services are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
echo.
echo Close the terminal windows to stop the services.
