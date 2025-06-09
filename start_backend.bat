@echo off
echo ====================================
echo   PDF Reports System - Backend
echo ====================================
echo.

:: Check if virtual environment exists
if not exist "venv\" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Make sure Python is installed and added to PATH
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

:: Start the backend server
echo.
echo Starting FastAPI backend server...
echo Backend will be available at: http://localhost:8001
echo Press Ctrl+C to stop the server
echo.
python server.py

pause