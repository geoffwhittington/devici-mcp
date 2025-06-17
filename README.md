# Devici MCP Server

A Model Context Protocol (MCP) server for interacting with the Devici API. This server provides LLM tools to manage users, collections, threat models, components, threats, mitigations, teams, and dashboard data through the Devici platform.

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

### Threats Management
- Get threats with pagination
- Get specific threat by ID
- Get threats by component

### Mitigations Management
- Get mitigations with pagination
- Get specific mitigation by ID
- Get mitigations by threat

### Teams Management
- Get teams with pagination
- Get specific team by ID

### Dashboard & Reports
- Get available dashboard chart types
- Get dashboard data with filtering
- Get threat models report data

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd devici-mcp
```

2. Install dependencies using uv (recommended) or pip:
```bash
# Using uv
uv sync

# Or using pip
pip install -e .
```

## Configuration

1. Copy the environment template:
```bash
cp env.example .env
```

2. Configure your Devici API credentials in `.env`:
```bash
DEVICI_API_BASE_URL=https://api.devici.com
DEVICI_CLIENT_ID=your_client_id
DEVICI_CLIENT_SECRET=your_client_secret
DEBUG=false
```

## Usage

### Running the Server

Start the MCP server:
```bash
python -m devici_mcp_server
```

The server will:
1. Load configuration from environment variables
2. Authenticate with the Devici API
3. Start the MCP server listening on stdin/stdout

### Using with LLM Applications

Configure your LLM application (such as Claude Desktop) to use this MCP server by adding it to your configuration:

```json
{
  "mcpServers": {
    "devici": {
      "command": "python",
      "args": ["-m", "devici_mcp_server"],
      "env": {
        "DEVICI_API_BASE_URL": "https://api.devici.com",
        "DEVICI_CLIENT_ID": "your_client_id",
        "DEVICI_CLIENT_SECRET": "your_client_secret"
      }
    }
  }
}
```

## Available Tools

Once connected, you can use natural language to interact with Devici through these tools:

- `get_users` - Retrieve users with pagination
- `get_user` - Get a specific user by ID
- `search_users` - Search users by field and text
- `invite_user` - Invite a new user
- `get_collections` - Retrieve collections with pagination
- `get_collection` - Get a specific collection by ID
- `create_collection` - Create a new collection
- `get_threat_models` - Retrieve threat models with pagination
- `get_threat_models_by_collection` - Get threat models for a collection
- `get_threat_model` - Get a specific threat model by ID
- `create_threat_model` - Create a new threat model
- `get_components` - Retrieve components with pagination
- `get_component` - Get a specific component by ID
- `get_components_by_canvas` - Get components for a canvas
- `get_threats` - Retrieve threats with pagination
- `get_threat` - Get a specific threat by ID
- `get_threats_by_component` - Get threats for a component
- `get_mitigations` - Retrieve mitigations with pagination
- `get_mitigation` - Get a specific mitigation by ID
- `get_mitigations_by_threat` - Get mitigations for a threat
- `get_teams` - Retrieve teams with pagination
- `get_team` - Get a specific team by ID
- `get_dashboard_types` - Get available dashboard chart types
- `get_dashboard_data` - Get dashboard data with filtering
- `get_threat_models_report` - Get threat models report data

## Examples

Example interactions with the LLM:

```
"Show me all users in Devici"
"Get the details for user ID abc123"
"Search for users with email containing 'john'"
"Invite a new user with email john@example.com, name John Doe, role admin"
"Create a new collection called 'Security Assessment'"
"Get all threat models for collection xyz789"
"Show me the dashboard data for threat trends"
```

## Development

### Project Structure

```
devici-mcp/
├── src/
│   └── devici_mcp_server/
│       ├── __init__.py
│       ├── __main__.py          # Entry point
│       ├── api_client.py        # Devici API client
│       └── server.py            # MCP server implementation
├── pyproject.toml               # Package configuration
├── env.example                  # Environment template
├── .gitignore
├── LICENSE
└── README.md
```

### Running Tests

```bash
# Install development dependencies
uv sync --dev

# Run tests
pytest

# Run type checking
mypy src/

# Format code
black src/
isort src/
```

### API Reference

The server is built using the Devici API documented at: https://docs.devici.com/

## Authentication

The server handles authentication automatically using client credentials flow:
1. Uses `DEVICI_CLIENT_ID` and `DEVICI_CLIENT_SECRET` to authenticate
2. Obtains an access token from `/auth` endpoint
3. Includes the token in all subsequent API requests

## Error Handling

The server includes comprehensive error handling:
- API authentication failures
- Network errors
- Invalid parameters
- Missing required fields

All errors are logged and returned as descriptive error messages to the LLM.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the development tools (tests, linting, formatting)
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For questions about the Devici API, consult the official documentation at https://docs.devici.com/

For issues with this MCP server, please open an issue in this repository. 