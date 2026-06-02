@echo off
:: ──────────────────────────────────────────────────────────────
:: run.bat — Launch Password Generator on Windows
:: ──────────────────────────────────────────────────────────────

cd /d "%~dp0"

where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8 or newer.
    echo         Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Using:
python --version

echo [INFO] Starting Password Generator...
echo.

python main.py

pause
