#!/bin/bash
# Build script for gushwork-rag SDK

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PYTHON_DIR"

echo "🔨 Building gushwork-rag package..."
echo ""

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/
echo "✅ Cleaned"

# Install build tools if needed
echo ""
echo "📦 Installing build tools..."
python -m pip install --upgrade build twine --quiet

# Build the package
echo ""
echo "🔨 Building package..."
python -m build

# Check the package
echo ""
echo "✅ Checking package..."
twine check dist/*

echo ""
echo "✅ Build complete!"
echo ""
echo "Built files:"
ls -lh dist/
echo ""
echo "To test installation:"
echo "  pip install dist/gushwork_rag-*.whl"
echo ""
echo "To publish:"
echo "  twine upload dist/*"

