#!/bin/bash

set -e  # Exit on error

echo "==================================="
echo "Building and uploading to PyPI"
echo "==================================="

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Build the wheel (pure Python, no compilation)
echo "Building wheel..."
python -m build

# Check if wheel was created
if [ ! -f dist/*.whl ]; then
    echo "Error: No wheel file found in dist/"
    exit 1
fi

echo "Wheel built successfully:"
ls -lh dist/

# Confirm before upload
echo ""
read -p "Do you want to upload to PyPI? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Upload cancelled."
    exit 0
fi

# Upload to PyPI
echo "Uploading to PyPI..."
twine upload dist/*

echo "==================================="
echo "Upload complete!"
echo "==================================="

# Optional: Clean up after upload
read -p "Do you want to clean the dist directory? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf dist/ build/ *.egg-info/
    echo "Cleaned up build artifacts"
fi