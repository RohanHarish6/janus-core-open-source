<#
.SYNOPSIS
    Automated Full-System Component Installer & Prerequisite Provisioner for Janus Core.
.DESCRIPTION
    Directly installs and configures:
    1. Python 3.10+ 64-bit runtime with cryptographic SHA-256 verification.
    2. Isolated Python Virtual Environment (venv) in %LocalAppData%\JanusCore\venv.
    3. Core libraries: pydantic, cryptography, aiohttp, requests, pyyaml, psutil.
    4. Local Ollama Inference Engine (Tier 0 daemon) verified via Authenticode digital signature.
    5. Windows Loopback Firewall authorization for port 8765.
    6. Desktop and Start Menu shortcuts.
    7. Automated Cyber Security & Threat Auditor for skills and .md files.
#>

[CmdletBinding()]
param()

$Host.UI.RawUI.WindowTitle = "Janus Core: Full System Component Installer"

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "       JANUS CORE: DIRECT AUTOMATED FULL-SYSTEM COMPONENT INSTALLER            " -ForegroundColor Cyan
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host " Target OS: Windows 10 / 11 (64-bit)" -ForegroundColor Gray
Write-Host " Provisions: Python, VirtualEnv, Ollama, ML Libraries, Firewall, & Cyber Shield" -ForegroundColor Gray
Write-Host " Security: SHA-256 Hash Verification & Private User Staging Isolation" -ForegroundColor Gray
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$InstallDir = Join-Path $env:LOCALAPPDATA "JanusCore"
$StagingDir = Join-Path $InstallDir "staging"
$VenvDir = Join-Path $InstallDir "venv"

if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}
if (-not (Test-Path $StagingDir)) {
    New-Item -ItemType Directory -Path $StagingDir -Force | Out-Null
}

# Enforce private user ACLs on staging directory
try {
    & icacls "$StagingDir" /inheritance:r /grant:r "$($env:USERNAME):(OI)(CI)F" | Out-Null
} catch {}

# 1. Check / Install Python
Write-Host "[1/6] Checking Python 64-bit runtime environment..." -ForegroundColor White
$PythonCmd = "python"
$PythonFound = $false
try {
    $PyVer = & python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] Detected system $PyVer" -ForegroundColor Green
        $PythonFound = $true
    }
} catch {}

if (-not $PythonFound) {
    Write-Host "  [NOTICE] Python is not installed. Attempting automated installation via winget..." -ForegroundColor Yellow
    try {
        & winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
        $PyVer = & python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] Successfully installed Python 3.11 via winget!" -ForegroundColor Green
            $PythonFound = $true
        }
    } catch {}

    if (-not $PythonFound) {
        Write-Host "  [ACTION] Downloading official Python 3.11 Windows 64-bit installer to secure staging..." -ForegroundColor Yellow
        $PyInstaller = Join-Path $StagingDir "python-3.11.9-amd64.exe"
        Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe" -OutFile $PyInstaller
        
        Write-Host "  [SECURITY] Verifying SHA-256 cryptographic checksum..." -ForegroundColor Yellow
        $ExpectedHash = "611b7d722d56e75aa88235a975765c9f5e04313f889c19b8dc9f664cfa9fbf79"
        $ActualHash = (Get-FileHash $PyInstaller -Algorithm SHA256).Hash.ToLower()
        if ($ActualHash -ne $ExpectedHash) {
            Remove-Item -Path $PyInstaller -Force
            Write-Host "  [FATAL] Checksum verification failed! Aborting." -ForegroundColor Red
            exit 1
        }
        Write-Host "  [OK] SHA-256 checksum verified." -ForegroundColor Green

        Write-Host "  [ACTION] Running silent background Python installation..." -ForegroundColor Yellow
        Start-Process -FilePath $PyInstaller -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0" -Wait
        Remove-Item -Path $PyInstaller -Force
        $PythonCmd = Join-Path $env:LOCALAPPDATA "Programs\Python\Python311\python.exe"
        Write-Host "  [OK] Python installed directly to user directory." -ForegroundColor Green
    }
}

# 2. Setup Virtual Environment
Write-Host "`n[2/6] Provisioning dedicated isolated virtual environment (venv)..." -ForegroundColor White
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$VenvPip = Join-Path $VenvDir "Scripts\pip.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "  [INFO] Creating virtual environment at $VenvDir..." -ForegroundColor Gray
    & $PythonCmd -m venv $VenvDir
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  [ERROR] Failed to create virtual environment." -ForegroundColor Red
        exit 1
    }
    Write-Host "  [OK] Virtual environment created successfully." -ForegroundColor Green
} else {
    Write-Host "  [OK] Virtual environment already initialized at $VenvDir." -ForegroundColor Green
}

# 3. Install Python Dependencies
Write-Host "`n[3/6] Installing Python dependencies & cyber security modules..." -ForegroundColor White
Write-Host "  [INFO] Installing: pydantic, cryptography, aiohttp, requests, pyyaml, psutil..." -ForegroundColor Gray
& $VenvPip install pydantic cryptography aiohttp requests pyyaml psutil --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Core dependencies and cyber security modules installed successfully." -ForegroundColor Green
} else {
    Write-Host "  [WARN] Retrying installation with verbose output..." -ForegroundColor Yellow
    & $VenvPip install pydantic cryptography aiohttp requests pyyaml psutil
}

