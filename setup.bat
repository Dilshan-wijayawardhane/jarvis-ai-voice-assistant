@echo off
echo ========================================
echo   J.A.R.V.I.S — Setup Wizard
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    echo    Please ensure Python 3.11+ is installed
    pause
    exit /b 1
)
echo ✅ Virtual environment created
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated
echo.

echo Step 3: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    echo    Please check your internet connection
    pause
    exit /b 1
)
echo ✅ Dependencies installed
echo.

echo Step 4: Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo ✅ Created .env file
    echo.
    echo ⚠️  IMPORTANT: Edit .env and add your API key!
) else (
    echo ✅ .env file already exists
)
echo.

echo Step 5: Initializing database...
python scripts\init_database.py
if errorlevel 1 (
    echo ❌ Failed to initialize database
    pause
    exit /b 1
)
echo ✅ Database initialized
echo.

echo ========================================
echo   ✅ Setup Complete!
echo ========================================
echo.
echo To run JARVIS:
echo   run.py
echo.
echo Or use:
echo   python main.py --voice   (voice mode)
echo   python main.py --text    (text mode)
echo   python main.py --test    (test mode)
echo.
pause