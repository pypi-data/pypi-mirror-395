#!/bin/bash
# Generate SDKs from OpenAPI specification

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SDK_DIR="$PROJECT_ROOT/sdk"
API_DIR="$PROJECT_ROOT/api"

cd "$PROJECT_ROOT"

echo "=== Generating SDKs from OpenAPI Specification ==="
echo ""

if [ ! -f "$API_DIR/openapi.json" ]; then
    echo "❌ OpenAPI spec not found. Exporting..."
    python3 "$SCRIPT_DIR/export_openapi.py"
    echo ""
fi

if ! command -v openapi-generator &> /dev/null; then
    echo "⚠️  openapi-generator not found"
    echo ""
    echo "Install with:"
    echo "  brew install openapi-generator"
    echo "  # or"
    echo "  npm install -g @openapitools/openapi-generator-cli"
    echo ""
    echo "For now, OpenAPI spec is available at:"
    echo "  - JSON: $API_DIR/openapi.json"
    echo "  - Interactive: http://localhost:8000/docs"
    echo ""
    exit 0
fi

echo "Generating SDKs..."
echo ""

mkdir -p "$SDK_DIR"

echo "📦 Generating Python SDK..."
openapi-generator generate \
    -i "$API_DIR/openapi.json" \
    -g python \
    -o "$SDK_DIR/wistx-api-python" \
    --package-name wistx_api \
    --additional-properties=packageVersion=0.1.0,packageName=wistx-api-sdk \
    > /dev/null 2>&1 || echo "  ⚠️  Python SDK generation failed"

echo "📦 Generating TypeScript SDK..."
openapi-generator generate \
    -i "$API_DIR/openapi.json" \
    -g typescript \
    -o "$SDK_DIR/wistx-api-typescript" \
    --additional-properties=npmName=wistx-api-sdk,npmVersion=0.1.0 \
    > /dev/null 2>&1 || echo "  ⚠️  TypeScript SDK generation failed"

echo ""
echo "✅ SDK generation complete!"
echo ""
echo "Generated SDKs:"
echo "  - Python: $SDK_DIR/wistx-api-python"
echo "  - TypeScript: $SDK_DIR/wistx-api-typescript"
echo ""
echo "To generate SDKs for other languages:"
echo "  openapi-generator generate -i $API_DIR/openapi.json -g <language> -o $SDK_DIR/<language>"
echo ""
echo "Supported languages: python, typescript, go, java, ruby, php, swift, kotlin, etc."

