@echo off
REM ============================================
REM HTTP Stub Server - Quick Start
REM ============================================
REM Double-click to start the server

echo.
echo ============================================
echo HTTP STUB SERVER - STARTING...
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Check if dependencies are installed
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Dependencies not installed!
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Start the server
echo Starting server on http://localhost:5600
echo.
echo Press Ctrl+C to stop the server
echo.
python server.py

pause
