@echo off
echo ====================================
echo  PDF Reports System - Quick Setup
echo ====================================
echo.

echo Checking prerequisites...

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

:: Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org
    pause
    exit /b 1
)

echo Prerequisites check passed!
echo.

:: Create reports directory if it doesn't exist
if not exist "reports\" (
    echo Creating reports directory...
    mkdir reports
    mkdir reports\financial_reports
    mkdir reports\project_updates
    mkdir reports\technical_docs
    mkdir reports\hr_documents
    mkdir reports\marketing_analytics
)

:: Setup backend
echo Setting up backend...
cd backend
if not exist "venv\" (
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt

:: Generate sample PDFs
echo Generating sample PDFs...
cd ..\scripts
python create_sample_pdfs.py

echo.
echo Setup complete!
echo.
echo To start the application:
echo 1. Run start_backend.bat
echo 2. Run start_frontend.bat (in a new window)
echo 3. Open http://localhost:3000 in your browser
echo.
pause