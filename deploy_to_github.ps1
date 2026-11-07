<#
.SYNOPSIS
    Janus Core Automated GitHub Deployment Script for PowerShell & Antigravity
#>

[CmdletBinding()]
param(
    [string]$Branch = "main",
    [string]$Message = ""
)

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   Janus Core: Automated GitHub Deployment (PowerShell) " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

# 1. Preflight Test Execution
Write-Host "`n[1/4] Running preflight test suite..." -ForegroundColor Yellow
$testResult = python run_tests.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Test suite failed! Deployment aborted." -ForegroundColor Red
    exit 1
}
Write-Host "[PASS] Preflight tests verified successfully." -ForegroundColor Green

# 2. Stage All Modifications
Write-Host "`n[2/4] Staging file modifications..." -ForegroundColor Yellow
git add -A

# 3. Check Git Status
$stagedChanges = git diff --cached --name-only
if (-not $stagedChanges) {
    Write-Host "[INFO] No staged modifications detected. Repository is up-to-date." -ForegroundColor Cyan
    exit 0
}

# 4. Commit Changes
if (-not $Message) {
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $Message = "Janus Core Update: Automated session deployment [$timestamp]"
}
Write-Host "`n[3/4] Committing changes: '$Message'..." -ForegroundColor Yellow
git commit -m "$Message"

# 5. Push to GitHub
Write-Host "`n[4/4] Pushing changes to remote ($Branch)..." -ForegroundColor Yellow
git push origin $Branch
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARNING] Direct push to $Branch failed. Attempting default git push..." -ForegroundColor Yellow
    git push
}

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host "   Janus Core deployed to GitHub successfully!          " -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
