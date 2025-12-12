#!/bin/bash
# Start WISTX API server

set -e

cd "$(dirname "$0")"

if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please copy env.example to .env and configure it"
    exit 1
fi

if [ ! -d .venv ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install --quiet -q pydantic-settings pymongo fastapi uvicorn[standard] 2>/dev/null || true

echo ""
echo "Starting WISTX API server..."
echo "Server will be available at: http://127.0.0.1:8000"
echo "API docs at: http://127.0.0.1:8000/docs"
echo "Health check: http://127.0.0.1:8000/health"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload

