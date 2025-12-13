# WISTX One-Click Setup Implementation Plan

## Executive Summary

This document outlines the **practical implementation plan** for adding one-click setup to WISTX, leveraging existing infrastructure and following Nia's proven patterns. The plan is designed to be implemented incrementally with minimal disruption to existing systems.

**Key Strategy:**
- ✅ Leverage existing FastAPI infrastructure
- ✅ Reuse existing authentication system
- ✅ Add new endpoints without breaking changes
- ✅ Progressive rollout (remote server → setup script → CLI)

---

## 1. Current Architecture Analysis

### 1.1 Existing Infrastructure

**FastAPI Application:**
- Location: `api/main.py`
- Base URL: `https://api.wistx.ai`
- Routers: `/v1/*` and `/internal/*`
- Middleware: Authentication, rate limiting, CORS, etc.

**Authentication System:**
- API keys via Bearer tokens
- Dependency: `get_current_user()` in `api/dependencies/auth.py`
- Middleware: `AuthenticationMiddleware` in `api/middleware/auth.py`
- Function: `get_user_from_api_key()` in `api/auth/api_keys.py`

**Existing Routers:**
- `/v1/*` - Public API endpoints
- `/internal/*` - Internal/admin endpoints
- Well-organized structure

**Deployment:**
- FastAPI app (likely Cloud Run or similar)
- MongoDB Atlas
- Redis/Memorystore
- Pinecone

### 1.2 What We Can Leverage

✅ **FastAPI app** - Add new routers  
✅ **Authentication** - Reuse API key validation  
✅ **Middleware** - Rate limiting, CORS already configured  
✅ **Database** - MongoDB for any storage needs  
✅ **Existing patterns** - Follow router structure  

### 1.3 What We Need to Add

❌ **MCP HTTP endpoint** - New router for MCP protocol over HTTP  
❌ **Setup script endpoint** - New endpoint to serve installation script  
❌ **MCP protocol handler** - Logic to handle MCP requests  
❌ **Setup script generator** - Logic to generate IDE-specific configs  

---

## 2. Implementation Strategy

### 2.1 Phase 1: Remote HTTP MCP Server (CRITICAL - Week 1-2)

**Goal:** Enable zero-dependency installation via HTTP endpoint

#### Step 1.1: Create MCP Router

**File:** `api/routers/v1/mcp.py`

**Purpose:** Handle MCP protocol requests over HTTP

**Implementation:**
```python
from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Any
import logging

from api.dependencies.auth import get_current_user
from api.services.mcp_http_service import MCPHTTPService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mcp", tags=["mcp"])

@router.post("/v1/request")
async def mcp_request(
    request: Request,
    mcp_request: dict[str, Any],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> JSONResponse:
    """Handle MCP protocol request over HTTP.
    
    This endpoint implements the MCP protocol over HTTP, allowing
    IDEs to connect to WISTX MCP server without local installation.
    
    Args:
        request: FastAPI request object
        mcp_request: MCP protocol request (JSON-RPC format)
        current_user: Authenticated user (from API key)
    
    Returns:
        MCP protocol response (JSON-RPC format)
    """
    try:
        service = MCPHTTPService()
        response = await service.handle_request(
            mcp_request=mcp_request,
            user_info=current_user,
        )
        return JSONResponse(content=response)
    except Exception as e:
        logger.error("MCP request failed: %s", e, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "jsonrpc": "2.0",
                "id": mcp_request.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e),
                },
            },
        )
```

#### Step 1.2: Create MCP HTTP Service

**File:** `api/services/mcp_http_service.py`

**Purpose:** Business logic for handling MCP protocol requests

