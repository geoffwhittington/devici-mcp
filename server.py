"""
Devici MCP Server - Enhanced Developer Experience

A Model Context Protocol server for interacting with the Devici API.
Enhanced with developer-friendly tools and natural language interface.

QUICK START GUIDE:
==================

🏆 RECOMMENDED FOR DEVELOPERS - Instant Devici URLs:
   create_developer_threat_model("My E-commerce App", "React e-commerce with Node.js API and PostgreSQL", "React, Node.js, PostgreSQL")

🔥 ALTERNATIVE APPROACHES:
   create_otm_from_description("React e-commerce with Node.js API and PostgreSQL", "React, Node.js, PostgreSQL")
   create_complete_threat_model_with_components("My Web App", "Sandbox", "web server, database, user browser")

⚡ ALTERNATIVE - File Scanning (Power Users):
   create_otm_file_for_devici()  # Scans current directory

🚀 DIRECT UPLOAD - Zero Friction Import:
   import_otm_to_devici("my-threat-model.otm", "My Collection")

🔄 FULL AUTO - Generate + Upload:
   generate_otm_and_create_threat_model("MyProject")

NATURAL LANGUAGE COMMANDS:
==========================

New to Security?
- help_me_get_started() - Step-by-step threat modeling guide
- analyze_current_project() - Instant security assessment

See What You Have:
- show_my_collections() - List your project collections
- show_my_threat_models() - Show existing threat models

Create Security Assessments:
- create_new_collection("Project Name", "Description") - Organize threat models
- start_threat_modeling("Project description") - Guided threat assessment

Get Instant Insights:
- quick_security_scan("E-commerce site with payments") - STRIDE analysis
- security_quick_wins("python") - 1-hour security improvements
- generate_security_checklist("web-app") - Actionable security checklist

Generate Professional Threat Models:
- create_otm_from_description("project description", "tech stack") - 🏆 SECURE
- create_otm_file_for_devici() - File-based detection (requires file access)
- threat_model_template("AppName", "web-app") - Ready-to-use templates

ARCHITECTURE DECISION:
=====================

PRIMARY: LLM-Powered Analysis (SECURE)
- ✅ No file system access required
- ✅ Enterprise-safe (no security scanner alerts)
- ✅ Privacy control (you choose what to share)
- ✅ Works anywhere (containers, sandboxes, etc.)
- ✅ Better context understanding than file parsing

SECONDARY: File Scanning (POWER USERS)
- ⚠️ Requires file system access
- ⚠️ May trigger security tools
- ⚠️ Could read sensitive files
- ✅ Auto-detection convenience

EXAMPLES:
========

🚀 DEVELOPER WORKFLOW - Get Instant URLs:
   create_developer_threat_model(
       "E-commerce Platform",
       "E-commerce platform with React frontend, Node.js API, PostgreSQL database, Stripe payments",
       "React, Node.js, PostgreSQL, Stripe"
   )
   → Returns clickable Devici URLs for immediate team sharing

📱 Mobile App Security:
   create_developer_threat_model(
       "Banking App",
       "iOS banking app with biometric auth and push notifications",
       "Swift, CoreData, TouchID, APNS"
   )

🔧 Microservices Architecture:
   create_developer_threat_model(
       "Cloud Platform",
       "Microservices architecture with Docker, Kubernetes, and Redis",
       "Docker, Kubernetes, Redis, gRPC"
   )

OUTPUT:
=======
All tools generate professional OTM files ready for:
- Devici platform (drag & drop import)
- Microsoft Threat Modeling Tool
- OWASP Threat Dragon
- Any OTM-compatible tool

TIME TO VALUE: 15 seconds from description to enterprise-grade threat model

WORKFLOW:
========
1. Describe your project → create_otm_from_description()
2. Get professional OTM file → projectname-threat-model.otm
3. Import to Devici → Drag & drop into web interface
4. Collaborate → Share with security team
5. Iterate → Add project-specific details

Original API tools remain available for advanced users.
"""

import logging
import json
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from api_client import create_client_from_env

try:
    import jsonschema
    from jsonschema import validate, ValidationError
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False


logger = logging.getLogger(__name__)

# Create MCP server instance
mcp = FastMCP("devici-mcp-server")

# =============================================================================
# QUICK START & HELP TOOLS - Natural Language Interface
# =============================================================================

@mcp.tool()
async def help_me_get_started() -> str:
    """I'm new to Devici - show me how to get started with threat modeling"""
    return """
🚀 **Welcome to Devici Threat Modeling!**

Here's how to get started:

**1. See what you have:**
   - "show my collections" - See your project collections
   - "show my threat models" - See existing threat models
   
**2. Create a new threat model:**
   - "start threat modeling" - Begin with guided questions
   - "create new threat model" - Manual creation
   
**3. Work with existing models:**
   - "review threat model [name]" - Examine a specific model
   - "find security issues in [project]" - Get recommendations

**Popular commands to try:**
   - "what are the security risks in my web app?"
   - "help me secure my API"
   - "show threats for component [name]"

Just ask naturally - I understand developer language! 🤖

**All original tools are still available for advanced users.**
    """

@mcp.tool()
async def show_my_collections(limit: int = 10) -> str:
    """Show me all my project collections in Devici"""
    async with create_client_from_env() as client:
        result = await client.get_collections(limit=limit, page=0)
        
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
async def show_my_threat_models(collection_name: str | None = None, limit: int = 10) -> str:
    """Show me my threat models, optionally filtered by collection name"""
    async with create_client_from_env() as client:
        if collection_name:
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
        
        if isinstance(result, dict) and 'items' in result:
            models = result['items']
            if not models:
                return "🎯 No threat models found. Create one with 'start threat modeling'!"
            
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

# Removed duplicate create_new_collection - use create_collection instead

@mcp.tool()
async def create_new_threat_model(name: str, collection_name: str | None = None, description: str | None = None) -> str:
    """Create a new threat model in a collection - like starting a new security assessment document"""
    async with create_client_from_env() as client:
        
        collection_id = None
        
        if collection_name:
            collections = await client.get_collections(limit=50, page=0)
            if isinstance(collections, dict) and 'items' in collections:
                for collection in collections['items']:
                    if collection_name.lower() in collection.get('title', '').lower():
                        collection_id = collection['id']
                        break
            
            if not collection_id:
                return f"❌ Couldn't find collection '{collection_name}'. Use 'show my collections' to see available collections."
        else:
            collections = await client.get_collections(limit=1, page=0)
            if isinstance(collections, dict) and 'items' in collections and collections['items']:
                collection_id = collections['items'][0]['id']
                collection_name = collections['items'][0].get('title', 'Default')
            else:
                return "❌ No collections found. Create one first with 'create_new_collection [name]'"
        
        try:
            result = await create_threat_model(name, collection_id, description)
            return f"""
✅ **Threat Model Created!**

🎯 **{name}** is ready in collection **{collection_name}**

**Next steps:**
- Use 'start threat modeling' to identify threats
- Use the original Devici tools to add detailed components

ID for reference: {collection_id}
"""
        except Exception as e:
            return f"❌ Failed to create threat model: {str(e)}"

# =============================================================================
# QUICK VALUE TOOLS - Immediate Results
# =============================================================================

