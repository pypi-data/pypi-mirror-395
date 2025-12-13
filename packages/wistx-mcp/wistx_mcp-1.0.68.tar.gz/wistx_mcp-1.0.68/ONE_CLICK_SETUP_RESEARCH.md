# One-Click Setup for WISTX MCP: Comprehensive Research & Analysis

## Executive Summary

This document provides a deep analysis of the current WISTX MCP system and comprehensive research on implementing one-click setup for all AI coding agents and IDEs. The goal is to eliminate manual configuration stress and provide a seamless installation experience across all supported platforms.

**Key Findings:**
- Current setup requires 3-5 manual steps per IDE
- Configuration files vary across IDEs (Cursor, Windsurf, Claude Desktop, VS Code, etc.)
- Users must manually edit JSON configuration files
- No unified installation experience
- Google Antigravity already supports one-click via MCP Server Store (reference implementation)

**Recommended Approach:**
- Multi-strategy implementation combining IDE-specific deep links, installation scripts, and MCP registry integration
- Progressive enhancement: start with most popular IDEs, expand to others
- Leverage existing patterns from successful MCP servers

---

## 1. Current System Analysis

### 1.1 Architecture Overview

**WISTX MCP Server Structure:**
```
wistx-mcp/
├── server.py              # Main MCP server entry point
├── config.py              # Configuration management
├── tools/                 # 151+ MCP tools
│   ├── compliance.py
│   ├── pricing.py
│   ├── code_examples.py
│   └── ... (unified tools)
└── models/                # Pydantic models
```

**Distribution:**
- Published to PyPI as `wistx-mcp` package
- Installed via `pipx` (recommended) or `uvx`
- Entry point: `wistx-mcp` command
- Version: 1.0.65+ (actively maintained)

### 1.2 Current Installation Process

**For Each IDE, Users Must:**

1. **Complete Onboarding** (one-time)
   - Visit wistx.ai/api-key
   - Get API key
   - No automation currently

2. **Install Package** (one-time per machine)
   ```bash
   pipx install wistx-mcp
   # OR
   uvx wistx-mcp  # (no pre-install needed)
   ```

3. **Locate IDE Config File** (varies by IDE)
   - Cursor: `~/.cursor/mcp.json`
   - Windsurf: `~/.codeium/windsurf/mcp_config.json`
   - Claude Desktop: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - VS Code: `~/.config/Code/User/mcp.json`
   - Continue.dev: `~/.continue/config.json`
   - Claude Code: Project-specific or global
   - Codex: CLI-based
   - Cline: IDE-specific
   - Gemini CLI: `~/.config/gemini-cli/config.json`

4. **Edit JSON Configuration** (manual)
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

5. **Restart IDE** (manual)

**Total Steps: 5 steps × 2-3 minutes = 10-15 minutes per IDE**

### 1.3 Pain Points Identified

**User Friction:**
1. **Configuration File Discovery**: Users must know exact file paths for each IDE
2. **JSON Syntax Errors**: Manual editing leads to syntax mistakes
3. **API Key Management**: Users must copy-paste API keys manually
4. **Multiple IDEs**: Users often use 2-3 IDEs, multiplying setup time
5. **Platform Differences**: macOS, Windows, Linux have different paths
6. **No Validation**: No feedback if configuration is incorrect
7. **Updates**: Manual reconfiguration when package updates

**Technical Challenges:**
1. **IDE Fragmentation**: Each IDE has different config formats
2. **No Standard Protocol**: MCP doesn't define installation standard
3. **Security Concerns**: API keys in plain text config files
4. **Cross-Platform**: Path differences across OS
5. **Package Manager Detection**: pipx vs uvx vs system Python

### 1.4 Current Strengths

**What Works Well:**
- ✅ Package distribution via PyPI is solid
- ✅ pipx/uvx isolation prevents conflicts
- ✅ Documentation is comprehensive
- ✅ Example config files exist (`.cursor-mcp.json.example`)
- ✅ Setup script exists (`setup_mcp.sh`) but requires manual execution
- ✅ Google Antigravity integration works (one-click via store)

---

## 2. Research: One-Click Setup Patterns

### 2.1 Successful Reference Implementations

