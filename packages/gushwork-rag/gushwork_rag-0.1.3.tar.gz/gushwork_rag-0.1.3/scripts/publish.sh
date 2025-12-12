#!/bin/bash
# Publish script for gushwork-rag SDK to PyPI

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PYTHON_DIR"

echo "📤 Publishing gushwork-rag to PyPI..."
echo ""

# Check if dist/ exists and has files
if [ ! -d "dist" ] || [ -z "$(ls -A dist/)" ]; then
    echo "❌ No distribution files found. Run build.sh first."
    exit 1
fi

# Check package
echo "✅ Checking package..."
twine check dist/*

# Confirm before publishing
echo ""
echo "⚠️  You are about to publish to PyPI!"
echo "Files to upload:"
ls -lh dist/
echo ""
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Publishing cancelled."
    exit 1
fi

# Upload to PyPI
echo ""
echo "📤 Uploading to PyPI..."
twine upload dist/*

echo ""
echo "✅ Published successfully!"
echo ""
echo "Package is now available at:"
echo "  https://pypi.org/project/gushwork-rag/"

