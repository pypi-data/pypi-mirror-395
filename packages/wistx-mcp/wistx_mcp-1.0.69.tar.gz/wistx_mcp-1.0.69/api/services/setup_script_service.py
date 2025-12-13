"""Service for generating setup scripts for different IDEs."""

from typing import Optional


class SetupScriptService:
    """Service for generating setup scripts."""

    IDE_CONFIGS = {
        "cursor": {
            "macos": "~/.cursor/mcp.json",
            "windows": "%APPDATA%\\Cursor\\mcp.json",
            "linux": "~/.config/cursor/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "windsurf": {
            "macos": "~/.codeium/windsurf/mcp_config.json",
            "windows": "%APPDATA%\\Codeium\\Windsurf\\mcp_config.json",
            "linux": "~/.codeium/windsurf/mcp_config.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "claude-desktop": {
            "macos": "~/Library/Application Support/Claude/claude_desktop_config.json",
            "windows": "%APPDATA%\\Claude\\claude_desktop_config.json",
            "linux": "~/.config/Claude/claude_desktop_config.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "vscode": {
            "macos": "~/.config/Code/User/mcp.json",
            "windows": "%APPDATA%\\Code\\User\\mcp.json",
            "linux": "~/.config/Code/User/mcp.json",
            "config_key": "servers",
            "config_type": "json",
        },
        "continue": {
            "macos": "~/.continue/config.json",
            "windows": "%APPDATA%\\Continue\\config.json",
            "linux": "~/.continue/config.json",
            "config_key": "mcpServers",
            "config_type": "json_array",
        },
        "claude-code": {
            "macos": None,
            "windows": None,
            "linux": None,
            "config_key": None,
            "config_type": "cli",
        },
        "codex": {
            "macos": None,
            "windows": None,
            "linux": None,
            "config_key": None,
            "config_type": "cli",
        },
        "cline": {
            "macos": "~/.config/cline/mcp.json",
            "windows": "%APPDATA%\\Cline\\mcp.json",
            "linux": "~/.config/cline/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "antigravity": {
            "macos": "~/.codeium/antigravity/mcp_config.json",
            "windows": "%APPDATA%\\Codeium\\Antigravity\\mcp_config.json",
            "linux": "~/.codeium/antigravity/mcp_config.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "gemini-cli": {
            "macos": "~/.config/gemini-cli/config.json",
            "windows": "%APPDATA%\\gemini-cli\\config.json",
            "linux": "~/.config/gemini-cli/config.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "factory": {
            "macos": None,
            "windows": None,
            "linux": None,
            "config_key": None,
            "config_type": "cli",
        },
        "amp": {
            "macos": None,
            "windows": None,
            "linux": None,
            "config_key": None,
            "config_type": "cli",
        },
        "warp": {
            "macos": "~/.warp/mcp.json",
            "windows": "%APPDATA%\\Warp\\mcp.json",
            "linux": "~/.config/warp/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "copilot-agent": {
            "macos": "~/.github/copilot/mcp.json",
            "windows": "%APPDATA%\\GitHub\\Copilot\\mcp.json",
            "linux": "~/.config/github/copilot/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "copilot-cli": {
            "macos": "~/.copilot/mcp-config.json",
            "windows": "%APPDATA%\\Copilot\\mcp-config.json",
            "linux": "~/.config/copilot/mcp-config.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "amazon-q": {
            "macos": "~/.amazon-q/mcp.json",
            "windows": "%APPDATA%\\AmazonQ\\mcp.json",
            "linux": "~/.config/amazon-q/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "opencode": {
            "macos": "~/.opencode/mcp.json",
            "windows": "%APPDATA%\\Opencode\\mcp.json",
            "linux": "~/.config/opencode/mcp.json",
            "config_key": "mcp",
            "config_type": "json",
        },
        "crush": {
            "macos": "~/.crush/mcp.json",
            "windows": "%APPDATA%\\Crush\\mcp.json",
            "linux": "~/.config/crush/mcp.json",
            "config_key": "mcp",
            "config_type": "json",
        },
        "augment": {
            "macos": "~/.augment/config.json",
            "windows": "%APPDATA%\\Augment\\config.json",
            "linux": "~/.config/augment/config.json",
            "config_key": "augment.advanced.mcpServers",
            "config_type": "json_array",
        },
        "trae": {
            "macos": "~/.trae/mcp.json",
            "windows": "%APPDATA%\\Trae\\mcp.json",
            "linux": "~/.config/trae/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "zed": {
            "macos": "~/.zed/settings.json",
            "windows": "%APPDATA%\\Zed\\settings.json",
            "linux": "~/.config/zed/settings.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "jetbrains": {
            "macos": "~/.config/JetBrains/mcp.json",
            "windows": "%APPDATA%\\JetBrains\\mcp.json",
            "linux": "~/.config/JetBrains/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "roo-code": {
            "macos": "~/.roo-code/mcp.json",
            "windows": "%APPDATA%\\RooCode\\mcp.json",
            "linux": "~/.config/roo-code/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "kilo-code": {
            "macos": "~/.kilo-code/mcp.json",
            "windows": "%APPDATA%\\KiloCode\\mcp.json",
            "linux": "~/.config/kilo-code/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "qodo-gen": {
            "macos": "~/.qodo-gen/mcp.json",
            "windows": "%APPDATA%\\QodoGen\\mcp.json",
            "linux": "~/.config/qodo-gen/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "qwen-coder": {
            "macos": "~/.qwen-coder/mcp.json",
            "windows": "%APPDATA%\\QwenCoder\\mcp.json",
            "linux": "~/.config/qwen-coder/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "visual-studio": {
            "macos": "~/.visual-studio/mcp.json",
            "windows": "%APPDATA%\\Microsoft\\VisualStudio\\mcp.json",
            "linux": "~/.config/visual-studio/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "lm-studio": {
            "macos": "~/.lm-studio/mcp.json",
            "windows": "%APPDATA%\\LMStudio\\mcp.json",
            "linux": "~/.config/lm-studio/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "bolt-ai": {
            "macos": "~/.bolt-ai/mcp.json",
            "windows": "%APPDATA%\\BoltAI\\mcp.json",
            "linux": "~/.config/bolt-ai/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
        "perplexity": {
            "macos": "~/.perplexity/mcp.json",
            "windows": "%APPDATA%\\Perplexity\\mcp.json",
            "linux": "~/.config/perplexity/mcp.json",
            "config_key": "mcpServers",
            "config_type": "json",
        },
    }

    def generate_script(
        self,
        api_key: Optional[str] = None,
        ide: Optional[str] = None,
        remote: bool = False,
    ) -> str:
        """Generate setup script.

        Args:
            api_key: Optional API key (can also be passed as script argument)
            ide: Optional IDE name (can also be passed as script argument)
            remote: Use remote server instead of local

        Returns:
            Bash script content
        """
        api_key_placeholder = api_key if api_key else "YOUR_API_KEY"
        ide_placeholder = ide if ide else "auto"
        mode_default = "remote" if remote else "local"

        script = """#!/bin/bash
# WISTX MCP Automated Setup Script
# Generated by WISTX API

set -e

API_KEY="${1:-__API_KEY_PLACEHOLDER__}"
IDE_NAME="${2:-__IDE_PLACEHOLDER__}"
MODE="${3:-__MODE_DEFAULT__}"

detect_os() {{
    case "$(uname -s)" in
        Darwin*) echo "macos" ;;
        Linux*) echo "linux" ;;
        CYGWIN*|MINGW*|MSYS*) echo "windows" ;;
        *) echo "unknown" ;;
    esac
}}

OS=$(detect_os)

detect_ides() {{
    local detected=()
    local os="$1"
    
    if [ -f "$HOME/.cursor/mcp.json" ] || [ -f "$HOME/.config/cursor/mcp.json" ]; then
        detected+=("cursor")
    fi
    
    if [ -f "$HOME/.codeium/windsurf/mcp_config.json" ]; then
        detected+=("windsurf")
    fi
    
    if [ "$os" = "macos" ] && [ -f "$HOME/Library/Application Support/Claude/claude_desktop_config.json" ]; then
        detected+=("claude-desktop")
    elif [ "$os" = "linux" ] && [ -f "$HOME/.config/Claude/claude_desktop_config.json" ]; then
        detected+=("claude-desktop")
    elif [ "$os" = "windows" ] && [ -f "$APPDATA/Claude/claude_desktop_config.json" ]; then
        detected+=("claude-desktop")
    fi
    
    if [ -f "$HOME/.config/Code/User/mcp.json" ]; then
        detected+=("vscode")
    fi
    
    if [ -f "$HOME/.continue/config.json" ]; then
        detected+=("continue")
    fi
    
    if [ -f "$HOME/.config/cline/mcp.json" ]; then
        detected+=("cline")
    fi
    
    if [ -f "$HOME/.codeium/antigravity/mcp_config.json" ]; then
        detected+=("antigravity")
    fi
    
    if [ -f "$HOME/.config/gemini-cli/config.json" ] || [ -f "$HOME/.gemini-cli/config.json" ]; then
        detected+=("gemini-cli")
    fi
    
    if command -v droid >/dev/null 2>&1; then
        detected+=("factory")
    fi
    
    if command -v amp >/dev/null 2>&1; then
        detected+=("amp")
    fi
    
    if [ -f "$HOME/.warp/mcp.json" ] || [ -f "$HOME/.config/warp/mcp.json" ]; then
        detected+=("warp")
    fi
    
    if [ -f "$HOME/.copilot/mcp-config.json" ]; then
        detected+=("copilot-cli")
    fi
    
    if [ -f "$HOME/.config/github/copilot/mcp.json" ]; then
        detected+=("copilot-agent")
    fi
    
    if [ -f "$HOME/.config/amazon-q/mcp.json" ]; then
        detected+=("amazon-q")
    fi
    
    if [ -f "$HOME/.opencode/mcp.json" ] || [ -f "$HOME/.config/opencode/mcp.json" ]; then
        detected+=("opencode")
    fi
    
    if [ -f "$HOME/.crush/mcp.json" ] || [ -f "$HOME/.config/crush/mcp.json" ]; then
        detected+=("crush")
    fi
    
    if [ -f "$HOME/.augment/config.json" ] || [ -f "$HOME/.config/augment/config.json" ]; then
        detected+=("augment")
    fi
    
    if [ -f "$HOME/.trae/mcp.json" ] || [ -f "$HOME/.config/trae/mcp.json" ]; then
        detected+=("trae")
    fi
    
    if [ -f "$HOME/.zed/settings.json" ] || [ -f "$HOME/.config/zed/settings.json" ]; then
        detected+=("zed")
    fi
    
    if [ -f "$HOME/.config/JetBrains/mcp.json" ]; then
        detected+=("jetbrains")
    fi
    
    if command -v claude >/dev/null 2>&1; then
        detected+=("claude-code")
    fi
    
    if command -v codex >/dev/null 2>&1; then
        detected+=("codex")
    fi
    
    echo "${{detected[*]}}"
}}

configure_ide() {{
    local ide="$1"
    local api_key="$2"
    local mode="$3"
    local os="$4"
    
    case "$ide" in
        claude-code)
            if [ "$mode" = "remote" ]; then
                if command -v claude >/dev/null 2>&1; then
                    claude mcp add --transport http wistx https://api.wistx.ai/v1/mcp/request \\
                        --header "Authorization: Bearer $api_key" --scope user || true
                    echo "✅ Configured claude-code (remote) successfully!"
                else
                    echo "❌ Claude Code CLI not found. Please install it first."
                    return 1
                fi
            else
                if command -v claude >/dev/null 2>&1; then
                    claude mcp add wistx -e WISTX_API_KEY="$api_key" --scope user -- pipx run --no-cache wistx-mcp || true
                    echo "✅ Configured claude-code (local) successfully!"
                else
                    echo "❌ Claude Code CLI not found. Please install it first."
                    return 1
                fi
            fi
            ;;
        codex)
            if [ "$mode" = "remote" ]; then
                if command -v codex >/dev/null 2>&1; then
                    codex mcp add wistx --type http --url https://api.wistx.ai/v1/mcp/request \\
                        --header "Authorization: Bearer $api_key" || true
                    echo "✅ Configured codex (remote) successfully!"
                else
                    echo "❌ Codex CLI not found. Please install it first."
                    return 1
                fi
            else
                if command -v codex >/dev/null 2>&1; then
                    codex mcp add wistx --env WISTX_API_KEY="$api_key" -- pipx run --no-cache wistx-mcp || true
                    echo "✅ Configured codex (local) successfully!"
                else
                    echo "❌ Codex CLI not found. Please install it first."
                    return 1
                fi
            fi
            ;;
        factory)
            if [ "$mode" = "remote" ]; then
                if command -v droid >/dev/null 2>&1; then
                    droid mcp add wistx https://api.wistx.ai/v1/mcp/request --type http \\
                        --header "Authorization: Bearer $api_key" || true
                    echo "✅ Configured factory (remote) successfully!"
                else
                    echo "❌ Factory droid CLI not found. Please install it first."
                    return 1
                fi
            else
                if command -v droid >/dev/null 2>&1; then
                    droid mcp add wistx "pipx run --no-cache wistx-mcp" --env WISTX_API_KEY="$api_key" || true
                    echo "✅ Configured factory (local) successfully!"
                else
                    echo "❌ Factory droid CLI not found. Please install it first."
                    return 1
                fi
            fi
            ;;
        amp)
            if command -v amp >/dev/null 2>&1; then
                amp mcp add wistx --header "Authorization=Bearer $api_key" https://api.wistx.ai/v1/mcp/request || true
                echo "✅ Configured amp successfully!"
            else
                echo "❌ Amp CLI not found. Please install it first."
                return 1
            fi
            ;;
        *)
            local config_path
            local config_key
            local config_type
            
            case "$ide" in
                cursor)
                    case "$os" in
                        macos) config_path="$HOME/.cursor/mcp.json" ;;
                        linux) config_path="$HOME/.config/cursor/mcp.json" ;;
                        windows) config_path="$APPDATA/Cursor/mcp.json" ;;
                    esac
                    config_key="mcpServers"
                    config_type="json"
                    ;;
                windsurf)
                    config_path="$HOME/.codeium/windsurf/mcp_config.json"
                    config_key="mcpServers"
                    config_type="json"
                    ;;
                claude-desktop)
                    case "$os" in
                        macos) config_path="$HOME/Library/Application Support/Claude/claude_desktop_config.json" ;;
                        linux) config_path="$HOME/.config/Claude/claude_desktop_config.json" ;;
                        windows) config_path="$APPDATA/Claude/claude_desktop_config.json" ;;
                    esac
                    config_key="mcpServers"
                    config_type="json"
                    ;;
                vscode)
                    case "$os" in
                        macos) config_path="$HOME/.config/Code/User/mcp.json" ;;
                        linux) config_path="$HOME/.config/Code/User/mcp.json" ;;
                        windows) config_path="$APPDATA/Code/User/mcp.json" ;;
                    esac
                    config_key="servers"
                    config_type="json"
                    ;;
                continue)
                    case "$os" in
                        macos) config_path="$HOME/.continue/config.json" ;;
                        linux) config_path="$HOME/.continue/config.json" ;;
                        windows) config_path="$APPDATA/Continue/config.json" ;;
                    esac
                    config_key="mcpServers"
                    config_type="json_array"
                    ;;
                cline)
                    case "$os" in
                        macos) config_path="$HOME/.config/cline/mcp.json" ;;
                        linux) config_path="$HOME/.config/cline/mcp.json" ;;
                        windows) config_path="$APPDATA/Cline/mcp.json" ;;
                    esac
                    config_key="mcpServers"
                    config_type="json"
                    ;;
                antigravity)
                    case "$os" in
                        macos) config_path="$HOME/.codeium/antigravity/mcp_config.json" ;;
                        linux) config_path="$HOME/.codeium/antigravity/mcp_config.json" ;;
                        windows) config_path="$APPDATA/Codeium/Antigravity/mcp_config.json" ;;
                    esac
                    config_key="mcpServers"
                    config_type="json"
                    ;;
                gemini-cli)
                    case "$os" in
                        macos) config_path="$HOME/.config/gemini-cli/config.json" ;;
                        linux) config_path="$HOME/.config/gemini-cli/config.json" ;;
                        windows) config_path="$APPDATA/gemini-cli/config.json" ;;
                    esac
                    config_key="mcpServers"
                    config_type="json"
                    ;;
                warp)
                    case "$os" in
                        macos) config_path="$HOME/.warp/mcp.json" ;;
                        linux) config_path="$HOME/.config/warp/mcp.json" ;;
                        windows) config_path="$APPDATA/Warp/mcp.json" ;;
                    esac
                    config_key="mcpServers"
                    config_type="json"
                    ;;
                copilot-agent)
                    case "$os" in
                        macos) config_path="$HOME/.github/copilot/mcp.json" ;;
                        linux) config_path="$HOME/.config/github/copilot/mcp.json" ;;
                        windows) config_path="$APPDATA/GitHub/Copilot/mcp.json" ;;
                    esac
                    config_key="mcpServers"
                    config_type="json"
                    ;;
                copilot-cli)
                    case "$os" in
                        macos) config_path="$HOME/.copilot/mcp-config.json" ;;
                        linux) config_path="$HOME/.config/copilot/mcp-config.json" ;;
                        windows) config_path="$APPDATA/Copilot/mcp-config.json" ;;
                    esac
                    config_key="mcpServers"
                    config_type="json"
                    ;;
                amazon-q)
                    case "$os" in
                        macos) config_path="$HOME/.amazon-q/mcp.json" ;;
                        linux) config_path="$HOME/.config/amazon-q/mcp.json" ;;
                        windows) config_path="$APPDATA/AmazonQ/mcp.json" ;;
                    esac
                    config_key="mcpServers"
                    config_type="json"
                    ;;
                opencode)
                    case "$os" in
                        macos) config_path="$HOME/.opencode/mcp.json" ;;
                        linux) config_path="$HOME/.config/opencode/mcp.json" ;;
                        windows) config_path="$APPDATA/Opencode/mcp.json" ;;
                    esac
                    config_key="mcp"
                    config_type="json"
                    ;;
                crush)
                    case "$os" in
                        macos) config_path="$HOME/.crush/mcp.json" ;;
                        linux) config_path="$HOME/.config/crush/mcp.json" ;;
                        windows) config_path="$APPDATA/Crush/mcp.json" ;;
                    esac
                    config_key="mcp"
                    config_type="json"
                    ;;
                augment)
                    case "$os" in
                        macos) config_path="$HOME/.augment/config.json" ;;
                        linux) config_path="$HOME/.config/augment/config.json" ;;
                        windows) config_path="$APPDATA/Augment/config.json" ;;
                    esac
                    config_key="augment.advanced.mcpServers"
                    config_type="json_array"
                    ;;
                trae)
                    case "$os" in
                        macos) config_path="$HOME/.trae/mcp.json" ;;
                        linux) config_path="$HOME/.config/trae/mcp.json" ;;
                        windows) config_path="$APPDATA/Trae/mcp.json" ;;
                    esac
                    config_key="mcpServers"
                    config_type="json"
                    ;;
                zed)
                    case "$os" in
                        macos) config_path="$HOME/.zed/settings.json" ;;
                        linux) config_path="$HOME/.config/zed/settings.json" ;;
                        windows) config_path="$APPDATA/Zed/settings.json" ;;
                    esac
                    config_key="mcpServers"
                    config_type="json"
                    ;;
                jetbrains)
                    case "$os" in
                        macos) config_path="$HOME/.config/JetBrains/mcp.json" ;;
                        linux) config_path="$HOME/.config/JetBrains/mcp.json" ;;
                        windows) config_path="$APPDATA/JetBrains/mcp.json" ;;
                    esac
                    config_key="mcpServers"
                    config_type="json"
                    ;;
                roo-code|kilo-code|qodo-gen|qwen-coder|visual-studio|lm-studio|bolt-ai|perplexity)
                    case "$ide" in
                        roo-code)
                            case "$os" in
                                macos) config_path="$HOME/.roo-code/mcp.json" ;;
                                linux) config_path="$HOME/.config/roo-code/mcp.json" ;;
                                windows) config_path="$APPDATA/RooCode/mcp.json" ;;
                            esac
                            ;;
                        kilo-code)
                            case "$os" in
                                macos) config_path="$HOME/.kilo-code/mcp.json" ;;
                                linux) config_path="$HOME/.config/kilo-code/mcp.json" ;;
                                windows) config_path="$APPDATA/KiloCode/mcp.json" ;;
                            esac
                            ;;
                        qodo-gen)
                            case "$os" in
                                macos) config_path="$HOME/.qodo-gen/mcp.json" ;;
                                linux) config_path="$HOME/.config/qodo-gen/mcp.json" ;;
                                windows) config_path="$APPDATA/QodoGen/mcp.json" ;;
                            esac
                            ;;
                        qwen-coder)
                            case "$os" in
                                macos) config_path="$HOME/.qwen-coder/mcp.json" ;;
                                linux) config_path="$HOME/.config/qwen-coder/mcp.json" ;;
                                windows) config_path="$APPDATA/QwenCoder/mcp.json" ;;
                            esac
                            ;;
                        visual-studio)
                            case "$os" in
                                macos) config_path="$HOME/.visual-studio/mcp.json" ;;
                                linux) config_path="$HOME/.config/visual-studio/mcp.json" ;;
                                windows) config_path="$APPDATA/Microsoft/VisualStudio/mcp.json" ;;
                            esac
                            ;;
                        lm-studio)
                            case "$os" in
                                macos) config_path="$HOME/.lm-studio/mcp.json" ;;
                                linux) config_path="$HOME/.config/lm-studio/mcp.json" ;;
                                windows) config_path="$APPDATA/LMStudio/mcp.json" ;;
                            esac
                            ;;
                        bolt-ai)
                            case "$os" in
                                macos) config_path="$HOME/.bolt-ai/mcp.json" ;;
                                linux) config_path="$HOME/.config/bolt-ai/mcp.json" ;;
                                windows) config_path="$APPDATA/BoltAI/mcp.json" ;;
                            esac
                            ;;
                        perplexity)
                            case "$os" in
                                macos) config_path="$HOME/.perplexity/mcp.json" ;;
                                linux) config_path="$HOME/.config/perplexity/mcp.json" ;;
                                windows) config_path="$APPDATA/Perplexity/mcp.json" ;;
                            esac
                            ;;
                    esac
                    config_key="mcpServers"
                    config_type="json"
                    ;;
                *)
                    echo "❌ Unknown IDE: $ide"
                    return 1
                    ;;
            esac
            
            mkdir -p "$(dirname "$config_path")"
            
            if [ "$mode" = "remote" ]; then
                if [ "$ide" = "antigravity" ]; then
                    wistx_server_config='{"serverUrl":"https://api.wistx.ai/v1/mcp/request","headers":{"Authorization":"Bearer '"$api_key"'"}}'
                elif [ "$ide" = "cline" ]; then
                    wistx_server_config='{"url":"https://api.wistx.ai/v1/mcp/request","type":"streamableHttp","headers":{"Authorization":"Bearer '"$api_key"'"}}'
                elif [ "$ide" = "vscode" ] || [ "$ide" = "copilot-agent" ] || [ "$ide" = "copilot-cli" ]; then
                    wistx_server_config='{"type":"http","url":"https://api.wistx.ai/v1/mcp/request","headers":{"Authorization":"Bearer '"$api_key"'"}}'
                elif [ "$ide" = "opencode" ]; then
                    wistx_server_config='{"type":"remote","url":"https://api.wistx.ai/v1/mcp/request","headers":{"Authorization":"Bearer '"$api_key"'"},"enabled":true}'
                elif [ "$ide" = "crush" ]; then
                    wistx_server_config='{"type":"http","url":"https://api.wistx.ai/v1/mcp/request","headers":{"Authorization":"Bearer '"$api_key"'"}}'
                elif [ "$ide" = "continue" ]; then
                    wistx_server_config='{"transport":{"type":"http","url":"https://api.wistx.ai/v1/mcp/request","headers":{"Authorization":"Bearer '"$api_key"'"}}}'
                else
                    wistx_server_config='{"url":"https://api.wistx.ai/v1/mcp/request","headers":{"Authorization":"Bearer '"$api_key"'"}}'
                fi
            else
                if [ "$ide" = "continue" ]; then
                    wistx_server_config='{"name":"wistx","command":"pipx","args":["run","--no-cache","wistx-mcp"],"env":{"WISTX_API_KEY":"'"$api_key"'"}}'
                elif [ "$ide" = "augment" ]; then
                    wistx_server_config='{"name":"wistx","command":"pipx","args":["run","--no-cache","wistx-mcp"],"env":{"WISTX_API_KEY":"'"$api_key"'"}}'
                elif [ "$ide" = "vscode" ] || [ "$ide" = "copilot-agent" ]; then
                    wistx_server_config='{"type":"stdio","command":"pipx","args":["run","--no-cache","wistx-mcp"],"env":{"WISTX_API_KEY":"'"$api_key"'"}}'
                elif [ "$ide" = "copilot-cli" ]; then
                    wistx_server_config='{"type":"local","command":"pipx","args":["run","--no-cache","wistx-mcp"],"env":{"WISTX_API_KEY":"'"$api_key"'"}}'
                elif [ "$ide" = "opencode" ]; then
                    wistx_server_config='{"type":"local","command":["pipx","run","--no-cache","wistx-mcp"],"env":{"WISTX_API_KEY":"'"$api_key"'"},"enabled":true}'
                elif [ "$ide" = "crush" ]; then
                    wistx_server_config='{"type":"stdio","command":"pipx","args":["run","--no-cache","wistx-mcp"],"env":{"WISTX_API_KEY":"'"$api_key"'"}}'
                else
                    wistx_server_config='{"command":"pipx","args":["run","--no-cache","wistx-mcp"],"env":{"WISTX_API_KEY":"'"$api_key"'"}}'
                fi
            fi
            
            python3 << EOF
import json
import sys
import os

config_path = os.path.expanduser("$config_path")
config_key = "$config_key"
config_type = "$config_type"
wistx_server_config_str = '''$wistx_server_config'''

if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
else:
    config = {{}}

if config_type == "json_array":
    if config_key == "mcpServers":
        if "mcpServers" not in config:
            config["mcpServers"] = []
        wistx_server_config = json.loads(wistx_server_config_str)
        existing = [s for s in config["mcpServers"] if isinstance(s, dict) and s.get("name") == "wistx"]
        if existing:
            config["mcpServers"] = [s for s in config["mcpServers"] if not (isinstance(s, dict) and s.get("name") == "wistx")]
        config["mcpServers"].append(wistx_server_config)
    elif config_key == "augment.advanced.mcpServers":
        if "augment" not in config:
            config["augment"] = {{}}
        if "advanced" not in config["augment"]:
            config["augment"]["advanced"] = {{}}
        if "mcpServers" not in config["augment"]["advanced"]:
            config["augment"]["advanced"]["mcpServers"] = []
        wistx_server_config = json.loads(wistx_server_config_str)
        existing = [s for s in config["augment"]["advanced"]["mcpServers"] if isinstance(s, dict) and s.get("name") == "wistx"]
        if existing:
            config["augment"]["advanced"]["mcpServers"] = [s for s in config["augment"]["advanced"]["mcpServers"] if not (isinstance(s, dict) and s.get("name") == "wistx")]
        config["augment"]["advanced"]["mcpServers"].append(wistx_server_config)
    elif config_key == "continue":
        if "experimental" not in config:
            config["experimental"] = {{}}
        if "modelContextProtocolServer" not in config["experimental"]:
            config["experimental"]["modelContextProtocolServer"] = {{}}
        wistx_server_config = json.loads(wistx_server_config_str)
        config["experimental"]["modelContextProtocolServer"] = wistx_server_config
else:
    if config_key not in config:
        config[config_key] = {{}}
    
    wistx_server_config = json.loads(wistx_server_config_str)
    config[config_key]["wistx"] = wistx_server_config
    
    ide_name = "$ide"
    if ide_name == "crush" and "$schema" not in config:
        config["$schema"] = "https://charm.land/crush.json"

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Configured $ide successfully!")
EOF
            ;;
    esac
}}

main() {{
    echo "🚀 WISTX MCP Installation"
    echo "========================"
    echo ""
    
    if [ "$API_KEY" = "__API_KEY_PLACEHOLDER__" ] || [ -z "$API_KEY" ]; then
        echo "⚠️  Please provide your API key:"
        echo "   curl -fsSL https://api.wistx.ai/v1/setup/script | bash -s -- YOUR_API_KEY"
        exit 1
    fi
    
    if [ "$IDE_NAME" = "__IDE_PLACEHOLDER__" ] || [ -z "$IDE_NAME" ]; then
        echo "🔍 Detecting installed IDEs..."
        detected=$(detect_ides "$OS")
        if [ -z "$detected" ]; then
            echo "❌ No supported IDEs detected"
            echo "   Please specify IDE: curl ... | bash -s -- YOUR_API_KEY cursor"
            echo ""
            echo "   Supported IDEs: cursor, vscode, windsurf, cline, antigravity, trae, continue,"
            echo "   claude-desktop, claude-code, codex, gemini-cli, factory, amp, warp,"
            echo "   copilot-agent, copilot-cli, opencode, crush, amazon-q, augment, jetbrains,"
            echo "   zed, roo-code, kilo-code, qodo-gen, qwen-coder, visual-studio, lm-studio,"
            echo "   bolt-ai, perplexity"
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
        script = script.replace("__API_KEY_PLACEHOLDER__", api_key_placeholder)
        script = script.replace("__IDE_PLACEHOLDER__", ide_placeholder)
        script = script.replace("__MODE_DEFAULT__", mode_default)
        return script