#### 2.1.1 Google Antigravity MCP Server Store

**How It Works:**
- Antigravity IDE includes built-in "MCP Server Store"
- Users browse/search for servers
- Click "Install" → automatic configuration
- Prompts for API key if needed

**Key Features:**
- Built into IDE (no external tools)
- Server discovery/registry
- One-click installation
- API key prompt during install
- Automatic config file management

**Lessons Learned:**
- IDE-native integration is best UX
- Registry/discovery is crucial
- Prompt for credentials during install
- Handle config file automatically

#### 2.1.2 VS Code Extension Marketplace

**Pattern:**
- Extensions published to marketplace
- Users click "Install" in VS Code
- Extension handles its own configuration
- Settings UI for configuration

**Applicable to MCP:**
- Could create VS Code extension wrapper
- Extension manages MCP server config
- Settings UI for API key
- Auto-install pipx if needed

#### 2.1.3 Homebrew Cask (macOS)

**Pattern:**
```bash
brew install --cask app-name
```

**How It Works:**
- Single command installs app + dependencies
- Handles configuration automatically
- Updates via `brew upgrade`

**Applicable to MCP:**
- Could create Homebrew formula
- Installs pipx + wistx-mcp
- Creates config files
- Sets up for all IDEs at once

### 2.2 Installation Script Patterns

#### 2.2.1 One-Liner Installation Scripts

**Popular Pattern (used by many tools):**
```bash
curl -fsSL https://example.com/install.sh | bash
```

**Examples:**
- Homebrew: `curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash`
- Docker: `curl -fsSL https://get.docker.com | bash`
- nvm: `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash`

**Advantages:**
- Single command
- Cross-platform (with OS detection)
- Can detect IDE installations
- Can prompt for API key
- Can validate setup

**Security Considerations:**
- Users must trust script
- Should be hosted on official domain
- Should show script contents
- Should use HTTPS

#### 2.2.2 Interactive Installation Wizards

**Pattern:**
```bash
./install.sh
# Prompts:
# - Which IDEs do you use? [Cursor, Windsurf, Claude Desktop, ...]
# - Enter your API key: [input]
# - Install for all IDEs? [Y/n]
```

**Advantages:**
- User-friendly
- Handles multiple IDEs
- Validates input
- Shows progress
- Error handling

### 2.3 IDE Deep Link Patterns

#### 2.3.1 URL Scheme Handlers

**Pattern:**
```
cursor://mcp/install?name=wistx&command=pipx&args=run,--no-cache,wistx-mcp&env=WISTX_API_KEY
```

**How It Works:**
- Website/button triggers URL scheme
- IDE opens and handles installation
- IDE prompts for missing env vars (API key)
- IDE writes config file

**Current Status:**
- Cursor: Already supports `cursor://mcp/install` (documented in docs)
- Windsurf: Unknown (needs research)
- VS Code: `vscode://` scheme exists
- Claude Desktop: Unknown

**Advantages:**
- True one-click from web
- IDE handles security
- IDE validates config
- Works across platforms

**Limitations:**
- Requires IDE support
- Not all IDEs support deep links
- Platform-specific (macOS vs Windows)

#### 2.3.2 Browser Extension Pattern

**Pattern:**
- Browser extension detects IDE config pages
- Offers "Auto-configure" button
- Injects configuration via extension API

**Advantages:**
- Works with any IDE
- Can detect open config files
- User-friendly

**Limitations:**
- Requires browser extension
- Security concerns
- Maintenance overhead

### 2.4 Package Manager Integration

#### 2.4.1 npm/pipx/brew Wrapper Scripts

**Pattern:**
```bash
npm install -g wistx-mcp-installer
wistx-mcp-installer --ide cursor --api-key YOUR_KEY
```

**Advantages:**
- Familiar to developers
- Can be versioned
- Easy updates

#### 2.4.2 System Package Managers

**Homebrew (macOS):**
```bash
brew install wistx-mcp
# Installs package + configs for all IDEs
```

**Chocolatey (Windows):**
```powershell
choco install wistx-mcp
```

**apt/yum (Linux):**
```bash
sudo apt install wistx-mcp
```

