# Devici MCP Server

A Model Context Protocol (MCP) server for interacting with the Devici API. This server provides LLM tools to manage users, collections, threat models, components, threats, mitigations, teams, and dashboard data through the Devici platform.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

## Features

The Devici MCP Server provides tools for:

### User Management
- Get users with pagination
- Get specific user by ID
- Search users by field and text
- Invite new users

### Collections Management
- Get collections with pagination
- Get specific collection by ID
- Create new collections

### Threat Models Management
- Get all threat models with pagination
- Get threat models by collection
- Get specific threat model by ID
- Create new threat models

### Components Management
- Get components with pagination
- Get specific component by ID
- Get components by canvas
- Create new components

### Threats Management
- Get threats with pagination
- Get specific threat by ID
- Get threats by component
- Create new threats

### Mitigations Management
- Get mitigations with pagination
- Get specific mitigation by ID
- Get mitigations by threat
- Create new mitigations

### Teams Management
- Get teams with pagination
- Get specific team by ID
- Get team users
- Create new teams

### Dashboard & Reports
- Get dashboard data
- Get report data
- Get threat model statistics

### Comments & Audit
- Get comments with pagination
- Get specific comment by ID
- Get audit logs

### Codex Integration
- Get codex attributes
- Get codex mitigations
- Get codex threats

## Quick Start

### Using uvx (recommended)

#### Option 1: From GitHub (Current)
```bash
uvx git+https://github.com/geoffwhittington/devici-mcp.git
```

#### Option 2: From PyPI (Future - when published)
```bash
uvx devici-mcp-server
```

### Using uv

#### Install from GitHub
```bash
uv pip install git+https://github.com/geoffwhittington/devici-mcp.git
devici-mcp-server
```

#### Install from PyPI (when available)
```bash
uv pip install devici-mcp-server
devici-mcp-server
```

### Using pip

#### Install from GitHub
```bash
pip install git+https://github.com/geoffwhittington/devici-mcp.git
devici-mcp-server
```

#### Install from PyPI (when available)
```bash
pip install devici-mcp-server
devici-mcp-server
```

## Configuration

The server requires three environment variables:
- `DEVICI_API_BASE_URL`: Your Devici instance URL (e.g., `https://api.devici.com/v1`)
- `DEVICI_CLIENT_ID`: Your Devici client ID
- `DEVICI_CLIENT_SECRET`: Your Devici client secret

### Setting Environment Variables

#### Option 1: Environment Variables
```bash
export DEVICI_API_BASE_URL="https://api.devici.com/v1"
export DEVICI_CLIENT_ID="your-client-id-here"
export DEVICI_CLIENT_SECRET="your-client-secret-here"
```

#### Option 2: .env File
Create a `.env` file in your working directory:
```
DEVICI_API_BASE_URL=https://api.devici.com/v1
DEVICI_CLIENT_ID=your-client-id-here
DEVICI_CLIENT_SECRET=your-client-secret-here
```

### Getting Your API Credentials
1. Log into your Devici instance
2. Go to **Settings** > **API Access**
3. Generate a new client ID and secret
4. Copy the values for use as `DEVICI_CLIENT_ID` and `DEVICI_CLIENT_SECRET`

## MCP Client Configuration

### Claude Desktop
Add this to your Claude Desktop configuration file:

#### Option 1: From GitHub (Current)
```json
{
  "mcpServers": {
    "devici": {
      "command": "uvx",
      "args": ["git+https://github.com/geoffwhittington/devici-mcp.git"],
      "env": {
        "DEVICI_API_BASE_URL": "https://api.devici.com/v1",
        "DEVICI_CLIENT_ID": "your-client-id-here",
        "DEVICI_CLIENT_SECRET": "your-client-secret-here"
      }
    }
  }
}
```

#### Option 2: From PyPI (Future)
```json
{
  "mcpServers": {
    "devici": {
      "command": "uvx",
      "args": ["devici-mcp-server"],
      "env": {
        "DEVICI_API_BASE_URL": "https://api.devici.com/v1",
        "DEVICI_CLIENT_ID": "your-client-id-here",
        "DEVICI_CLIENT_SECRET": "your-client-secret-here"
      }
    }
  }
}
```

