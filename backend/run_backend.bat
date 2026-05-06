@echo off
echo Starting CineStyle AI Backend...
echo.
cd /d "%~dp0backend"
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Installing dependencies...
pip install -r requirements.txt -q
echo.
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
