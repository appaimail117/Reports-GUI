@echo off
echo ====================================
echo   PDF Reports System - Frontend  
echo ====================================
echo.

:: Check if node_modules exists
if not exist "node_modules\" (
    echo Installing Node.js dependencies...
    npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo Make sure Node.js and npm are installed
        pause
        exit /b 1
    )
)

:: Start the frontend server
echo.
echo Starting React frontend server...
echo Frontend will be available at: http://localhost:3000
echo Press Ctrl+C to stop the server
echo.
npm start

pause