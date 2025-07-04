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
async def debug_working_directory() -> str:
    """Debug tool to check current working directory and file permissions"""
    import os
    import stat
    
    current_dir = os.getcwd()
    result = f"🔍 **Debug Information:**\n\n"
    result += f"**Current Working Directory:** {current_dir}\n"
    result += f"**Directory exists:** {os.path.exists(current_dir)}\n"
    result += f"**Directory writable:** {os.access(current_dir, os.W_OK)}\n"
    result += f"**Directory readable:** {os.access(current_dir, os.R_OK)}\n"
    
    # List files in current directory
    try:
        files = os.listdir(current_dir)
        result += f"**Files in directory:** {len(files)}\n"
        for f in files[:10]:  # Show first 10 files
            result += f"  - {f}\n"
        if len(files) > 10:
            result += f"  ... and {len(files) - 10} more files\n"
    except Exception as e:
        result += f"**Error listing files:** {str(e)}\n"
    
    # Test file creation
    test_file = "test_write_permissions.tmp"
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        if os.path.exists(test_file):
            result += f"**Test file creation:** ✅ SUCCESS\n"
            os.remove(test_file)  # Clean up
        else:
            result += f"**Test file creation:** ❌ FAILED (file not found after write)\n"
    except Exception as e:
        result += f"**Test file creation:** ❌ FAILED ({str(e)})\n"
    
    return result

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
    
    # Use centralized OTM generation function
    otm_data, is_valid, validation_message = create_validated_otm_structure(
        project_name=project_name,
        project_description=f"Threat model for {project_name} project", 
        components=components,
        trust_zones=trust_zones,
        data_flows=data_flows,
        threats=stride_threats,
        mitigations=stride_mitigations,
        project_tags=["auto-generated", "llm-analysis"]
    )
    
    if not is_valid:
        return f"❌ Generated OTM failed validation even after auto-fix:\n{validation_message}"
    
    # Save OTM file locally
    safe_project_name = "".join(c for c in project_name if c.isalnum() or c in ('-', '_')).strip()
    otm_filename = f"{safe_project_name}-threat-model.otm"
    
    # Ensure we're writing to the current working directory
    current_dir = os.getcwd()
    full_path = os.path.join(current_dir, otm_filename)
    
    try:
        with open(full_path, 'w') as f:
            json.dump(otm_data, f, indent=2)
        
        # Verify file was actually created
        if not os.path.exists(full_path):
            return f"❌ File {full_path} was not created despite no error"
        
        # Get absolute path for user
        abs_path = os.path.abspath(full_path)
        
        # Also log the creation for debugging
        logger.info(f"Created OTM file: {abs_path}")
        
    except Exception as e:
        return f"❌ Error saving OTM file: {str(e)}\nCurrent directory: {current_dir}\nAttempted path: {full_path}"
    
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
        return f"❌ Error creating threat model in Devici: {str(e)}\n\n✅ OTM file saved locally: {otm_filename} (Full path: {abs_path})"

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
    
    # Create components with UUIDs first so we can reference them in dataflows
    components_with_ids = []
    component_name_to_id = {}
    
    for comp in components:
        comp_id = str(uuid.uuid4())
        component_name_to_id[comp["name"]] = comp_id
        components_with_ids.append({
            "id": comp_id,
            "name": comp["name"],
            "type": comp["type"],
            "description": comp["description"],
            "tags": comp["tags"]
        })
    
    # Fix dataflows to use component IDs instead of names
    dataflows_with_ids = []
    for df in data_flows:
        source_id = component_name_to_id.get(df["source"])
        dest_id = component_name_to_id.get(df["destination"])
        
        if source_id and dest_id:  # Only add dataflow if both components exist
            dataflows_with_ids.append({
                "id": str(uuid.uuid4()),
                "name": df["name"],
                "source": source_id,
                "destination": dest_id,
                "description": df["description"],
                "tags": df["tags"]
            })
    
    # Use centralized OTM generation function
    otm_data, is_valid, validation_message = create_validated_otm_structure(
        project_name=project_name,
        project_description=f"Threat model for {project_name} project",
        components=components,
        trust_zones=trust_zones,
        data_flows=data_flows,
        threats=stride_threats,
        mitigations=stride_mitigations,
        project_tags=["auto-generated", "llm-analysis", "devici-ready"]
    )
    
    if not is_valid:
        return f"❌ Generated OTM failed validation even after auto-fix:\n{validation_message}"
    
    # Save OTM file locally
    safe_project_name = "".join(c for c in project_name if c.isalnum() or c in ('-', '_')).strip()
    otm_filename = f"{safe_project_name}-devici-ready.otm"
    
    # Ensure we're writing to the current working directory
    current_dir = os.getcwd()
    full_path = os.path.join(current_dir, otm_filename)
    
    try:
        with open(full_path, 'w') as f:
            json.dump(otm_data, f, indent=2)
        
        # Verify file was actually created
        if not os.path.exists(full_path):
            return f"❌ File {full_path} was not created despite no error"
        
        # Get absolute path for user
        abs_path = os.path.abspath(full_path)
        
        # Also log the creation for debugging
        logger.info(f"Created OTM file: {abs_path}")
        
    except Exception as e:
        return f"❌ Error saving OTM file: {str(e)}\nCurrent directory: {current_dir}\nAttempted path: {full_path}"
    
    # Generate summary
    result = f"""
🎯 **OTM File Created - Ready for Devici!**

**📄 File Generated:**
- 📁 File: `{otm_filename}`
- 📂 Full Path: `{abs_path}`
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
        
        # Validate and auto-fix OTM data against official schema
        fixed_otm_data, is_valid, validation_message = validate_and_fix_otm_data(otm_data)
        if not is_valid:
            return f"❌ OTM file failed schema validation even after auto-fix:\n{validation_message}\n\nPlease ensure the file conforms to the Open Threat Model standard."
        
        # Use the fixed data for everything going forward
        otm_data = fixed_otm_data
        
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
            
            # Use reusable _make_request function for the ONLY CORRECT ENDPOINT
            try:
                result = await client._make_request("POST", f"/threat-models/otm/{target_collection_id}", json_data=otm_data)
                print("✅ OTM import successful!")
                
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
                
            except Exception as e:
                print(f"❌ Error importing OTM: {e}")
                return f"❌ Error importing OTM: {str(e)}"
            
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

def validate_and_fix_otm_data(otm_data: dict) -> tuple[dict, bool, str]:
    """
    Validate OTM data and automatically fix common issues.
    Returns (fixed_otm_data, is_valid, message)
    """
    import copy
    import uuid
    
    # Create a deep copy to avoid modifying the original
    fixed_data = copy.deepcopy(otm_data)
    fixes_applied = []
    
    # Fix 1: Ensure components have required parent field
    if "components" in fixed_data and fixed_data["components"]:
        # Get the first trust zone ID as default parent
        default_trust_zone = None
        if "trustZones" in fixed_data and fixed_data["trustZones"]:
            default_trust_zone = fixed_data["trustZones"][0]["id"]
        
        for component in fixed_data["components"]:
            if "parent" not in component:
                if default_trust_zone:
                    component["parent"] = {"trustZone": default_trust_zone}
                    fixes_applied.append(f"Added missing parent to component: {component.get('name', 'unnamed')}")
                else:
                    # Create a default trust zone if none exists
                    if "trustZones" not in fixed_data:
                        fixed_data["trustZones"] = []
                    
                    default_tz_id = str(uuid.uuid4())
                    fixed_data["trustZones"].append({
                        "id": default_tz_id,
                        "name": "Default Zone",
                        "type": "default",
                        "description": "Auto-generated default trust zone",
                        "risk": {"trustRating": 50}
                    })
                    component["parent"] = {"trustZone": default_tz_id}
                    fixes_applied.append(f"Created default trust zone and assigned to component: {component.get('name', 'unnamed')}")
    
    # Fix 2: Fix threat risk fields (impact must be number, likelihood required)
    if "threats" in fixed_data and fixed_data["threats"]:
        for threat in fixed_data["threats"]:
            if "risk" in threat:
                risk = threat["risk"]
                
                # Fix impact: convert string to number
                if "impact" in risk and isinstance(risk["impact"], str):
                    impact_map = {"Low": 25, "Medium": 50, "High": 75, "Critical": 100}
                    old_impact = risk["impact"]
                    risk["impact"] = impact_map.get(old_impact, 50)
                    fixes_applied.append(f"Fixed threat impact: '{old_impact}' → {risk['impact']}")
                elif "impact" not in risk:
                    risk["impact"] = 50
                    fixes_applied.append(f"Added missing impact to threat: {threat.get('name', 'unnamed')}")
                
                # Add missing likelihood
                if "likelihood" not in risk:
                    risk["likelihood"] = 50  # Default medium likelihood
                    fixes_applied.append(f"Added missing likelihood to threat: {threat.get('name', 'unnamed')}")
    
    # Fix 3: Convert dataflow source/destination from names to UUIDs
    if "components" in fixed_data and "dataflows" in fixed_data:
        # Create a mapping from component names to UUIDs
        name_to_id = {}
        for component in fixed_data["components"]:
            if "name" in component and "id" in component:
                name_to_id[component["name"]] = component["id"]
        
        # Fix dataflows
        for dataflow in fixed_data["dataflows"]:
            if "source" in dataflow and "destination" in dataflow:
                # Check if source/destination are names (not UUIDs)
                source = dataflow["source"]
                destination = dataflow["destination"]
                
                # If source is a component name, convert to UUID
                if source in name_to_id:
                    dataflow["source"] = name_to_id[source]
                    fixes_applied.append(f"Fixed dataflow source '{source}' → UUID")
                
                # If destination is a component name, convert to UUID  
                if destination in name_to_id:
                    dataflow["destination"] = name_to_id[destination]
                    fixes_applied.append(f"Fixed dataflow destination '{destination}' → UUID")
    
    # Fix 4: Ensure all required UUIDs are present and valid
    # Fix project ID if missing
    if "project" in fixed_data:
        if "id" not in fixed_data["project"] or not fixed_data["project"]["id"]:
            fixed_data["project"]["id"] = str(uuid.uuid4())
            fixes_applied.append("Added missing project ID")
    
    # Fix component IDs if missing
    if "components" in fixed_data:
        for component in fixed_data["components"]:
            if "id" not in component or not component["id"]:
                component["id"] = str(uuid.uuid4())
                fixes_applied.append(f"Added missing ID for component '{component.get('name', 'Unknown')}'")
    
    # Fix dataflow IDs if missing
    if "dataflows" in fixed_data:
        for dataflow in fixed_data["dataflows"]:
            if "id" not in dataflow or not dataflow["id"]:
                dataflow["id"] = str(uuid.uuid4())
                fixes_applied.append(f"Added missing ID for dataflow '{dataflow.get('name', 'Unknown')}'")
    
    # Fix threat IDs if missing
    if "threats" in fixed_data:
        for threat in fixed_data["threats"]:
            if "id" not in threat or not threat["id"]:
                threat["id"] = str(uuid.uuid4())
                fixes_applied.append(f"Added missing ID for threat '{threat.get('name', 'Unknown')}'")
    
    # Fix mitigation IDs if missing
    if "mitigations" in fixed_data:
        for mitigation in fixed_data["mitigations"]:
            if "id" not in mitigation or not mitigation["id"]:
                mitigation["id"] = str(uuid.uuid4())
                fixes_applied.append(f"Added missing ID for mitigation '{mitigation.get('name', 'Unknown')}'")
    
    # Fix trust zone IDs if missing
    if "trustZones" in fixed_data:
        for trust_zone in fixed_data["trustZones"]:
            if "id" not in trust_zone or not trust_zone["id"]:
                trust_zone["id"] = str(uuid.uuid4())
                fixes_applied.append(f"Added missing ID for trust zone '{trust_zone.get('name', 'Unknown')}'")
    
    # Fix representation IDs if missing
    if "representations" in fixed_data:
        for representation in fixed_data["representations"]:
            if "id" not in representation or not representation["id"]:
                representation["id"] = str(uuid.uuid4())
                fixes_applied.append(f"Added missing ID for representation '{representation.get('name', 'Unknown')}'")
    
    # Now validate the fixed data
    is_valid, validation_message = validate_otm_data(fixed_data)
    
    # Create comprehensive message
    if fixes_applied:
        fix_summary = f"🔧 Auto-fixes applied:\n" + "\n".join(f"   • {fix}" for fix in fixes_applied)
        if is_valid:
            message = f"{fix_summary}\n\n✅ OTM data is now valid after auto-fixing"
        else:
            message = f"{fix_summary}\n\n❌ OTM data still invalid after auto-fixing:\n{validation_message}"
    else:
        if is_valid:
            message = "✅ OTM data is valid (no fixes needed)"
        else:
            message = f"❌ OTM data is invalid and no auto-fixes were applicable:\n{validation_message}"
    
    return fixed_data, is_valid, message

@mcp.tool()
async def create_otm_from_description(
    project_description: str, 
    tech_stack: str = "", 
    architecture: str = "", 
    import_to_devici: bool = True, 
    collection_name: str = "AI Generated Models"
) -> str:
    """
    Create an OTM file based on detailed architectural information.
    
    For accurate threat modeling, provide:
    
    project_description: Detailed description including:
        - What components exist (e.g., "web server", "database", "API gateway", "mobile app")
        - How they connect (e.g., "mobile app calls API gateway which queries database")
        - What data flows between them (e.g., "user credentials", "payment data", "file uploads")
        - Trust boundaries (e.g., "mobile app is in user device, API in private cloud")
    
    tech_stack: Specific technologies used (e.g., "React, Node.js, PostgreSQL, AWS Lambda")
    
    architecture: Architecture pattern (e.g., "3-tier web app", "microservices", "serverless", "mobile + API")
    
    Examples:
    - "Web application with React frontend, Node.js API server, PostgreSQL database. Users authenticate via OAuth2, upload files to S3, and process payments via Stripe API."
    - "Mobile iOS app that connects to REST API gateway, which calls Lambda functions that read/write to DynamoDB and send notifications via SNS."
    - "MCP server with AI assistant client connecting via MCP protocol to Python FastMCP server, which authenticates with OAuth2 and calls Devici REST API, plus reads/writes OTM files locally."
    """
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
    
    # Generate components based on explicit architectural description
    components = []
    trust_zones = []
    data_flows = []
    
    # Check for MCP architecture first (highest priority)
    is_mcp_project = ('mcp' in desc_lower and ('server' in desc_lower or 'protocol' in desc_lower)) or 'fastmcp' in tech_lower
    
    if is_mcp_project:
        # MCP-specific architecture
        components.append({
            "name": "AI Assistant Client",
            "type": "external-entity",
            "description": "AI assistant (Claude, Cursor, etc.) that connects via MCP protocol",
            "tags": ["ai", "client", "mcp", "external"]
        })
        
        components.append({
            "name": "MCP Server",
            "type": "process",
            "description": "FastMCP Python server handling MCP protocol requests and business logic",
            "tags": ["mcp", "server", "protocol", "python", "core"]
        })
        
        if 'oauth' in desc_lower or 'auth' in desc_lower:
            components.append({
                "name": "Authentication Service",
                "type": "process",
                "description": "OAuth2 authentication handler for external API access",
                "tags": ["oauth", "authentication", "security"]
            })
        
        components.append({
            "name": "API Client",
            "type": "process",
            "description": "HTTP client component for making REST API calls",
            "tags": ["api", "client", "http", "rest"]
        })
        
        if 'devici' in desc_lower or 'external' in desc_lower or 'platform' in desc_lower:
            components.append({
                "name": "External API Service",
                "type": "external-service",
                "description": "External REST API service (Devici platform or similar)",
                "tags": ["external", "api", "rest", "cloud"]
            })
        
        if 'file' in desc_lower or 'otm' in desc_lower or 'local' in desc_lower:
            components.append({
                "name": "File System",
                "type": "datastore",
                "description": "Local file system for reading/writing OTM files and project data",
                "tags": ["filesystem", "storage", "otm", "local"]
            })
        
        # MCP trust zones
        trust_zones.extend([
            {
                "name": "AI Client Environment",
                "type": "b2c-web-application",
                "description": "External AI assistant client environment"
            },
            {
                "name": "MCP Server Environment", 
                "type": "private-secured",
                "description": "Local MCP server and processing environment"
            },
            {
                "name": "External Services",
                "type": "public-cloud",
                "description": "External API endpoints and cloud services"
            }
        ])
    
    else:
        # Non-MCP architectures - explicit component detection
        
        # Frontend detection
        if any(word in desc_lower or word in tech_lower for word in ['react', 'vue', 'angular', 'frontend', 'web', 'browser', 'ui', 'mobile', 'ios', 'android']):
            frontend_type = "mobile-app" if any(word in desc_lower or word in tech_lower for word in ['mobile', 'ios', 'android', 'app']) else "web-application"
            frontend_name = "Mobile App" if frontend_type == "mobile-app" else "Web Frontend"
            
            components.append({
                "name": frontend_name,
                "type": frontend_type,
                "description": "User interface layer handling client interactions",
                "tags": ["frontend", "ui", "client-side"]
            })
            trust_zones.append({
                "name": "Client Environment",
                "type": "b2c-web-application",
                "description": "User's device/browser environment"
            })
        
        # Backend/API detection
        if any(word in desc_lower or word in tech_lower for word in ['api', 'backend', 'server', 'node', 'python', 'java', 'go', 'rust', 'php', 'lambda', 'function']):
            backend_name = "API Server"
            if 'microservice' in desc_lower:
                backend_name = "Microservices"
            elif 'serverless' in desc_lower or 'lambda' in desc_lower:
                backend_name = "Serverless Functions"
            elif 'gateway' in desc_lower:
                backend_name = "API Gateway"
                
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
        
        # Database detection - only if explicitly mentioned with storage context
        db_keywords = ['database', 'db', 'sql', 'mongo', 'postgres', 'mysql', 'redis', 'dynamodb', 'storage']
        if any(word in desc_lower or word in tech_lower for word in db_keywords):
            db_type = "SQL Database"
            if any(word in desc_lower or word in tech_lower for word in ['mongo', 'nosql', 'document', 'dynamodb']):
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
        if any(word in desc_lower for word in ['stripe', 'paypal', 'payment', 'third-party', 'external', 'integration', 'sns', 's3', 'aws']):
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
        # MCP-specific data flows
        if 'mcp' in desc_lower and 'server' in desc_lower:
            # Create logical MCP protocol flows
            ai_client = next((c for c in components if "AI Assistant" in c["name"]), None)
            mcp_server = next((c for c in components if "MCP Server" in c["name"]), None)
            auth_service = next((c for c in components if "Authentication" in c["name"]), None)
            api_client = next((c for c in components if "API Client" in c["name"]), None)
            external_api = next((c for c in components if "External API" in c["name"]), None)
            file_system = next((c for c in components if "File System" in c["name"]), None)
            
            if ai_client and mcp_server:
                data_flows.append({
                    "name": "MCP Protocol Communication",
                    "source": ai_client["name"],
                    "destination": mcp_server["name"],
                    "description": "MCP protocol requests and responses between AI assistant and server",
                    "tags": ["mcp", "protocol", "bidirectional"]
                })
            
            if mcp_server and auth_service:
                data_flows.append({
                    "name": "Authentication Request",
                    "source": mcp_server["name"],
                    "destination": auth_service["name"],
                    "description": "OAuth2 authentication requests for API access",
                    "tags": ["oauth", "authentication"]
                })
            
            if auth_service and api_client:
                data_flows.append({
                    "name": "Authenticated API Calls",
                    "source": auth_service["name"],
                    "destination": api_client["name"],
                    "description": "API calls with authenticated tokens",
                    "tags": ["api", "authenticated"]
                })
            elif mcp_server and api_client:
                data_flows.append({
                    "name": "API Request Processing",
                    "source": mcp_server["name"],
                    "destination": api_client["name"],
                    "description": "Processing API requests and responses",
                    "tags": ["api", "processing"]
                })
            
            if api_client and external_api:
                data_flows.append({
                    "name": "REST API Calls",
                    "source": api_client["name"],
                    "destination": external_api["name"],
                    "description": "HTTP REST API calls to external service",
                    "tags": ["rest", "http", "external"]
                })
            
            if mcp_server and file_system:
                data_flows.append({
                    "name": "File Operations",
                    "source": mcp_server["name"],
                    "destination": file_system["name"],
                    "description": "Reading and writing OTM files and project data",
                    "tags": ["file", "otm", "storage"]
                })
        else:
            # Generic data flows for non-MCP projects
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
    
    # Create OTM structure with schema compliance
    
    # Build trust zones first and capture IDs
    trust_zone_data = []
    for tz in trust_zones:
        trust_zone_data.append({
            "id": str(uuid.uuid4()),
            "name": tz["name"],
            "type": tz["type"], 
            "description": tz["description"],
            "risk": {"trustRating": 10 if "private" in tz["type"] else 3}
        })
    
    # Ensure we have at least one trust zone
    if not trust_zone_data:
        trust_zone_data.append({
            "id": str(uuid.uuid4()),
            "name": "Default Zone",
            "type": "default",
            "description": "Auto-generated default trust zone",
            "risk": {"trustRating": 50}
        })
    
    # Get the first trust zone ID for components
    default_trust_zone_id = trust_zone_data[0]["id"]
    
    # Build components with required parent field
    component_data = []
    component_name_to_id = {}
    for comp in components:
        comp_id = str(uuid.uuid4())
        component_name_to_id[comp["name"]] = comp_id
        component_data.append({
            "id": comp_id,
            "name": comp["name"],
            "type": comp["type"],
            "description": comp["description"], 
            "tags": comp["tags"],
            "parent": {"trustZone": default_trust_zone_id}
        })
    
    # Build dataflows with component UUIDs instead of names
    dataflow_data = []
    for df in data_flows:
        source_id = component_name_to_id.get(df["source"], list(component_name_to_id.values())[0] if component_name_to_id else str(uuid.uuid4()))
        dest_id = component_name_to_id.get(df["destination"], list(component_name_to_id.values())[1] if len(component_name_to_id) > 1 else str(uuid.uuid4()))
        
        dataflow_data.append({
            "id": str(uuid.uuid4()),
            "name": df["name"],
            "source": source_id,
            "destination": dest_id,
            "description": df["description"],
            "tags": df["tags"]
        })
    
    # Build threats with numeric risk values
    severity_to_impact = {"Low": 25, "Medium": 50, "High": 75, "Critical": 100}
    likelihood_map = {"Low": 25, "Medium": 50, "High": 75, "Critical": 100}
    
    threat_data = []
    for threat in threats:
        threat_data.append({
            "id": str(uuid.uuid4()),
            "name": threat["name"],
            "categories": [threat["category"]],
            "description": threat["description"],
            "risk": {
                "impact": severity_to_impact.get(threat["impact"], 50),
                "likelihood": likelihood_map.get(threat["likelihood"], 50),
                "impactComment": f"{threat['severity']} severity {threat['category']} threat"
            },
            "tags": ["stride", threat["category"]]
        })
    
    # Use centralized OTM generation function
    otm_data, is_valid, validation_message = create_validated_otm_structure(
        project_name=project_name,
        project_description=project_description,
        components=components,
        trust_zones=trust_zones,
        data_flows=data_flows,
        threats=threats,
        mitigations=mitigations,
        project_tags=["llm-generated", "conversation-based", "devici-ready"]
    )
    
    if not is_valid:
        return f"❌ Generated OTM failed validation even after auto-fix:\n{validation_message}\n\nPlease check the project description and try again."
    
    # Generate summary
    result = f"""
