# PyTorch ResNet50 Image Classifier - PowerShell Setup Script
# ============================================================

Write-Host "PyTorch ResNet50 Image Classifier - Setup Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if command was successful
function Test-LastCommand {
    param([string]$ErrorMessage)
    # Initialize LASTEXITCODE if not defined
    if (-not (Get-Variable -Name LASTEXITCODE -ErrorAction SilentlyContinue)) {
        $global:LASTEXITCODE = 0
    }
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host $ErrorMessage -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Check PowerShell execution policy
Write-Host "Checking PowerShell execution policy..." -ForegroundColor Yellow
$executionPolicy = Get-ExecutionPolicy
Write-Host "Current execution policy: $executionPolicy" -ForegroundColor Cyan

if ($executionPolicy -eq "Restricted") {
    Write-Host "⚠ Execution policy is Restricted. You may need to allow script execution." -ForegroundColor Yellow
    Write-Host "Run this command in an elevated PowerShell:" -ForegroundColor Yellow
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine" -ForegroundColor White
    Write-Host "Or for current user only:" -ForegroundColor Yellow
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor White
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        exit 1
    }
} elseif ($executionPolicy -in @("Bypass", "Unrestricted", "RemoteSigned", "AllSigned")) {
    Write-Host "✓ Execution policy allows script execution" -ForegroundColor Green
} else {
# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonFound = $false
try {
    $output = & python --version 2>&1
    # Initialize LASTEXITCODE if not defined
    if (-not (Get-Variable -Name LASTEXITCODE -ErrorAction SilentlyContinue)) {
        $global:LASTEXITCODE = 0
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Found Python: $output" -ForegroundColor Green
        $pythonFound = $true
    }
} catch {
    # Python not found
}
        $pythonFound = $true
    }
} catch {
Write-Host ""
Write-Host "Setting up virtual environment..." -ForegroundColor Yellow
python -m pip install virtualenv
python -m virtualenv env
Test-LastCommand "Error creating virtual environment"
    Write-Host "✗ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.9+ from https://python.org" -ForegroundColor Yellow
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
try {
    & ".\env\Scripts\Activate.ps1"
} catch {
    Write-Host "⚠ Could not activate virtual environment script (execution policy)" -ForegroundColor Yellow
}
Test-LastCommand "Error creating virtual environment"

Write-Host "✓ Virtual environment created successfully" -ForegroundColor Green

Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
try {
    & ".\venv\Scripts\Activate.ps1"
} catch {
    Write-Host "⚠ Could not activate virtual environment script (execution policy)" -ForegroundColor Yellow
}

# Check if activation was successful
if ($env:VIRTUAL_ENV) {
    Write-Host "✓ Virtual environment activated: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "⚠ Virtual environment may not be activated properly" -ForegroundColor Yellow
    Write-Host "This might be due to execution policy settings, but we can continue..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
Test-LastCommand "Error upgrading pip"

Write-Host "✓ pip upgraded successfully" -ForegroundColor Green

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes (downloading PyTorch)..." -ForegroundColor Cyan
pip install -r requirements.txt
Test-LastCommand "Error installing dependencies"

Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green

Write-Host ""
Write-Host "Running demo script..." -ForegroundColor Yellow
python demo.py
Test-LastCommand "Error running demo script"

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  - Run specific tests: python -m pytest tests/test_model.py" -ForegroundColor White
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Cyan
Write-Host "  1. Use PowerShell scripts: .\run_app.ps1" -ForegroundColor White
Write-Host "  2. Or manually: python main.py" -ForegroundColor White
Write-Host "  3. Run tests: .\run_tests.ps1" -ForegroundColor White
Write-Host ""
Write-Host "For development:" -ForegroundColor Cyan
Write-Host "  - Format code: black ." -ForegroundColor White
Write-Host "  - Lint code: flake8 ." -ForegroundColor White
Write-Host "  - Run specific tests: pytest tests/test_model.py" -ForegroundColor White
Write-Host ""
Write-Host "Note: If you encounter execution policy issues with .ps1 scripts," -ForegroundColor Yellow
Write-Host "you can always use the Python scripts directly (python main.py, etc.)" -ForegroundColor Yellow
Write-Host ""

Read-Host "Press Enter to exit"

setup_bypass.bat
