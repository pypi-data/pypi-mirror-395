#!/bin/bash

# Wrapper script to run MCP server with stderr redirected to log file
# This prevents error output from interfering with MCP JSON protocol

LOG_DIR="$HOME/Library/Logs/Claude/wistx-mcp"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/server-$(date +%Y%m%d-%H%M%S).log"

cd /Users/clever/Desktop/wistx-model

# Redirect stderr to log file, keep stdout for MCP JSON protocol
exec 2>> "$LOG_FILE"

# Run the server
uv run python -m wistx_mcp.server "$@"



