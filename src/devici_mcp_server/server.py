"""
Devici MCP Server

A Model Context Protocol server for interacting with the Devici API.
"""

import os
import logging
from typing import Any, Sequence
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.server.stdio
import mcp.types as types
from .api_client import DeviciAPIClient, create_client_from_env


logger = logging.getLogger(__name__)


class DeviciMCPServer:
    """MCP Server for Devici API integration."""
    
    def __init__(self):
        self.server = Server("devici-mcp-server")
        self.client: DeviciAPIClient | None = None
        self.setup_handlers()
        
    def setup_handlers(self):
        """Setup MCP server handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="get_users",
                    description="Get users from Devici with pagination",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {"type": "integer", "description": "Number of users to retrieve (default: 20)", "minimum": 1, "maximum": 100},
                            "page": {"type": "integer", "description": "Page number for pagination (default: 0)", "minimum": 0}
                        }
                    }
                ),
                Tool(
                    name="get_user",
                    description="Get a specific user by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID to retrieve"}
                        },
                        "required": ["user_id"]
                    }
                ),
                Tool(
                    name="search_users",
                    description="Search users by field and text",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "field": {"type": "string", "description": "Field to search by (e.g., email, firstName, lastName)"},
                            "text": {"type": "string", "description": "Text to search for"}
                        },
                        "required": ["field", "text"]
                    }
                ),
                Tool(
                    name="invite_user",
                    description="Invite a new user to Devici",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "email": {"type": "string", "description": "User's email address"},
                            "first_name": {"type": "string", "description": "User's first name"},
                            "last_name": {"type": "string", "description": "User's last name"},
                            "role": {"type": "string", "description": "User's role"}
                        },
                        "required": ["email", "first_name", "last_name", "role"]
                    }
                ),
                Tool(
                    name="get_collections",
                    description="Get collections from Devici with pagination",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {"type": "integer", "description": "Number of collections to retrieve (default: 20)", "minimum": 1, "maximum": 100},
                            "page": {"type": "integer", "description": "Page number for pagination (default: 0)", "minimum": 0}
                        }
                    }
                ),
                Tool(
                    name="get_collection",
                    description="Get a specific collection by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "collection_id": {"type": "string", "description": "The collection ID to retrieve"}
                        },
                        "required": ["collection_id"]
                    }
                ),
                Tool(
                    name="create_collection",
                    description="Create a new collection",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Collection name"},
                            "description": {"type": "string", "description": "Collection description"},
                            "other_properties": {"type": "object", "description": "Additional collection properties"}
                        },
                        "required": ["name"]
                    }
                ),
                Tool(
                    name="get_threat_models",
                    description="Get threat models from Devici with pagination",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {"type": "integer", "description": "Number of threat models to retrieve (default: 20)", "minimum": 1, "maximum": 100},
                            "page": {"type": "integer", "description": "Page number for pagination (default: 0)", "minimum": 0}
                        }
                    }
                ),
                Tool(
                    name="get_threat_models_by_collection",
                    description="Get threat models for a specific collection",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "collection_id": {"type": "string", "description": "The collection ID"},
                            "limit": {"type": "integer", "description": "Number of threat models to retrieve (default: 20)", "minimum": 1, "maximum": 100},
                            "page": {"type": "integer", "description": "Page number for pagination (default: 0)", "minimum": 0}
                        },
                        "required": ["collection_id"]
                    }
                ),
                Tool(
                    name="get_threat_model",
                    description="Get a specific threat model by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "threat_model_id": {"type": "string", "description": "The threat model ID to retrieve"}
                        },
                        "required": ["threat_model_id"]
                    }
                ),
                Tool(
                    name="create_threat_model",
                    description="Create a new threat model",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Threat model name"},
                            "collection_id": {"type": "string", "description": "Collection ID to associate with"},
                            "description": {"type": "string", "description": "Threat model description"},
                            "other_properties": {"type": "object", "description": "Additional threat model properties"}
                        },
                        "required": ["name", "collection_id"]
                    }
                ),
                Tool(
                    name="get_components",
                    description="Get components from Devici with pagination",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {"type": "integer", "description": "Number of components to retrieve (default: 20)", "minimum": 1, "maximum": 100},
                            "page": {"type": "integer", "description": "Page number for pagination (default: 0)", "minimum": 0}
                        }
                    }
                ),
                Tool(
                    name="get_component",
                    description="Get a specific component by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "component_id": {"type": "string", "description": "The component ID to retrieve"}
                        },
                        "required": ["component_id"]
                    }
                ),
                Tool(
                    name="get_components_by_canvas",
                    description="Get components for a specific canvas",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "canvas_id": {"type": "string", "description": "The canvas ID"}
                        },
                        "required": ["canvas_id"]
                    }
                ),
                Tool(
                    name="get_threats",
                    description="Get threats from Devici with pagination",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {"type": "integer", "description": "Number of threats to retrieve (default: 20)", "minimum": 1, "maximum": 100},
                            "page": {"type": "integer", "description": "Page number for pagination (default: 0)", "minimum": 0}
                        }
                    }
                ),
                Tool(
                    name="get_threat",
                    description="Get a specific threat by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "threat_id": {"type": "string", "description": "The threat ID to retrieve"}
                        },
                        "required": ["threat_id"]
                    }
                ),
                Tool(
                    name="get_threats_by_component",
                    description="Get threats for a specific component",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "component_id": {"type": "string", "description": "The component ID"}
                        },
                        "required": ["component_id"]
                    }
                ),
                Tool(
                    name="get_mitigations",
                    description="Get mitigations from Devici with pagination",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {"type": "integer", "description": "Number of mitigations to retrieve (default: 20)", "minimum": 1, "maximum": 100},
                            "page": {"type": "integer", "description": "Page number for pagination (default: 0)", "minimum": 0}
                        }
                    }
                ),
                Tool(
                    name="get_mitigation",
                    description="Get a specific mitigation by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "mitigation_id": {"type": "string", "description": "The mitigation ID to retrieve"}
                        },
                        "required": ["mitigation_id"]
                    }
                ),
                Tool(
                    name="get_mitigations_by_threat",
                    description="Get mitigations for a specific threat",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "threat_id": {"type": "string", "description": "The threat ID"}
                        },
                        "required": ["threat_id"]
                    }
                ),
                Tool(
                    name="get_teams",
                    description="Get teams from Devici with pagination",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {"type": "integer", "description": "Number of teams to retrieve (default: 20)", "minimum": 1, "maximum": 100},
                            "page": {"type": "integer", "description": "Page number for pagination (default: 0)", "minimum": 0}
                        }
                    }
                ),
                Tool(
                    name="get_team",
                    description="Get a specific team by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "team_id": {"type": "string", "description": "The team ID to retrieve"}
                        },
                        "required": ["team_id"]
                    }
                ),
                Tool(
                    name="get_dashboard_types",
                    description="Get available dashboard chart types",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="get_dashboard_data",
                    description="Get dashboard data for a specific chart type",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "chart_type": {"type": "string", "description": "Type of chart to get data for"},
                            "limit": {"type": "integer", "description": "Number of items to retrieve (default: 20)", "minimum": 1, "maximum": 100},
                            "page": {"type": "integer", "description": "Page number for pagination (default: 0)", "minimum": 0},
                            "start": {"type": "string", "description": "Start date filter (ISO format)"},
                            "end": {"type": "string", "description": "End date filter (ISO format)"},
                            "project_id": {"type": "string", "description": "Project ID filter"}
                        },
                        "required": ["chart_type"]
                    }
                ),
                Tool(
                    name="get_threat_models_report",
                    description="Get threat models report data",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start": {"type": "string", "description": "Start date filter (ISO format)"},
                            "end": {"type": "string", "description": "End date filter (ISO format)"}
                        }
                    }
                )
            ]
            
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.TextContent]:
            """Handle tool calls."""
            if not self.client:
                self.client = create_client_from_env()
                
            try:
                async with self.client as client:
                    result = await self._execute_tool(client, name, arguments or {})
                    return [types.TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"Tool execution failed: {e}")
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]
                
    async def _execute_tool(self, client: DeviciAPIClient, name: str, arguments: dict[str, Any]) -> Any:
        """Execute a specific tool with the given arguments."""
        
        # User Management Tools
        if name == "get_users":
            limit = arguments.get("limit", 20)
            page = arguments.get("page", 0)
            return await client.get_users(limit=limit, page=page)
            
        elif name == "get_user":
            user_id = arguments["user_id"]
            return await client.get_user(user_id)
            
        elif name == "search_users":
            field = arguments["field"]
            text = arguments["text"]
            return await client.search_users(field, text)
            
        elif name == "invite_user":
            email = arguments["email"]
            first_name = arguments["first_name"]
            last_name = arguments["last_name"]
            role = arguments["role"]
            return await client.invite_user(email, first_name, last_name, role)
            
        # Collections Management Tools
        elif name == "get_collections":
            limit = arguments.get("limit", 20)
            page = arguments.get("page", 0)
            return await client.get_collections(limit=limit, page=page)
            
        elif name == "get_collection":
            collection_id = arguments["collection_id"]
            return await client.get_collection(collection_id)
            
        elif name == "create_collection":
            # Build collection data from arguments
            collection_data = {"name": arguments["name"]}
            if "description" in arguments:
                collection_data["description"] = arguments["description"]
            if "other_properties" in arguments:
                collection_data.update(arguments["other_properties"])
            return await client.create_collection(collection_data)
            
        # Threat Models Management Tools
        elif name == "get_threat_models":
            limit = arguments.get("limit", 20)
            page = arguments.get("page", 0)
            return await client.get_threat_models(limit=limit, page=page)
            
        elif name == "get_threat_models_by_collection":
            collection_id = arguments["collection_id"]
            limit = arguments.get("limit", 20)
            page = arguments.get("page", 0)
            return await client.get_threat_models_by_collection(collection_id, limit=limit, page=page)
            
        elif name == "get_threat_model":
            threat_model_id = arguments["threat_model_id"]
            return await client.get_threat_model(threat_model_id)
            
        elif name == "create_threat_model":
            # Build threat model data from arguments
            threat_model_data = {
                "name": arguments["name"],
                "collection_id": arguments["collection_id"]
            }
            if "description" in arguments:
                threat_model_data["description"] = arguments["description"]
            if "other_properties" in arguments:
                threat_model_data.update(arguments["other_properties"])
            return await client.create_threat_model(threat_model_data)
            
        # Components Management Tools
        elif name == "get_components":
            limit = arguments.get("limit", 20)
            page = arguments.get("page", 0)
            return await client.get_components(limit=limit, page=page)
            
        elif name == "get_component":
            component_id = arguments["component_id"]
            return await client.get_component(component_id)
            
        elif name == "get_components_by_canvas":
            canvas_id = arguments["canvas_id"]
            return await client.get_components_by_canvas(canvas_id)
            
        # Threats Management Tools
        elif name == "get_threats":
            limit = arguments.get("limit", 20)
            page = arguments.get("page", 0)
            return await client.get_threats(limit=limit, page=page)
            
        elif name == "get_threat":
            threat_id = arguments["threat_id"]
            return await client.get_threat(threat_id)
            
        elif name == "get_threats_by_component":
            component_id = arguments["component_id"]
            return await client.get_threats_by_component(component_id)
            
        # Mitigations Management Tools
        elif name == "get_mitigations":
            limit = arguments.get("limit", 20)
            page = arguments.get("page", 0)
            return await client.get_mitigations(limit=limit, page=page)
            
        elif name == "get_mitigation":
            mitigation_id = arguments["mitigation_id"]
            return await client.get_mitigation(mitigation_id)
            
        elif name == "get_mitigations_by_threat":
            threat_id = arguments["threat_id"]
            return await client.get_mitigations_by_threat(threat_id)
            
        # Teams Management Tools
        elif name == "get_teams":
            limit = arguments.get("limit", 20)
            page = arguments.get("page", 0)
            return await client.get_teams(limit=limit, page=page)
            
        elif name == "get_team":
            team_id = arguments["team_id"]
            return await client.get_team(team_id)
            
        # Dashboard Tools
        elif name == "get_dashboard_types":
            return await client.get_dashboard_types()
            
        elif name == "get_dashboard_data":
            chart_type = arguments["chart_type"]
            limit = arguments.get("limit", 20)
            page = arguments.get("page", 0)
            start = arguments.get("start")
            end = arguments.get("end")
            project_id = arguments.get("project_id")
            return await client.get_dashboard_data(
                chart_type=chart_type,
                limit=limit,
                page=page,
                start=start,
                end=end,
                project_id=project_id
            )
            
        elif name == "get_threat_models_report":
            start = arguments.get("start")
            end = arguments.get("end")
            return await client.get_threat_models_report(start=start, end=end)
            
        else:
            raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main entry point for the server."""
    server_instance = DeviciMCPServer()
    
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="devici-mcp-server",
                server_version="0.1.0",
                capabilities=server_instance.server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={}
                )
            )
        ) 