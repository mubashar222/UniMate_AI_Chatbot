@echo off
title UniMate AI - First Time Setup
cd /d "%~dp0"

echo ==========================================
echo       UniMate AI - First Time Setup
echo ==========================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed.
    echo Install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

where ollama >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Ollama is not installed or not in PATH.
    echo.
    echo Download Ollama for Windows:
    echo https://ollama.com/download/windows
    echo.
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
if not exist "venv\Scripts\python.exe" python -m venv venv

echo [2/4] Installing packages...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt

echo [3/4] Downloading local AI model...
ollama pull llama3.2:3b

echo [4/4] Setup complete.
echo.
echo Now run run.bat
echo.
pause