**Implementation:**
```python
import logging
from typing import Any
from wistx_mcp.server import handle_mcp_tool_call
from wistx_mcp.tools.lib.auth_context import set_auth_context, AuthContext

logger = logging.getLogger(__name__)

class MCPHTTPService:
    """Service for handling MCP protocol over HTTP."""
    
    async def handle_request(
        self,
        mcp_request: dict[str, Any],
        user_info: dict[str, Any],
    ) -> dict[str, Any]:
        """Handle MCP protocol request.
        
        Args:
            mcp_request: MCP protocol request (JSON-RPC format)
            user_info: User information from authentication
        
        Returns:
            MCP protocol response (JSON-RPC format)
        """
        method = mcp_request.get("method")
        params = mcp_request.get("params", {})
        request_id = mcp_request.get("id")
        
        # Set auth context for MCP tools
        auth_context = AuthContext(
            user_id=user_info.get("user_id"),
            organization_id=user_info.get("organization_id"),
            api_key=user_info.get("api_key"),
        )
        set_auth_context(auth_context)
        
        # Route to appropriate handler
        if method == "initialize":
            return await self._handle_initialize(params, request_id)
        elif method == "tools/list":
            return await self._handle_tools_list(params, request_id)
        elif method == "tools/call":
            return await self._handle_tools_call(params, request_id)
        elif method == "resources/list":
            return await self._handle_resources_list(params, request_id)
        elif method == "resources/read":
            return await self._handle_resources_read(params, request_id)
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}",
                },
            }
    
    async def _handle_initialize(
        self,
        params: dict[str, Any],
        request_id: Any,
    ) -> dict[str, Any]:
        """Handle initialize request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {},
                },
                "serverInfo": {
                    "name": "wistx-mcp",
                    "version": "1.0.65",
                },
            },
        }
    
    async def _handle_tools_list(
        self,
        params: dict[str, Any],
        request_id: Any,
    ) -> dict[str, Any]:
        """Handle tools/list request."""
        # Import tool registry from MCP server
        from wistx_mcp.tools.lib.tool_registry import get_all_tools
        
        tools = get_all_tools()
        tool_schemas = [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema,
            }
            for tool in tools
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tool_schemas,
            },
        }
    
    async def _handle_tools_call(
        self,
        params: dict[str, Any],
        request_id: Any,
    ) -> dict[str, Any]:
        """Handle tools/call request."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        # Call MCP tool (reuse existing logic)
        result = await handle_mcp_tool_call(
            tool_name=tool_name,
            arguments=arguments,
        )
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": str(result),
                    }
                ],
            },
        }
    
    async def _handle_resources_list(
        self,
        params: dict[str, Any],
        request_id: Any,
    ) -> dict[str, Any]:
        """Handle resources/list request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "resources": [],
            },
        }
    
    async def _handle_resources_read(
        self,
        params: dict[str, Any],
        request_id: Any,
    ) -> dict[str, Any]:
        """Handle resources/read request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": "Resource not found",
            },
        }
```

#### Step 1.3: Register Router

**File:** `api/routers/v1/__init__.py`

**Add:**
```python
from api.routers.v1 import mcp

router.include_router(mcp.router)
```

#### Step 1.4: Update MCP Server to Support HTTP

**File:** `wistx_mcp/server.py`

**Add helper function:**
```python
async def handle_mcp_tool_call(
    tool_name: str,
    arguments: dict[str, Any],
) -> Any:
    """Handle MCP tool call (shared between stdio and HTTP).
    
    Args:
        tool_name: Name of the tool to call
        arguments: Tool arguments
    
    Returns:
        Tool result
    """
    # Import tool registry
    from wistx_mcp.tools.lib.tool_registry import get_tool_by_name
    
    tool = get_tool_by_name(tool_name)
    if not tool:
        raise ValueError(f"Tool not found: {tool_name}")
    
    # Call tool
    result = await tool.call(arguments)
    return result
```

#### Step 1.5: Testing

**Test Endpoint:**
```bash
curl -X POST https://api.wistx.ai/mcp/v1/request \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {}
  }'
```

### 2.2 Phase 2: Setup Script Endpoint (HIGH - Week 3)

**Goal:** One-command installation script

#### Step 2.1: Create Setup Router

**File:** `api/routers/v1/setup.py`

**Purpose:** Serve installation script and handle setup requests

