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
# CONVERSATIONAL ANALYSIS TOOLS
# =============================================================================

@mcp.tool()
async def analyze_my_project(project_path: str, project_name: str = None) -> str:
    """Analyze my project's code structure and security - like running a security scanner on my codebase"""
    if not os.path.exists(project_path):
        return f"❌ Could not find project at: {project_path}"
    
    # Auto-detect project name if not provided
    if not project_name:
        project_name = os.path.basename(os.path.abspath(project_path))
    
    try:
        # Use existing project analysis functionality
        result = await analyze_project_structure(project_path)
        analysis = json.loads(result)
        
        # Format results in a developer-friendly way
        summary = f"""
🔍 **Security Analysis Complete for {project_name}**

**📁 Project Overview:**
- 📄 Files analyzed: {len(analysis.get('files', []))}
- 🔧 Components found: {len(analysis.get('components', []))}
- 📦 Dependencies: {len(analysis.get('dependencies', []))}
- 💻 Languages: {', '.join(analysis.get('languages', ['Unknown']))}

**🛡️ Key Components Identified:**
"""
        
        # Show key components
        components = analysis.get('components', [])[:5]  # Top 5
        for comp in components:
            summary += f"- {comp.get('type', 'Unknown').title()}: {comp.get('name', 'Unknown')}\n"
        
        if len(analysis.get('components', [])) > 5:
            summary += f"... and {len(analysis.get('components', [])) - 5} more\n"
        
        summary += f"\n**🔗 External Dependencies:**\n"
        deps = analysis.get('dependencies', [])[:5]  # Top 5
        for dep in deps:
            summary += f"- {dep.get('name', 'Unknown')}\n"
        
        if len(analysis.get('dependencies', [])) > 5:
            summary += f"... and {len(analysis.get('dependencies', [])) - 5} more\n"
        
        summary += f"\n**Next Steps:**\n"
        summary += f"- Use 'find security risks in my project' to identify threats\n"
        summary += f"- Use 'start threat modeling' for guided security assessment\n"
        summary += f"- Use 'create threat model from analysis' to build a formal model\n"
        
        return summary
        
    except Exception as e:
        return f"❌ Error analyzing project: {str(e)}\nMake sure the path exists and you have read permissions."

@mcp.tool()
async def find_security_risks_in_my_project(project_description: str, project_type: str = "web-application") -> str:
    """Help me identify security risks and vulnerabilities in my project - like getting a security consultation"""
    
    # Use the existing guided threat assessment
    result = await guided_threat_assessment(project_description, project_type)
    assessment = json.loads(result)
    
    # Reformat in a more conversational way
    formatted = f"""
🚨 **Security Risk Assessment**

**📋 Based on your description:** "{project_description}"

**❓ Key Security Questions to Consider:**
"""
    
    for i, question in enumerate(assessment.get('guided_questions', []), 1):
        formatted += f"{i}. {question}\n"
    
    formatted += f"""
**⚠️ Common Risk Areas for {project_type.replace('-', ' ').title()}:**
"""
    
    threat_descriptions = {
        'injection': 'SQL/Code injection attacks through user input',
        'broken-authentication': 'Weak login systems and session management', 
        'sensitive-data-exposure': 'Unprotected sensitive information',
        'xxe': 'XML external entity attacks',
        'broken-access-control': 'Users accessing unauthorized resources',
        'excessive-data-exposure': 'APIs returning too much information',
        'lack-of-rate-limiting': 'No protection against abuse/DoS',
        'insecure-data-storage': 'Sensitive data stored insecurely',
        'insecure-communication': 'Unencrypted or weak communication'
    }
    
    for threat in assessment.get('suggested_threat_categories', []):
        description = threat_descriptions.get(threat, 'Security vulnerability')
        formatted += f"- **{threat.replace('-', ' ').title()}**: {description}\n"
    
    formatted += f"""
**🔧 What to do next:**
- Answer the questions above honestly
- Use 'analyze component security' for specific parts of your system  
- Use 'get security recommendations' for specific threats
- Use 'create security plan' to build a complete threat model

💡 **Pro tip**: Be specific about your tech stack for better recommendations!
"""
    
    return formatted

@mcp.tool()
async def start_threat_modeling(project_description: str = None) -> str:
    """Start a guided threat modeling session - I'll ask questions to help identify security risks"""
    
    if not project_description:
        return """
🎯 **Let's Start Threat Modeling!**

I need to know about your project first. Please tell me:

**What does your project do?** 
Example: "It's a web API that handles user payments and stores customer data in PostgreSQL"

**What type of project is it?**
- web-application (websites, web apps)
- api (REST APIs, microservices)  
- mobile-app (iOS/Android apps)
- desktop-app (standalone applications)
- iot-device (connected devices)

Once you describe your project, I'll ask targeted security questions and help identify risks!

**Example to try:**
"start threat modeling" with description "An e-commerce API that processes payments"
"""
    
    # Detect project type from description
    project_type = "web-application"  # default
    desc_lower = project_description.lower()
    
    if any(word in desc_lower for word in ['api', 'rest', 'microservice', 'endpoint']):
        project_type = "api"
    elif any(word in desc_lower for word in ['mobile', 'ios', 'android', 'app store']):
        project_type = "mobile-app"
    elif any(word in desc_lower for word in ['desktop', 'electron', 'standalone']):
        project_type = "desktop-app"
    elif any(word in desc_lower for word in ['iot', 'device', 'sensor', 'embedded']):
        project_type = "iot-device"
    
    return await find_security_risks_in_my_project(project_description, project_type)

# =============================================================================
# LEGACY TOOLS (Original Functionality) - Preserved for compatibility
# =============================================================================

# User Management Tools
@mcp.tool()
async def get_users(limit: int = 20, page: int = 0) -> str:
    """Get users from Devici with pagination"""
    async with create_client_from_env() as client:
        result = await client.get_users(limit=limit, page=page)
        return str(result)

# ... (I'll add the rest of the original tools in the next part)

def main():
    """Main entry point for the server."""
    mcp.run()

if __name__ == "__main__":
    main() 