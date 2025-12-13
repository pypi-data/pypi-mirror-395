# setup-dev.ps1 - Windows development environment setup for prism-view
# Usage: .\setup-dev.ps1

$ErrorActionPreference = "Stop"

# Set UTF-8 encoding for emoji support
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'

Write-Host ""
Write-Host "    ██████╗ ██████╗ ██╗███████╗███╗   ███╗" -ForegroundColor Magenta
Write-Host "    ██╔══██╗██╔══██╗██║██╔════╝████╗ ████║" -ForegroundColor Magenta
Write-Host "    ██████╔╝██████╔╝██║███████╗██╔████╔██║" -ForegroundColor Cyan
Write-Host "    ██╔═══╝ ██╔══██╗██║╚════██║██║╚██╔╝██║" -ForegroundColor Cyan
Write-Host "    ██║     ██║  ██║██║███████║██║ ╚═╝ ██║" -ForegroundColor Blue
Write-Host "    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚═╝" -ForegroundColor Blue
Write-Host ""
Write-Host "    prism-view Development Setup" -ForegroundColor White
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}
Write-Host "Found: $pythonVersion" -ForegroundColor Green

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "Virtual environment already exists, reusing..." -ForegroundColor Gray
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to upgrade pip" -ForegroundColor Red
    exit 1
}

# Install package in editable mode with dev dependencies
Write-Host "Installing prism-view with dev dependencies..." -ForegroundColor Yellow
pip install -e ".[dev]"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install prism-view" -ForegroundColor Red
    exit 1
}

# Verify installation
Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Yellow
$verifyResult = python -c "from prism.view import __version__; print(f'prism-view v{__version__}')" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "$verifyResult installed successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "  Setup complete!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "WARNING: Installation may have issues" -ForegroundColor Yellow
    Write-Host "The package installed but verification failed." -ForegroundColor Yellow
    Write-Host "This is expected if __init__.py is not yet complete." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "To activate the virtual environment:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To run tests:" -ForegroundColor Cyan
Write-Host "  pytest" -ForegroundColor White
Write-Host ""
Write-Host "To run tests with coverage:" -ForegroundColor Cyan
Write-Host "  pytest --cov=src/prism/view --cov-report=term-missing" -ForegroundColor White
Write-Host ""