**Implementation:**
```python
from fastapi import APIRouter, Query
from fastapi.responses import Response
from typing import Optional
import logging

from api.services.setup_script_service import SetupScriptService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/setup", tags=["setup"])

@router.get("/script")
async def get_setup_script(
    api_key: Optional[str] = Query(None, description="API key (optional, can be provided via script parameter)"),
    ide: Optional[str] = Query(None, description="IDE name (optional, script will auto-detect)"),
    remote: bool = Query(False, description="Use remote server (default: False)"),
) -> Response:
    """Return automated setup script.
    
    Usage:
        curl -fsSL https://api.wistx.ai/v1/setup/script | bash -s -- YOUR_API_KEY cursor --remote
    
    Args:
        api_key: Optional API key (can also be passed as script argument)
        ide: Optional IDE name (can also be passed as script argument)
        remote: Use remote server instead of local
    
    Returns:
        Bash script content
    """
    service = SetupScriptService()
    script_content = service.generate_script(
        api_key=api_key,
        ide=ide,
        remote=remote,
    )
    
    return Response(
        content=script_content,
        media_type="text/x-shellscript",
        headers={
            "Content-Disposition": "attachment; filename=wistx-setup.sh",
        },
    )
```

#### Step 2.2: Create Setup Script Service

**File:** `api/services/setup_script_service.py`

**Purpose:** Generate installation scripts for different IDEs

