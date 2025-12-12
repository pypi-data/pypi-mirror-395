#!/usr/bin/env bash
# Run linting and formatting checks

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

echo "🔍 Running linters and formatters..."

# Run black
echo "🎨 Checking code formatting with black..."
black --check src/ tests/

# Run ruff
echo "🔧 Running ruff linter..."
ruff check src/ tests/

# Run mypy
echo "🔬 Running type checking with mypy..."
mypy src/

echo ""
echo "✅ All linting checks passed!"
