"""
Devici MCP Server - Enhanced Developer Experience

A Model Context Protocol server for interacting with the Devici API.
Enhanced with developer-friendly tools and natural language interface.
"""

import logging
import json
import os
from mcp.server.fastmcp import FastMCP
from .api_client import create_client_from_env


logger = logging.getLogger(__name__)

# Create MCP server instance
mcp = FastMCP("devici-mcp-server")

# =============================================================================
# QUICK START & HELP TOOLS - Natural Language Interface
# =============================================================================

@mcp.tool()
async def help_me_get_started() -> str:
    """I'm new to Devici - show me how to get started with threat modeling"""
    help_text = """
🚀 **Welcome to Devici Threat Modeling!**

Here's how to get started:

**1. See what you have:**
   - "show my collections" - See your project collections
   - "show my threat models" - See existing threat models
   
**2. Create a new threat model:**
   - "analyze my project" - Automatically analyze a codebase
   - "start threat modeling" - Begin with guided questions
   - "create new threat model" - Manual creation
   
**3. Work with existing models:**
   - "review threat model [name]" - Examine a specific model
   - "find security issues in [project]" - Get recommendations
   - "generate security report" - Create documentation

**Popular commands to try:**
   - "analyze my project at /path/to/project"
   - "what are the security risks in my web app?"
   - "help me secure my API"
   - "show threats for component [name]"

Just ask naturally - I understand developer language! 🤖

**All original tools are still available for advanced users.**
    """
    return help_text

@mcp.tool()
async def show_my_collections(limit: int = 10) -> str:
    """Show me all my project collections in Devici"""
    async with create_client_from_env() as client:
        result = await client.get_collections(limit=limit, page=0)
        
        # Format for better readability
        if isinstance(result, dict) and 'items' in result:
            collections = result['items']
            if not collections:
                return "📁 You don't have any collections yet. Create one with 'create new collection'!"
            
            formatted = "📁 **Your Collections:**\n\n"
            for i, collection in enumerate(collections, 1):
                formatted += f"{i}. **{collection.get('title', 'Untitled')}**\n"
                if collection.get('description'):
                    formatted += f"   Description: {collection['description']}\n"
                formatted += f"   ID: {collection['id']}\n\n"
            return formatted
        
        return str(result)

@mcp.tool()
async def show_my_threat_models(collection_name: str = None, limit: int = 10) -> str:
    """Show me my threat models, optionally filtered by collection name"""
    async with create_client_from_env() as client:
        if collection_name:
            # First find the collection
            collections = await client.get_collections(limit=50, page=0)
            collection_id = None
            if isinstance(collections, dict) and 'items' in collections:
                for collection in collections['items']:
                    if collection_name.lower() in collection.get('title', '').lower():
                        collection_id = collection['id']
                        break
            
            if collection_id:
                result = await client.get_threat_models_by_collection(collection_id, limit=limit, page=0)
            else:
                return f"❌ Couldn't find a collection matching '{collection_name}'"
        else:
            result = await client.get_threat_models(limit=limit, page=0)
        
        # Format for better readability
        if isinstance(result, dict) and 'items' in result:
            models = result['items']
            if not models:
                return "🎯 No threat models found. Create one with 'analyze my project' or 'start threat modeling'!"
            
            formatted = "🎯 **Your Threat Models:**\n\n"
            for i, model in enumerate(models, 1):
                formatted += f"{i}. **{model.get('title', 'Untitled')}**\n"
                if model.get('description'):
                    formatted += f"   📝 {model['description']}\n"
                formatted += f"   📊 Status: {model.get('status', 'Unknown')}\n"
                formatted += f"   🏷️ Priority: {model.get('priority', 'Not set')}\n"
                if model.get('collection', {}).get('title'):
                    formatted += f"   📁 Collection: {model['collection']['title']}\n"
                formatted += f"   🆔 ID: {model['id']}\n\n"
            return formatted
        
        return str(result)

@mcp.tool()
async def whats_my_security_status() -> str:
    """Give me an overview of my security posture across all threat models"""
    async with create_client_from_env() as client:
        try:
            # Get overview data
            collections = await client.get_collections(limit=10, page=0)
            threat_models = await client.get_threat_models(limit=20, page=0)
            
            collections_data = collections if isinstance(collections, dict) else {"items": []}
            models_data = threat_models if isinstance(threat_models, dict) else {"items": []}
            
            collections_count = len(collections_data.get('items', []))
            models_count = len(models_data.get('items', []))
            
            # Analyze threat model statuses
            status_counts = {}
            priority_counts = {}
            
            for model in models_data.get('items', []):
                status = model.get('status', 'Unknown')
                priority = model.get('priority', 'Unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            # Format overview
            overview = f"""
📊 **Your Security Overview**

**📁 Collections:** {collections_count}
**🎯 Threat Models:** {models_count}

**📈 Model Status Distribution:**
"""
            for status, count in status_counts.items():
                overview += f"   • {status}: {count}\n"
            
            overview += f"\n**🏷️ Priority Distribution:**\n"
            for priority, count in priority_counts.items():
                overview += f"   • {priority}: {count}\n"
            
            # Add recommendations
            overview += f"""
**💡 Quick Actions:**
- Use 'analyze my project' to create new threat models
- Use 'review threat model [name]' to examine specific models
- Use 'find security risks' to assess new projects

**🎯 Focus Areas:**
"""
            
            if models_count == 0:
                overview += "- Start by creating your first threat model!\n"
            elif status_counts.get('draft', 0) > 0:
                overview += f"- Complete {status_counts['draft']} draft models\n"
            elif priority_counts.get('high', 0) > 0:
                overview += f"- Review {priority_counts['high']} high-priority models\n"
            else:
                overview += "- Consider adding more projects to your portfolio\n"
            
            return overview
            
        except Exception as e:
            return f"❌ Error getting security overview: {str(e)}"

# =============================================================================
# LEGACY TOOLS (Original Functionality) - Preserved for compatibility
# =============================================================================

# User Management Tools

def main():
    """Main entry point for the server."""
    mcp.run()

if __name__ == "__main__":
    main() 