**Advantages:**
- System-level installation
- Automatic updates
- Handles dependencies

**Limitations:**
- Requires package maintainer
- Platform-specific
- Approval process

### 2.5 MCP Registry/Discovery

#### 2.5.1 Centralized MCP Server Registry

**Concept:**
- Central registry of MCP servers (like npm registry)
- IDEs query registry for available servers
- One-click install from IDE

**Current State:**
- No official MCP registry exists
- Antigravity has its own store
- Opportunity to create community registry

**Implementation Ideas:**
1. **GitHub-Based Registry**
   - JSON file in GitHub repo
   - IDEs fetch from GitHub
   - Community-maintained

2. **Dedicated Registry Service**
   - API endpoint for server metadata
   - Search/discovery
   - Installation instructions

3. **Package Manager Integration**
   - PyPI metadata includes MCP info
   - IDEs read PyPI for MCP servers
   - Automatic discovery

### 2.6 Configuration Management Patterns

#### 2.6.1 Environment Variable Injection

**Pattern:**
- Install script creates `.env` file
- MCP server reads from `.env`
- Config file references env vars

**Example:**
```json
{
  "mcpServers": {
    "wistx": {
      "command": "pipx",
      "args": ["run", "--no-cache", "wistx-mcp"],
      "env": {
        "WISTX_API_KEY": "${WISTX_API_KEY}"
      }
    }
  }
}
```

**Advantages:**
- API key not in config file
- Can use system keychain
- More secure

**Limitations:**
- Not all IDEs support env var expansion
- Requires additional setup

#### 2.6.2 Keychain/Secret Management

**Pattern:**
- Store API key in system keychain (macOS Keychain, Windows Credential Manager, Linux Secret Service)
- MCP server reads from keychain
- Config file doesn't contain secrets

**Advantages:**
- Most secure
- OS-native
- No secrets in files

**Limitations:**
- Requires keychain library
- Platform-specific code
- More complex

#### 2.6.3 Config File Templates with Placeholders

**Pattern:**
- Install script copies template
- Replaces placeholders with values
- Validates JSON before writing

**Example:**
```json
{
  "mcpServers": {
    "wistx": {
      "command": "pipx",
      "args": ["run", "--no-cache", "wistx-mcp"],
      "env": {
        "WISTX_API_KEY": "{{API_KEY}}"
      }
    }
  }
}
```

**Advantages:**
- Simple
- Works everywhere
- Easy to validate

---

## 3. Recommended Implementation Strategy

### 3.1 Multi-Tier Approach

**Tier 1: Quick Wins (Immediate)**
- Enhanced installation script with IDE detection
- Interactive wizard
- Better documentation with copy-paste configs

**Tier 2: IDE Integration (Short-term)**
- Deep link support for Cursor (already documented)
- VS Code extension wrapper
- Homebrew formula

**Tier 3: Registry Integration (Long-term)**
- MCP server registry participation
- IDE store listings
- Community registry

### 3.2 Implementation Plan

#### Phase 1: Enhanced Installation Script (Week 1-2)

**Deliverables:**
1. **Cross-platform installation script**
   - Detects OS (macOS, Windows, Linux)
   - Detects installed IDEs
   - Prompts for API key
   - Installs pipx if needed
   - Configures all detected IDEs

2. **Interactive wizard**
   - CLI interface
   - IDE selection
   - API key input
   - Validation
   - Progress indicators

3. **One-liner installation**
   ```bash
   curl -fsSL https://install.wistx.ai | bash
   ```

**Features:**
- Auto-detects: Cursor, Windsurf, Claude Desktop, VS Code
- Creates config files automatically
- Validates JSON syntax
- Tests MCP server connection
- Provides feedback

**File Structure:**
```
scripts/
├── install.sh              # Main installer (bash)
├── install.ps1             # Windows PowerShell version
├── install.py              # Python version (cross-platform)
└── install-wizard.sh       # Interactive version
```

#### Phase 2: IDE Deep Links (Week 3-4)

**Deliverables:**
1. **Cursor deep link** (already documented, enhance)
   - `cursor://mcp/install?name=wistx&command=pipx&args=run,--no-cache,wistx-mcp&env=WISTX_API_KEY`
   - Web button on docs site
   - Handles API key prompt

