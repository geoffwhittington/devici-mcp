# Devici MCP Server - Deployment Guide

This guide provides deployment options for the Devici MCP Server using modern Python tooling.

## Prerequisites

- Devici instance URL
- Devici API credentials (Client ID and Secret - generate in Devici under Settings > API Access)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed (recommended)
- Python 3.10+ (if using pip directly)

## Configuration

All deployment methods require setting environment variables:

- `DEVICI_API_BASE_URL`: Your Devici instance URL (e.g., `https://api.devici.com`)
- `DEVICI_CLIENT_ID`: Your Devici client ID
- `DEVICI_CLIENT_SECRET`: Your Devici client secret

## Deployment Options

### Option 1: uvx (Recommended)

The easiest way to run the server without installation:

```bash
# Set environment variables
export DEVICI_API_BASE_URL="https://api.devici.com"
export DEVICI_CLIENT_ID="your-client-id-here"
export DEVICI_CLIENT_SECRET="your-client-secret-here"

# Run directly with uvx from GitHub
uvx git+https://github.com/geoffwhittington/devici-mcp.git

# Once published to PyPI (future):
# uvx devici-mcp-server
```

### Option 2: uv pip Install

Install the package with uv:

```bash
# Install the package from GitHub
uv pip install git+https://github.com/geoffwhittington/devici-mcp.git

# Set environment variables
export DEVICI_API_BASE_URL="https://api.devici.com"
export DEVICI_CLIENT_ID="your-client-id-here"
export DEVICI_CLIENT_SECRET="your-client-secret-here"

# Run the server
devici-mcp-server
```

### Option 3: Traditional pip Install

```bash
# Install the package from GitHub
pip install git+https://github.com/geoffwhittington/devici-mcp.git

# Set environment variables
export DEVICI_API_BASE_URL="https://api.devici.com"
export DEVICI_CLIENT_ID="your-client-id-here"
export DEVICI_CLIENT_SECRET="your-client-secret-here"

# Run the server
devici-mcp-server
```

### Option 4: Development Installation

For development or local modifications:

```bash
# Clone the repository
git clone https://github.com/geoffwhittington/devici-mcp.git
cd devici-mcp

# Create virtual environment and install dependencies
uv sync

# Set environment variables
export DEVICI_API_BASE_URL="https://api.devici.com"
export DEVICI_CLIENT_ID="your-client-id-here"
export DEVICI_CLIENT_SECRET="your-client-secret-here"

# Run in development mode
uv run python -m devici_mcp_server
```

## MCP Client Configuration

### Cursor

To configure the Devici MCP server in Cursor:

#### Step 1: Open Cursor Settings

1. Open Cursor
2. Go to **Settings** (Ctrl/Cmd + ,)
3. Search for "MCP" or navigate to **Extensions** > **Model Context Protocol**

#### Step 2: Add Server Configuration

Choose one of the following configuration options:

#### Option 1: Using uvx (Recommended)

```json
{
  "mcpServers": {
    "devici": {
      "command": "uvx",
      "args": ["git+https://github.com/geoffwhittington/devici-mcp.git"],
      "env": {
        "DEVICI_API_BASE_URL": "https://api.devici.com",
        "DEVICI_CLIENT_ID": "your-client-id-here",
        "DEVICI_CLIENT_SECRET": "your-client-secret-here"
      }
    }
  }
}
```

#### Option 2: Using local installation

If you have installed the package locally with `pip` or `uv pip install`:

```json
{
  "mcpServers": {
    "devici": {
      "command": "devici-mcp-server",
      "env": {
        "DEVICI_API_BASE_URL": "https://api.devici.com",
        "DEVICI_CLIENT_ID": "your-client-id-here",
        "DEVICI_CLIENT_SECRET": "your-client-secret-here"
      }
    }
  }
}
```

#### Option 3: Using Python module directly

If you have the source code and want to run it directly:

```json
{
  "mcpServers": {
    "devici": {
      "command": "python",
      "args": ["-m", "devici_mcp_server"],
      "env": {
        "DEVICI_API_BASE_URL": "https://api.devici.com",
        "DEVICI_CLIENT_ID": "your-client-id-here",
        "DEVICI_CLIENT_SECRET": "your-client-secret-here"
      },
      "cwd": "/path/to/devici-mcp"
    }
  }
}
```

#### Step 3: Restart Cursor

After adding the configuration, restart Cursor for the changes to take effect.

#### Step 4: Verify Connection

1. Open a chat or use the AI assistant in Cursor
2. The Devici tools should now be available
3. You can ask questions like "List all users in Devici" or "Show me threat models for collection ID 123"

### Claude Desktop

Add this to your Claude Desktop configuration file (`~/.config/claude-desktop/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "devici": {
      "command": "uvx",
      "args": ["git+https://github.com/geoffwhittington/devici-mcp.git"],
      "env": {
        "DEVICI_API_BASE_URL": "https://api.devici.com",
        "DEVICI_CLIENT_ID": "your-client-id-here",
        "DEVICI_CLIENT_SECRET": "your-client-secret-here"
      }
    }
  }
}
```

### Cline (VS Code Extension)

Add this to your Cline MCP settings:

```json
{
  "mcpServers": {
    "devici": {
      "command": "uvx",
      "args": ["git+https://github.com/geoffwhittington/devici-mcp.git"],
      "env": {
        "DEVICI_API_BASE_URL": "https://api.devici.com",
        "DEVICI_CLIENT_ID": "your-client-id-here",
        "DEVICI_CLIENT_SECRET": "your-client-secret-here"
      }
    }
  }
}
```

### Continue (VS Code Extension)

Add this to your Continue configuration:

```json
{
  "mcpServers": {
    "devici": {
      "command": "uvx",
      "args": ["git+https://github.com/geoffwhittington/devici-mcp.git"],
      "env": {
        "DEVICI_API_BASE_URL": "https://api.devici.com",
        "DEVICI_CLIENT_ID": "your-client-id-here",
        "DEVICI_CLIENT_SECRET": "your-client-secret-here"
      }
    }
  }
}
```

## Environment Configuration

### Using .env File

Create a `.env` file in your working directory:

```
DEVICI_API_BASE_URL=https://api.devici.com
DEVICI_CLIENT_ID=your-client-id-here
DEVICI_CLIENT_SECRET=your-client-secret-here
```

The server will automatically load these variables if the file is present.

## Testing Your Installation

### Basic Connection Test

```bash
# Test that the package can be imported
python -c "import devici_mcp_server; print('✓ Package imported successfully')"
```

### Full Integration Test

```bash
# Run with test environment variables
DEVICI_API_BASE_URL=https://api.devici.com DEVICI_CLIENT_ID=test DEVICI_CLIENT_SECRET=test uvx git+https://github.com/geoffwhittington/devici-mcp.git
```

## Troubleshooting

### Common Issues

- **"Command not found: uvx"**
  - Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Or use pip: `pip install uv`

- **"Authentication failed"**
  - Verify your `DEVICI_API_BASE_URL` is correct
  - Check that your `DEVICI_CLIENT_ID` and `DEVICI_CLIENT_SECRET` are valid
  - Ensure the client credentials have the necessary permissions

- **"Connection timeout"**
  - Check network connectivity
  - Verify firewall settings
  - Ensure Devici instance is accessible

### Debug Mode

Run with debug logging:

```bash
# Enable debug logging
export DEBUG=true
uvx git+https://github.com/geoffwhittington/devici-mcp.git
```

---

For additional support, see the main [README.md](README.md) or open an issue in the repository.