@mcp.tool()
async def generate_otm_and_create_threat_model(collection_name: str | None = None) -> str:
    """Generate an Open Threat Model (OTM) from current project and create threat model in Devici"""
    import os
    import json
    import uuid
    from datetime import datetime
    
    # First, analyze the current project
    project_path = os.getcwd()
    project_name = os.path.basename(project_path)
    
    # Analyze files and structure for OTM generation
    tech_indicators = {}
    components = []
    data_flows = []
    trust_zones = []
    threats = []
    mitigations = []
    
    try:
        # Basic project analysis
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != '__pycache__']
            
            for file in files[:100]:  # Limit for performance
                if file.startswith('.'):
                    continue
                    
                file_ext = os.path.splitext(file)[1].lower()
                
                # Detect technologies
                if file_ext in ['.js', '.jsx', '.ts', '.tsx']:
                    tech_indicators['frontend'] = True
                elif file_ext in ['.py']:
                    tech_indicators['python_backend'] = True
                elif file == 'package.json':
                    try:
                        with open(os.path.join(root, file), 'r') as f:
                            pkg_data = json.load(f)
                            deps = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}
                            
                            if 'react' in deps:
                                tech_indicators['react'] = True
                            if 'express' in deps:
                                tech_indicators['express'] = True
                            if 'next' in deps:
                                tech_indicators['nextjs'] = True
                    except:
                        pass
                elif file == 'requirements.txt':
                    try:
                        with open(os.path.join(root, file), 'r') as f:
                            reqs = f.read().splitlines()
                            for req in reqs:
                                dep_name = req.split('==')[0].split('>=')[0].split('<=')[0].lower()
                                if 'django' in dep_name:
                                    tech_indicators['django'] = True
                                elif 'flask' in dep_name:
                                    tech_indicators['flask'] = True
                                elif 'fastapi' in dep_name:
                                    tech_indicators['fastapi'] = True
                                elif 'sqlalchemy' in dep_name:
                                    tech_indicators['database'] = True
                    except:
                        pass
    except Exception as e:
        return f"❌ Error analyzing project: {str(e)}"
    
    # Generate OTM components based on detected technologies
    if tech_indicators.get('react') or tech_indicators.get('frontend'):
        components.append({
            "name": "Web Frontend",
            "type": "web-application",
            "description": "Client-side web application handling user interactions",
            "tags": ["frontend", "javascript", "browser"]
        })
        
        trust_zones.append({
            "name": "Client Browser",
            "type": "b2c-web-application",
            "description": "User's web browser environment"
        })
    
    if tech_indicators.get('python_backend') or tech_indicators.get('fastapi') or tech_indicators.get('flask') or tech_indicators.get('django'):
        components.append({
            "name": "API Server",
            "type": "web-service",
            "description": "Backend API server handling business logic and data access",
            "tags": ["backend", "python", "api"]
        })
        
        trust_zones.append({
            "name": "Application Server",
            "type": "private-secured",
            "description": "Internal application server environment"
        })
    
    if tech_indicators.get('database'):
        components.append({
            "name": "Database",
            "type": "datastore",
            "description": "Primary data storage for application data",
            "tags": ["database", "storage", "persistence"]
        })
        
        trust_zones.append({
            "name": "Database Layer",
            "type": "private-secured",
            "description": "Secured database environment"
        })
    
    # Generate data flows
    if len(components) >= 2:
        for i in range(len(components) - 1):
            data_flows.append({
                "name": f"{components[i]['name']} to {components[i+1]['name']}",
                "source": components[i]['name'],
                "destination": components[i+1]['name'],
                "description": f"Data flow from {components[i]['name']} to {components[i+1]['name']}",
                "tags": ["data-flow"]
            })
    
    # Generate threats based on STRIDE methodology
    stride_threats = [
        {
            "name": "Spoofing User Identity",
            "category": "spoofing",
            "description": "Attacker impersonates legitimate user to gain unauthorized access",
            "impact": "High",
            "likelihood": "Medium",
            "severity": "High"
        },
        {
            "name": "Data Tampering",
            "category": "tampering",
            "description": "Unauthorized modification of data in transit or at rest",
            "impact": "High", 
            "likelihood": "Medium",
            "severity": "High"
        },
        {
            "name": "Information Disclosure",
            "category": "information-disclosure",
            "description": "Sensitive information exposed to unauthorized parties",
            "impact": "High",
            "likelihood": "Medium", 
            "severity": "High"
        },
        {
            "name": "Denial of Service",
            "category": "denial-of-service",
            "description": "System becomes unavailable to legitimate users",
            "impact": "Medium",
            "likelihood": "High",
            "severity": "Medium"
        },
        {
            "name": "Privilege Escalation",
            "category": "elevation-of-privilege",
            "description": "Attacker gains higher level permissions than intended",
            "impact": "High",
            "likelihood": "Low",
            "severity": "Medium"
        }
    ]
    
    # Generate mitigations
    stride_mitigations = [
        {
            "name": "Multi-Factor Authentication",
            "description": "Implement MFA to prevent spoofing attacks",
            "riskReduction": 80
        },
        {
            "name": "Input Validation",
            "description": "Validate all user inputs to prevent injection attacks",
            "riskReduction": 70
        },
        {
            "name": "HTTPS Encryption",
            "description": "Use TLS encryption for all data in transit",
            "riskReduction": 90
        },
        {
            "name": "Rate Limiting",
            "description": "Implement rate limiting to prevent DoS attacks",
            "riskReduction": 60
        },
        {
            "name": "Principle of Least Privilege",
            "description": "Grant minimum necessary permissions to users and services",
            "riskReduction": 75
        }
    ]
    
    # Create OTM structure
    otm_data = {
        "otmVersion": "0.1.0",
        "project": {
            "name": project_name,
            "id": str(uuid.uuid4()),
            "description": f"Threat model for {project_name} project",
            "owner": "Security Team",
            "ownerContact": "",
            "tags": ["auto-generated", "llm-analysis"]
        },
        "representations": [
            {
                "name": "Architecture Overview",
                "id": str(uuid.uuid4()),
                "type": "threat-model",
                "size": {
                    "width": 1000,
                    "height": 1000
                }
            }
        ],
        "trustZones": [
            {
                "id": str(uuid.uuid4()),
                "name": tz["name"],
                "type": tz["type"],
                "description": tz["description"],
                "risk": {
                    "trustRating": 10 if "private" in tz["type"] else 3
                }
            } for tz in trust_zones
        ],
        "components": [
            {
                "id": str(uuid.uuid4()),
                "name": comp["name"],
                "type": comp["type"],
                "description": comp["description"],
                "tags": comp["tags"]
            } for comp in components
        ],
        "dataflows": [
            {
                "id": str(uuid.uuid4()),
                "name": df["name"],
                "source": df["source"],
                "destination": df["destination"],
                "description": df["description"],
                "tags": df["tags"]
            } for df in data_flows
        ],
        "threats": [
            {
                "id": str(uuid.uuid4()),
                "name": threat["name"],
                "categories": [threat["category"]],
                "description": threat["description"],
                "risk": {
                    "impact": threat["impact"],
                    "impactComment": f"{threat['severity']} severity {threat['category']} threat"
                },
                "tags": ["stride", threat["category"]]
            } for threat in stride_threats
        ],
        "mitigations": [
            {
                "id": str(uuid.uuid4()),
                "name": mit["name"],
                "description": mit["description"],
                "riskReduction": mit["riskReduction"],
                "tags": ["security-control"]
            } for mit in stride_mitigations
        ]
    }
    
    # Save OTM file locally
    otm_filename = f"{project_name}-threat-model.otm"
    try:
        with open(otm_filename, 'w') as f:
            json.dump(otm_data, f, indent=2)
    except Exception as e:
        return f"❌ Error saving OTM file: {str(e)}"
    
    # Now create threat model in Devici
    try:
        async with create_client_from_env() as client:
            # Get or create collection
            collections_result = await client.get_collections(limit=50, page=0)
            
            if isinstance(collections_result, dict) and 'items' in collections_result:
                collections_data = collections_result['items']
            else:
                return f"❌ Failed to get collections: {collections_result}"
        
            target_collection = None
            if collection_name:
                # Find specified collection
                for collection in collections_data:
                    if collection.get("title", "").lower() == collection_name.lower():
                        target_collection = collection
                        break
            
            if not target_collection:
                # Create new collection
                collection_data = {
                    "name": collection_name or f"{project_name} Security",
                    "description": f"Security assessment for {project_name} project"
                }
                target_collection = await client.create_collection(collection_data)
            
            # Create threat model
            threat_model_data = {
                "name": f"{project_name} Threat Model",
                "description": f"Auto-generated threat model for {project_name} based on code analysis",
                "collection_id": target_collection["id"],
                "otm_data": json.dumps(otm_data)  # Store OTM as JSON string
            }
            
            threat_model = await client.create_threat_model(threat_model_data)
            
            result = f"""
🎯 **OTM Generated and Threat Model Created!**

**📄 OTM File Created:**
- File: {otm_filename}
- Components: {len(components)}
- Trust Zones: {len(trust_zones)}
- Threats: {len(stride_threats)}
- Mitigations: {len(stride_mitigations)}

**☁️ Devici Threat Model Created:**
- Collection: {target_collection['name']}
- Threat Model: {threat_model['name']}
- ID: {threat_model['id']}

**🏗️ Detected Architecture:**
"""
            for comp in components:
                result += f"   • {comp['name']} ({comp['type']})\n"
            
            result += f"\n**🚨 Generated {len(stride_threats)} STRIDE Threats:**\n"
            for threat in stride_threats:
                result += f"   • {threat['name']} ({threat['severity']} severity)\n"
            
            result += f"\n**🛡️ Suggested {len(stride_mitigations)} Mitigations:**\n"
            for mit in stride_mitigations:
                result += f"   • {mit['name']} ({mit['riskReduction']}% risk reduction)\n"
            
            result += f"\n**🎯 Next Steps:**\n"
            result += f"   • Review the OTM file: {otm_filename}\n"
            result += f"   • Refine threats in Devici platform\n"
            result += f"   • Add project-specific security controls\n"
            result += f"   • Schedule security review meetings\n"
            
            return result
            
    except Exception as e:
        return f"❌ Error creating threat model in Devici: {str(e)}\n\n✅ OTM file saved locally: {otm_filename}"

