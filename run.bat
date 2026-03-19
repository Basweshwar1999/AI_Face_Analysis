@echo off
set PYTHONNOUSERSITE=1
echo ===================================================
echo     AI Face Analysis System - Environment Setup
echo ===================================================

if not exist "venv\" (
    echo Creating isolated virtual environment...
    python -m venv venv
)

echo Activating environment...
call venv\Scripts\activate.bat

echo Installing dependencies into local venv safely...
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Dependency installation failed! 
    echo Please make sure you close ALL running Streamlit terminals.
    pause
    exit /b %errorlevel%
)

echo.
echo ===================================================
echo     Starting Streamlit Application...
echo ===================================================
venv\Scripts\python.exe -m streamlit run app.py

pause
