@echo off
REM Marketing Research AI - Startup Script (Windows)
REM For MachinePoem.agency

echo 🎯 Starting Marketing Research AI...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\installed" (
    echo 📦 Installing requirements...
    pip install -r requirements.txt
    echo. > venv\installed
    echo ✅ Requirements installed
    echo.
)

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found!
    echo Creating .env from template...
    copy .env.example .env
    echo.
    echo ❗ Please edit .env and add your API keys before continuing
    echo    Required: ANTHROPIC_API_KEY
    echo.
    pause
)

REM Start the app
echo.
echo 🚀 Launching Streamlit app...
echo.
streamlit run app.py