2. **VS Code deep link** (research required)
   - `vscode://wistx.install`
   - Or extension-based approach

3. **Web-based installer**
   - Landing page: `install.wistx.ai`
   - Detects OS and installed IDEs
   - Generates appropriate deep link or script
   - One-click button per IDE

**Implementation:**
- Update docs with deep link buttons
- Create installer landing page
- Test with each IDE

#### Phase 3: Package Manager Integration (Week 5-6)

**Deliverables:**
1. **Homebrew formula** (macOS)
   ```bash
   brew install wistx-mcp
   ```

2. **Chocolatey package** (Windows)
   ```powershell
   choco install wistx-mcp
   ```

3. **npm wrapper** (cross-platform)
   ```bash
   npm install -g @wistx/mcp-installer
   wistx-mcp-installer
   ```

**Features:**
- Installs pipx + wistx-mcp
- Configures all IDEs
- Handles updates

#### Phase 4: VS Code Extension (Week 7-8)

**Deliverables:**
1. **VS Code extension**
   - Marketplace listing
   - Settings UI for API key
   - Auto-configures MCP server
   - Status indicator
   - Tool explorer

**Features:**
- Install from VS Code marketplace
- Settings page for configuration
- Visual feedback
- Tool discovery

#### Phase 5: MCP Registry Integration (Week 9-10)

**Deliverables:**
1. **Registry metadata**
   - Standard MCP server manifest
   - PyPI integration
   - GitHub integration

2. **IDE store listings**
   - Submit to Antigravity store (if possible)
   - Submit to other IDE stores
   - Community registry

---

## 4. Detailed Implementation Recommendations

### 4.1 Installation Script Architecture

**Recommended: Python-based installer (cross-platform)**

**Why Python:**
- Already required (Python 3.11+)
- Cross-platform (macOS, Windows, Linux)
- Easy JSON manipulation
- Good error handling
- Can use existing dependencies

**Script Structure:**
```python
# install.py
class MCPInstaller:
    def detect_ides(self) -> list[str]
    def install_package(self) -> bool
    def configure_ide(self, ide: str, api_key: str) -> bool
    def validate_setup(self) -> bool
    def run_interactive(self) -> None
```

**Features:**
- Auto-detects IDEs
- Checks for pipx/uvx
- Installs package if needed
- Configures each IDE
- Validates JSON
- Tests connection
- Provides feedback

**Usage:**
```bash
# Interactive
python install.py

# Non-interactive
python install.py --api-key YOUR_KEY --ides cursor,windsurf

# One-liner
curl -fsSL https://install.wistx.ai/install.py | python3
```

### 4.2 IDE-Specific Strategies

#### 4.2.1 Cursor

**Current:** Manual config file editing

**Recommended:**
1. **Deep link** (already documented)
   - `cursor://mcp/install?name=wistx&command=pipx&args=run,--no-cache,wistx-mcp&env=WISTX_API_KEY`
   - Web button triggers this
   - Cursor prompts for API key

2. **Installation script**
   - Detects Cursor installation
   - Creates `~/.cursor/mcp.json`
   - Merges with existing config

3. **Future: Cursor extension**
   - If Cursor adds extension support
   - Marketplace listing

#### 4.2.2 Windsurf

**Current:** Manual config file editing

**Recommended:**
1. **Installation script**
   - Detects Windsurf installation
   - Creates `~/.codeium/windsurf/mcp_config.json`
   - Handles JSON merging

2. **Deep link** (research required)
   - Check if Windsurf supports URL schemes
   - If yes, implement similar to Cursor

#### 4.2.3 Claude Desktop

**Current:** Manual config file editing

**Recommended:**
1. **Installation script**
   - Detects Claude Desktop
   - Platform-specific paths:
     - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
     - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
     - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Deep link** (research required)
   - Check Claude Desktop URL scheme support

#### 4.2.4 VS Code

**Current:** Manual config file editing

**Recommended:**
1. **VS Code Extension** (best approach)
   - Marketplace listing
   - Settings UI
   - Auto-configuration
   - Tool explorer

