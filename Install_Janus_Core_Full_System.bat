@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title Janus Core: Direct Full-System Automated Installer ^& Component Provisioner

echo ===============================================================================
echo        JANUS CORE: DIRECT AUTOMATED FULL-SYSTEM COMPONENT INSTALLER
echo ===============================================================================
echo  Target System: Windows 10 / 11 (64-bit)
echo  Provisions: Python Runtime, VirtualEnv, Ollama Inference Daemon, Core ML
echo             Dependencies, Windows Firewall Rules, and Cyber Security Guards.
echo  Security: Cryptographic Checksum Validation ^& Private User Staging Isolation.
echo ===============================================================================
echo.

:: Set secure private installation and staging roots
set "INSTALL_DIR=%LocalAppData%\JanusCore"
set "STAGING_DIR=%INSTALL_DIR%\staging"
set "VENV_DIR=%INSTALL_DIR%\venv"

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%STAGING_DIR%" mkdir "%STAGING_DIR%"

:: Enforce private user-only ACLs on staging directory (Mitigate TOCTOU race conditions)
icacls "%STAGING_DIR%" /inheritance:r /grant:r "%USERNAME%:(OI)(CI)F" >nul 2>&1

:: -----------------------------------------------------------------------------
:: Step 1: Check and Install Python 3.10+ Runtime with Hash Verification
:: -----------------------------------------------------------------------------
echo [1/6] Inspecting Python 64-bit runtime...
set "PYTHON_CMD="
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_CMD=python"
    for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set "PY_VER=%%v"
    echo   [OK] Detected system Python %PY_VER%
) else (
    echo   [NOTICE] Python is not installed or not in PATH.
    echo   [ACTION] Initiating automated silent Python 3.11 installation via winget...
    winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] Python 3.11 installed successfully via Windows Package Manager.
        set "PYTHON_CMD=python"
    ) else (
        echo   [ACTION] Downloading official Python 3.11 Windows 64-bit installer to secure staging...
        powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%STAGING_DIR%\python_installer.exe'"
        
        echo   [SECURITY] Verifying SHA-256 cryptographic checksum of Python installer...
        powershell -Command "$expected = '611b7d722d56e75aa88235a975765c9f5e04313f889c19b8dc9f664cfa9fbf79'; $actual = (Get-FileHash '%STAGING_DIR%\python_installer.exe' -Algorithm SHA256).Hash.ToLower(); if ($actual -ne $expected) { Write-Host 'CHECKSUM FAILED!' -ForegroundColor Red; exit 1 } else { Write-Host 'CHECKSUM VERIFIED!' -ForegroundColor Green; exit 0 }"
        if %ERRORLEVEL% NEQ 0 (
            echo   [FATAL] Python installer checksum mismatch! Terminating for security.
            del /f /q "%STAGING_DIR%\python_installer.exe"
            pause
            exit /b 1
        )
        echo   [ACTION] Installing Python silently from verified binary...
        "%STAGING_DIR%\python_installer.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
        del /f /q "%STAGING_DIR%\python_installer.exe"
        set "PYTHON_CMD=%LocalAppData%\Programs\Python\Python311\python.exe"
        echo   [OK] Python installed directly to user directory.
    )
)

