@echo off
REM ============================================
REM HTTP Stub Server - Python Installation
REM ============================================
REM Ye script automatically setup kar dega
REM Double-click karo ya CMD mein run karo

echo.
echo ============================================
echo HTTP STUB SERVER - PYTHON SETUP
echo ============================================
echo.

REM Check Python installation
echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python is installed
python --version
echo.

REM Install dependencies
echo [2/3] Installing dependencies...
echo This may take 1-2 minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)
echo [OK] Dependencies installed successfully
echo.

REM Check if config.json exists
echo [3/3] Checking configuration...
if not exist config.json (
    echo [ERROR] config.json not found!
    pause
    exit /b 1
)
echo [OK] Configuration file found
echo.

echo ============================================
echo SETUP COMPLETE!
echo ============================================
echo.
echo To start the server, run:
echo    python server.py
echo.
echo To test the API, run:
echo    python test_api.py
echo.
echo For documentation, read:
echo    README_PYTHON.md
echo    QUICK_START_HINDI.md
echo.
pause
