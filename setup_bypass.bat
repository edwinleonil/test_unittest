@echo off
echo Starting PyTorch ResNet50 Image Classifier Setup...
echo This will run the PowerShell setup script with bypass execution policy.
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0setup.ps1"

echo.
echo Setup script completed.
pause
