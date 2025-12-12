#!/usr/bin/env bash
# Build the Ontonaut package

set -e

# Ensure we're in the project root
cd "$(dirname "$0")/.."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "🏗️  Building Ontonaut package..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info src/*.egg-info

# Install build tool if not present
if ! python -c "import build" 2>/dev/null; then
    echo "📦 Installing build tool..."
    uv pip install build
fi

# Build the package
echo "📦 Building wheel and source distribution..."
python -m build

echo ""
echo "✅ Build complete!"
echo ""
echo "Distribution files created in dist/:"
ls -lh dist/
