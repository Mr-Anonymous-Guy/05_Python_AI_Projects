@echo off
:: run.bat - Run EduSense on Windows

echo ==============================================
echo        EduSense - AI Learning Platform
echo ==============================================

:: Check Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python not found. Please install Python.
    exit /b 1
)

:: Install Dependencies
echo [INFO] Checking dependencies...
python -m pip install -r requirements.txt >nul 2>&1

:: Run Streamlit
echo [INFO] Starting Streamlit UI...
python -m streamlit run app/main.py

pause
