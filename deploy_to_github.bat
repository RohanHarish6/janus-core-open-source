@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo   Janus Core: Automated GitHub Deployment Launcher
echo ========================================================
echo.

:: 1. Verify Git Installation
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not found in system PATH.
    echo Please install Git for Windows from https://git-scm.com/
    pause
    exit /b 1
)

:: 2. Run Test Suite Preflight
echo [1/4] Running Janus Core verification test suite...
python run_tests.py
if %errorlevel% neq 0 (
    echo [ERROR] Test suite failed! Deployment aborted to prevent broken builds.
    pause
    exit /b 1
)
echo [PASS] All unit tests verified.
echo.

:: 3. Stage Changes
echo [2/4] Staging file modifications...
git add -A

:: 4. Check for Changes
git diff --cached --quiet
if %errorlevel% equ 0 (
    echo [INFO] No changes detected to commit. Working directory clean.
    pause
    exit /b 0
)

:: 5. Commit Changes
set TIMESTAMP=%DATE% %TIME%
echo [3/4] Committing changes with automated session timestamp...
git commit -m "Janus Core Update: Automated session deployment [%TIMESTAMP%]"

:: 6. Push to GitHub
echo [4/4] Pushing to remote GitHub repository...
git push origin main
if %errorlevel% neq 0 (
    echo [WARNING] Direct push failed. Trying to push to current upstream branch...
    git push
)

echo.
echo ========================================================
echo   Deployment to GitHub completed successfully!
echo ========================================================
pause
