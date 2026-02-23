@echo off
REM Setup script for Portfolio Backend on Windows

echo Configuring Portfolio Backend...
echo.

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv
if errorlevel 1 goto error

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 goto error

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 goto error

REM Copy environment file
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env and add your OpenRouter API key
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env and add your OpenRouter API key
echo 2. Run: python main.py
echo 3. Visit: http://localhost:8000/docs
echo.
goto end

:error
echo Error occurred during setup!
exit /b 1

:end
