# Google Antigravity Setup Guide

**Last Updated:** 2024-12-19  
**Antigravity Version:** Public Preview (November 2025)

---

## Overview

[Google Antigravity](https://antigravity.google/) is Google's new agent-first IDE that supports MCP (Model Context Protocol) servers. Antigravity provides a streamlined interface for managing MCP servers with **one-click installation** from the MCP server store.

---

## Installation Methods

### Method 1: One-Click Installation (Recommended) ✅

Antigravity includes an **MCP Server Store** with one-click installation:

1. **Open Antigravity IDE**
2. **Navigate to "Manage MCPs"** tab
3. **Click "View MCP server store"** (if no servers are installed)
4. **Search for "WISTX"** or browse available servers
5. **Click "Install"** - Antigravity will automatically configure the server

**✅ Confirmed:** Antigravity supports one-click installation via the MCP server store.

### Method 2: Manual Configuration

If you prefer manual configuration or the server isn't in the store:

1. **Open Antigravity IDE**
2. **Navigate to "mcp_config.json"** tab
3. **Add WISTX configuration:**

```json
{
  "mcpServers": {
    "wistx": {
      "command": "pipx",
      "args": ["run", "--no-cache", "wistx-mcp"],
      "env": {
        "WISTX_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

**Note:** Replace `YOUR_API_KEY` with your actual API key from [app.wistx.ai](https://app.wistx.ai/).

---

## Configuration Options

### Using pipx (Recommended)

```json
{
  "mcpServers": {
    "wistx": {
      "command": "pipx",
      "args": ["run", "--no-cache", "wistx-mcp"],
      "env": {
        "WISTX_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### Using uvx

```json
{
  "mcpServers": {
    "wistx": {
      "command": "uvx",
      "args": ["wistx-mcp"],
      "env": {
        "WISTX_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

---

## Prerequisites

Before configuring WISTX in Antigravity:

1. **Python 3.11+** installed
2. **pipx** (recommended) or **uvx** installed:
   ```bash
   # Install pipx
   python -m pip install --user pipx
   python -m pipx ensurepath
   
   # Or install uvx (comes with uv)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **Your WISTX API key** from [app.wistx.ai](https://app.wistx.ai/)

---

## Verification

After configuration:

1. **Restart Antigravity** completely
2. **Open the agent chat** in Antigravity
3. **Test WISTX tools** by asking:
   - "What are the PCI-DSS compliance requirements for payment processing?"
   - "Calculate the cost of an AWS EC2 instance"
   - "Show me Terraform examples for Kubernetes"

If configured correctly, Antigravity agents will automatically use WISTX tools to answer these questions.

---

## Troubleshooting

### Server Not Starting

**Issue:** MCP server fails to start in Antigravity

**Solutions:**
1. Check that `pipx` or `uvx` is in your PATH
2. Verify Python 3.11+ is installed: `python --version`
3. Verify `mcp_config.json` syntax is valid JSON
4. Check Antigravity logs: View → Output → MCP

### Tools Not Available

**Issue:** WISTX tools don't appear in Antigravity

**Solutions:**
1. Verify `mcp_config.json` syntax is valid JSON
2. Restart Antigravity completely
3. Verify `WISTX_API_KEY` is correct and active
4. Check that pipx/uvx is working correctly

### Connection Errors

**Issue:** Connection errors when using WISTX tools

**Solutions:**
1. Verify `WISTX_API_KEY` is correct
2. Check your API key is active at [app.wistx.ai](https://app.wistx.ai/)
3. Check network connectivity
4. Verify pipx/uvx installation

---

## Antigravity Features

### MCP Server Management

Antigravity provides a user-friendly interface for managing MCP servers:

- **Manage MCPs Tab:** View and configure installed servers
- **MCP Server Store:** Browse and install servers with one click
- **Raw Config View:** Edit `mcp_config.json` directly
- **Refresh Button:** Reload server configurations

### Agent Integration

Antigravity's agent-first architecture means:

- **Autonomous Agents:** AI agents can use WISTX tools independently
- **Multi-Agent Support:** Multiple agents can use WISTX simultaneously
- **Direct Access:** Agents have direct access to MCP tools
- **Self-Validation:** Agents can test and validate using WISTX tools

---

## Additional Resources

- **Antigravity Website:** https://antigravity.google/
- **Antigravity Documentation:** See Antigravity's built-in docs
- **WISTX Documentation:** See `README.md` in project root
- **MCP Protocol:** https://modelcontextprotocol.io/

---

## Support

For issues with:
- **Antigravity:** Check Antigravity's documentation and support
- **WISTX MCP Server:** Open an issue in the WISTX repository
- **Configuration:** See troubleshooting section above

---

**Last Updated:** 2024-12-19  
**Antigravity Version:** Public Preview (November 2025)  
**WISTX Version:** Latest

