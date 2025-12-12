#!/usr/bin/env bash
# Setup script for Ontonaut project using uv

set -e

echo "🚀 Setting up Ontonaut development environment..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   brew install uv"
    exit 1
fi

# Create virtual environment using uv
echo "📦 Creating virtual environment at .venv..."
uv venv .venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Install the package in editable mode with dev dependencies
echo "📥 Installing package with dev dependencies..."
uv pip install -e ".[dev]"

# Install pre-commit hooks (if pre-commit is available)
if command -v pre-commit &> /dev/null; then
    echo "🪝 Installing pre-commit hooks..."
    pre-commit install
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "   source .venv/bin/activate"
echo ""
echo "To run tests:"
echo "   ./scripts/test.sh"
echo ""
echo "To build the package:"
echo "   ./scripts/build.sh"
