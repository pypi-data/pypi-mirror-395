#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"

Write-Host "==> Testing package installation"

# Create temporary directory
$TempDir = New-Item -ItemType Directory -Path (Join-Path $env:TEMP ([System.IO.Path]::GetRandomFileName()))
Write-Host "==> Using temporary directory: $TempDir"

try {
    # Generate production requirements from pyproject.toml
    Write-Host "==> Extracting production dependencies"
    uv export --format requirements-txt --no-dev --no-emit-project > "$TempDir/requirements.txt"

    Write-Host "==> Production dependencies:"
    Get-Content "$TempDir/requirements.txt"

    # Create virtual environment
    Write-Host "==> Creating virtual environment"
    python -m venv "$TempDir/venv"

    # Activate virtual environment
    & "$TempDir/venv/Scripts/Activate.ps1"

    # Install production dependencies
    Write-Host "==> Installing production dependencies"
    pip install --quiet --upgrade pip
    pip install --quiet -r "$TempDir/requirements.txt"

    # Clean old builds
    Write-Host "==> Cleaning old builds"
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue dist, build, *.egg-info

    # Build fresh package
    Write-Host "==> Building package"
    pip install --quiet build
    python -m build

    # Install the built package
    Write-Host "==> Installing built package"
    $wheel = Get-ChildItem -Path dist -Filter *.whl | Select-Object -First 1
    pip install --quiet $wheel.FullName

    # Test import
    Write-Host "==> Testing package import"
    python -c "from ghanon.cli import main; print('Import successful')"

    Write-Host "==> Installation test completed successfully"
}
finally {
    # Clean up
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $TempDir
}