**Implementation:**
```python
import platform
from typing import Optional
from pathlib import Path

class SetupScriptService:
    """Service for generating setup scripts."""
    
    IDE_CONFIGS = {
        "cursor": {
            "macos": "~/.cursor/mcp.json",
            "windows": "%APPDATA%\\Cursor\\mcp.json",
            "linux": "~/.config/cursor/mcp.json",
            "config_key": "mcpServers",
        },
        "windsurf": {
            "macos": "~/.codeium/windsurf/mcp_config.json",
            "windows": "%APPDATA%\\Codeium\\Windsurf\\mcp_config.json",
            "linux": "~/.codeium/windsurf/mcp_config.json",
            "config_key": "mcpServers",
        },
        "claude-desktop": {
            "macos": "~/Library/Application Support/Claude/claude_desktop_config.json",
            "windows": "%APPDATA%\\Claude\\claude_desktop_config.json",
            "linux": "~/.config/Claude/claude_desktop_config.json",
            "config_key": "mcpServers",
        },
        "vscode": {
            "macos": "~/.config/Code/User/mcp.json",
            "windows": "%APPDATA%\\Code\\User\\mcp.json",
            "linux": "~/.config/Code/User/mcp.json",
            "config_key": "servers",
        },
        # Add more IDEs...
    }
    
    def generate_script(
        self,
        api_key: Optional[str] = None,
        ide: Optional[str] = None,
        remote: bool = False,
    ) -> str:
        """Generate setup script.
        
        Args:
            api_key: Optional API key
            ide: Optional IDE name
            remote: Use remote server
        
        Returns:
            Bash script content
        """
        script = f"""#!/bin/bash
# WISTX MCP Automated Setup Script
# Generated by WISTX API

set -e

API_KEY="${{1:-{api_key or 'YOUR_API_KEY'}}}"
IDE_NAME="${{2:-{ide or 'auto'}}}"
MODE="${{3:-{'remote' if remote else 'local'}}}"

# Detect OS
detect_os() {{
    case "$(uname -s)" in
        Darwin*) echo "macos" ;;
        Linux*) echo "linux" ;;
        CYGWIN*|MINGW*|MSYS*) echo "windows" ;;
        *) echo "unknown" ;;
    esac
}}

OS=$(detect_os)

# Detect IDEs
detect_ides() {{
    local detected=()
    local os="$1"
    
    # Check Cursor
    if [ -f "$HOME/.cursor/mcp.json" ] || [ -f "$HOME/.config/cursor/mcp.json" ]; then
        detected+=("cursor")
    fi
    
    # Check Windsurf
    if [ -f "$HOME/.codeium/windsurf/mcp_config.json" ]; then
        detected+=("windsurf")
    fi
    
    # Check Claude Desktop
    if [ "$os" = "macos" ] && [ -f "$HOME/Library/Application Support/Claude/claude_desktop_config.json" ]; then
        detected+=("claude-desktop")
    fi
    
    # Check VS Code
    if [ -f "$HOME/.config/Code/User/mcp.json" ] || [ -f "$HOME/.vscode/mcp.json" ]; then
        detected+=("vscode")
    fi
    
    echo "${{detected[*]}}"
}}

# Configure IDE
configure_ide() {{
    local ide="$1"
    local api_key="$2"
    local mode="$3"
    local os="$4"
    
    local config_path
    local config_key
    
    case "$ide" in
        cursor)
            case "$os" in
                macos) config_path="$HOME/.cursor/mcp.json" ;;
                linux) config_path="$HOME/.config/cursor/mcp.json" ;;
                windows) config_path="$APPDATA/Cursor/mcp.json" ;;
            esac
            config_key="mcpServers"
            ;;
        windsurf)
            config_path="$HOME/.codeium/windsurf/mcp_config.json"
            config_key="mcpServers"
            ;;
        claude-desktop)
            case "$os" in
                macos) config_path="$HOME/Library/Application Support/Claude/claude_desktop_config.json" ;;
                linux) config_path="$HOME/.config/Claude/claude_desktop_config.json" ;;
                windows) config_path="$APPDATA/Claude/claude_desktop_config.json" ;;
            esac
            config_key="mcpServers"
            ;;
        vscode)
            case "$os" in
                macos) config_path="$HOME/.config/Code/User/mcp.json" ;;
                linux) config_path="$HOME/.config/Code/User/mcp.json" ;;
                windows) config_path="$APPDATA/Code/User/mcp.json" ;;
            esac
            config_key="servers"
            ;;
        *)
            echo "❌ Unknown IDE: $ide"
            return 1
            ;;
    esac
    
    # Create config directory
    mkdir -p "$(dirname "$config_path")"
    
    # Read or create config
    if [ -f "$config_path" ]; then
        config=$(cat "$config_path")
    else
        config="{{}}"
    fi
    
    # Merge WISTX server config
    if [ "$mode" = "remote" ]; then
        wistx_config='{{"wistx":{{"url":"https://api.wistx.ai/mcp/v1/request","headers":{{"Authorization":"Bearer {api_key or 'YOUR_API_KEY'}"}}}}}}'
    else
        wistx_config='{{"wistx":{{"command":"pipx","args":["run","--no-cache","wistx-mcp"],"env":{{"WISTX_API_KEY":"{api_key or 'YOUR_API_KEY'}"}}}}}}'
    fi
    
    # Use Python to merge JSON (more reliable than jq)
    python3 << EOF
import json
import sys
import os

config_path = os.path.expanduser("$config_path")
config_key = "$config_key"

# Read existing config
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
else:
    config = {{}}

# Ensure config_key exists
if config_key not in config:
    config[config_key] = {{}}

# Add WISTX server
wistx_config = {wistx_config}
config[config_key]["wistx"] = wistx_config["wistx"]

# Write back
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print(f"✅ Configured {ide} successfully!")
EOF
}}

# Main
main() {{
    echo "🚀 WISTX MCP Installation"
    echo "========================"
    echo ""
    
    if [ "$API_KEY" = "YOUR_API_KEY" ] || [ -z "$API_KEY" ]; then
        echo "⚠️  Please provide your API key:"
        echo "   curl -fsSL https://api.wistx.ai/v1/setup/script | bash -s -- YOUR_API_KEY"
        exit 1
    fi
    
    if [ "$IDE_NAME" = "auto" ] || [ -z "$IDE_NAME" ]; then
        echo "🔍 Detecting installed IDEs..."
        detected=$(detect_ides "$OS")
        if [ -z "$detected" ]; then
            echo "❌ No supported IDEs detected"
            echo "   Please specify IDE: curl ... | bash -s -- YOUR_API_KEY cursor"
            exit 1
        fi
        echo "✅ Detected: $detected"
        for ide in $detected; do
            configure_ide "$ide" "$API_KEY" "$MODE" "$OS"
        done
    else
        configure_ide "$IDE_NAME" "$API_KEY" "$MODE" "$OS"
    fi
    
    echo ""
    echo "✅ Installation complete!"
    echo "   Restart your IDE to apply changes."
}}

main "$@"
"""
        return script
```

#### Step 2.3: Register Router

**File:** `api/routers/v1/__init__.py`

**Add:**
```python
from api.routers.v1 import setup

router.include_router(setup.router)
```

### 2.3 Phase 3: Python CLI Setup Command (MEDIUM - Week 4)

**Goal:** Alternative to curl script

#### Step 3.1: Add Setup Command to CLI

**File:** `wistx_mcp/server.py`

