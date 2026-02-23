@echo off
REM Database Quick Start Script (Windows)
REM Run from: cmd terminal in VS Code
REM Command: backend\quickstart.bat

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║       Database Integration - Quick Start Setup             ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Step 1: Navigate to backend
echo → Navigating to backend directory...
cd backend
if errorlevel 1 (
    echo Error: backend directory not found
    exit /b 1
)
echo ✅ Backend directory ready
echo.

REM Step 2: Check Python
echo → Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8+
    exit /b 1
)
python --version
echo ✅ Python found
echo.

REM Step 3: Activate virtual environment
echo → Activating virtual environment...
if exist venv (
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo ⚠️  Virtual environment not found. Creating new one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment created
)
echo.

REM Step 4: Install dependencies
echo → Installing/updating dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo Error: Failed to install dependencies
    exit /b 1
)
echo ✅ Dependencies installed
echo.

REM Step 5: Initialize database
echo → Initializing database...
python init_db.py
if errorlevel 1 (
    echo Error: Database initialization failed
    exit /b 1
)
echo ✅ Database initialized
echo.

REM Step 6: Summary
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                   Setup Complete! 🎉                        ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo What's next?
echo.
echo 1. Start the backend server:
echo    python main.py
echo.
echo 2. Open API documentation:
echo    http://localhost:8000/docs
echo.
echo 3. Test an endpoint:
echo    curl -X POST http://localhost:8000/api/v1/conversations/start ^
echo    -H "Content-Type: application/json" ^
echo    -d "{\"user_name\": \"TestUser\"}"
echo.
echo 4. Check database connection:
echo    curl http://localhost:8000/api/v1/conversations/db-health
echo.
echo 5. Read documentation:
echo    - DATABASE.md
echo    - DATABASE_EXAMPLES.py
echo    - FRONTEND_INTEGRATION.py
echo.

set /p start_server="Start backend server now? (y/n): "
if /i "%start_server%"=="y" (
    echo Starting server...
    python main.py
)

endlocal