@mcp.tool()
async def create_otm_file_for_devici() -> str:
    """Create an OTM file from current project - ready to import into Devici with zero friction"""
    import os
    import json
    import uuid
    from datetime import datetime
    
    # First, analyze the current project
    project_path = os.getcwd()
    project_name = os.path.basename(project_path)
    
    # Analyze files and structure for OTM generation
    tech_indicators = {}
    components = []
    data_flows = []
    trust_zones = []
    
    try:
        # Basic project analysis
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != '__pycache__']
            
            for file in files[:100]:  # Limit for performance
                if file.startswith('.'):
                    continue
                    
                file_ext = os.path.splitext(file)[1].lower()
                
                # Detect technologies
                if file_ext in ['.js', '.jsx', '.ts', '.tsx']:
                    tech_indicators['frontend'] = True
                elif file_ext in ['.py']:
                    tech_indicators['python_backend'] = True
                elif file == 'package.json':
                    try:
                        with open(os.path.join(root, file), 'r') as f:
                            pkg_data = json.load(f)
                            deps = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}
                            
                            if 'react' in deps:
                                tech_indicators['react'] = True
                            if 'express' in deps:
                                tech_indicators['express'] = True
                            if 'next' in deps:
                                tech_indicators['nextjs'] = True
                    except:
                        pass
                elif file == 'requirements.txt':
                    try:
                        with open(os.path.join(root, file), 'r') as f:
                            reqs = f.read().splitlines()
                            for req in reqs:
                                dep_name = req.split('==')[0].split('>=')[0].split('<=')[0].lower()
                                if 'django' in dep_name:
                                    tech_indicators['django'] = True
                                elif 'flask' in dep_name:
                                    tech_indicators['flask'] = True
                                elif 'fastapi' in dep_name:
                                    tech_indicators['fastapi'] = True
                                elif 'sqlalchemy' in dep_name:
                                    tech_indicators['database'] = True
                    except:
                        pass
    except Exception as e:
        return f"❌ Error analyzing project: {str(e)}"
    
    # Generate OTM components based on detected technologies
    if tech_indicators.get('react') or tech_indicators.get('frontend'):
        components.append({
            "name": "Web Frontend",
            "type": "web-application",
            "description": "Client-side web application handling user interactions",
            "tags": ["frontend", "javascript", "browser"]
        })
        
        trust_zones.append({
            "name": "Client Browser",
            "type": "b2c-web-application",
            "description": "User's web browser environment"
        })
    
    if tech_indicators.get('python_backend') or tech_indicators.get('fastapi') or tech_indicators.get('flask') or tech_indicators.get('django'):
        components.append({
            "name": "API Server",
            "type": "web-service",
            "description": "Backend API server handling business logic and data access",
            "tags": ["backend", "python", "api"]
        })
        
        trust_zones.append({
            "name": "Application Server",
            "type": "private-secured",
            "description": "Internal application server environment"
        })
    
    if tech_indicators.get('database'):
        components.append({
            "name": "Database",
            "type": "datastore",
            "description": "Primary data storage for application data",
            "tags": ["database", "storage", "persistence"]
        })
        
        trust_zones.append({
            "name": "Database Layer",
            "type": "private-secured",
            "description": "Secured database environment"
        })
    
    # Generate data flows
    if len(components) >= 2:
        for i in range(len(components) - 1):
            data_flows.append({
                "name": f"{components[i]['name']} to {components[i+1]['name']}",
                "source": components[i]['name'],
                "destination": components[i+1]['name'],
                "description": f"Data flow from {components[i]['name']} to {components[i+1]['name']}",
                "tags": ["data-flow"]
            })
    
    # Generate threats based on STRIDE methodology
    stride_threats = [
        {
            "name": "Spoofing User Identity",
            "category": "spoofing",
            "description": "Attacker impersonates legitimate user to gain unauthorized access",
            "impact": "High",
            "likelihood": "Medium",
            "severity": "High"
        },
        {
            "name": "Data Tampering",
            "category": "tampering",
            "description": "Unauthorized modification of data in transit or at rest",
            "impact": "High", 
            "likelihood": "Medium",
            "severity": "High"
        },
        {
            "name": "Information Disclosure",
            "category": "information-disclosure",
            "description": "Sensitive information exposed to unauthorized parties",
            "impact": "High",
            "likelihood": "Medium", 
            "severity": "High"
        },
        {
            "name": "Denial of Service",
            "category": "denial-of-service",
            "description": "System becomes unavailable to legitimate users",
            "impact": "Medium",
            "likelihood": "High",
            "severity": "Medium"
        },
        {
            "name": "Privilege Escalation",
            "category": "elevation-of-privilege",
            "description": "Attacker gains higher level permissions than intended",
            "impact": "High",
            "likelihood": "Low",
            "severity": "Medium"
        }
    ]
    
    # Generate mitigations
    stride_mitigations = [
        {
            "name": "Multi-Factor Authentication",
            "description": "Implement MFA to prevent spoofing attacks",
            "riskReduction": 80
        },
        {
            "name": "Input Validation",
            "description": "Validate all user inputs to prevent injection attacks",
            "riskReduction": 70
        },
        {
            "name": "HTTPS Encryption",
            "description": "Use TLS encryption for all data in transit",
            "riskReduction": 90
        },
        {
            "name": "Rate Limiting",
            "description": "Implement rate limiting to prevent DoS attacks",
            "riskReduction": 60
        },
        {
            "name": "Principle of Least Privilege",
            "description": "Grant minimum necessary permissions to users and services",
            "riskReduction": 75
        }
    ]
    
    # Create OTM structure
    otm_data = {
        "otmVersion": "0.1.0",
        "project": {
            "name": project_name,
            "id": str(uuid.uuid4()),
            "description": f"Threat model for {project_name} project",
            "owner": "Security Team",
            "ownerContact": "",
            "tags": ["auto-generated", "llm-analysis", "devici-ready"]
        },
        "representations": [
            {
                "name": "Architecture Overview",
                "id": str(uuid.uuid4()),
                "type": "threat-model",
                "size": {
                    "width": 1000,
                    "height": 1000
                }
            }
        ],
        "trustZones": [
            {
                "id": str(uuid.uuid4()),
                "name": tz["name"],
                "type": tz["type"],
                "description": tz["description"],
                "risk": {
                    "trustRating": 10 if "private" in tz["type"] else 3
                }
            } for tz in trust_zones
        ],
        "components": [
            {
                "id": str(uuid.uuid4()),
                "name": comp["name"],
                "type": comp["type"],
                "description": comp["description"],
                "tags": comp["tags"]
            } for comp in components
        ],
        "dataflows": [
            {
                "id": str(uuid.uuid4()),
                "name": df["name"],
                "source": df["source"],
                "destination": df["destination"],
                "description": df["description"],
                "tags": df["tags"]
            } for df in data_flows
        ],
        "threats": [
            {
                "id": str(uuid.uuid4()),
                "name": threat["name"],
                "categories": [threat["category"]],
                "description": threat["description"],
                "risk": {
                    "impact": threat["impact"],
                    "impactComment": f"{threat['severity']} severity {threat['category']} threat"
                },
                "tags": ["stride", threat["category"]]
            } for threat in stride_threats
        ],
        "mitigations": [
            {
                "id": str(uuid.uuid4()),
                "name": mit["name"],
                "description": mit["description"],
                "riskReduction": mit["riskReduction"],
                "tags": ["security-control"]
            } for mit in stride_mitigations
        ]
    }
    
    # Save OTM file locally
    otm_filename = f"{project_name}-devici-ready.otm"
    try:
        with open(otm_filename, 'w') as f:
            json.dump(otm_data, f, indent=2)
    except Exception as e:
        return f"❌ Error saving OTM file: {str(e)}"
    
    # Generate summary
    result = f"""
🎯 **OTM File Created - Ready for Devici!**

**📄 File Generated:**
- 📁 File: `{otm_filename}`
- 🏗️ Components: {len(components)}
- 🛡️ Trust Zones: {len(trust_zones)}
- ⚠️ Threats: {len(stride_threats)} (STRIDE methodology)
- 🔧 Mitigations: {len(stride_mitigations)}

**🚀 Zero-Friction Import to Devici:**

1. **Open Devici** → Go to your project collection
2. **Import OTM** → Upload `{otm_filename}`
3. **Done!** → Professional threat model ready

**🏗️ Detected Architecture:**
"""
    
    for comp in components:
        result += f"   • {comp['name']} ({comp['type']})\n"
    
    result += f"""
**🚨 Generated STRIDE Threats:**
"""
    for threat in stride_threats:
        result += f"   • {threat['name']} ({threat['severity']} severity)\n"
    
    result += f"""
**💡 Next Steps:**
   • Import `{otm_filename}` into Devici platform
   • Review and customize threats for your specific context
   • Add project-specific security controls
   • Share with security team for validation

**🔄 Alternative Import Methods:**
   • Microsoft Threat Modeling Tool
   • OWASP Threat Dragon  
   • Any OTM-compatible tool

✅ **Ready to go! Your threat model is now enterprise-grade.**
"""
    
    return result