### Cline
Add this to your Cline MCP settings:

#### From GitHub (Current)
```json
{
  "mcpServers": {
    "devici": {
      "command": "uvx",
      "args": ["git+https://github.com/geoffwhittington/devici-mcp.git"],
      "env": {
        "DEVICI_API_BASE_URL": "https://api.devici.com/v1",
        "DEVICI_CLIENT_ID": "your-client-id-here",
        "DEVICI_CLIENT_SECRET": "your-client-secret-here"
      }
    }
  }
}
```

### Continue
Add this to your Continue configuration:

#### From GitHub (Current)
```json
{
  "mcpServers": {
    "devici": {
      "command": "uvx",
      "args": ["git+https://github.com/geoffwhittington/devici-mcp.git"],
      "env": {
        "DEVICI_API_BASE_URL": "https://api.devici.com/api/v1",
        "DEVICI_CLIENT_ID": "your-client-id-here",
        "DEVICI_CLIENT_SECRET": "your-client-secret-here"
      }
    }
  }
}
```

### Cursor
Add this to your Cursor configuration file:

#### Option 1: From GitHub (Current)
```json
{
  "mcpServers": {
    "devici": {
      "command": "uvx",
      "args": ["git+https://github.com/geoffwhittington/devici-mcp.git"],
      "env": {
        "DEVICI_API_BASE_URL": "https://api.devici.com/api/v1",
        "DEVICI_CLIENT_ID": "your-client-id-here",
        "DEVICI_CLIENT_SECRET": "your-client-secret-here"
      }
    }
  }
}
```

#### Option 2: Using local installation
If you have the package installed locally:
```json
{
  "mcpServers": {
    "devici": {
      "command": "devici-mcp-server",
      "env": {
        "DEVICI_API_BASE_URL": "https://api.devici.com/api/v1",
        "DEVICI_CLIENT_ID": "your-client-id-here",
        "DEVICI_CLIENT_SECRET": "your-client-secret-here"
      }
    }
  }
}
```

#### Option 3: Using Python module directly
```json
{
  "mcpServers": {
    "devici": {
      "command": "python",
      "args": ["-m", "devici_mcp_server"],
      "env": {
        "DEVICI_API_BASE_URL": "https://api.devici.com/api/v1",
        "DEVICI_CLIENT_ID": "your-client-id-here",
        "DEVICI_CLIENT_SECRET": "your-client-secret-here"
      }
    }
  }
}
```

## Development

### Prerequisites
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed
- Python 3.10 or higher

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd devici-mcp

# Create virtual environment and install dependencies
uv sync

# Run in development mode
uv run python -m devici_mcp_server
```

### Testing
```bash
# Run the import test
uv run python test_basic.py

# Test with environment variables
DEVICI_API_BASE_URL=https://api.devici.com/api/v1 DEVICI_CLIENT_ID=test DEVICI_CLIENT_SECRET=test uv run python -m devici_mcp_server
```

### Building
```bash
# Build the package
uv build

# Install locally for testing
uv pip install dist/*.whl
```

## Features

- **Full API Coverage**: Supports all major Devici API endpoints
- **Authentication**: Secure client ID/secret-based authentication
- **Error Handling**: Comprehensive error handling and validation
- **Environment Configuration**: Flexible configuration via environment variables
- **Modern Python**: Built with modern Python packaging (uv, pyproject.toml)
- **MCP Compliant**: Fully compatible with the Model Context Protocol

## API Coverage

This server provides access to:
- Users and Teams
- Collections and Threat Models
- Components and Threats
- Mitigations and Comments
- Dashboard Data and Reports
- Audit Logs and Codex Integration
- Search and Bulk Operations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues and questions:
- Check the [Issues](https://github.com/geoffwhittington/devici-mcp/issues) page
- Review the Devici API documentation
- Ensure your API credentials have proper permissions

---

**Note**: This is an unofficial MCP server for Devici. For official Devici support, please contact the Devici team. 