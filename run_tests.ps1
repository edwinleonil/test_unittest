# PyTorch ResNet50 Image Classifier - PowerShell Test Runner
# =========================================================

Write-Host "PyTorch ResNet50 Image Classifier - Test Runner" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan
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
$srcPath = Join-Path $projectRoot "src"
$testsPath = Join-Path $projectRoot "tests"

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
        Write-Host "⚠ Virtual environment not found. Run setup.ps1 first." -ForegroundColor Yellow
    }
}

# Check if pytest is available
Write-Host "Checking pytest availability..." -ForegroundColor Yellow
try {
    $pytestVersion = python -m pytest --version 2>&1
    Write-Host "✓ pytest is available: $pytestVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ pytest is not installed" -ForegroundColor Red
    Write-Host "Install with: pip install pytest pytest-cov" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if test directory exists
if (-not (Test-Path $testsPath)) {
    Write-Host "✗ Tests directory not found: $testsPath" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✓ Tests directory found: $testsPath" -ForegroundColor Green

# Check if source directory exists
if (-not (Test-Path $srcPath)) {
    Write-Host "✗ Source directory not found: $srcPath" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✓ Source directory found: $srcPath" -ForegroundColor Green
Write-Host ""

# Run tests with coverage
Write-Host "Running tests with coverage..." -ForegroundColor Yellow
Write-Host "This may take a moment..." -ForegroundColor Cyan
Write-Host ""

$testArgs = @(
    "-m", "pytest",
    "-v",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html:htmlcov",
    "tests/"
)

try {
    & python $testArgs
    
    if (Test-LastCommand "Tests completed with errors") {
        Write-Host ""
        Write-Host "✓ All tests passed!" -ForegroundColor Green
        Write-Host "✓ Coverage report generated in htmlcov/" -ForegroundColor Green
        
        # Check if coverage HTML report was created
        $coverageReport = Join-Path $projectRoot "htmlcov\index.html"
        if (Test-Path $coverageReport) {
            Write-Host ""
            Write-Host "Coverage report available at: $coverageReport" -ForegroundColor Cyan
            $openReport = Read-Host "Open coverage report in browser? (y/N)"
            if ($openReport -eq 'y' -or $openReport -eq 'Y') {
                Start-Process $coverageReport
            }
        }
        
        $exitCode = 0
    } else {
        Write-Host ""
        Write-Host "✗ Some tests failed" -ForegroundColor Red
        $exitCode = 1
    }
} catch {
    Write-Host ""
    Write-Host "✗ Error running tests: $_" -ForegroundColor Red
    $exitCode = 1
}

Write-Host ""
Write-Host "Test run complete." -ForegroundColor Cyan

# Additional options
Write-Host ""
Write-Host "Additional test options:" -ForegroundColor Yellow
Write-Host "  - Run specific test file: python -m pytest tests/test_model.py -v" -ForegroundColor White
Write-Host "  - Run tests without coverage: python -m pytest tests/ -v" -ForegroundColor White
Write-Host "  - Run tests with more verbose output: python -m pytest tests/ -vv" -ForegroundColor White
Write-Host "  - Run only fast tests: python -m pytest tests/ -m 'not slow'" -ForegroundColor White

Write-Host ""
Read-Host "Press Enter to exit"

exit $exitCode