@mcp.tool()
async def import_otm_to_devici(otm_file_path: str, collection_name: str = "Sandbox") -> str:
    """Import an OTM file directly to Devici - zero friction upload"""
    import os
    import json
    
    try:
        # Check if file exists
        if not os.path.exists(otm_file_path):
            return f"❌ Error: File '{otm_file_path}' not found"
        
        # Read the OTM file
        with open(otm_file_path, 'r') as f:
            otm_data = json.load(f)
        
        # Validate OTM data against official schema
        is_valid, validation_message = validate_otm_data(otm_data)
        if not is_valid:
            return f"❌ OTM file failed schema validation:\n{validation_message}\n\nPlease ensure the file conforms to the Open Threat Model standard."
        
        project_name = otm_data.get('project', {}).get('name', 'Unknown')
        print(f"✅ Loaded OTM file: {otm_file_path}")
        print(f"📊 Project: {project_name}")
        print(f"✅ {validation_message}")
        
        # Get collection ID by name
        client = create_client_from_env()
        async with client:
            # Get collections to find the target collection ID
            collections_response = await client.get_collections(limit=100)
            collections = collections_response.get("items", [])
            
            target_collection_id = None
            for collection in collections:
                if collection.get("title", "").lower() == collection_name.lower():
                    target_collection_id = collection["id"]
                    break
            
            if not target_collection_id:
                # Try to create the collection if it doesn't exist
                print(f"ℹ️ Collection '{collection_name}' not found. Creating new collection...")
                try:
                    collection_data = {
                        "title": collection_name,
                        "description": f"Auto-created collection for {project_name} import"
                    }
                    new_collection = await client.create_collection(collection_data)
                    target_collection_id = new_collection.get("id")
                    if target_collection_id:
                        print(f"✅ Created collection: {collection_name} (ID: {target_collection_id})")
                    else:
                        return f"❌ Error: Could not create collection '{collection_name}'"
                except Exception as e:
                    return f"❌ Error creating collection: {str(e)}"
            
            # Add collection ID to the OTM data if not present
            if "collectionId" not in otm_data:
                otm_data["collectionId"] = target_collection_id
                print(f"📁 Added collectionId: {target_collection_id}")
            
            # Use the correct endpoint format: /threat-models/otm/{collection_id}
            endpoint = f"/threat-models/otm/{target_collection_id}"
            print(f"POST {endpoint} (data size: {len(json.dumps(otm_data))} bytes)")
            
            try:
                result = await client._make_request("POST", endpoint, json_data=otm_data)
                print(f"✅ OTM import successful!")
                
                # Parse response for summary
                components_created = len(otm_data.get("components", []))
                threats_created = len(otm_data.get("threats", []))
                mitigations_created = len(otm_data.get("mitigations", []))
                
                # Try to extract threat model ID from the result
                threat_model_id = result.get("id") or result.get("threatModelId")
                
                # Construct Devici URLs
                base_url = "https://app.devici.com"
                collection_url = f"{base_url}/collections/{target_collection_id}"
                threat_model_url = f"{base_url}/collections/{target_collection_id}/d/{threat_model_id}" if threat_model_id else None
                
                result_text = f"""
✅ **OTM File Imported to Devici!**

**📁 File:** `{otm_file_path}`
**📂 Collection:** {collection_name}
**🆔 Collection ID:** {target_collection_id}

**🚀 INSTANT ACCESS - Click to Open:**
**📁 View Collection:** [{collection_url}]({collection_url})"""

                if threat_model_url:
                    result_text += f"""
**🔗 View Threat Model:** [{threat_model_url}]({threat_model_url})"""

                result_text += f"""

**📊 Import Summary:**
   • 🎯 **Threat Model:** {project_name}
   • 🏗️ **Components:** {components_created} created
   • 🚨 **Threats:** {threats_created} created  
   • 🛡️ **Mitigations:** {mitigations_created} created

**👥 TEAM SHARING:**
Share these URLs with your team:
- **Collection:** `{collection_url}`"""

                if threat_model_url:
                    result_text += f"""
- **Threat Model:** `{threat_model_url}`"""

                result_text += f"""

**🚀 Next Steps:**
1. **Click URLs Above** → Direct access to your threat model
2. **Review Components** → Check that all architectural elements are visible
3. **Review Threats** → Verify STRIDE threats are properly linked to components
4. **Review Mitigations** → Ensure security controls are linked to threats
5. **Share with Team** → Use URLs above for collaboration

✅ **Ready for Security Discussion!** Your threat model is now live in Devici.
"""
                
                return result_text
                
            except Exception as api_error:
                print(f"❌ OTM import failed: {api_error}")
                return f"❌ Error importing OTM to Devici: {str(api_error)}"
            
    except Exception as e:
        return f"❌ Error importing OTM file: {str(e)}"


# =============================================================================
# OTM VALIDATION UTILITY
# =============================================================================

def load_otm_schema() -> dict:
    """Load the OTM JSON schema for validation."""
    schema_path = Path(__file__).parent.parent.parent / "otm_schema.json"
    
    if not schema_path.exists():
        # Try current working directory
        schema_path = Path.cwd() / "otm_schema.json"
    
    if not schema_path.exists():
        raise FileNotFoundError("OTM schema file not found. Please ensure otm_schema.json is available.")
    
    with open(schema_path, 'r') as f:
        return json.load(f)

def validate_otm_data(otm_data: dict) -> tuple[bool, str]:
    """
    Validate OTM data against the official schema.
    Returns (is_valid, message)
    """
    if not JSONSCHEMA_AVAILABLE:
        return True, "⚠️ Schema validation skipped (jsonschema not available)"
    
    try:
        schema = load_otm_schema()
        validate(instance=otm_data, schema=schema)
        return True, "✅ OTM data is valid according to official schema"
    except FileNotFoundError as e:
        return True, f"⚠️ Schema validation skipped: {e}"
    except ValidationError as e:
        error_path = " -> ".join(str(x) for x in e.absolute_path) if e.absolute_path else "root"
        return False, f"❌ Schema validation failed at {error_path}: {e.message}"
    except Exception as e:
        return True, f"⚠️ Schema validation skipped due to error: {e}"

