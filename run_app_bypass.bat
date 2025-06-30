@echo off
echo Starting PyTorch ResNet50 Image Classifier...
echo This will run the PowerShell app runner with bypass execution policy.
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0run_app.ps1"

pause
