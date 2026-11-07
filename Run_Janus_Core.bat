@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title Janus Core: Autonomous Multi-Agent Desktop Launcher ^& Cyber Guard

echo ===============================================================================
echo JANUS CORE: Autonomous Multi-Agent Architecture
echo Dual-Horizon Inference, Cityscape Command Center ^& Cyber Security Shield
echo ===============================================================================
echo.

set "INSTALL_DIR=%LocalAppData%\JanusCore"
set "VENV_DIR=%INSTALL_DIR%\venv"

:: 1. Check if compiled standalone executable exists
if exist "%~dp0dist\JanusCore.exe" (
    echo [INFO] Found compiled binary: dist\JanusCore.exe
    echo [INFO] Launching Janus Core standalone...
    start "" "%~dp0dist\JanusCore.exe"
    exit /b 0
)

:: 2. Check for isolated Virtual Environment
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [NOTICE] Janus Core environment is not yet provisioned.
    echo [ACTION] Invoking automated direct component installer...
    call "%~dp0Install_Janus_Core_Full_System.bat"
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Installation failed. Please check the logs above.
        pause
        exit /b 1
    )
)

set "PY_EXE=%VENV_DIR%\Scripts\python.exe"

:: 3. Check Local Ollama daemon status (Tier 0)
echo [1/3] Checking Local Ollama daemon status (Tier 0)...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Local Ollama daemon active on http://localhost:11434.
) else (
    where ollama >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo [INFO] Starting Ollama daemon in background...
        start /b ollama serve >nul 2>&1
        timeout /t 2 /nobreak >nul
    ) else (
        echo [NOTICE] Ollama not detected. Multi-agent router will use Tier 1/2 cloud failover.
    )
)

:: 4. Run Pre-flight Cyber Security Audit on Skills and Markdown files
echo.
echo [2/3] Executing Cyber Security Pre-Flight Audit on Skills ^& Markdown...
"%PY_EXE%" "%~dp0preflight_audit.py"

:: 5. Launch Janus Core Desktop Server & UI Dashboard
echo.
echo [3/3] Starting Janus Core Server on http://127.0.0.1:8765...
echo Dashboard opening automatically in your default browser...
echo.
echo [NOTE] Keep this window open. Press CTRL+C to terminate gracefully.
echo ===============================================================================
echo.

cd /d "%~dp0"
"%PY_EXE%" desktop_app.py

pause