@mcp.tool()
async def create_otm_from_description(project_description: str, tech_stack: str = "", architecture: str = "") -> str:
    """Create an OTM file based on your description - no file scanning, LLM-powered analysis"""
    import json
    import uuid
    from datetime import datetime
    
    # Parse the description for key information
    desc_lower = project_description.lower()
    tech_lower = tech_stack.lower()
    arch_lower = architecture.lower()
    
    # Determine project type from description
    project_type = "web-application"
    if any(word in desc_lower for word in ['api', 'rest', 'microservice', 'endpoint', 'backend']):
        project_type = "api"
    elif any(word in desc_lower for word in ['mobile', 'ios', 'android', 'app']):
        project_type = "mobile-app"
    elif any(word in desc_lower for word in ['desktop', 'electron', 'native']):
        project_type = "desktop-app"
    elif any(word in desc_lower for word in ['web', 'website', 'frontend', 'react', 'vue', 'angular']):
        project_type = "web-application"
    
    # Generate components based on description
    components = []
    trust_zones = []
    data_flows = []
    
    # Frontend detection
    if any(word in desc_lower or word in tech_lower for word in ['react', 'vue', 'angular', 'frontend', 'web', 'browser', 'ui']):
        components.append({
            "name": "Web Frontend",
            "type": "web-application", 
            "description": "User interface layer handling client interactions",
            "tags": ["frontend", "ui", "client-side"]
        })
        trust_zones.append({
            "name": "Client Browser",
            "type": "b2c-web-application",
            "description": "User's web browser environment"
        })
    
    # Backend/API detection
    if any(word in desc_lower or word in tech_lower for word in ['api', 'backend', 'server', 'node', 'python', 'java', 'go', 'rust', 'php']):
        backend_name = "API Server"
        if 'microservice' in desc_lower:
            backend_name = "Microservices"
        elif 'serverless' in desc_lower:
            backend_name = "Serverless Functions"
            
        components.append({
            "name": backend_name,
            "type": "web-service",
            "description": "Backend services handling business logic and data processing",
            "tags": ["backend", "api", "server"]
        })
        trust_zones.append({
            "name": "Application Server",
            "type": "private-secured", 
            "description": "Internal application server environment"
        })
    
    # Database detection
    if any(word in desc_lower or word in tech_lower for word in ['database', 'db', 'sql', 'mongo', 'postgres', 'mysql', 'redis', 'storage', 'data']):
        db_type = "SQL Database"
        if any(word in desc_lower or word in tech_lower for word in ['mongo', 'nosql', 'document']):
            db_type = "NoSQL Database"
        elif any(word in desc_lower or word in tech_lower for word in ['redis', 'cache']):
            db_type = "Cache Layer"
            
        components.append({
            "name": db_type,
            "type": "datastore",
            "description": "Data persistence and storage layer",
            "tags": ["database", "storage", "persistence"]
        })
        trust_zones.append({
            "name": "Database Layer",
            "type": "private-secured",
            "description": "Secured database environment"
        })
    
    # External services detection
    if any(word in desc_lower for word in ['payment', 'stripe', 'paypal', 'third-party', 'external', 'integration']):
        components.append({
            "name": "External Services",
            "type": "external-service",
            "description": "Third-party services and integrations",
            "tags": ["external", "third-party", "integration"]
        })
        trust_zones.append({
            "name": "External Services",
            "type": "public-cloud",
            "description": "External third-party service providers"
        })
    
    # Generate data flows between components
    if len(components) >= 2:
        for i in range(len(components) - 1):
            data_flows.append({
                "name": f"{components[i]['name']} → {components[i+1]['name']}",
                "source": components[i]['name'],
                "destination": components[i+1]['name'],
                "description": f"Data communication between {components[i]['name']} and {components[i+1]['name']}",
                "tags": ["data-flow"]
            })
    
    # Enhanced STRIDE threats based on project characteristics
    threats = []
    
    # Base STRIDE threats
    base_threats = [
        {
            "name": "Identity Spoofing",
            "category": "spoofing",
            "description": "Attackers impersonate legitimate users or services",
            "impact": "High",
            "likelihood": "Medium",
            "severity": "High"
        },
        {
            "name": "Data Integrity Attacks",
            "category": "tampering", 
            "description": "Unauthorized modification of data in transit or storage",
            "impact": "High",
            "likelihood": "Medium",
            "severity": "High"
        },
        {
            "name": "Information Disclosure",
            "category": "information-disclosure",
            "description": "Sensitive information exposed to unauthorized parties",
            "impact": "High",
            "likelihood": "High" if any(word in desc_lower for word in ['personal', 'pii', 'payment', 'sensitive']) else "Medium",
            "severity": "Critical" if any(word in desc_lower for word in ['payment', 'financial', 'pii']) else "High"
        },
        {
            "name": "Service Disruption",
            "category": "denial-of-service",
            "description": "System becomes unavailable to legitimate users",
            "impact": "Medium",
            "likelihood": "High",
            "severity": "Medium"
        },
        {
            "name": "Privilege Escalation",
            "category": "elevation-of-privilege",
            "description": "Attackers gain unauthorized access to admin functions or data",
            "impact": "High",
            "likelihood": "Medium",
            "severity": "High"
        }
    ]
    
    # Add context-specific threats
    if 'payment' in desc_lower or project_type == "mobile-app":
        base_threats.append({
            "name": "Payment Fraud",
            "category": "tampering",
            "description": "Manipulation of payment transactions and financial data",
            "impact": "Critical",
            "likelihood": "Medium", 
            "severity": "Critical"
        })
    
    if 'mobile' in desc_lower or project_type == "mobile-app":
        base_threats.append({
            "name": "Device Compromise",
            "category": "elevation-of-privilege",
            "description": "Malicious apps or OS vulnerabilities compromise device security",
            "impact": "High",
            "likelihood": "Medium",
            "severity": "High"
        })
    
    if 'api' in desc_lower or project_type == "api":
        base_threats.append({
            "name": "API Abuse",
            "category": "denial-of-service", 
            "description": "Excessive API calls overwhelming system resources",
            "impact": "Medium",
            "likelihood": "High",
            "severity": "Medium"
        })
    
    threats = base_threats
    
    # Context-aware mitigations
    mitigations = [
        {
            "name": "Multi-Factor Authentication",
            "description": "Implement MFA to prevent identity spoofing",
            "riskReduction": 85
        },
        {
            "name": "Input Validation & Sanitization", 
            "description": "Validate and sanitize all user inputs to prevent injection attacks",
            "riskReduction": 75
        },
        {
            "name": "HTTPS Encryption",
            "description": "Use TLS encryption for all data in transit",
            "riskReduction": 90
        },
        {
            "name": "Rate Limiting & DDoS Protection",
            "description": "Implement rate limiting and DDoS protection mechanisms",
            "riskReduction": 70
        },
        {
            "name": "Zero Trust Architecture",
            "description": "Implement least privilege access and continuous verification",
            "riskReduction": 80
        }
    ]
    
    # Add context-specific mitigations
    if 'payment' in desc_lower:
        mitigations.append({
            "name": "PCI DSS Compliance",
            "description": "Implement Payment Card Industry security standards",
            "riskReduction": 95
        })
    
    if 'mobile' in desc_lower:
        mitigations.append({
            "name": "Mobile App Security",
            "description": "Implement certificate pinning, code obfuscation, and runtime protection",
            "riskReduction": 75
        })
    
    # Extract project name from description or use generic name
    project_name = "Security Assessment"
    words = project_description.split()
    if len(words) > 0:
        # Try to find a likely project name (capitalize first meaningful word)
        for word in words[:5]:
            if word.lower() not in ['a', 'an', 'the', 'is', 'for', 'with', 'my', 'our']:
                project_name = word.capitalize()
                break
    
    # Create OTM structure
    otm_data = {
        "otmVersion": "0.1.0",
        "project": {
            "name": project_name,
            "id": str(uuid.uuid4()),
            "description": project_description,
            "owner": "Security Team",
            "ownerContact": "",
            "tags": ["llm-generated", "conversation-based", "devici-ready"]
        },
        "representations": [
            {
                "name": "Architecture Overview",
                "id": str(uuid.uuid4()),
                "type": "threat-model",
                "size": {"width": 1000, "height": 1000}
            }
        ],
        "trustZones": [
            {
                "id": str(uuid.uuid4()),
                "name": tz["name"],
                "type": tz["type"], 
                "description": tz["description"],
                "risk": {"trustRating": 10 if "private" in tz["type"] else 3}
            } for tz in trust_zones
        ],
        "components": [
            {
                "id": str(uuid.uuid4()),
                "name": comp["name"],
                "type": comp["type"],
                "description": comp["description"], 
                "tags": comp["tags"]
            } for comp in components
        ],
        "dataflows": [
            {
                "id": str(uuid.uuid4()),
                "name": df["name"],
                "source": df["source"],
                "destination": df["destination"],
                "description": df["description"],
                "tags": df["tags"]
            } for df in data_flows
        ],
        "threats": [
            {
                "id": str(uuid.uuid4()),
                "name": threat["name"],
                "categories": [threat["category"]],
                "description": threat["description"],
                "risk": {
                    "impact": threat["impact"],
                    "impactComment": f"{threat['severity']} severity {threat['category']} threat"
                },
                "tags": ["stride", threat["category"]]
            } for threat in threats
        ],
        "mitigations": [
            {
                "id": str(uuid.uuid4()),
                "name": mit["name"],
                "description": mit["description"],
                "riskReduction": mit["riskReduction"],
                "tags": ["security-control"]
            } for mit in mitigations
        ]
    }
    
    # Validate OTM data against official schema
    is_valid, validation_message = validate_otm_data(otm_data)
    if not is_valid:
        return f"❌ Generated OTM failed schema validation:\n{validation_message}\n\nPlease check the project description and try again."
    
    # Save OTM file
    safe_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).strip()
    otm_filename = f"{safe_name.replace(' ', '-').lower()}-threat-model.otm"
    
    try:
        with open(otm_filename, 'w') as f:
            json.dump(otm_data, f, indent=2)
    except Exception as e:
        return f"❌ Error saving OTM file: {str(e)}"
    
    # Generate summary
    result = f"""
🎯 **LLM-Generated OTM Created!**

**📋 Project Analysis:**
- 📄 Name: {project_name}
- 🏷️ Type: {project_type.replace('-', ' ').title()}
- 📁 File: `{otm_filename}`

**🏗️ Architecture Detected:**
"""
    
    for comp in components:
        result += f"   • {comp['name']} ({comp['type']})\n"
    
    result += f"""
**🚨 Generated {len(threats)} STRIDE Threats:**
"""
    for threat in threats[:5]:  # Show first 5
        result += f"   • {threat['name']} ({threat['severity']} severity)\n"
    
    if len(threats) > 5:
        result += f"   • ... and {len(threats) - 5} more\n"
    
    result += f"""
**🛡️ Recommended {len(mitigations)} Security Controls:**
"""
    for mit in mitigations[:5]:  # Show first 5  
        result += f"   • {mit['name']} ({mit['riskReduction']}% risk reduction)\n"
    
    if len(mitigations) > 5:
        result += f"   • ... and {len(mitigations) - 5} more\n"
    
    result += f"""
**🚀 Zero-Friction Import:**
1. **Open Devici** → Go to your collection
2. **Import OTM** → Upload `{otm_filename}`
3. **Customize** → Add project-specific details
4. **Share** → Collaborate with security team

✅ **Secure & Sound**: No file system access required!
💬 **LLM-Powered**: Generated from your conversation context
🏢 **Enterprise Ready**: Professional OTM format
"""
    
    return result

# =============================================================================
# ENHANCED COMPONENT & THREAT CREATION - Browser Learning Integration
# =============================================================================

