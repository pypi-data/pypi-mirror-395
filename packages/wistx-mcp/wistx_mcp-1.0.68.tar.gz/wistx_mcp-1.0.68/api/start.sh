#!/bin/bash
set -e

# Ensure Python output is not buffered
export PYTHONUNBUFFERED=1

echo "=========================================="
echo "Starting WISTX API"
echo "=========================================="
echo "PORT: ${PORT:-8000}"
echo "ENVIRONMENT: ${ENVIRONMENT:-not set}"
echo "DEBUG: ${DEBUG:-false}"

echo ""
echo "Checking required environment variables..."
if [ -z "$MONGODB_URI" ]; then
    echo "ERROR: MONGODB_URI is not set!"
    echo "This is a required environment variable."
    echo "Check your Cloud Run environment variables and Secret Manager configuration."
    exit 1
fi
echo "✓ MONGODB_URI is set"

echo ""
echo "Checking Python environment..."
python3 --version || echo "WARNING: python3 not found"
which uv || echo "WARNING: uv not found"

echo ""
echo "All checks passed. Starting uvicorn..."
echo "Note: Import tests skipped - uvicorn will show any import errors"

echo ""
echo "Starting uvicorn server on port ${PORT:-8000}..."
echo "Command: uv run uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"
echo ""

# Run uvicorn and capture output
uv run uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000} 2>&1 || {
    echo ""
    echo "ERROR: Uvicorn failed to start!"
    echo "Exit code: $?"
    echo ""
    echo "Attempting to diagnose the issue..."
    echo ""
    
    # Try to import the app directly to see the error
    echo "Testing direct import..."
    uv run python -c "from api.main import app; print('✓ App imported successfully')" 2>&1 || {
        echo "ERROR: Failed to import app"
        echo "This usually indicates a Python import error or configuration issue."
    }
    
    exit 1
}

