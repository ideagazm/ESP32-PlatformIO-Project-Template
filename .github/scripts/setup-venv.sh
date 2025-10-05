#!/bin/bash
# Setup virtual environment for GitHub Actions
set -e

echo "Setting up Python virtual environment..."

# Create virtual environment
python -m venv .venv

# Activate and upgrade pip
source .venv/bin/activate
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo "Virtual environment setup complete!"
echo "Python version: $(python --version)"
echo "PlatformIO version: $(pio --version)"