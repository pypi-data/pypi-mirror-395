#!/bin/bash
#
# Quick build script for Synqed
#

set -e

echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info src/*.egg-info

echo "📦 Building package..."
python -m build

echo "✅ Checking package..."
twine check dist/*

echo ""
echo "✨ Build complete!"
echo ""
echo "Built files:"
ls -lh dist/

echo ""
echo "To publish:"
echo "  Test PyPI:  ./scripts/publish.sh --test"
echo "  Production: ./scripts/publish.sh --prod"

