#!/usr/bin/env bash
# Run tests for Ontonaut project

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

echo "🧪 Running tests..."

# Parse command line arguments
PYTEST_ARGS=()

# Check for specific test types
if [[ "$*" == *"--fast"* ]]; then
    echo "⚡ Running fast tests only (excluding slow and integration tests)..."
    PYTEST_ARGS+=("-m" "not slow and not integration")
fi

if [[ "$*" == *"--integration"* ]]; then
    echo "🔗 Running integration tests..."
    PYTEST_ARGS+=("-m" "integration")
fi

if [[ "$*" == *"--no-cov"* ]]; then
    echo "📊 Running without coverage..."
    PYTEST_ARGS+=("--no-cov")
fi

# Run pytest
pytest "${PYTEST_ARGS[@]}" "$@"

echo ""
echo "✅ Tests passed!"