2. **Installation script** (fallback)
   - Detects VS Code
   - Creates config file
   - Handles profiles

3. **Deep link** (if supported)
   - `vscode://wistx.install`

#### 4.2.5 Google Antigravity

**Current:** One-click via MCP Server Store ✅

**Recommended:**
- Maintain store listing
- Ensure metadata is up-to-date
- Provide clear description
- Include screenshots/demos

### 4.3 Security Considerations

#### 4.3.1 API Key Handling

**Current:** API key in plain text config file

**Recommended Approaches:**

1. **Environment Variables** (immediate)
   - Config file references `${WISTX_API_KEY}`
   - Install script sets env var
   - More secure than plain text

2. **System Keychain** (future)
   - macOS: Keychain
   - Windows: Credential Manager
   - Linux: Secret Service
   - MCP server reads from keychain

3. **Encrypted Config** (advanced)
   - Encrypt API key in config file
   - MCP server decrypts on startup
   - Requires password/key

**Recommendation:** Start with environment variables, move to keychain later.

#### 4.3.2 Installation Script Security

**Best Practices:**
- Host on official domain (install.wistx.ai)
- Use HTTPS
- Show script contents before execution
- Checksum verification
- Signed scripts (future)

**Example:**
```bash
# Show script first
curl -fsSL https://install.wistx.ai/install.sh

# Then execute
curl -fsSL https://install.wistx.ai/install.sh | bash
```

### 4.4 Error Handling & Validation

**Installation Script Should:**
1. **Pre-flight checks**
   - Python 3.11+ installed
   - pipx/uvx available
   - IDE installations detected
   - Write permissions for config directories

2. **Validation**
   - JSON syntax validation
   - API key format validation
   - MCP server connection test
   - Tool availability check

3. **Error Messages**
   - Clear, actionable errors
   - Links to troubleshooting
   - Platform-specific guidance

4. **Rollback**
   - Backup existing config files
   - Restore on failure
   - Log changes

### 4.5 User Experience Enhancements

#### 4.5.1 Progress Indicators

**During Installation:**
```
🚀 WISTX MCP Installation
========================

✓ Detected Python 3.12
✓ Detected pipx
✓ Installing wistx-mcp...
✓ Detected Cursor IDE
✓ Configuring Cursor...
✓ Detected Windsurf IDE
✓ Configuring Windsurf...
✓ Testing connection...
✓ Installation complete!

Next steps:
1. Restart your IDEs
2. Test with: "What compliance requirements do I need for RDS?"
```

#### 4.5.2 Verification

**Post-Installation:**
```bash
wistx-mcp verify
# Checks:
# - Package installed
# - Config files valid
# - API key works
# - Tools available
```

#### 4.5.3 Updates

**Auto-update notification:**
```bash
wistx-mcp update
# Checks for updates
# Updates package
# Validates config still works
```

### 4.6 Documentation Updates

**Recommended Documentation Structure:**

1. **Quick Start** (one-click focus)
   - "Install in 30 seconds" section
   - One-liner command
   - Deep link buttons per IDE

2. **IDE-Specific Guides**
   - One-click method (if available)
   - Manual method (fallback)
   - Troubleshooting

3. **Advanced Configuration**
   - Environment variables
   - Keychain setup
   - Custom configurations

4. **Troubleshooting**
   - Common issues
   - Platform-specific problems
   - Validation commands

---

## 5. Technical Implementation Details

### 5.1 IDE Detection Logic

**Detection Methods:**

1. **Config File Existence**
   - Check if IDE config directory exists
   - Check if config file exists
   - Platform-specific paths

2. **Process Detection**
   - Check if IDE process is running
   - Platform-specific (ps, tasklist, etc.)

3. **Installation Paths**
   - Common installation locations
   - Registry (Windows)
   - Applications folder (macOS)

**Example:**
```python
def detect_cursor() -> bool:
    """Detect if Cursor is installed."""
    # Check config file location
    config_paths = [
        Path.home() / ".cursor" / "mcp.json",
        Path.home() / ".config" / "cursor" / "mcp.json",
    ]
    return any(p.exists() for p in config_paths)
```

### 5.2 Configuration File Management

