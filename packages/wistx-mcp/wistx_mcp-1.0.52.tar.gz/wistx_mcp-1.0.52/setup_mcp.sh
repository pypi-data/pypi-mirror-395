#!/bin/bash
# Quick setup script for MCP server configuration

set -e

PROJECT_ROOT="/Users/clever/Desktop/wistx-model"
CURSOR_CONFIG="$HOME/.cursor/mcp.json"

# Detect Windsurf config location - Windsurf uses Codeium's directory
if [[ "$OSTYPE" == "darwin"* ]]; then
    WINDSURF_CONFIG="$HOME/.codeium/windsurf/mcp_config.json"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    WINDSURF_CONFIG="$HOME/.codeium/windsurf/mcp_config.json"
else
    WINDSURF_CONFIG="$HOME/.codeium/windsurf/mcp_config.json"
fi

echo "🚀 WISTX MCP Server Setup"
echo "========================="
echo ""
echo "Supported IDEs:"
echo "  ✅ Cursor"
echo "  ✅ Windsurf"
echo "  ✅ Google Antigravity (one-click install via MCP Server Store)"
echo ""

# Check if API server is running
echo "📡 Checking API server..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API server is running"
else
    echo "⚠️  API server is NOT running"
    echo "   Start it with: uv run uvicorn api.main:app --reload"
    echo ""
fi

# Check if .env file exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo "✅ .env file found"
else
    echo "⚠️  .env file not found - create it with required variables"
fi

echo ""
echo "📝 Configuration Files:"
echo ""

# Cursor setup
echo "1. Cursor IDE Configuration:"
if [ -f "$CURSOR_CONFIG" ]; then
    echo "   ✅ Cursor config exists: $CURSOR_CONFIG"
else
    echo "   ⚠️  Cursor config not found"
    echo "   📋 Copy from: $PROJECT_ROOT/.cursor-mcp.json.example"
    echo "   📍 To: $CURSOR_CONFIG"
    echo ""
    read -p "   Create Cursor config now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        mkdir -p "$HOME/.cursor"
        cp "$PROJECT_ROOT/.cursor-mcp.json.example" "$CURSOR_CONFIG"
        echo "   ✅ Created $CURSOR_CONFIG"
        echo "   💡 No credentials needed - MCP server reads from .env automatically!"
    fi
fi

echo ""

# Windsurf setup
echo "2. Windsurf Configuration:"
if [ -f "$WINDSURF_CONFIG" ]; then
    echo "   ✅ Windsurf config exists: $WINDSURF_CONFIG"
    
    # Check if wistx server is already configured
    if python3 -c "import json; data = json.load(open('$WINDSURF_CONFIG')); print('wistx' in data.get('mcpServers', {}))" 2>/dev/null | grep -q "True"; then
        echo "   ✅ 'wistx' server already configured"
    else
        echo "   ⚠️  'wistx' server not found in config"
        echo ""
        read -p "   Add 'wistx' server to existing config? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Create a Python script to safely merge the config
            python3 << 'EOF'
import json
import sys
import os

config_path = os.path.expanduser("~/.codeium/windsurf/mcp_config.json")
wistx_config = {
    "wistx": {
        "command": "uv",
        "args": ["run", "--directory", "/Users/clever/Desktop/wistx-model", "python", "-m", "wistx_mcp.server"],
        "env": {
            "WISTX_API_URL": "http://localhost:8000"
        }
    }
}

try:
    # Read existing config
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {"mcpServers": {}}
    
    # Ensure mcpServers exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    # Add wistx server if not already present
    if "wistx" not in config["mcpServers"]:
        config["mcpServers"]["wistx"] = wistx_config["wistx"]
        
        # Write back
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"   ✅ Added 'wistx' server to {config_path}")
    else:
        print("   ℹ️  'wistx' server already exists in config")
        
except json.JSONDecodeError as e:
    print(f"   ❌ Error: Invalid JSON in config file: {e}")
    sys.exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)
EOF
            if [ $? -eq 0 ]; then
                echo "   💡 Restart Windsurf to apply changes"
            fi
        fi
    fi
else
    echo "   ⚠️  Windsurf config not found"
    echo "   📋 Copy from: $PROJECT_ROOT/.windsurf-mcp.json.example"
    echo "   📍 To: $WINDSURF_CONFIG"
    echo ""
    echo "   ⚠️  Note: If the file already exists, you'll need to manually add the 'wistx' server"
    echo "      to the existing mcpServers object in the JSON file."
    echo ""
    read -p "   Create Windsurf config now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        mkdir -p "$(dirname "$WINDSURF_CONFIG")"
        cp "$PROJECT_ROOT/.windsurf-mcp.json.example" "$WINDSURF_CONFIG"
        echo "   ✅ Created $WINDSURF_CONFIG"
        echo "   💡 No credentials needed - MCP server reads from .env automatically!"
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "   1. Ensure your .env file has all required variables (MONGODB_URI, PINECONE_API_KEY, etc.)"
echo "   2. Ensure API server is running: uv run uvicorn api.main:app --reload"
echo "   3. Restart Cursor/Windsurf completely"
echo "   4. Test MCP tools in chat"
echo ""
echo "💡 Note: No credentials needed in config files - they're read from .env automatically!"
echo "📖 Full guide: MCP_SETUP_GUIDE.md"

