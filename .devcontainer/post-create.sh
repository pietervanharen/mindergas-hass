#!/bin/bash
set -e

echo "🚀 Installing MinderGas Integration Development Environment..."

# Update pip
pip install --upgrade pip setuptools wheel

# Install Home Assistant development tools
pip install homeassistant

# Install Python linting and formatting tools
pip install pylint black flake8 ruff

# Install testing dependencies
pip install pytest pytest-asyncio pytest-cov

# Install additional development tools
pip install pre-commit

# Create necessary directories
mkdir -p /config/custom_components

echo "✅ Development environment setup complete!"
echo ""
echo "📋 Available commands:"
echo "  - python -m homeassistant: Run Home Assistant"
echo "  - pytest: Run tests"
echo "  - black . --check: Check code formatting"
echo "  - pylint custom_components/mindergas: Lint integration"
echo ""
echo "🐳 Docker is available for running Home Assistant in a container"
echo "📚 See DOCKER_SETUP.md for more information"