**Challenges:**
- Existing configs may have other servers
- Need to merge, not overwrite
- JSON syntax must be valid
- Platform-specific paths

**Solution:**
```python
def configure_ide(ide: str, api_key: str) -> bool:
    """Configure IDE with WISTX MCP server."""
    config_path = get_ide_config_path(ide)
    
    # Read existing config
    if config_path.exists():
        config = json.loads(config_path.read_text())
    else:
        config = {"mcpServers": {}}
    
    # Add/update WISTX server
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    config["mcpServers"]["wistx"] = {
        "command": "pipx",
        "args": ["run", "--no-cache", "wistx-mcp"],
        "env": {
            "WISTX_API_KEY": api_key
        }
    }
    
    # Validate JSON
    json.dumps(config)  # Raises if invalid
    
    # Write back
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2))
    
    return True
```

### 5.3 Package Installation

**Check for pipx/uvx:**
```python
def ensure_package_manager() -> str:
    """Ensure pipx or uvx is available."""
    if shutil.which("pipx"):
        return "pipx"
    elif shutil.which("uvx"):
        return "uvx"
    else:
        # Offer to install pipx
        install_pipx()
        return "pipx"
```

**Install package:**
```python
def install_package(package_manager: str) -> bool:
    """Install wistx-mcp package."""
    if package_manager == "pipx":
        subprocess.run(["pipx", "install", "wistx-mcp"], check=True)
    elif package_manager == "uvx":
        # uvx doesn't need pre-install
        pass
    return True
```

### 5.4 Validation & Testing

**Connection Test:**
```python
def test_connection(api_key: str) -> bool:
    """Test MCP server connection."""
    try:
        # Start MCP server in test mode
        # Call a simple tool
        # Verify response
        return True
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False
```

**Config Validation:**
```python
def validate_config(config_path: Path) -> bool:
    """Validate MCP config file."""
    try:
        config = json.loads(config_path.read_text())
        # Check structure
        assert "mcpServers" in config
        assert "wistx" in config["mcpServers"]
        # Check command exists
        command = config["mcpServers"]["wistx"]["command"]
        assert shutil.which(command)
        return True
    except Exception as e:
        logger.error(f"Config validation failed: {e}")
        return False
```

---

## 6. Competitive Analysis

### 6.1 Other MCP Servers

**Research Needed:**
- How do other popular MCP servers handle installation?
- Do they have one-click setup?
- What patterns do they use?

**Servers to Research:**
- Nia (codebase context)
- GitHub MCP server
- Slack MCP server
- Other popular MCP servers

### 6.2 Similar Tools

**VS Code Extensions:**
- How do extensions handle first-time setup?
- Settings UI patterns
- Auto-configuration

**CLI Tools:**
- Homebrew formulas
- npm packages
- Installation patterns

---

## 7. Success Metrics

### 7.1 Installation Metrics

**Track:**
- Installation time (target: < 2 minutes)
- Success rate (target: > 95%)
- Error rate by platform
- Most common errors

### 7.2 User Feedback

**Collect:**
- Installation experience surveys
- Support tickets related to setup
- Feature requests

### 7.3 Adoption Metrics

**Track:**
- Installations per week
- Active users
- IDE distribution
- Platform distribution

---

## 8. Risks & Mitigation

### 8.1 Technical Risks

**Risk: IDE Config Format Changes**
- Mitigation: Version detection, fallback to manual
- Monitoring: Test with IDE updates

**Risk: Platform-Specific Issues**
- Mitigation: Extensive testing on all platforms
- Fallback: Platform-specific installers

**Risk: Security Concerns**
- Mitigation: Security review, best practices
- Transparency: Open source installer

### 8.2 User Experience Risks

**Risk: Users Prefer Manual Setup**
- Mitigation: Make installer optional, not required
- Provide both options

**Risk: Installation Fails Silently**
- Mitigation: Comprehensive error messages
- Validation and testing

---

## 9. Future Enhancements

### 9.1 Advanced Features

1. **Auto-Updates**
   - Check for package updates
   - Notify users
   - One-click update

2. **Multi-User Support**
   - Team installations
   - Shared configurations
   - Enterprise setup

3. **Cloud-Based Configuration**
   - Sync configs across machines
   - Team settings
   - Centralized management

4. **GUI Installer**
   - Graphical installer (Electron?)
   - Visual IDE selection
   - Progress bars
   - Better UX for non-technical users

### 9.2 IDE Integration

1. **IDE Extensions**
   - Native extensions for each IDE
   - Settings UI
   - Tool explorers
   - Status indicators

2. **IDE Store Listings**
   - Submit to all IDE marketplaces
   - Featured listings
   - Ratings and reviews

### 9.3 MCP Registry

1. **Community Registry**
   - Create/open MCP server registry
   - Standard metadata format
   - Discovery API
   - IDE integration

2. **Package Manager Integration**
   - PyPI metadata
   - npm registry
   - Homebrew
   - Chocolatey

---

## 10. Conclusion & Next Steps

### 10.1 Key Recommendations

1. **Immediate (Week 1-2)**
   - Build enhanced installation script
   - Add interactive wizard
   - Create one-liner installation
   - Update documentation

2. **Short-term (Week 3-6)**
   - Implement IDE deep links
   - Create Homebrew formula
   - Build VS Code extension
   - Web-based installer page

3. **Long-term (Week 7+)**
   - MCP registry integration
   - IDE store listings
   - Advanced features (auto-updates, etc.)

### 10.2 Success Criteria

**One-Click Setup is Successful When:**
- ✅ Installation takes < 2 minutes
- ✅ Works on macOS, Windows, Linux
- ✅ Supports all major IDEs
- ✅ > 95% success rate
- ✅ Users prefer installer over manual setup
- ✅ Support tickets for setup decrease by 80%

### 10.3 Research Gaps

**Additional Research Needed:**
1. **IDE Deep Link Support**
   - Test deep links for each IDE
   - Document supported schemes
   - Create compatibility matrix

2. **MCP Registry Standards**
   - Research existing registries
   - Propose standard format
   - Engage with MCP community

3. **Security Best Practices**
   - Review API key storage options
   - Keychain integration research
   - Security audit

4. **User Testing**
   - Test installation with real users
   - Gather feedback
   - Iterate based on results

---

## Appendix A: IDE Configuration File Locations

### macOS

- **Cursor**: `~/.cursor/mcp.json`
- **Windsurf**: `~/.codeium/windsurf/mcp_config.json`
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **VS Code**: `~/.config/Code/User/mcp.json`
- **Continue.dev**: `~/.continue/config.json`
- **Gemini CLI**: `~/.config/gemini-cli/config.json`

### Windows

- **Cursor**: `%APPDATA%\Cursor\mcp.json`
- **Windsurf**: `%APPDATA%\Codeium\Windsurf\mcp_config.json`
- **Claude Desktop**: `%APPDATA%\Claude\claude_desktop_config.json`
- **VS Code**: `%APPDATA%\Code\User\mcp.json`
- **Continue.dev**: `%APPDATA%\Continue\config.json`
- **Gemini CLI**: `%APPDATA%\gemini-cli\config.json`

### Linux

- **Cursor**: `~/.config/cursor/mcp.json`
- **Windsurf**: `~/.codeium/windsurf/mcp_config.json`
- **Claude Desktop**: `~/.config/Claude/claude_desktop_config.json`
- **VS Code**: `~/.config/Code/User/mcp.json`
- **Continue.dev**: `~/.continue/config.json`
- **Gemini CLI**: `~/.config/gemini-cli/config.json`

---

## Appendix B: Configuration File Formats

### Cursor
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

### Windsurf
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