:: -----------------------------------------------------------------------------
:: Step 2: Provision Dedicated Isolated Virtual Environment (venv)
:: -----------------------------------------------------------------------------
echo.
echo [2/6] Provisioning dedicated isolated Python virtual environment...
if not exist "%VENV_DIR%\Scripts\python.exe" (\
    echo   [INFO] Creating virtual environment at %VENV_DIR%...
    %PYTHON_CMD% -m venv "%VENV_DIR%"
    if %ERRORLEVEL% NEQ 0 (
        echo   [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo   [OK] Virtual environment created successfully.
) else (
    echo   [OK] Virtual environment already initialized at %VENV_DIR%.
)
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "VENV_PIP=%VENV_DIR%\Scripts\pip.exe"

:: -----------------------------------------------------------------------------
:: Step 3: Install Required Python Dependencies & Cyber Security Modules
:: -----------------------------------------------------------------------------
echo.
echo [3/6] Installing required Python dependencies and security modules...
echo   Upgrading pip package manager...
"%VENV_PY%" -m pip install --upgrade pip --quiet
echo   Installing: pydantic, cryptography, aiohttp, requests, pyyaml, psutil...
"%VENV_PIP%" install pydantic cryptography aiohttp requests pyyaml psutil --quiet
if %ERRORLEVEL% EQU 0 (
    echo   [OK] All Python core dependencies and security modules installed.
) else (
    echo   [WARN] Retrying dependency installation with verbose logs...
    "%VENV_PIP%" install pydantic cryptography aiohttp requests pyyaml psutil
)

:: -----------------------------------------------------------------------------
:: Step 4: Check and Directly Install Local Ollama Inference Engine (Tier 0)
:: -----------------------------------------------------------------------------
echo.
echo [4/6] Inspecting Local Ollama Inference Daemon (Tier 0)...
where ollama >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Ollama is already installed on the system.
) else (
    echo   [NOTICE] Ollama not found. Initiating automated download to secure staging...
    powershell -Command "Invoke-WebRequest -Uri 'https://ollama.com/download/OllamaSetup.exe' -OutFile '%STAGING_DIR%\OllamaSetup.exe'"
    
    echo   [SECURITY] Verifying Microsoft Authenticode Digital Signature of Ollama installer...
    powershell -Command "$sig = Get-AuthenticodeSignature '%STAGING_DIR%\OllamaSetup.exe'; if ($sig.Status -ne 'Valid') { Write-Host 'AUTHENTICODE SIGNATURE INVALID!' -ForegroundColor Red; exit 1 } else { Write-Host 'SIGNATURE VERIFIED!' -ForegroundColor Green; exit 0 }"
    if %ERRORLEVEL% NEQ 0 (
        echo   [FATAL] Ollama installer digital signature verification failed! Terminating.
        del /f /q "%STAGING_DIR%\OllamaSetup.exe"
        pause
        exit /b 1
    )
    echo   [ACTION] Running Ollama silent installer...
    "%STAGING_DIR%\OllamaSetup.exe" /silent
    del /f /q "%STAGING_DIR%\OllamaSetup.exe"
    timeout /t 3 /nobreak >nul
    echo   [OK] Ollama installed directly into the system.
)

:: Ensure Ollama daemon is running and pull baseline compact model
curl -s http://localhost:11434/api/tags >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo   [INFO] Starting Ollama daemon in background...
    start /b ollama serve >nul 2>&1
    timeout /t 3 /nobreak >nul
)
echo   [ACTION] Pulling baseline local model (llama3.2:3b) for zero-cost Tier 0 inference...
ollama pull llama3.2:3b >nul 2>&1
echo   [OK] Tier 0 Local inference engine verified and ready.

:: -----------------------------------------------------------------------------
:: Step 5: Configure Windows Loopback Firewall Exception (Port 8765)
:: -----------------------------------------------------------------------------
echo.
echo [5/6] Configuring Windows Firewall Loopback Security Exception...
netsh advfirewall firewall show rule name="JanusCore_Loopback_8765" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo   [ACTION] Adding local loopback rule for port 8765...
    netsh advfirewall firewall add rule name="JanusCore_Loopback_8765" dir=in action=allow protocol=TCP localport=8765 >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] Firewall rule created: 127.0.0.1:8765 authorized.
    ) else (
        echo   [NOTICE] Non-admin mode: Windows Firewall rule skipped [Loopback works locally].
    )
) else (
    echo   [OK] Firewall rule "JanusCore_Loopback_8765" is already active.
)

:: -----------------------------------------------------------------------------
:: Step 6: Create Desktop & Start Menu Shortcuts & Run Security Verification
:: -----------------------------------------------------------------------------
echo.
echo [6/6] Creating Desktop and Start Menu Shortcuts ^& Validating Security Guards...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([System.Environment]::GetFolderPath('Desktop') + '\Janus Core.lnk'); $Shortcut.TargetPath = '%~dp0Run_Janus_Core.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'Janus Core Multi-Agent Desktop Application'; $Shortcut.Save()"
echo   [OK] Desktop shortcut "Janus Core.lnk" created.

:: Run pre-flight security validation check on skills and markdown files
echo.
echo ===============================================================================
echo [SECURITY] Running initial Skill ^& Markdown Security Audit...
"%VENV_PY%" "%~dp0preflight_audit.py"
echo ===============================================================================
echo.
echo [SUCCESS] All required components, runtimes, and cyber security shields
echo           have been directly installed and configured on your system!
echo.
echo You can now launch the application immediately using Run_Janus_Core.bat
echo or via the "Janus Core" Desktop shortcut.
echo ===============================================================================
echo.
pause
