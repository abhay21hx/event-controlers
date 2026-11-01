@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Install Python and try again.
    pause
    exit /b 1
)

python -c "import fastapi, uvicorn, httpx, dotenv" >nul 2>nul
if errorlevel 1 (
    echo Backend dependencies are missing. Installing them now...
    python -m pip install -r "..\requirements.txt"
    if errorlevel 1 (
        echo Dependency installation failed.
        pause
        exit /b 1
    )
)

python -c "from dotenv import load_dotenv; import os; load_dotenv(); exit(0 if os.getenv('TINYFISH_API_KEY') else 1)" >nul 2>nul
if errorlevel 1 (
    echo TINYFISH_API_KEY is missing from this folder's .env file.
    echo Add a line: TINYFISH_API_KEY=your-key
    pause
    exit /b 1
)

echo Starting Mission Control. Keep this window open.
echo Open http://127.0.0.1:8000 in your browser.
start "Mission Control Backend" /D "%~dp0" python -m uvicorn main:app --host 127.0.0.1 --port 8000
python "%~dp0wait_for_backend.py"
if errorlevel 1 (
    echo Backend did not start. Check the Mission Control Backend window.
    pause
    exit /b 1
)
start "" "http://127.0.0.1:8000"