**Add CLI command:**
```python
import click

@click.group()
def cli():
    """WISTX MCP Server CLI."""
    pass

@cli.command()
@click.argument("api_key")
@click.option("--ide", default="auto", help="IDE name (default: auto-detect)")
@click.option("--remote", is_flag=True, help="Use remote server")
def setup(api_key: str, ide: str, remote: bool):
    """Setup WISTX MCP server for an IDE.
    
    Examples:
        wistx-mcp setup YOUR_API_KEY --ide cursor --remote
        wistx-mcp setup YOUR_API_KEY --ide windsurf
    """
    from wistx_mcp.setup import setup_ide
    
    setup_ide(
        api_key=api_key,
        ide=ide,
        remote=remote,
    )
```

#### Step 3.2: Create Setup Module

**File:** `wistx_mcp/setup.py`

**Implementation:**
```python
import json
import platform
from pathlib import Path
from typing import Optional

IDE_CONFIG_PATHS = {
    "cursor": {
        "macos": "~/.cursor/mcp.json",
        "windows": "%APPDATA%\\Cursor\\mcp.json",
        "linux": "~/.config/cursor/mcp.json",
    },
    "windsurf": {
        "macos": "~/.codeium/windsurf/mcp_config.json",
        "windows": "%APPDATA%\\Codeium\\Windsurf\\mcp_config.json",
        "linux": "~/.codeium/windsurf/mcp_config.json",
    },
    # Add more IDEs...
}

def setup_ide(api_key: str, ide: str, remote: bool = False):
    """Setup WISTX MCP server for an IDE.
    
    Args:
        api_key: WISTX API key
        ide: IDE name or "auto" to detect
        remote: Use remote server instead of local
    """
    os_name = platform.system().lower()
    if os_name == "darwin":
        os_name = "macos"
    
    if ide == "auto":
        # Auto-detect IDEs
        detected = []
        for ide_name, paths in IDE_CONFIG_PATHS.items():
            config_path = Path(paths.get(os_name, paths.get("linux", ""))).expanduser()
            if config_path.exists() or config_path.parent.exists():
                detected.append(ide_name)
        
        if not detected:
            print("❌ No supported IDEs detected")
            return
        
        print(f"✅ Detected IDEs: {', '.join(detected)}")
        for detected_ide in detected:
            _configure_single_ide(detected_ide, api_key, remote, os_name)
    else:
        _configure_single_ide(ide, api_key, remote, os_name)

def _configure_single_ide(ide: str, api_key: str, remote: bool, os_name: str):
    """Configure a single IDE."""
    if ide not in IDE_CONFIG_PATHS:
        print(f"❌ Unknown IDE: {ide}")
        return
    
    paths = IDE_CONFIG_PATHS[ide]
    config_path = Path(paths.get(os_name, paths.get("linux", ""))).expanduser()
    
    # Read or create config
    if config_path.exists():
        config = json.loads(config_path.read_text())
    else:
        config = {}
    
    # Determine config key
    if ide == "vscode":
        config_key = "servers"
    else:
        config_key = "mcpServers"
    
    # Ensure config key exists
    if config_key not in config:
        config[config_key] = {}
    
    # Add WISTX server
    if remote:
        config[config_key]["wistx"] = {
            "url": "https://api.wistx.ai/mcp/v1/request",
            "headers": {
                "Authorization": f"Bearer {api_key}"
            }
        }
    else:
        config[config_key]["wistx"] = {
            "command": "pipx",
            "args": ["run", "--no-cache", "wistx-mcp"],
            "env": {
                "WISTX_API_KEY": api_key
            }
        }
    
    # Write back
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2))
    
    print(f"✅ Configured {ide} successfully!")
    print(f"   Config: {config_path}")
```

---

## 3. File Structure

### 3.1 New Files to Create

```
api/
├── routers/
│   └── v1/
│       ├── mcp.py              # NEW: MCP HTTP endpoint
│       └── setup.py            # NEW: Setup script endpoint
├── services/
│   ├── mcp_http_service.py     # NEW: MCP HTTP service
│   └── setup_script_service.py # NEW: Setup script service

wistx_mcp/
├── setup.py                     # NEW: CLI setup command
└── server.py                    # MODIFY: Add handle_mcp_tool_call helper
```

### 3.2 Files to Modify

```
api/
├── routers/
│   └── v1/
│       └── __init__.py         # ADD: Include mcp and setup routers
└── main.py                      # (No changes needed - routers auto-registered)

wistx_mcp/
└── server.py                    # ADD: handle_mcp_tool_call helper, setup CLI command
```

