@echo off
REM Start Backend and Frontend
echo ========================================
echo Starting CineStyle AI Application
echo ========================================
echo.

echo Starting Backend Server (Port 8000)...
start "Backend" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3

echo Starting Frontend Server (Port 5173)...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Both servers are starting:
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:5173
echo - API Health Check: http://localhost:8000/health
echo ========================================
echo Press Enter to close all servers...
pause
taskkill /F /IM python.exe /T
taskkill /F /IM node.exe /T
