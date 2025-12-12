#!/usr/bin/env bash
# Clean up build artifacts and cache files

set -e

# Ensure we're in the project root
cd "$(dirname "$0")/.."

echo "🧹 Cleaning up build artifacts and cache files..."

# Remove build artifacts
rm -rf build/
rm -rf dist/
rm -rf *.egg-info
rm -rf src/*.egg-info

# Remove Python cache files (excluding .venv)
find . -path ./.venv -prune -o -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -path ./.venv -prune -o -type f -name "*.pyc" -exec rm -f {} + 2>/dev/null || true
find . -path ./.venv -prune -o -type f -name "*.pyo" -exec rm -f {} + 2>/dev/null || true
find . -path ./.venv -prune -o -type f -name "*.pyd" -exec rm -f {} + 2>/dev/null || true

# Remove pytest cache
rm -rf .pytest_cache/

# Remove coverage reports
rm -rf htmlcov/
rm -rf .coverage
rm -rf coverage.xml

# Remove mypy cache
rm -rf .mypy_cache/

# Remove ruff cache
rm -rf .ruff_cache/

# Remove virtual environment
echo "🗑️  Removing virtual environment..."
rm -rf .venv/

echo ""
echo "✅ Cleanup complete!"