---

## 4. Integration Points

### 4.1 Authentication

**Reuse:** `get_current_user()` dependency

**How:**
- MCP endpoint uses same authentication
- API key in `Authorization: Bearer {key}` header
- User context passed to MCP service

### 4.2 Tool Execution

**Reuse:** Existing MCP tool registry

**How:**
- Import tools from `wistx_mcp.tools`
- Call tools with user context
- Return results in MCP format

### 4.3 Error Handling

**Reuse:** Existing exception handlers

**How:**
- FastAPI exception handlers catch errors
- Return proper MCP error format
- Log errors with existing logging

---

## 5. Testing Strategy

### 5.1 Unit Tests

**Files:**
- `tests/api/services/test_mcp_http_service.py`
- `tests/api/services/test_setup_script_service.py`
- `tests/wistx_mcp/test_setup.py`

### 5.2 Integration Tests

**Test MCP HTTP endpoint:**
```python
async def test_mcp_initialize(client, api_key):
    response = await client.post(
        "/mcp/v1/request",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {},
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"]["serverInfo"]["name"] == "wistx-mcp"
```

**Test setup script:**
```python
async def test_setup_script(client):
    response = await client.get("/v1/setup/script?ide=cursor&remote=true")
    assert response.status_code == 200
    assert "WISTX MCP Installation" in response.text
```

### 5.3 Manual Testing

**Test with real IDEs:**
1. Configure Cursor with remote server
2. Test tool calls
3. Verify authentication works
4. Test setup script

---

## 6. Deployment Checklist

### 6.1 Pre-Deployment

- [ ] All tests passing
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Migration plan reviewed

### 6.2 Deployment Steps

1. **Deploy API changes**
   - Add new routers
   - Deploy to staging
   - Test endpoints

2. **Update documentation**
   - Add remote server instructions
   - Update installation guide
   - Add setup script usage

3. **Monitor**
   - Check error rates
   - Monitor API usage
   - Watch for authentication issues

### 6.3 Rollback Plan

- Keep local server as fallback
- No breaking changes
- Can disable new endpoints if needed

---

## 7. Success Metrics

### 7.1 Technical Metrics

- ✅ MCP HTTP endpoint responds in < 500ms
- ✅ Setup script success rate > 95%
- ✅ Zero authentication errors
- ✅ All tools work via HTTP

### 7.2 User Metrics

- ✅ Setup time: < 30 seconds (from 10-15 minutes)
- ✅ Remote server adoption: > 60% of new installs
- ✅ Support tickets: -80% reduction
- ✅ User satisfaction: > 4.5/5

---

## 8. Timeline

### Week 1: MCP HTTP Server
- Day 1-2: Create MCP router and service
- Day 3-4: Implement MCP protocol handlers
- Day 5: Testing and bug fixes

### Week 2: MCP HTTP Server (continued)
- Day 1-2: Integration with existing tools
- Day 3-4: Testing with real IDEs
- Day 5: Documentation and deployment

### Week 3: Setup Script
- Day 1-2: Create setup script service
- Day 3-4: Generate scripts for all IDEs
- Day 5: Testing and deployment

### Week 4: CLI Setup Command
- Day 1-2: Implement CLI setup
- Day 3-4: Testing
- Day 5: Documentation

---

## 9. Risks & Mitigation

### 9.1 Technical Risks

**Risk:** MCP protocol complexity  
**Mitigation:** Start with simple request/response, add streaming later

**Risk:** Authentication issues  
**Mitigation:** Reuse existing auth, extensive testing

**Risk:** Performance issues  
**Mitigation:** Monitor latency, optimize as needed

### 9.2 User Experience Risks

**Risk:** Setup script fails on some systems  
**Mitigation:** Extensive testing, fallback to manual setup

**Risk:** Users prefer local server  
**Mitigation:** Support both options, let users choose

---

## 10. Next Steps

1. **Review this plan** with team
2. **Start with Phase 1** (MCP HTTP server)
3. **Create tickets** for each phase
4. **Begin implementation** following this plan

---

**Document Version:** 1.0  
**Last Updated:** 2025-01-XX  
**Status:** Ready for Implementation