### Claude Desktop
```json
{
  "mcpServers": {
    "mcp-server-wistx": {
      "command": "pipx",
      "args": ["run", "--no-cache", "wistx-mcp"],
      "env": {
        "WISTX_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### VS Code
```json
{
  "servers": {
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

### Continue.dev
```json
{
  "models": [...],
  "mcpServers": [
    {
      "name": "wistx",
      "command": "pipx",
      "args": ["run", "--no-cache", "wistx-mcp"],
      "env": {
        "WISTX_API_KEY": "YOUR_API_KEY"
      }
    }
  ]
}
```

---

## Appendix C: Installation Script Pseudocode

```python
#!/usr/bin/env python3
"""
WISTX MCP One-Click Installer
Cross-platform installation script for all IDEs
"""

import json
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Optional

class WISTXInstaller:
    def __init__(self):
        self.os = platform.system()
        self.detected_ides = []
        self.api_key = None
        
    def detect_ides(self) -> list[str]:
        """Detect installed IDEs."""
        ides = []
        # Check each IDE
        if self._detect_cursor():
            ides.append("cursor")
        if self._detect_windsurf():
            ides.append("windsurf")
        if self._detect_claude_desktop():
            ides.append("claude-desktop")
        if self._detect_vscode():
            ides.append("vscode")
        # ... more IDEs
        return ides
    
    def ensure_package_manager(self) -> str:
        """Ensure pipx or uvx is available."""
        if shutil.which("pipx"):
            return "pipx"
        elif shutil.which("uvx"):
            return "uvx"
        else:
            # Install pipx
            self._install_pipx()
            return "pipx"
    
    def install_package(self, package_manager: str):
        """Install wistx-mcp package."""
        if package_manager == "pipx":
            subprocess.run(["pipx", "install", "wistx-mcp"], check=True)
        # uvx doesn't need pre-install
    
    def configure_ide(self, ide: str, api_key: str) -> bool:
        """Configure IDE with WISTX MCP server."""
        config_path = self._get_ide_config_path(ide)
        
        # Read or create config
        if config_path.exists():
            config = json.loads(config_path.read_text())
        else:
            config = self._get_default_config(ide)
        
        # Merge WISTX server
        self._add_wistx_server(config, ide, api_key)
        
        # Validate
        json.dumps(config)  # Raises if invalid
        
        # Write
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(config, indent=2))
        
        return True
    
    def validate_setup(self) -> bool:
        """Validate installation."""
        # Check package installed
        # Check config files valid
        # Test connection
        return True
    
    def run_interactive(self):
        """Run interactive installation wizard."""
        print("🚀 WISTX MCP Installation")
        print("=" * 40)
        
        # Detect IDEs
        self.detected_ides = self.detect_ides()
        print(f"✓ Detected IDEs: {', '.join(self.detected_ides)}")
        
        # Get API key
        self.api_key = input("Enter your WISTX API key: ").strip()
        
        # Ensure package manager
        pm = self.ensure_package_manager()
        print(f"✓ Using {pm}")
        
        # Install package
        print("Installing wistx-mcp...")
        self.install_package(pm)
        print("✓ Package installed")
        
        # Configure each IDE
        for ide in self.detected_ides:
            print(f"Configuring {ide}...")
            self.configure_ide(ide, self.api_key)
            print(f"✓ {ide} configured")
        
        # Validate
        if self.validate_setup():
            print("✓ Installation complete!")
        else:
            print("⚠️  Installation completed with warnings")
            print("   Run 'wistx-mcp verify' to check setup")

if __name__ == "__main__":
    installer = WISTXInstaller()
    installer.run_interactive()
```

---

## Appendix D: Deep Link Examples

### Cursor
```
cursor://mcp/install?name=wistx&command=pipx&args=run,--no-cache,wistx-mcp&env=WISTX_API_KEY
```

### VS Code (hypothetical)
```
vscode://wistx.install?apiKey=YOUR_KEY
```

### Web Button HTML
```html
<a href="cursor://mcp/install?name=wistx&command=pipx&args=run,--no-cache,wistx-mcp&env=WISTX_API_KEY">
  <button>Install in Cursor</button>
</a>
```

---

## Appendix E: Resources & References

### MCP Protocol
- [MCP Specification](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/anthropics/anthropic-mcp-python)

### IDE Documentation
- Cursor MCP docs
- Windsurf MCP docs
- Claude Desktop config
- VS Code MCP extension

### Installation Patterns
- Homebrew formulas
- npm install scripts
- One-liner installers

### Security
- API key storage best practices
- System keychain APIs
- Environment variable security

---

**Document Version:** 1.0  
**Last Updated:** 2025-01-XX  
**Author:** WISTX Engineering Team  
**Status:** Research Complete - Ready for Implementation Planning

