@echo off
echo Starting PyTorch ResNet50 Test Runner...
echo This will run the PowerShell test runner with bypass execution policy.
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0run_tests.ps1"

pause
