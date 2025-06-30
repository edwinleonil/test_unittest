# PyTorch ResNet50 Image Classifier - PowerShell Application Runner
# ================================================================

Write-Host "PyTorch ResNet50 Image Classifier - Application Runner" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Function to check if command was successful
function Test-LastCommand {
    param([string]$ErrorMessage)
    if ($LASTEXITCODE -ne 0) {
        Write-Host $ErrorMessage -ForegroundColor Red
        return $false
    }
    return $true
}

# Get project root directory
$projectRoot = $PSScriptRoot

# Change to project directory
Set-Location $projectRoot

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠ Virtual environment not detected" -ForegroundColor Yellow
    Write-Host "Attempting to activate virtual environment..." -ForegroundColor Yellow
    
    $venvActivate = Join-Path $projectRoot "venv\Scripts\Activate.ps1"
    if (Test-Path $venvActivate) {
        & $venvActivate
        if ($env:VIRTUAL_ENV) {
            Write-Host "✓ Virtual environment activated" -ForegroundColor Green
        } else {
            Write-Host "⚠ Could not activate virtual environment" -ForegroundColor Yellow
            Write-Host "You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✗ Virtual environment not found. Run setup.ps1 first." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "✓ Virtual environment is active: $env:VIRTUAL_ENV" -ForegroundColor Green
}

# Check if main.py exists
$mainScript = Join-Path $projectRoot "main.py"
if (-not (Test-Path $mainScript)) {
    Write-Host "✗ main.py not found in project directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✓ Application script found: $mainScript" -ForegroundColor Green

# Check if dependencies are installed
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import torch, torchvision, PIL; print('✓ Core dependencies available')"
    Write-Host "✓ Core dependencies are installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Missing dependencies. Run setup.ps1 first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Starting PyTorch ResNet50 Image Classifier..." -ForegroundColor Green
Write-Host "Please wait while the model loads..." -ForegroundColor Cyan
Write-Host ""

# Run the application
try {
    python main.py
    
    if (Test-LastCommand "Application finished") {
        Write-Host ""
        Write-Host "Application closed successfully." -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "Application encountered an error." -ForegroundColor Red
    }
} catch {
    Write-Host ""
    Write-Host "Error starting application: $_" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"