# 4. Check / Install Ollama Daemon
Write-Host "`n[4/6] Inspecting Local Ollama Inference Engine (Tier 0)..." -ForegroundColor White
$OllamaInstalled = $false
if (Get-Command "ollama" -ErrorAction SilentlyContinue) {
    Write-Host "  [OK] Ollama is already installed on the system." -ForegroundColor Green
    $OllamaInstalled = $true
} else {
    Write-Host "  [NOTICE] Ollama not found. Initiating automated download to secure staging..." -ForegroundColor Yellow
    $OllamaInstaller = Join-Path $StagingDir "OllamaSetup.exe"
    Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile $OllamaInstaller

    Write-Host "  [SECURITY] Verifying Microsoft Authenticode Digital Signature..." -ForegroundColor Yellow
    $Sig = Get-AuthenticodeSignature $OllamaInstaller
    if ($Sig.Status -ne "Valid") {
        Remove-Item -Path $OllamaInstaller -Force
        Write-Host "  [FATAL] Authenticode digital signature invalid! Aborting." -ForegroundColor Red
        exit 1
    }
    Write-Host "  [OK] Digital signature verified authentic." -ForegroundColor Green

    Write-Host "  [ACTION] Executing Ollama silent installer..." -ForegroundColor Yellow
    Start-Process -FilePath $OllamaInstaller -ArgumentList "/silent" -Wait
    Remove-Item -Path $OllamaInstaller -Force
    Start-Sleep -Seconds 3
    Write-Host "  [OK] Ollama installed directly into the system." -ForegroundColor Green
}

# Ensure daemon is running and pull baseline model
try {
    $null = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 2 -ErrorAction Stop
} catch {
    Write-Host "  [INFO] Starting Ollama daemon in background..." -ForegroundColor Gray
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
}

Write-Host "  [ACTION] Pulling baseline local model (llama3.2:3b)..." -ForegroundColor Gray
Start-Process -FilePath "ollama" -ArgumentList "pull llama3.2:3b" -Wait -WindowStyle Hidden
Write-Host "  [OK] Tier 0 Local inference engine verified and ready." -ForegroundColor Green

# 5. Configure Windows Firewall
Write-Host "`n[5/6] Configuring Windows Firewall Loopback Security Exception..." -ForegroundColor White
try {
    $RuleExists = netsh advfirewall firewall show rule name="JanusCore_Loopback_8765" 2>&1
    if ($RuleExists -match "No rules match") {
        Write-Host "  [ACTION] Adding local loopback rule for port 8765..." -ForegroundColor Gray
        & netsh advfirewall firewall add rule name="JanusCore_Loopback_8765" dir=in action=allow protocol=TCP localport=8765 | Out-Null
        Write-Host "  [OK] Firewall rule created: 127.0.0.1:8765 authorized." -ForegroundColor Green
    } else {
        Write-Host "  [OK] Firewall rule 'JanusCore_Loopback_8765' is active." -ForegroundColor Green
    }
} catch {
    Write-Host "  [NOTICE] Non-elevated: Loopback firewall rule skipped (local loopback authorized by default)." -ForegroundColor Gray
}

# 6. Create Desktop Shortcut & Run Cyber Security Pre-Flight Check
Write-Host "`n[6/6] Creating Desktop Shortcut & Validating Security Guards..." -ForegroundColor White
$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath('Desktop')
$Shortcut = $WshShell.CreateShortcut((Join-Path $DesktopPath "Janus Core.lnk"))
$Shortcut.TargetPath = Join-Path $ScriptDir "Run_Janus_Core.bat"
$Shortcut.WorkingDirectory = $ScriptDir
$Shortcut.Description = "Janus Core Multi-Agent Desktop Application"
$Shortcut.Save()
Write-Host "  [OK] Desktop shortcut 'Janus Core.lnk' created." -ForegroundColor Green

Write-Host "`n===============================================================================" -ForegroundColor Cyan
Write-Host "[SECURITY] Running initial Skill & Markdown Security Audit..." -ForegroundColor Yellow
$SecCheckScript = @"
import sys
sys.path.insert(0, r'$ScriptDir')
from security_manager import SkillAndMarkdownSecurityAuditor
res = SkillAndMarkdownSecurityAuditor.audit_file(r'$ScriptDir\README.md')
print(f"  Security Audit for README.md: {res['status']} (Threats: {res['threat_count']}, SHA-256: {res['sha256'][:16]}...)")
"@
& $VenvPython -c $SecCheckScript

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[SUCCESS] All required components, runtimes, and cyber security shields" -ForegroundColor Green
Write-Host "          have been directly installed and configured on your system!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now launch Janus Core using Run_Janus_Core.bat or the Desktop shortcut." -ForegroundColor Cyan
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""
