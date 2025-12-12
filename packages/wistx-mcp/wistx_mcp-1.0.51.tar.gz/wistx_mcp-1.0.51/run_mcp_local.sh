#!/bin/bash
# Run MCP server locally with access to local API module

set -e

PROJECT_ROOT="/Users/clever/Desktop/wistx-model"
cd "$PROJECT_ROOT"

echo "🚀 Starting WISTX MCP Server (Local Development Mode)"
echo "========================================================"
echo ""
echo "📋 Prerequisites:"
echo "  - API server should be running on http://localhost:8000"
echo "  - .env file should be configured"
echo ""

if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo ""
fi

if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "⚠️  Warning: API server doesn't appear to be running on http://localhost:8000"
    echo "   Start it with: uv run uvicorn api.main:app --reload"
    echo ""
fi

export WISTX_API_URL="${WISTX_API_URL:-http://localhost:8000}"
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

echo "🔧 Configuration:"
echo "  - Project root: $PROJECT_ROOT"
echo "  - API URL: $WISTX_API_URL"
echo "  - Python path: $PYTHONPATH"
echo ""
echo "▶️  Starting MCP server..."
echo ""

uv run python -m wistx_mcp.server

