@echo off
set PYTHONNOUSERSITE=1
echo ===================================================
echo     AI Face Analysis System - Production Build
echo ===================================================

if not exist "venv\" (
    echo [ERROR] Virtual environment missing! Please run run.bat first to build your environment.
    pause
    exit /b 1
)

echo Activating environment...
call venv\Scripts\activate.bat

echo Installing PyInstaller...
python -m pip install pyinstaller
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install PyInstaller.
    pause
    exit /b 1
)

echo.
echo ===================================================
echo Starting PyInstaller Compilation...
echo WARNING: This process may take 5 - 10 minutes depending on your CPU.
echo          It is packaging gigabytes of AI models!
echo ===================================================
python build_exe.py

echo.
echo ===================================================
echo DONE!
echo Your production executable is located in:
echo   dist\AI_Face_Analysis\
echo.
echo You can zip this entire AI_Face_Analysis folder and share it with colleagues.
echo They can just double-click "AI_Face_Analysis.exe" inside the folder!
echo ===================================================
pause
