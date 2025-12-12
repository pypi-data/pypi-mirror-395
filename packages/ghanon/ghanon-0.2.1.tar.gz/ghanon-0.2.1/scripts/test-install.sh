#!/usr/bin/env bash
set -euo pipefail

echo "==> Testing package installation"

# Create temporary directory
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

# Generate production requirements from pyproject.toml
echo "==> Extracting production dependencies"
uv export --format requirements-txt --no-dev --no-emit-project > "$TEMP_DIR/requirements.txt"

echo "==> Using temporary directory: $TEMP_DIR"

echo "==> Production dependencies:"
cat "$TEMP_DIR/requirements.txt"

# Create virtual environment
echo "==> Creating virtual environment"
python3 -m venv "$TEMP_DIR/venv"

# Activate virtual environment
source "$TEMP_DIR/venv/bin/activate"

# Install production dependencies
echo "==> Installing production dependencies"
pip install --quiet --upgrade pip
pip install --quiet -r "$TEMP_DIR/requirements.txt"

# Clean old builds
echo "==> Cleaning old builds"
rm -rf dist/ build/ *.egg-info

# Build fresh package
echo "==> Building package"
pip install --quiet build
python3 -m build

# Install the built package
echo "==> Installing built package"
pip install --quiet dist/*.whl

# Test import
echo "==> Testing package import"
python3 -c "from ghanon.cli import main; print('Import successful')"

echo "==> Installation test completed successfully"

# Cleanup
deactivate
