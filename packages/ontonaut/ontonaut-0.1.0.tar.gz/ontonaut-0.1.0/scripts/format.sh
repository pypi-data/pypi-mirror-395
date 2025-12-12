#!/usr/bin/env bash
# Format code automatically

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

echo "🎨 Formatting code..."

# Run black
echo "📝 Formatting with black..."
black src/ tests/

# Run ruff with auto-fix
echo "🔧 Auto-fixing with ruff..."
ruff check --fix src/ tests/

echo ""
echo "✅ Code formatting complete!"
