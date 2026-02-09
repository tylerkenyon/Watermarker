@echo off
REM Watermarker installation script for Windows
REM This script adds the watermark.py to your PATH

echo ========================================
echo Watermarker Installation Script
echo ========================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Python found!
echo.

REM Install required packages
echo Installing required Python packages...
python -m pip install -r "%SCRIPT_DIR%requirements.txt"
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

REM Create a batch file wrapper in the same directory
echo Creating watermark command wrapper...
(
echo @echo off
echo python "%SCRIPT_DIR%watermark.py" %%*
) > "%SCRIPT_DIR%watermark.cmd"

echo.
echo ========================================
echo Installation Options
echo ========================================
echo.
echo The watermark tool is now ready to use!
echo.
echo To use it, you have two options:
echo.
echo 1. Add to PATH manually:
echo    - Add this directory to your PATH environment variable:
echo      %SCRIPT_DIR%
echo    - Then you can run 'watermark' from anywhere
echo.
echo 2. Use from this directory:
echo    - Navigate to %SCRIPT_DIR%
echo    - Run: watermark --path yourimage.jpg --text "Your Text"
echo.
echo Would you like to add this directory to your PATH now?
echo (This requires administrator privileges)
echo.
set /p ADD_TO_PATH="Add to PATH? (y/n): "

if /i "%ADD_TO_PATH%"=="y" (
    echo.
    echo Adding to PATH...
    
    REM Add to user PATH (doesn't require admin)
    for /f "skip=2 tokens=3*" %%a in ('reg query HKCU\Environment /v PATH 2^>nul') do set USER_PATH=%%b
    
    REM Check if already in PATH
    echo %USER_PATH% | find /i "%SCRIPT_DIR%" >nul
    if %errorlevel% equ 0 (
        echo Directory is already in PATH!
    ) else (
        setx PATH "%USER_PATH%;%SCRIPT_DIR%"
        echo.
        echo Successfully added to PATH!
        echo Please restart your command prompt for changes to take effect.
    )
) else (
    echo.
    echo Skipping PATH addition.
    echo You can manually add the directory to PATH later.
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Usage Examples:
echo   watermark --path image.jpg --text "CONFIDENTIAL"
echo   watermark  (for interactive mode)
echo.
echo For more information, run: watermark --help
echo.
pause