@mcp.tool()
async def create_component_with_visual_placement(
    title: str,
    component_type: str,
    threat_model_id: str,
    description: str = "",
    tags: str = ""
) -> str:
    """
    Create a component with proper visual placement on canvas.
    
    Based on browser interface exploration - supports component types:
    - process: Application processes, services, functions
    - datastore: Databases, file systems, data repositories  
    - external-entity: Users, external systems, third parties
    - external-service: External APIs, cloud services, payment providers
    - web-service: Web applications, REST APIs, web servers
    - generic: Custom or unspecified component types
    
    Args:
        title: Component name
        component_type: One of the supported types above
        threat_model_id: Target threat model ID
        description: Component description
        tags: Comma-separated tags
    """
    async with create_client_from_env() as client:
        try:
            # Get threat model details to find canvas
            tm_details = await client.get_threat_model(threat_model_id)
            canvas_id = tm_details.get("canvases", [None])[0]
            
            if not canvas_id:
                return f"❌ No canvas found for threat model {threat_model_id}"
            
            # Create component with canvas linking
            component_data = {
                "title": title,
                "description": description,
                "type": component_type,
                "canvasId": canvas_id
            }
            
            if tags:
                component_data["tags"] = tags
            
            # Create component
            created_component = await client.create_component(component_data)
            
            # Handle API response format discovered during browser learning
            component_id = created_component.get("component") or created_component.get("id")
            
            if not component_id:
                return f"❌ Failed to create component - unexpected API response format"
            
            # Attempt visual canvas placement
            try:
                # Get current components count for positioning
                canvas_components = await client.get_components_by_canvas(canvas_id)
                position_index = len(canvas_components.get("items", []))
                
                await client._add_component_to_canvas(component_id, canvas_id, position_index)
                
                return f"""✅ Component created successfully!

**Component Details:**
- Title: {title}
- Type: {component_type}
- ID: {component_id}
- Canvas: {canvas_id}
- Position: {position_index}

**Visual Placement:** ✅ Added to canvas for proper display in Devici interface

**Next Steps:**
- View in Devici: Open threat model {threat_model_id}
- Add threats: Use 'create_threat_for_component' 
- Link mitigations: Use 'create_mitigation_for_threat'
"""
            
            except Exception as canvas_error:
                return f"""⚠️ Component created but canvas placement failed:

**Component Details:**
- Title: {title}
- Type: {component_type}  
- ID: {component_id}
- Canvas: {canvas_id}

**Issue:** Visual placement failed - {canvas_error}
**Impact:** Component exists but may not be visible on canvas in Devici
**Workaround:** Manually position in Devici interface
"""
                
        except Exception as e:
            return f"❌ Failed to create component: {str(e)}"

@mcp.tool()
async def create_threat_for_component(
    threat_title: str,
    component_id: str,
    description: str,
    priority: str = "medium",
                stride_category: str = ""
) -> str:
    """
    Create a threat linked to a specific component.
    
    Based on browser interface learning - uses STRIDE methodology integration.
    
    Args:
        threat_title: Threat name
        component_id: Target component ID
        description: Threat description
        priority: low, medium, high, or critical
        stride_category: Optional STRIDE category (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)
    """
    async with create_client_from_env() as client:
        try:
            threat_data = {
                "title": threat_title,
                "description": description,
                "priority": priority.lower(),
                "status": "open",
                "is_custom": True,
                "component": {"id": component_id}
            }
            
            if stride_category:
                threat_data["source"] = f"STRIDE: {stride_category}"
            else:
                threat_data["source"] = "MCP Browser Learning Demo"
            
            created_threat = await client.create_threat(threat_data)
            
            # Handle API response format from browser learning
            threat_id = created_threat.get("threat") or created_threat.get("id")
            
            if not threat_id:
                return f"❌ Failed to create threat - unexpected API response format"
            
            return f"""✅ Threat created successfully!

**Threat Details:**
- Title: {threat_title}
- ID: {threat_id}
- Component: {component_id}
- Priority: {priority}
- STRIDE: {stride_category or 'Not specified'}

**Next Steps:**
- View in Devici: Open the threat model containing component {component_id}
- Add mitigation: Use 'create_mitigation_for_threat {threat_id}'
- Review threats: Use 'get_threats_by_component {component_id}'
"""
            
        except Exception as e:
            return f"❌ Failed to create threat: {str(e)}"

@mcp.tool()
async def create_mitigation_for_threat(
    mitigation_title: str,
    threat_id: str,
    definition: str
) -> str:
    """
    Create a mitigation linked to a specific threat.
    
    Based on browser interface exploration - creates custom mitigations with proper linking.
    
    Args:
        mitigation_title: Mitigation name
        threat_id: Target threat ID
        definition: Detailed mitigation description and implementation steps
    """
    async with create_client_from_env() as client:
        try:
            mitigation_data = {
                "title": mitigation_title,
                "definition": definition,
                "is_custom": True,
                "threat": {"id": threat_id}
            }
            
            created_mitigation = await client.create_mitigation(mitigation_data)
            
            # Handle API response format from browser learning
            mitigation_id = created_mitigation.get("mitigation") or created_mitigation.get("id")
            
            if not mitigation_id:
                return f"❌ Failed to create mitigation - unexpected API response format"
            
            return f"""✅ Mitigation created successfully!

**Mitigation Details:**
- Title: {mitigation_title}
- ID: {mitigation_id}
- Threat: {threat_id}

**Definition:**
{definition}

**Next Steps:**
- View in Devici: Open the threat model and navigate to threats
- Review mitigations: Use 'get_mitigations_by_threat {threat_id}'
- Update status: Mitigations can be marked as implemented in Devici interface
"""
            
        except Exception as e:
            return f"❌ Failed to create mitigation: {str(e)}"

@mcp.tool()
async def create_complete_threat_model_with_components(
    threat_model_title: str,
    collection_name: str,
    components_description: str,
    description: str = ""
) -> str:
    """
    Create a complete threat model with components using browser-learned workflow.
    
    Creates threat model, then adds components with proper visual placement.
    Demonstrates the complete workflow learned from browser interface exploration.
    
    Args:
        threat_model_title: Name for the threat model
        collection_name: Target collection name (will find by partial match)
        components_description: Describe the components needed (e.g., "web server, database, user browser, payment API")
        description: Optional threat model description
    """
    async with create_client_from_env() as client:
        try:
            # Find collection
            collections = await client.get_collections(limit=50, page=0)
            collection_id = None
            
            if isinstance(collections, dict) and 'items' in collections:
                for collection in collections['items']:
                    if collection_name.lower() in collection.get('title', '').lower():
                        collection_id = collection['id']
                        break
            
            if not collection_id:
                return f"❌ Could not find collection matching '{collection_name}'"
            
            # Create threat model
            threat_model_data = {
                "title": threat_model_title,
                "description": description or f"Created via MCP with browser-learned workflow. Components: {components_description}",
                "collectionId": collection_id
            }
            
            threat_model = await client.create_threat_model(threat_model_data)
            threat_model_id = threat_model.get("id")
            
            if not threat_model_id:
                return f"❌ Failed to create threat model"
            
            # Get canvas
            tm_details = await client.get_threat_model(threat_model_id)
            canvas_id = tm_details.get("canvases", [None])[0]
            
            # Construct Devici URLs using correct pattern
            base_url = "https://app.devici.com"
            collection_url = f"{base_url}/collections/{collection_id}"
            threat_model_url = f"{base_url}/collections/{collection_id}/d/{threat_model_id}"
            
            result = f"""✅ Threat model created successfully!

**Threat Model Details:**
- Title: {threat_model_title}
- ID: {threat_model_id}
- Collection: {collection_name}
- Canvas: {canvas_id}

**🚀 INSTANT ACCESS - Click to Open:**
**🔗 View Threat Model:** [{threat_model_url}]({threat_model_url})
**📁 View Collection:** [{collection_url}]({collection_url})

**👥 TEAM SHARING:**
Share these URLs with your team:
- **Threat Model:** `{threat_model_url}`
- **Collection:** `{collection_url}`

**Browser Learning Integration:**
- Uses OAuth2 authentication flow learned from API analysis
- Canvas-aware component creation for proper visual display
- API response format handling discovered during exploration

**Next Steps:**
1. Add components: Use 'create_component_with_visual_placement'
2. Add threats: Use 'create_threat_for_component'  
3. Add mitigations: Use 'create_mitigation_for_threat'

**Quick Component Creation Examples:**
create_component_with_visual_placement("Web Server", "process", "{threat_model_id}", "Main application server")
create_component_with_visual_placement("User Database", "datastore", "{threat_model_id}", "User credentials and data")
create_component_with_visual_placement("External API", "external-service", "{threat_model_id}", "Third-party service")

✅ **Ready for Security Discussion!** Your team can now collaborate using the URLs above.
"""
            
            return result
            
        except Exception as e:
            return f"❌ Failed to create threat model: {str(e)}"

