@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title Janus Core Standalone Binary Compiler

echo ===============================================================================
echo                JANUS CORE: STANDALONE EXECUTABLE BUILDER
echo ===============================================================================
echo Target Directory: %CD%
echo.

:: 1. Verify Python Installation
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python runtime is not installed or not in system PATH.
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

:: 2. Check for required core source files
if not exist "desktop_app.py" (
    echo [ERROR] "desktop_app.py" was not found in %CD%!
    echo Please ensure all files from the Janus Core suite are extracted into this folder.
    pause
    exit /b 1
)

:: 3. Automatically generate janus_core.spec if not found
if not exist "janus_core.spec" (
    echo [INFO] "janus_core.spec" not found. Generating build spec dynamically...
    (
        echo # -*- mode: python ; coding: utf-8 -*-
        echo datas = [
        echo     ^('cityscape_agent_dashboard.html', '.'^),
        echo     ^('specs', 'specs'^),
        echo     ^('tests', 'tests'^),
        echo     ^('logging_config.py', '.'^),
        echo     ^('security_manager.py', '.'^),
        echo     ^('token_optimized_multiagent.py', '.'^)
        echo ]
        echo if __import__^('os'^).path.exists^('results_window.html'^):
        echo     datas.append^(^('results_window.html', '.'^)^)
        echo a = Analysis^(
        echo     ['desktop_app.py'],
        echo     pathex=[],
        echo     binaries=[],
        echo     datas=datas,
        echo     hiddenimports=['pydantic', 'cryptography', 'aiohttp', 'pyyaml', 'psutil'],
        echo     hookspath=[],
        echo     hooksconfig={},
        echo     runtime_hooks=[],
        echo     excludes=['tkinter', 'matplotlib'],
        echo     noarchive=False,
        echo     optimize=0,
        echo ^)
        echo pyz = PYZ^(a.pure^)
        echo exe = EXE^(
        echo     pyz,
        echo     a.scripts,
        echo     a.binaries,
        echo     a.datas,
        echo     [],
        echo     name='JanusCore',
        echo     debug=False,
        echo     bootloader_ignore_signals=False,
        echo     strip=False,
        echo     upx=True,
        echo     upx_exclude=[],
        echo     runtime_tmpdir=None,
        echo     console=True,
        echo     disable_windowed_traceback=False,
        echo     argv_emulation=False,
        echo     target_arch=None,
        echo     codesign_identity=None,
        echo     entitlements_file=None,
        echo ^)
    ) > "%~dp0janus_core.spec"
    echo   [OK] Generated janus_core.spec successfully.
)

:: 4. Verify & Install PyInstaller and Build Dependencies
echo.
echo [1/3] Verifying and installing PyInstaller and dependencies...
python -m pip install pyinstaller pydantic cryptography aiohttp pyyaml psutil --quiet

:: 5. Clean Previous Artifacts
echo.
echo [2/3] Cleaning previous build artifacts...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

:: 6. Compile Executable
echo.
echo [3/3] Compiling JanusCore.exe with PyInstaller...
python -m PyInstaller --clean --noconfirm janus_core.spec

:: 7. Verify Output Binary
if exist "dist\JanusCore.exe" (
    echo.
    echo ===============================================================================
    echo [SUCCESS] Binary successfully generated!
    echo Location: %CD%\dist\JanusCore.exe
    echo You can now launch "dist\JanusCore.exe" or use "Run_Janus_Core.bat".
    echo ===============================================================================
) else (
    echo.
    echo [ERROR] Expected output "dist\JanusCore.exe" was not found. Build failed.
    echo Please review the compiler output above for missing packages or syntax errors.
)

pause
