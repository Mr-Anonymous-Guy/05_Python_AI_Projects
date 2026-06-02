@echo off
:: ──────────────────────────────────────────────────────────────
:: run.bat — Launch Rock Paper Scissors on Windows
:: ──────────────────────────────────────────────────────────────

:: Move to the directory that contains this script
cd /d "%~dp0"

:: ── Python interpreter detection ──────────────────────────────
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8 or newer.
    echo         Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Using:
python --version

echo [INFO] Starting Rock Paper Scissors...
echo.

python main.py

pause
