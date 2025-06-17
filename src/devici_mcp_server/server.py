"""
Devici MCP Server

A Model Context Protocol server for interacting with the Devici API.
"""

import logging
from mcp.server.fastmcp import FastMCP
from .api_client import create_client_from_env


logger = logging.getLogger(__name__)

# Create MCP server instance
mcp = FastMCP("devici-mcp-server")


# User Management Tools
@mcp.tool()
async def get_users(limit: int = 20, page: int = 0) -> str:
    """Get users from Devici with pagination"""
    async with create_client_from_env() as client:
        result = await client.get_users(limit=limit, page=page)
        return str(result)


@mcp.tool()
async def get_user(user_id: str) -> str:
    """Get a specific user by ID"""
    async with create_client_from_env() as client:
        result = await client.get_user(user_id)
        return str(result)


@mcp.tool()
async def search_users(field: str, text: str) -> str:
    """Search users by field and text"""
    async with create_client_from_env() as client:
        result = await client.search_users(field, text)
        return str(result)


@mcp.tool()
async def invite_user(email: str, first_name: str, last_name: str, role: str) -> str:
    """Invite a new user to Devici"""
    async with create_client_from_env() as client:
        result = await client.invite_user(email, first_name, last_name, role)
        return str(result)


# Collections Management Tools
@mcp.tool()
async def get_collections(limit: int = 20, page: int = 0) -> str:
    """Get collections from Devici with pagination"""
    async with create_client_from_env() as client:
        result = await client.get_collections(limit=limit, page=page)
        return str(result)


@mcp.tool()
async def get_collection(collection_id: str) -> str:
    """Get a specific collection by ID"""
    async with create_client_from_env() as client:
        result = await client.get_collection(collection_id)
        return str(result)


@mcp.tool()
async def create_collection(name: str, description: str = None, **other_properties) -> str:
    """Create a new collection"""
    async with create_client_from_env() as client:
        collection_data = {"name": name}
        if description:
            collection_data["description"] = description
        collection_data.update(other_properties)
        result = await client.create_collection(collection_data)
        return str(result)


# Threat Models Management Tools
@mcp.tool()
async def get_threat_models(limit: int = 20, page: int = 0) -> str:
    """Get threat models from Devici with pagination"""
    async with create_client_from_env() as client:
        result = await client.get_threat_models(limit=limit, page=page)
        return str(result)


@mcp.tool()
async def get_threat_models_by_collection(collection_id: str, limit: int = 20, page: int = 0) -> str:
    """Get threat models for a specific collection"""
    async with create_client_from_env() as client:
        result = await client.get_threat_models_by_collection(collection_id, limit=limit, page=page)
        return str(result)


@mcp.tool()
async def get_threat_model(threat_model_id: str) -> str:
    """Get a specific threat model by ID"""
    async with create_client_from_env() as client:
        result = await client.get_threat_model(threat_model_id)
        return str(result)


@mcp.tool()
async def create_threat_model(name: str, collection_id: str, description: str = None, **other_properties) -> str:
    """Create a new threat model"""
    async with create_client_from_env() as client:
        threat_model_data = {
            "name": name,
            "collection_id": collection_id
        }
        if description:
            threat_model_data["description"] = description
        threat_model_data.update(other_properties)
        result = await client.create_threat_model(threat_model_data)
        return str(result)


# Components Management Tools
@mcp.tool()
async def get_components(limit: int = 20, page: int = 0) -> str:
    """Get components from Devici with pagination"""
    async with create_client_from_env() as client:
        result = await client.get_components(limit=limit, page=page)
        return str(result)


@mcp.tool()
async def get_component(component_id: str) -> str:
    """Get a specific component by ID"""
    async with create_client_from_env() as client:
        result = await client.get_component(component_id)
        return str(result)


@mcp.tool()
async def get_components_by_canvas(canvas_id: str) -> str:
    """Get components for a specific canvas"""
    async with create_client_from_env() as client:
        result = await client.get_components_by_canvas(canvas_id)
        return str(result)


# Threats Management Tools
@mcp.tool()
async def get_threats(limit: int = 20, page: int = 0) -> str:
    """Get threats from Devici with pagination"""
    async with create_client_from_env() as client:
        result = await client.get_threats(limit=limit, page=page)
        return str(result)


@mcp.tool()
async def get_threat(threat_id: str) -> str:
    """Get a specific threat by ID"""
    async with create_client_from_env() as client:
        result = await client.get_threat(threat_id)
        return str(result)


@mcp.tool()
async def get_threats_by_component(component_id: str) -> str:
    """Get threats for a specific component"""
    async with create_client_from_env() as client:
        result = await client.get_threats_by_component(component_id)
        return str(result)


# Mitigations Management Tools
@mcp.tool()
async def get_mitigations(limit: int = 20, page: int = 0) -> str:
    """Get mitigations from Devici with pagination"""
    async with create_client_from_env() as client:
        result = await client.get_mitigations(limit=limit, page=page)
        return str(result)


@mcp.tool()
async def get_mitigation(mitigation_id: str) -> str:
    """Get a specific mitigation by ID"""
    async with create_client_from_env() as client:
        result = await client.get_mitigation(mitigation_id)
        return str(result)


@mcp.tool()
async def get_mitigations_by_threat(threat_id: str) -> str:
    """Get mitigations for a specific threat"""
    async with create_client_from_env() as client:
        result = await client.get_mitigations_by_threat(threat_id)
        return str(result)


# Teams Management Tools
@mcp.tool()
async def get_teams(limit: int = 20, page: int = 0) -> str:
    """Get teams from Devici with pagination"""
    async with create_client_from_env() as client:
        result = await client.get_teams(limit=limit, page=page)
        return str(result)


@mcp.tool()
async def get_team(team_id: str) -> str:
    """Get a specific team by ID"""
    async with create_client_from_env() as client:
        result = await client.get_team(team_id)
        return str(result)


# Dashboard Tools
@mcp.tool()
async def get_dashboard_types() -> str:
    """Get available dashboard chart types"""
    async with create_client_from_env() as client:
        result = await client.get_dashboard_types()
        return str(result)


@mcp.tool()
async def get_dashboard_data(chart_type: str, limit: int = 20, page: int = 0, start: str = None, end: str = None, project_id: str = None) -> str:
    """Get dashboard data for a specific chart type"""
    async with create_client_from_env() as client:
        result = await client.get_dashboard_data(
            chart_type=chart_type,
            limit=limit,
            page=page,
            start=start,
            end=end,
            project_id=project_id
        )
        return str(result)


@mcp.tool()
async def get_threat_models_report(start: str = None, end: str = None) -> str:
    """Get threat models report data"""
    async with create_client_from_env() as client:
        result = await client.get_threat_models_report(start=start, end=end)
        return str(result)


def main():
    """Main entry point for the server."""
    mcp.run()


if __name__ == "__main__":
    main() 