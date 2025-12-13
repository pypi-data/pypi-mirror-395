@echo off
REM AI Browser Extension Server Management
REM Windows wrapper for unified Python server manager

REM Get script directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Detect and activate virtual environment
if exist ".venv-windows\Scripts\activate.bat" (
    call .venv-windows\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo Warning: No virtual environment found
)

REM Check for arguments
if "%1"=="" (
    echo Usage: server.bat {start^|stop^|restart^|status}
    exit /b 1
)

REM Call unified Python manager with all arguments
python aibe_server\server_manager.py %*