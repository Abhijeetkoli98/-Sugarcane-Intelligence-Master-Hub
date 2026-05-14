@echo off
title Sugarcane AI Desktop Debugger
echo [1/3] Checking environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in your PATH.
    pause
    exit
)

echo [2/3] Verifying files...
if not exist "c:\Users\ABHIJEET\OneDrive\Desktop\sugarcane_app.pyw" (
    echo ERROR: Could not find sugarcane_app.pyw on your Desktop.
    pause
    exit
)

echo [3/3] Launching App...
python "c:\Users\ABHIJEET\OneDrive\Desktop\sugarcane_app.pyw"
if %errorlevel% neq 0 (
    echo.
    echo ERROR: The application crashed. Please see the error above.
    pause
)
exit
