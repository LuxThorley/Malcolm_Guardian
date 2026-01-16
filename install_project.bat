@echo off
setlocal

echo [Malcolm Guardian Installer]
echo.

REM Check Python
py -3 --version >nul 2>&1
if errorlevel 1 (
    echo Python 3 is not installed or not on PATH.
    echo Please install Python 3.9+ from https://www.python.org/downloads/ and try again.
    pause
    goto :eof
)

echo Creating virtual environment (.venv)...
py -3 -m venv .venv
if errorlevel 1 (
    echo Failed to create virtual environment.
    pause
    goto :eof
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    echo You may need to run this script as Administrator or check your internet connection.
    pause
    goto :eof
)

if not exist "logs" (
    mkdir logs
)

if not exist "config\\config.yaml" (
    echo Creating default config\\config.yaml...
    mkdir config 2>nul
    copy /Y config\\config.yaml config\\config.yaml >nul 2>&1
)

echo.
echo [DONE] Malcolm Guardian environment is ready.
echo To start Malcolm Guardian, run:
echo   run_guardian.bat
echo.
pause
