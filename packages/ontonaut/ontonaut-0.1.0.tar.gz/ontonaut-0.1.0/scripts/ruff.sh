#!/usr/bin/env bash
# Run ruff linter and formatter

set -e

# Ensure we're in the project root
cd "$(dirname "$0")/.."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found. Run ./scripts/setup.sh first."
    exit 1
fi

echo "🔧 Running ruff..."

# Parse command line arguments
if [[ "$*" == *"--fix"* ]] || [[ "$*" == *"-f"* ]]; then
    echo "🔨 Running ruff with auto-fix..."
    ruff check --fix src/ tests/
    echo "✅ Ruff auto-fix complete!"
else
    echo "🔍 Running ruff check..."
    ruff check src/ tests/
    echo "✅ Ruff check passed!"
fi
