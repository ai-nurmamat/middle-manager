#!/bin/bash

set -e

echo "=========================================================="
echo "🌌 Starting Chronos-MCP System Verification & Standardization"
echo "=========================================================="

echo "----------------------------------------------------------"
echo "1. Verifying Python Ecosystem (PyPI Package)"
echo "----------------------------------------------------------"
cd /workspace/chronos-mcp

# Formatting code
echo "Running Black formatter..."
black src/ tests/

# Type checking
echo "Running MyPy type checker..."
mypy src/ --ignore-missing-imports

# Install dependencies just in case
echo "Installing Python dependencies..."
pip install -e .[dev]

# Testing
echo "Running Pytest..."
PYTHONPATH=src python -m pytest tests/

echo "✅ Python Ecosystem Verified."

echo ""
echo "----------------------------------------------------------"
echo "2. Verifying TypeScript Ecosystem (NPM Package)"
echo "----------------------------------------------------------"
cd /workspace/chronos-mcp-ts

# Install missing dependencies if any
if [ ! -d "node_modules" ]; then
    echo "Installing NPM dependencies..."
    npm install
fi

# Formatting and Type Checking are handled during the build process
echo "Running TypeScript Compiler (Build)..."
npm run build

echo "Running Jest Tests..."
npm run test

echo "✅ TypeScript Ecosystem Verified."

echo ""
echo "=========================================================="
echo "🎉 ALL SYSTEMS GO! Chronos-MCP is fully standardized."
echo "=========================================================="