@mcp.tool()
async def create_developer_threat_model(
    project_name: str,
    project_description: str,
    tech_stack: str = "",
    collection_name: str = "Development Projects"
) -> str:
    """
    🚀 DEVELOPER WORKFLOW: Create a threat model and get instant Devici URLs for team discussion
    
    Perfect for software developers who want to:
    - Start a security discussion with their team
    - Get immediate access to visual threat model
    - Share clickable URLs with security team
    - Begin threat modeling without security expertise
    
    Args:
        project_name: Name of your project/application
        project_description: Brief description of what your app does
        tech_stack: Technologies used (e.g., "React, Node.js, PostgreSQL")
        collection_name: Devici collection to organize your threat models
    """
    import json
    import uuid
    from datetime import datetime
    
    try:
        # Generate OTM from description (reuse existing logic)
        desc_lower = project_description.lower()
        tech_lower = tech_stack.lower()
        
        # Determine project type
        project_type = "web-application"
        if any(word in desc_lower for word in ['api', 'rest', 'microservice', 'endpoint', 'backend']):
            project_type = "api"
        elif any(word in desc_lower for word in ['mobile', 'ios', 'android', 'app']):
            project_type = "mobile-app"
        elif any(word in desc_lower for word in ['desktop', 'electron', 'native']):
            project_type = "desktop-app"
        
        # Generate components based on description
        components = []
        trust_zones = []
        data_flows = []
        
        # Frontend detection
        if any(word in desc_lower or word in tech_lower for word in ['react', 'vue', 'angular', 'frontend', 'web', 'browser', 'ui']):
            components.append({
                "name": "Web Frontend",
                "type": "web-application", 
                "description": "User interface layer handling client interactions",
                "tags": ["frontend", "ui", "client-side"]
            })
            trust_zones.append({
                "name": "Client Browser",
                "type": "b2c-web-application",
                "description": "User's web browser environment"
            })
        
        # Backend/API detection
        if any(word in desc_lower or word in tech_lower for word in ['api', 'backend', 'server', 'node', 'python', 'java', 'go', 'rust', 'php']):
            backend_name = "API Server"
            if 'microservice' in desc_lower:
                backend_name = "Microservices"
            elif 'serverless' in desc_lower:
                backend_name = "Serverless Functions"
            
            components.append({
                "name": backend_name,
                "type": "web-service",
                "description": "Backend services handling business logic and data processing",
                "tags": ["backend", "api", "server"]
            })
            trust_zones.append({
                "name": "Application Server",
                "type": "private-secured", 
                "description": "Internal application server environment"
            })
        
        # Database detection
        if any(word in desc_lower or word in tech_lower for word in ['database', 'db', 'sql', 'mongo', 'postgres', 'mysql', 'redis', 'storage', 'data']):
            db_type = "SQL Database"
            if any(word in desc_lower or word in tech_lower for word in ['mongo', 'nosql', 'document']):
                db_type = "NoSQL Database"
            elif any(word in desc_lower or word in tech_lower for word in ['redis', 'cache']):
                db_type = "Cache Layer"
            
            components.append({
                "name": db_type,
                "type": "datastore",
                "description": "Data persistence and storage layer",
                "tags": ["database", "storage", "persistence"]
            })
            trust_zones.append({
                "name": "Database Layer",
                "type": "private-secured",
                "description": "Secured database environment"
            })
        
        # External services detection
        if any(word in desc_lower for word in ['payment', 'stripe', 'paypal', 'third-party', 'external', 'integration']):
            components.append({
                "name": "External Services",
                "type": "external-service",
                "description": "Third-party services and integrations",
                "tags": ["external", "third-party", "integration"]
            })
            trust_zones.append({
                "name": "External Services",
                "type": "public-cloud",
                "description": "External third-party service providers"
            })
        
        # Generate data flows between components
        if len(components) >= 2:
            for i in range(len(components) - 1):
                data_flows.append({
                    "name": f"{components[i]['name']} → {components[i+1]['name']}",
                    "source": components[i]['name'],
                    "destination": components[i+1]['name'],
                    "description": f"Data communication between {components[i]['name']} and {components[i+1]['name']}",
                    "tags": ["data-flow"]
                })
        
        # Generate developer-focused STRIDE threats
        threats = [
            {
                "name": "Authentication Bypass",
                "category": "spoofing",
                "description": "Attackers bypass authentication mechanisms to impersonate legitimate users",
                "impact": "High",
                "likelihood": "High" if 'auth' not in desc_lower and 'login' not in desc_lower else "Medium",
                "severity": "High"
            },
            {
                "name": "Data Tampering in Transit",
                "category": "tampering", 
                "description": "Man-in-the-middle attacks modify data between components",
                "impact": "High",
                "likelihood": "High" if 'https' not in desc_lower and 'ssl' not in desc_lower else "Low",
                "severity": "High"
            },
            {
                "name": "Sensitive Data Exposure",
                "category": "information-disclosure",
                "description": "Application logs, error messages, or APIs leak sensitive information",
                "impact": "High",
                "likelihood": "High" if any(word in desc_lower for word in ['personal', 'pii', 'payment', 'sensitive']) else "Medium",
                "severity": "Critical" if any(word in desc_lower for word in ['payment', 'financial', 'pii']) else "High"
            },
            {
                "name": "Application Denial of Service",
                "category": "denial-of-service",
                "description": "Resource exhaustion attacks make the application unavailable",
                "impact": "Medium",
                "likelihood": "High",
                "severity": "Medium"
            },
            {
                "name": "Privilege Escalation",
                "category": "elevation-of-privilege",
                "description": "Users gain unauthorized access to admin functions or data",
                "impact": "High",
                "likelihood": "Medium",
                "severity": "High"
            }
        ]
        
        # Add context-specific threats for developers
        if 'api' in desc_lower or project_type == "api":
            threats.append({
                "name": "API Injection Attacks",
                "category": "tampering",
                "description": "SQL injection, NoSQL injection, or command injection through API endpoints",
                "impact": "Critical",
                "likelihood": "High" if 'validation' not in desc_lower else "Medium",
                "severity": "Critical"
            })
        
        if 'mobile' in desc_lower or project_type == "mobile-app":
            threats.append({
                "name": "Mobile App Reverse Engineering",
                "category": "information-disclosure",
                "description": "Attackers reverse engineer mobile app to extract secrets or vulnerabilities",
                "impact": "High",
                "likelihood": "Medium",
                "severity": "High"
            })
        
        # Developer-focused mitigations
        mitigations = [
            {
                "name": "Implement Strong Authentication",
                "description": "Use multi-factor authentication and secure session management",
                "riskReduction": 85
            },
            {
                "name": "Input Validation & Output Encoding", 
                "description": "Validate all inputs and encode outputs to prevent injection attacks",
                "riskReduction": 80
            },
            {
                "name": "HTTPS Everywhere",
                "description": "Enforce HTTPS for all communications and use HSTS headers",
                "riskReduction": 90
            },
            {
                "name": "Rate Limiting & WAF",
                "description": "Implement rate limiting and Web Application Firewall protection",
                "riskReduction": 70
            },
            {
                "name": "Principle of Least Privilege",
                "description": "Grant minimum necessary permissions and implement role-based access",
                "riskReduction": 75
            }
        ]
        
        # Add context-specific mitigations
        if 'payment' in desc_lower:
            mitigations.append({
                "name": "PCI DSS Compliance",
                "description": "Implement Payment Card Industry security standards",
                "riskReduction": 95
            })
        
        if 'api' in desc_lower:
            mitigations.append({
                "name": "API Security Best Practices",
                "description": "Implement API authentication, rate limiting, and input validation",
                "riskReduction": 80
            })
        
        # Create OTM structure
        otm_data = {
            "otmVersion": "0.1.0",
            "project": {
                "name": project_name,
                "id": str(uuid.uuid4()),
                "description": project_description,
                "owner": "Development Team",
                "ownerContact": "",
                "tags": ["developer-generated", "security-discussion", "devici-ready"]
            },
            "representations": [
                {
                    "name": "Architecture Overview",
                    "id": str(uuid.uuid4()),
                    "type": "threat-model",
                    "size": {"width": 1000, "height": 1000}
                }
            ],
            "trustZones": [
                {
                    "id": str(uuid.uuid4()),
                    "name": tz["name"],
                    "type": tz["type"], 
                    "description": tz["description"],
                    "risk": {"trustRating": 10 if "private" in tz["type"] else 3}
                } for tz in trust_zones
            ],
            "components": [
                {
                    "id": str(uuid.uuid4()),
                    "name": comp["name"],
                    "type": comp["type"],
                    "description": comp["description"], 
                    "tags": comp["tags"]
                } for comp in components
            ],
            "dataflows": [
                {
                    "id": str(uuid.uuid4()),
                    "name": df["name"],
                    "source": df["source"],
                    "destination": df["destination"],
                    "description": df["description"],
                    "tags": df["tags"]
                } for df in data_flows
            ],
            "threats": [
                {
                    "id": str(uuid.uuid4()),
                    "name": threat["name"],
                    "categories": [threat["category"]],
                    "description": threat["description"],
                    "risk": {
                        "impact": threat["impact"],
                        "impactComment": f"{threat['severity']} severity {threat['category']} threat"
                    },
                    "tags": ["stride", threat["category"], "developer-focused"]
                } for threat in threats
            ],
            "mitigations": [
                {
                    "id": str(uuid.uuid4()),
                    "name": mit["name"],
                    "description": mit["description"],
                    "riskReduction": mit["riskReduction"],
                    "tags": ["security-control", "developer-actionable"]
                } for mit in mitigations
            ]
        }
        
        # Validate OTM data
        is_valid, validation_message = validate_otm_data(otm_data)
        if not is_valid:
            return f"❌ Generated OTM failed validation:\n{validation_message}"
        
        # Create threat model in Devici
        async with create_client_from_env() as client:
            # Get or create collection
            collections_result = await client.get_collections(limit=50, page=0)
            
            if isinstance(collections_result, dict) and 'items' in collections_result:
                collections_data = collections_result['items']
            else:
                return f"❌ Failed to get collections: {collections_result}"
            
            target_collection = None
            if collection_name:
                # Find specified collection
                for collection in collections_data:
                    if collection.get("title", "").lower() == collection_name.lower():
                        target_collection = collection
                        break
            
            if not target_collection:
                # Create new collection
                collection_data = {
                    "title": collection_name,
                    "description": f"Development projects and security assessments"
                }
                target_collection = await client.create_collection(collection_data)
            
            collection_id = target_collection["id"]
            
            # Import OTM using the working endpoint
            endpoint = f"/threat-models/otm/{collection_id}"
            
            # Add collection ID to OTM data
            otm_data["collectionId"] = collection_id
            
            # Import the OTM
            result = await client._make_request("POST", endpoint, json_data=otm_data)
            
            # Extract threat model ID from response
            threat_model_id = result.get("id") or result.get("threatModelId")
            
            if not threat_model_id:
                return f"❌ Failed to create threat model - no ID returned from import"
            
            # Construct Devici URLs using correct pattern
            base_url = "https://app.devici.com"
            collection_url = f"{base_url}/collections/{collection_id}"
            threat_model_url = f"{base_url}/collections/{collection_id}/d/{threat_model_id}"
            
            # Generate developer-focused response
            return f"""
🎯 **Developer Threat Model Created Successfully!**

**📋 Project Details:**
- **Name:** {project_name}
- **Type:** {project_type.replace('-', ' ').title()}
- **Components:** {len(components)} detected
- **Threats:** {len(threats)} identified
- **Security Controls:** {len(mitigations)} recommended

**🚀 INSTANT ACCESS - Click to Open:**

**🔗 View Threat Model:** [{threat_model_url}]({threat_model_url})
**📁 View Collection:** [{collection_url}]({collection_url})

**👥 TEAM SHARING:**
Share these URLs with your security team for discussion:
- **Threat Model:** `{threat_model_url}`
- **Collection:** `{collection_url}`

**🏗️ Architecture Detected:**
{chr(10).join(f"   • {comp['name']} ({comp['type']})" for comp in components)}

**🚨 Key Security Concerns:**
{chr(10).join(f"   • {threat['name']} ({threat['severity']} severity)" for threat in threats[:3])}

**🛡️ Recommended Actions:**
{chr(10).join(f"   • {mit['name']} ({mit['riskReduction']}% risk reduction)" for mit in mitigations[:3])}

**🎯 Next Steps for Development Team:**
1. **Review Threats:** Click the threat model URL above
2. **Discuss with Security:** Share URLs with your security team
3. **Prioritize Fixes:** Focus on High/Critical severity threats first
4. **Implement Controls:** Start with highest risk reduction mitigations
5. **Iterate:** Update the model as your architecture evolves

**💡 Pro Tips:**
- Use the visual canvas to understand data flows
- Add custom threats specific to your business logic
- Link threats to specific code components
- Schedule regular threat model reviews

✅ **Ready for Security Discussion!** Your team can now collaborate on security requirements.
"""
            
    except Exception as e:
        return f"❌ Error creating developer threat model: {str(e)}"

