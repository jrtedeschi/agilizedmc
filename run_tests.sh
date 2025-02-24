#!/bin/bash
set -e

# Ensure we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
    source .venv/bin/activate
fi

echo "📦 Installing dependencies..."
uv pip install -r requirements.txt -r requirements-test.txt

echo "🧪 Running unit tests..."
python -m pytest tests/ -v -m "not integration"

if [ -n "$RUN_INTEGRATION" ]; then
    echo "🔄 Running integration tests..."
    python -m pytest tests/ -v -m "integration"
fi

echo "📊 Generating coverage report..."
python -m pytest --cov=agilizedmc --cov-report=html

echo "✨ All tests completed!" 