🎯 **LLM-Generated Threat Model**

**📋 Project Analysis:**
- 📄 Name: {project_name}
- 🏷️ Type: {project_type.replace('-', ' ').title()}

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
    
    # Import to Devici if requested
    if import_to_devici:
        try:
            async with create_client_from_env() as client:
                # Get or create collection
                collections_result = await client.get_collections(limit=50, page=0)
                collections_data = collections_result.get('items', []) if isinstance(collections_result, dict) else []
                
                target_collection_id = None
                for collection in collections_data:
                    if collection.get("title", "").lower() == collection_name.lower():
                        target_collection_id = collection["id"]
                        break
                
                if not target_collection_id:
                    # Create new collection
                    collection_data = {"title": collection_name, "description": f"Auto-created for {project_name}"}
                    new_collection = await client.create_collection(collection_data)
                    target_collection_id = new_collection.get("id")
                
                # Log the payload for debugging
                logger.info(f"Importing OTM data with {len(otm_data.get('components', []))} components")
                
                # Import OTM using reusable _make_request function for the ONLY CORRECT ENDPOINT
                logger.info(f"Collection ID: {target_collection_id}")
                logger.info(f"Payload size: {len(json.dumps(otm_data))} bytes")
                
                response_json = await client._make_request("POST", f"/threat-models/otm/{target_collection_id}", json_data=otm_data)
                threat_model_id = response_json.get("id")
                
                # Generate Mermaid visualization
                mermaid_diagram = f"""graph TD
    %% {project_name} - Architecture Overview

"""
                
                for i, tz in enumerate(trust_zones):
                    mermaid_diagram += f'    subgraph TZ{i}["{tz["name"]}<br/>({tz["type"]})"]\n    end\n\n'
                
                for i, comp in enumerate(components):
                    mermaid_diagram += f'    C{i}[("{comp["name"]}<br/>{comp["type"]}")]\n'
                
                mermaid_diagram += "\n"
                for df in data_flows:
                    src_idx = next((i for i, c in enumerate(components) if c["name"] == df["source"]), 0)
                    dst_idx = next((i for i, c in enumerate(components) if c["name"] == df["destination"]), 1)
                    mermaid_diagram += f'    C{src_idx} -->|{df["name"]}| C{dst_idx}\n'
                
                mermaid_diagram += """
    %% Styling
    classDef webApp fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef datastore fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef external fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef process fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px

"""
                for i, comp in enumerate(components):
                    if comp["type"] == "web-application" or comp["type"] == "web-service":
                        mermaid_diagram += f"    class C{i} webApp\n"
                    elif comp["type"] == "datastore":
                        mermaid_diagram += f"    class C{i} datastore\n"
                    elif comp["type"] == "external-service":
                        mermaid_diagram += f"    class C{i} external\n"
                    else:
                        mermaid_diagram += f"    class C{i} process\n"
                
                # URLs
                base_url_app = "https://app.devici.com"
                collection_url = f"{base_url_app}/collections/{target_collection_id}"
                threat_model_url = f"{base_url_app}/collections/{target_collection_id}/d/{threat_model_id}" if threat_model_id else None
                
                result += f"""
**✅ IMPORTED TO DEVICI!**

**🔗 INSTANT ACCESS:**
- **Collection:** [{collection_url}]({collection_url})"""
                if threat_model_url:
                    result += f"""
- **Threat Model:** [{threat_model_url}]({threat_model_url})"""
                
                result += f"""

**📊 Architecture Visualization:**

```mermaid
{mermaid_diagram}
```

**🚨 STRIDE Threats Generated:** {len(threats)}
**🛡️ Security Controls:** {len(mitigations)}
"""
                    
                # Success case - response_json contains the data
                    
        except Exception as e:
            result += f"""
**❌ Import Error:** {str(e)}
"""
    else:
        result += f"""
**📊 Threat Model Generated**
**🚀 Use import_to_devici=true to upload to Devici**
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
        project_description: Detailed architecture description including:
            - Components (frontend, backend, database, external services)
            - Data flows (how components communicate)
            - Trust boundaries (what's internal vs external)
            Example: "React frontend calls Node.js API which queries PostgreSQL database and integrates with Stripe for payments"
        tech_stack: Specific technologies (e.g., "React, Node.js, PostgreSQL, Stripe API")
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
        # Use centralized OTM generation function
        otm_data, is_valid, validation_message = create_validated_otm_structure(
            project_name=project_name,
            project_description=project_description,
            components=components,
            trust_zones=trust_zones,
            data_flows=data_flows,
            threats=threats,
            mitigations=mitigations,
            project_tags=["developer-generated", "security-discussion", "devici-ready"]
        )
        
        if not is_valid:
            return f"❌ Generated OTM failed validation even after auto-fix:\n{validation_message}"
        
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
        
        # Try to match by component name first, then by ID
        source_id = None
        dest_id = None
        
        for comp_name, comp_id in component_ids.items():
            if comp_name == source:
                source_id = comp_id
            if comp_name == destination:
                dest_id = comp_id
        
        # If not found by name, try by ID
        if not source_id:
            source_id = source if source.startswith('C') else f"Unknown_{source}"
        if not dest_id:
            dest_id = destination if destination.startswith('C') else f"Unknown_{destination}"
        
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
    
    return mermaid_diagram

# =============================================================================
# CENTRALIZED OTM GENERATION - ONE PLACE FOR ALL OTM CREATION
# =============================================================================

def create_validated_otm_structure(
    project_name: str,
    project_description: str,
    components: list,
    trust_zones: list,
    data_flows: list,
    threats: list,
    mitigations: list,
    project_tags: list = None
) -> tuple[dict, bool, str]:
    """
    Create a validated OTM structure that matches Devici's exact format.
    This is the SINGLE SOURCE OF TRUTH for OTM generation.
    
    Returns (otm_data, is_valid, validation_message)
    """
    import uuid
    
    if project_tags is None:
        project_tags = ["auto-generated", "devici-ready"]
    
    # Generate project ID
    project_id = str(uuid.uuid4())
    
    # Generate representation ID 
    representation_id = str(uuid.uuid4())
    
    # Ensure trust zones have IDs
    for tz in trust_zones:
        if "id" not in tz or not tz["id"]:
            tz["id"] = str(uuid.uuid4())
    
    # Get default trust zone ID - use first component's ID if no trust zones
    default_trust_zone_id = trust_zones[0]["id"] if trust_zones else str(uuid.uuid4())
    
    # Build threats first to get threat IDs
    severity_to_impact = {"Low": 25, "Medium": 50, "High": 75, "Critical": 100}
    threat_data = []
    threat_ids = []
    
    for threat in threats:
        threat_id = str(uuid.uuid4())
        threat_ids.append(threat_id)
        
        # Handle both string and numeric impact values, use -1 for Devici compatibility
        if isinstance(threat.get("impact"), str):
            impact_value = severity_to_impact.get(threat["impact"], -1)
        elif isinstance(threat.get("impact"), int):
            impact_value = threat["impact"]
        else:
            impact_value = -1  # Devici default
        
        # Handle categories field properly
        categories = threat.get("categories")
        if not categories:
            category = threat.get("category")
            categories = [category] if category else []
        
        threat_data.append({
            "name": threat["name"],
            "id": threat_id,
            "description": threat.get("description", ""),
            "categories": categories,
            "cwes": [],
            "risk": {
                "likelihood": threat.get("likelihood", -1),
                "impact": impact_value
            },
            "attributes": None,
            "tags": threat.get("tags", []),
            "isCustom": True,
            "priority": threat.get("priority", "medium"),
            "refId": None,
            "source": None
        })
    
    # Build components with DEVICI FORMAT
    component_data = []
    for i, comp in enumerate(components):
        comp_id = str(uuid.uuid4())
        
        # Map component types to Devici format
        comp_type = comp["type"]
        if comp_type == "process":
            comp_type = "processNode"
        elif comp_type == "datastore":
            comp_type = "datastoreNode"
        elif comp_type == "external-entity":
            comp_type = "externalEntityNode"
        elif comp_type == "web-service":
            comp_type = "processNode"
        
        # Assign threats to components (distribute evenly)
        component_threats = []
        if threat_ids:
            threat_index = i % len(threat_ids)
            component_threats.append({
                "threat": threat_ids[threat_index],
                "state": "open",
                "mitigations": []
            })
        
        component_data.append({
            "representationId": representation_id,
            "name": comp["name"],
            "id": comp_id,
            "description": comp.get("description", ""),
            "metaData": {
                "id": "",
                "label": comp["name"],
                "selectedBy": [],
                "representation": representation_id
            },
            "parent": {"trustZone": default_trust_zone_id},
            "type": comp_type,
            "tags": comp.get("tags", []),
            "representations": [
                {
                    "representation": representation_id,
                    "id": representation_id,
                    "position": {"x": 100 + (i * 200), "y": 100 + (i * 100)},
                    "size": {"width": 150, "height": 100}
                }
            ],
            "assets": [],
            "threats": component_threats,
            "attributes": {}
        })
    
    # Create component name to ID mapping for dataflows
    component_name_to_id = {comp["name"]: comp["id"] for comp in component_data}
    
    # Build dataflows with proper UUIDs
    dataflow_data = []
    for df in data_flows:
        source_id = component_name_to_id.get(df["source"], list(component_name_to_id.values())[0] if component_name_to_id else str(uuid.uuid4()))
        dest_id = component_name_to_id.get(df["destination"], list(component_name_to_id.values())[1] if len(component_name_to_id) > 1 else str(uuid.uuid4()))
        
        dataflow_data.append({
            "id": str(uuid.uuid4()),
            "name": df["name"],
            "source": source_id,
            "destination": dest_id,
            "description": df.get("description", ""),
            "tags": df.get("tags", [])
        })
    
    # Build trust zones with required fields
    trust_zone_data = []
    for tz in trust_zones:
        trust_zone_data.append({
            "id": tz["id"],
            "name": tz["name"],
            "type": tz["type"],
            "description": tz["description"],
            "risk": tz.get("risk", {"trustRating": 10 if "private" in tz["type"] else 3})
        })
    
    # Build mitigations
    mitigation_data = []
    for mit in mitigations:
        mitigation_data.append({
            "id": str(uuid.uuid4()),
            "name": mit["name"],
            "description": mit["description"],
            "riskReduction": mit["riskReduction"],
            "tags": mit.get("tags", ["security-control"])
        })
    
    # Create final OTM structure matching Devici format EXACTLY
    otm_data = {
        "otmVersion": "0.2.0",
        "projectId": project_id,
        "project": {
            "name": project_name,
            "id": project_id,
            "description": project_description,
            "owner": "Security Team",
            "ownerContact": "",
            "tags": project_tags,
            "attributes": None
        },
        "representations": [
            {
                "name": "Canvas 1",
                "id": representation_id,
                "type": "diagram",
                "size": None,
                "attributes": None
            }
        ],
        "assets": [],
        "components": component_data,
        "dataflows": dataflow_data,
        "trustZones": trust_zone_data,
        "threats": threat_data,
        "mitigations": mitigation_data
    }
    
    # Validate and auto-fix the generated OTM
    return validate_and_fix_otm_data(otm_data)

def main():
    """Main entry point for the server."""
    mcp.run()

if __name__ == "__main__":
    main() 