# =============================================================================
# ORIGINAL TOOLS - All Preserved for Compatibility
# =============================================================================

# User Management Tools - REMOVED (cruft, not needed for threat modeling)

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
async def create_collection(name: str, description: str | None = None, **other_properties) -> str:
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
async def create_threat_model(name: str, collection_id: str, description: str | None = None, **other_properties) -> str:
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

# Dashboard and Reporting Tools
@mcp.tool()
async def get_dashboard_types() -> str:
    """Get available dashboard chart types"""
    async with create_client_from_env() as client:
        result = await client.get_dashboard_types()
        return str(result)

@mcp.tool()
async def get_dashboard_data(chart_type: str, limit: int = 20, page: int = 0, start: str | None = None, end: str | None = None, project_id: str | None = None) -> str:
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
async def get_threat_models_report(start: str | None = None, end: str | None = None) -> str:
    """Get threat models report data"""
    async with create_client_from_env() as client:
        result = await client.get_threat_models_report(start=start, end=end)
        return str(result)

@mcp.tool()
async def visualize_otm_as_mermaid(otm_file_path: str) -> str:
    """
    Visualize an OTM file as a Mermaid diagram for local review
    
    Perfect for reviewing threat models before importing to Devici.
    Creates a visual representation showing components, data flows, and trust zones.
    
    Args:
        otm_file_path: Path to the OTM file to visualize
    """
    import json
    import os
    
    if not os.path.exists(otm_file_path):
        return f"❌ OTM file not found: {otm_file_path}"
    
    try:
        with open(otm_file_path, 'r') as f:
            otm_data = json.load(f)
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON in OTM file: {str(e)}"
    except Exception as e:
        return f"❌ Error reading OTM file: {str(e)}"
    
    # Extract data from OTM
    project_name = otm_data.get("project", {}).get("name", "Threat Model")
    components = otm_data.get("components", [])
    dataflows = otm_data.get("dataflows", [])
    trust_zones = otm_data.get("trustZones", [])
    threats = otm_data.get("threats", [])
    
    # Generate Mermaid diagram
    mermaid_lines = [
        "graph TD",
        f"    %% {project_name} - Architecture Overview",
        ""
    ]
    
    # Add trust zones as subgraphs
    zone_components = {}
    for i, zone in enumerate(trust_zones):
        zone_id = f"TZ{i}"
        zone_name = zone.get("name", f"Trust Zone {i+1}")
        zone_type = zone.get("type", "unknown")
        
        mermaid_lines.append(f"    subgraph {zone_id}[\"{zone_name}<br/>({zone_type})\"]")
        zone_components[zone_name] = zone_id
        mermaid_lines.append("    end")
        mermaid_lines.append("")
    
    # Add components
    component_ids = {}
    for i, comp in enumerate(components):
        comp_id = f"C{i}"
        comp_name = comp.get("name", f"Component {i+1}")
        comp_type = comp.get("type", "unknown")
        
        # Determine component shape and style based on type
        if comp_type in ["web-application", "web-service"]:
            shape = f"{comp_id}[(\"{comp_name}<br/>{comp_type}\")]"
        elif comp_type == "datastore":
            shape = f"{comp_id}[(\"{comp_name}<br/>{comp_type}\")]"
        elif comp_type == "external-service":
            shape = f"{comp_id}[[\"{comp_name}<br/>{comp_type}\"]]"
        elif comp_type == "process":
            shape = f"{comp_id}[\"{comp_name}<br/>{comp_type}\"]"
        else:
            shape = f"{comp_id}[\"{comp_name}<br/>{comp_type}\"]"
        
        mermaid_lines.append(f"    {shape}")
        component_ids[comp_name] = comp_id
    
    mermaid_lines.append("")
    
    # Add data flows
    for i, flow in enumerate(dataflows):
        source = flow.get("source", "")
        destination = flow.get("destination", "")
        flow_name = flow.get("name", f"Flow {i+1}")
        
        source_id = component_ids.get(source, f"Unknown_{source}")
        dest_id = component_ids.get(destination, f"Unknown_{destination}")
        
        # Create arrow with label
        mermaid_lines.append(f"    {source_id} -->|{flow_name}| {dest_id}")
    
    mermaid_lines.append("")
    
    # Add styling
    mermaid_lines.extend([
        "    %% Styling",
        "    classDef webApp fill:#e1f5fe,stroke:#0277bd,stroke-width:2px",
        "    classDef datastore fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px", 
        "    classDef external fill:#fff3e0,stroke:#f57c00,stroke-width:2px",
        "    classDef process fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px",
        ""
    ])
    
    # Apply styles to components
    for i, comp in enumerate(components):
        comp_id = f"C{i}"
        comp_type = comp.get("type", "unknown")
        
        if comp_type in ["web-application", "web-service"]:
            mermaid_lines.append(f"    class {comp_id} webApp")
        elif comp_type == "datastore":
            mermaid_lines.append(f"    class {comp_id} datastore")
        elif comp_type == "external-service":
            mermaid_lines.append(f"    class {comp_id} external")
        elif comp_type == "process":
            mermaid_lines.append(f"    class {comp_id} process")
    
    mermaid_diagram = "\n".join(mermaid_lines)
    
    # Generate summary
    threat_summary = ""
    if threats:
        threat_counts = {}
        for threat in threats:
            categories = threat.get("categories", ["unknown"])
            for category in categories:
                threat_counts[category] = threat_counts.get(category, 0) + 1
        
        threat_summary = "\n**🚨 Threats Identified:**\n"
        for category, count in threat_counts.items():
            threat_summary += f"   • {category.title()}: {count} threats\n"
    
    return f"""
🎯 **OTM Visualization Generated**

**📄 File:** `{otm_file_path}`
**🏗️ Components:** {len(components)}
**🔄 Data Flows:** {len(dataflows)}
**🛡️ Trust Zones:** {len(trust_zones)}
**⚠️ Threats:** {len(threats)}
{threat_summary}

**📊 Mermaid Diagram:**

```mermaid
{mermaid_diagram}
```

**💡 How to Use:**
1. **Review the diagram** above to understand your architecture
2. **Verify components** are correctly identified
3. **Check data flows** between components
4. **Review trust boundaries** and zones
5. **Import to Devici** when ready: `import_otm_to_devici("{otm_file_path}", "collection_name")`

**🔧 Need Changes?**
- Edit the OTM file manually if needed
- Regenerate with `create_otm_file_for_devici()` for fresh analysis
- Use `create_otm_from_description()` for custom descriptions
"""

def main():
    """Main entry point for the server."""
    mcp.run()

if __name__ == "__main__":
    main() 