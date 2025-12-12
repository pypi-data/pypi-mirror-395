# Run this from within the activated virtual environment
# Ensures modal command works properly

# Activate virtual environment
$venvPath = "..\..\..\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & $venvPath
} else {
    Write-Host "Error: Virtual environment not found at $venvPath" -ForegroundColor Red
    exit 1
}

# Check if modal is installed
try {
    $modalVersion = python -m modal --version 2>$null
    Write-Host "✓ Modal is installed: $modalVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Modal is not installed. Installing..." -ForegroundColor Yellow
    python -m pip install modal
}

# Run the Ceylon Modal agent example  
Write-Host "`nRunning Ceylon AI Modal example..." -ForegroundColor Cyan
python -m modal run examples\modal_examples\ceylon_modal_agent.py
