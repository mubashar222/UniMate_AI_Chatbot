@echo off
title UniMate AI - Local University Chatbot
cd /d "%~dp0"

echo ==========================================
echo        UniMate AI - Starting...
echo ==========================================
echo.

where ollama >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Ollama is not installed or not in PATH.
    echo Install it from: https://ollama.com/download/windows
    echo.
    pause
    exit /b 1
)

if not exist "venv\Scripts\python.exe" (
    echo [1/3] Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Could not create virtual environment.
        pause
        exit /b 1
    )
)

echo [2/3] Installing/updating Python packages...
venv\Scripts\python.exe -m pip install -r requirements.txt

echo [3/3] Checking local AI model...
ollama pull llama3.2:3b

echo.
echo Starting UniMate AI...
echo Browser: http://localhost:8501
echo.
venv\Scripts\python.exe -m streamlit run app.py

pause
