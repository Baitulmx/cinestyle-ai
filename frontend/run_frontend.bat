@echo off
echo Starting CineStyle AI Frontend...
echo.
cd /d "%~dp0"
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)
echo.
echo Starting Vite development server on http://localhost:5173
echo Press Ctrl+C to stop
echo.
npm run dev
pause
