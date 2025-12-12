# Running MCP Server Locally with Local API

This guide explains how to run the WISTX MCP server locally so it can access your local `api` module for testing.

## Prerequisites

1. **Local API server running**: Start your FastAPI server first:
   ```bash
   cd /Users/clever/Desktop/wistx-model
   uv run uvicorn api.main:app --reload
   ```

2. **Environment variables**: Make sure your `.env` file has the required variables:
   - `MONGODB_URI` - MongoDB connection string
   - `DATABASE_NAME` - Database name (default: `wistx-production`)
   - `WISTX_API_URL` - Set to `http://localhost:8000` for local testing
   - Optional: `PINECONE_API_KEY`, `GEMINI_API_KEY`, `TAVILY_API_KEY` for advanced features

## Method 1: Direct Python Module Execution (Recommended)

Run the MCP server as a Python module from the project root:

```bash
cd /Users/clever/Desktop/wistx-model
uv run python -m wistx_mcp.server
```

This ensures:
- The project root is in `sys.path`, so `api` module can be imported
- All local code changes are immediately available
- No need to rebuild/reinstall the package

## Method 2: Using uv with Directory Flag

```bash
uv run --directory /Users/clever/Desktop/wistx-model python -m wistx_mcp.server
```

## Method 3: Configure IDE MCP Settings

### For Cursor IDE

Create or edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "wistx-local": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/clever/Desktop/wistx-model",
        "python",
        "-m",
        "wistx_mcp.server"
      ],
      "env": {
        "WISTX_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

### For Windsurf

Create or edit `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "wistx-local": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/clever/Desktop/wistx-model",
        "python",
        "-m",
        "wistx_mcp.server"
      ],
      "env": {
        "WISTX_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

### For Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%/Claude/claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "wistx-local": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/clever/Desktop/wistx-model",
        "python",
        "-m",
        "wistx_mcp.server"
      ],
      "env": {
        "WISTX_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

## Method 4: Using PYTHONPATH

Set `PYTHONPATH` to include the project root:

```bash
export PYTHONPATH="/Users/clever/Desktop/wistx-model:$PYTHONPATH"
uv run python -m wistx_mcp.server
```

Or inline:

```bash
PYTHONPATH=/Users/clever/Desktop/wistx-model uv run python -m wistx_mcp.server
```

## Testing the Setup

1. **Start the API server** (in one terminal):
   ```bash
   cd /Users/clever/Desktop/wistx-model
   uv run uvicorn api.main:app --reload
   ```

2. **Start the MCP server** (in another terminal):
   ```bash
   cd /Users/clever/Desktop/wistx-model
   uv run python -m wistx_mcp.server
   ```

3. **Verify it's working**:
   - The MCP server should start without `ModuleNotFoundError: No module named 'api'`
   - Check logs for successful connection to MongoDB
   - Try calling an MCP tool from your IDE

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'api'`

**Solution**: Make sure you're running from the project root directory and using `python -m wistx_mcp.server` instead of `pipx run wistx-mcp`.

### Issue: API calls failing

**Solution**: 
- Verify `WISTX_API_URL` is set to `http://localhost:8000`
- Check that the API server is running on port 8000
- Check API server logs for errors

### Issue: MongoDB connection errors

**Solution**:
- Verify `MONGODB_URI` is set correctly in `.env`
- Check that MongoDB is running and accessible
- The MCP server will use the same MongoDB connection as the API server

### Issue: Quota/Budget checks not working

**Solution**: This is expected when running locally without the full `api` module. The MCP server will gracefully skip these checks and log debug messages. To enable full functionality, ensure you're running from the project root so `api` can be imported.

## Differences: Local vs Installed Package

| Aspect | Local Development | Installed Package (pipx) |
|--------|------------------|--------------------------|
| `api` module access | ✅ Available | ❌ Not available |
| Quota checking | ✅ Enabled | ⚠️ Disabled (graceful fallback) |
| Budget checking | ✅ Enabled | ⚠️ Disabled (graceful fallback) |
| Usage tracking | ✅ Enabled | ⚠️ Disabled (graceful fallback) |
| Code changes | ✅ Immediate | ❌ Requires rebuild |
| Command | `python -m wistx_mcp.server` | `pipx run wistx-mcp` |

## Quick Start Script

Create a `run_mcp_local.sh` script:

```bash
#!/bin/bash
cd /Users/clever/Desktop/wistx-model
export WISTX_API_URL="http://localhost:8000"
uv run python -m wistx_mcp.server
```

Make it executable:
```bash
chmod +x run_mcp_local.sh
```

Then run:
```bash
./run_mcp_local.sh
```

