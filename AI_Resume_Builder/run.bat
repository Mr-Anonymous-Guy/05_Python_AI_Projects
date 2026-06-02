@echo off
:: ──────────────────────────────────────────────────────────────
:: run.bat — Launch AI Resume Builder on Windows
:: ──────────────────────────────────────────────────────────────

cd /d "%~dp0"

echo ╔══════════════════════════════════════════════════════╗
echo ║        AI RESUME BUILDER - Flask Application         ║
echo ╚══════════════════════════════════════════════════════╝
echo.

:: ── Python check ──────────────────────────────────────────────
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python not found. Install Python 3.8+
    pause
    exit /b 1
)

echo [OK] Using:
python --version

:: ── Ollama check ──────────────────────────────────────────────
where ollama >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [WARN] Ollama not found.
    echo        AI features require Ollama to be installed.
    echo        Visit: https://ollama.ai
    echo.
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i not "%CONTINUE%"=="y" exit /b 1
) else (
    echo [OK] Ollama is installed
)

:: ── Dependencies ──────────────────────────────────────────────
python -c "import flask" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo.
    echo [INFO] Installing dependencies...
    python -m pip install -r requirements.txt
)

echo.
echo [INFO] Starting Flask server...
echo        URL: http://localhost:5000
echo        Press CTRL+C to stop
echo.

python app.py

pause
