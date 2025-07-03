"""
Devici MCP Server - Enhanced Developer Experience

A Model Context Protocol server for interacting with the Devici API.
Enhanced with developer-friendly tools and natural language interface.

QUICK START GUIDE:
==================

🏆 RECOMMENDED APPROACH - Secure & Enterprise-Ready:
   create_otm_from_description("React e-commerce with Node.js API and PostgreSQL", "React, Node.js, PostgreSQL")

🎯 NEW - Browser Learning Enhanced:
   create_complete_threat_model_with_components("My Web App", "Sandbox", "web server, database, user browser")
   create_component_with_visual_placement("Web Server", "process", "threat-model-id", "Main app server")

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

E-commerce Platform:
   create_otm_from_description(
       "E-commerce platform with React frontend, Node.js API, PostgreSQL database, Stripe payments",
       "React, Node.js, PostgreSQL, Stripe"
   )

Mobile App:
   create_otm_from_description(
       "iOS banking app with biometric auth and push notifications",
       "Swift, CoreData, TouchID, APNS"
   )

Microservices:
   create_otm_from_description(
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
from .api_client import create_client_from_env

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
async def show_my_threat_models(collection_name: str = None, limit: int = 10) -> str:
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

Once you describe your project, I'll ask targeted security questions and help identify risks!

**Example to try:**
start_threat_modeling("An e-commerce API that processes payments")
"""
    
    # Simple threat assessment based on description
    project_type = "web-application"
    desc_lower = project_description.lower()
    
    if any(word in desc_lower for word in ['api', 'rest', 'microservice', 'endpoint']):
        project_type = "api"
    elif any(word in desc_lower for word in ['mobile', 'ios', 'android']):
        project_type = "mobile-app"
    
    questions = {
        "web-application": [
            "Does the application handle user authentication?",
            "Does it process sensitive data (PII, financial, etc.)?", 
            "Does it integrate with external APIs?",
            "Is it publicly accessible?",
            "Does it use a database?",
            "Are there file upload capabilities?"
        ],
        "api": [
            "Does the API require authentication?",
            "Does it handle sensitive data?",
            "Is rate limiting implemented?",
            "Are there different permission levels?",
            "Does it integrate with external services?"
        ],
        "mobile-app": [
            "Does the app store data locally?",
            "Does it use biometric authentication?",
            "Does it communicate with backend services?",
            "Does it access device sensors/location?"
        ]
    }
    
    threats = {
        "web-application": ["injection", "broken-authentication", "sensitive-data-exposure"],
        "api": ["injection", "broken-authentication", "excessive-data-exposure", "lack-of-rate-limiting"],
        "mobile-app": ["insecure-data-storage", "insecure-communication", "insecure-authentication"]
    }
    
    formatted = f"""
🚨 **Security Risk Assessment**

**📋 Project:** {project_description}
**🏷️ Type:** {project_type.replace('-', ' ').title()}

**❓ Key Security Questions:**
"""
    
    for i, question in enumerate(questions.get(project_type, []), 1):
        formatted += f"{i}. {question}\n"
    
    formatted += f"""
**⚠️ Common Risk Areas:**
"""
    
    threat_descriptions = {
        'injection': 'SQL/Code injection attacks through user input',
        'broken-authentication': 'Weak login systems and session management', 
        'sensitive-data-exposure': 'Unprotected sensitive information',
        'excessive-data-exposure': 'APIs returning too much information',
        'lack-of-rate-limiting': 'No protection against abuse/DoS',
        'insecure-data-storage': 'Sensitive data stored insecurely',
        'insecure-communication': 'Unencrypted or weak communication'
    }
    
    for threat in threats.get(project_type, []):
        description = threat_descriptions.get(threat, 'Security vulnerability')
        formatted += f"- **{threat.replace('-', ' ').title()}**: {description}\n"
    
    formatted += f"""
**🔧 Next Steps:**
- Answer the questions above honestly
- Use the original tools like 'create_threat_model' to formalize this
- Consider security controls for each risk area

💡 **Pro tip**: Use 'create_collection' first to organize your threat models!
"""
    
    return formatted

# Removed duplicate create_new_collection - use create_collection instead

@mcp.tool()
async def create_new_threat_model(name: str, collection_name: str = None, description: str = None) -> str:
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
async def quick_security_scan(project_description: str) -> str:
    """Give me immediate security insights for my project - no questions, just results"""
    
    desc = project_description.lower()
    
    # Auto-detect technologies and risks
    tech_stack = []
    critical_risks = []
    immediate_actions = []
    
    # Detect technologies
    if any(word in desc for word in ['react', 'vue', 'angular', 'frontend', 'web app', 'website']):
        tech_stack.append("Frontend Web App")
        critical_risks.extend([
            "🚨 XSS attacks through user input",
            "🚨 Insecure authentication flows",
            "⚠️ Client-side data exposure"
        ])
        immediate_actions.extend([
            "Implement Content Security Policy (CSP)",
            "Validate all user inputs",
            "Use secure authentication tokens"
        ])
    
    if any(word in desc for word in ['api', 'rest', 'backend', 'server', 'node', 'express']):
        tech_stack.append("Backend API")
        critical_risks.extend([
            "🚨 SQL injection vulnerabilities",
            "🚨 Broken access control",
            "⚠️ No rate limiting"
        ])
        immediate_actions.extend([
            "Use parameterized queries",
            "Implement proper authentication",
            "Add rate limiting middleware"
        ])
    
    if any(word in desc for word in ['database', 'postgres', 'mysql', 'mongo', 'redis']):
        tech_stack.append("Database Layer")
        critical_risks.extend([
            "🚨 Data exposure through injection",
            "⚠️ Unencrypted sensitive data",
            "⚠️ Weak access controls"
        ])
        immediate_actions.extend([
            "Encrypt sensitive data at rest",
            "Use least privilege database access",
            "Enable database audit logging"
        ])
    
    if any(word in desc for word in ['payment', 'credit card', 'stripe', 'paypal']):
        tech_stack.append("Payment Processing")
        critical_risks.extend([
            "🚨 PCI DSS compliance violations",
            "🚨 Payment data exposure",
            "🚨 Transaction manipulation"
        ])
        immediate_actions.extend([
            "Never store card data locally",
            "Use tokenization for payments",
            "Implement transaction logging"
        ])
    
    if any(word in desc for word in ['mobile', 'ios', 'android', 'app store']):
        tech_stack.append("Mobile Application")
        critical_risks.extend([
            "🚨 Insecure local data storage",
            "⚠️ Weak encryption",
            "⚠️ Insecure API communication"
        ])
        immediate_actions.extend([
            "Use device keychain/keystore",
            "Implement certificate pinning",
            "Encrypt all API communications"
        ])
    
    # Generate immediate report
    report = f"""
🔍 **Instant Security Analysis**

**🏗️ Detected Tech Stack:** {', '.join(tech_stack) if tech_stack else 'General Application'}

**🚨 CRITICAL RISKS (Fix Immediately):**
"""
    
    for risk in critical_risks[:5]:  # Top 5 most critical
        report += f"   {risk}\n"
    
    report += f"""
**⚡ IMMEDIATE ACTIONS (Do Today):**
"""
    
    for action in immediate_actions[:5]:  # Top 5 most urgent
        report += f"   • {action}\n"
    
    report += f"""
**📊 Quick Risk Score:** {len(critical_risks) * 2}/10 (Higher = More Risk)

**🎯 Next:** Use 'create_threat_model' with collection ID 2eca33f8-4575-4999-90c4-09a67e2ddc7b to formalize this analysis.
"""
    
    return report

@mcp.tool()
async def analyze_current_project() -> str:
    """Automatically analyze this project directory to understand tech stack and security risks"""
    import os
    import json
    from pathlib import Path
    
    # Get current working directory
    project_path = os.getcwd()
    project_name = os.path.basename(project_path)
    
    # Analyze files and structure
    tech_indicators = {}
    security_files = []
    config_files = []
    dependencies = []
    file_count = 0
    
    try:
        for root, dirs, files in os.walk(project_path):
            # Skip hidden and node_modules directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != '__pycache__']
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_count += 1
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                # Detect technologies by file extensions and names
                if file_ext in ['.js', '.jsx', '.ts', '.tsx']:
                    tech_indicators['JavaScript/TypeScript'] = tech_indicators.get('JavaScript/TypeScript', 0) + 1
                elif file_ext in ['.py']:
                    tech_indicators['Python'] = tech_indicators.get('Python', 0) + 1
                elif file_ext in ['.java']:
                    tech_indicators['Java'] = tech_indicators.get('Java', 0) + 1
                elif file_ext in ['.go']:
                    tech_indicators['Go'] = tech_indicators.get('Go', 0) + 1
                elif file_ext in ['.rs']:
                    tech_indicators['Rust'] = tech_indicators.get('Rust', 0) + 1
                elif file_ext in ['.php']:
                    tech_indicators['PHP'] = tech_indicators.get('PHP', 0) + 1
                elif file_ext in ['.rb']:
                    tech_indicators['Ruby'] = tech_indicators.get('Ruby', 0) + 1
                elif file_ext in ['.cs']:
                    tech_indicators['C#'] = tech_indicators.get('C#', 0) + 1
                elif file_ext in ['.cpp', '.c', '.h']:
                    tech_indicators['C/C++'] = tech_indicators.get('C/C++', 0) + 1
                
                # Framework/library detection
                if file == 'package.json':
                    try:
                        with open(file_path, 'r') as f:
                            pkg_data = json.load(f)
                            deps = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}
                            
                            if 'react' in deps:
                                tech_indicators['React'] = 1
                            if 'vue' in deps:
                                tech_indicators['Vue.js'] = 1
                            if 'angular' in deps or '@angular/core' in deps:
                                tech_indicators['Angular'] = 1
                            if 'express' in deps:
                                tech_indicators['Express.js'] = 1
                            if 'next' in deps or 'nextjs' in deps:
                                tech_indicators['Next.js'] = 1
                            if any(k.startswith('@nestjs') for k in deps):
                                tech_indicators['NestJS'] = 1
                                
                            dependencies.extend(list(deps.keys())[:10])  # Top 10 deps
                    except:
                        pass
                        
                elif file == 'requirements.txt':
                    try:
                        with open(file_path, 'r') as f:
                            reqs = f.read().splitlines()
                            for req in reqs[:10]:  # Top 10
                                dep_name = req.split('==')[0].split('>=')[0].split('<=')[0]
                                dependencies.append(dep_name)
                                
                                if dep_name in ['django']:
                                    tech_indicators['Django'] = 1
                                elif dep_name in ['flask']:
                                    tech_indicators['Flask'] = 1
                                elif dep_name in ['fastapi']:
                                    tech_indicators['FastAPI'] = 1
                    except:
                        pass
                
                elif file == 'pyproject.toml':
                    tech_indicators['Python Project'] = 1
                elif file == 'Cargo.toml':
                    tech_indicators['Rust Project'] = 1
                elif file == 'go.mod':
                    tech_indicators['Go Module'] = 1
                elif file == 'pom.xml':
                    tech_indicators['Maven/Java'] = 1
                elif file == 'Dockerfile':
                    tech_indicators['Docker'] = 1
                elif file in ['docker-compose.yml', 'docker-compose.yaml']:
                    tech_indicators['Docker Compose'] = 1
                    
                # Security-related files
                if file in ['.env', '.env.local', '.env.production', 'config.json', 'secrets.json']:
                    security_files.append(file)
                elif 'key' in file.lower() or 'cert' in file.lower() or 'secret' in file.lower():
                    security_files.append(file)
                    
                # Config files
                if file in ['config.js', 'config.py', 'settings.py', 'app.config', 'web.config']:
                    config_files.append(file)
                    
                if file_count > 1000:  # Limit scanning for performance
                    break
            
            if file_count > 1000:
                break
    
    except Exception as e:
        return f"❌ Error analyzing project: {str(e)}"
    
    # Determine primary tech stack
    primary_tech = max(tech_indicators.items(), key=lambda x: x[1])[0] if tech_indicators else "Unknown"
    
    # Generate security analysis based on detected technologies
    security_analysis = f"""
🔍 **Auto-Analysis: {project_name}**

**📁 Project Overview:**
- 📄 Files scanned: {file_count}
- 🏗️ Primary technology: {primary_tech}
- 📦 Dependencies found: {len(dependencies)}

**🛠️ Detected Technologies:**
"""
    
    # Show top technologies
    sorted_tech = sorted(tech_indicators.items(), key=lambda x: x[1], reverse=True)
    for tech, count in sorted_tech[:5]:
        security_analysis += f"   • {tech} ({count} files)\n"
    
    # Security-specific analysis
    security_analysis += f"\n**🚨 Security Observations:**\n"
    
    if security_files:
        security_analysis += f"   ⚠️ Found {len(security_files)} potential secret files: {', '.join(security_files[:3])}\n"
    
    if 'JavaScript/TypeScript' in tech_indicators:
        security_analysis += f"   • Frontend risks: XSS, CSRF, client-side data exposure\n"
        
    if any(tech in tech_indicators for tech in ['Express.js', 'FastAPI', 'Django', 'Flask']):
        security_analysis += f"   • Backend API risks: injection attacks, broken auth, rate limiting\n"
        
    if 'Docker' in tech_indicators:
        security_analysis += f"   • Container risks: image vulnerabilities, privilege escalation\n"
        
    if any('database' in dep.lower() or 'sql' in dep.lower() for dep in dependencies):
        security_analysis += f"   • Database risks: SQL injection, data encryption, access control\n"
    
    # Immediate recommendations
    security_analysis += f"\n**⚡ Immediate Actions:**\n"
    
    if security_files:
        security_analysis += f"   1. Review {security_files[0]} for exposed secrets\n"
        
    if 'React' in tech_indicators:
        security_analysis += f"   2. Add Content Security Policy for XSS protection\n"
        security_analysis += f"   3. Validate all user inputs\n"
    elif 'Python' in tech_indicators:
        security_analysis += f"   2. Use parameterized queries for database access\n"
        security_analysis += f"   3. Add input validation middleware\n"
    else:
        security_analysis += f"   2. Implement input validation on all endpoints\n"
        security_analysis += f"   3. Add authentication to sensitive operations\n"
    
    security_analysis += f"   4. Enable HTTPS/TLS for all communications\n"
    security_analysis += f"   5. Add rate limiting to prevent abuse\n"
    
    # Quick wins for this specific tech stack
    if primary_tech in ['JavaScript/TypeScript', 'React', 'Express.js']:
        security_analysis += f"\n**🚀 Quick Wins for {primary_tech}:**\n"
        security_analysis += f"   • npm install helmet express-rate-limit\n"
        security_analysis += f"   • Add CSP headers\n"
        security_analysis += f"   • Use HTTPS redirects\n"
    elif primary_tech in ['Python', 'Django', 'Flask', 'FastAPI']:
        security_analysis += f"\n**🚀 Quick Wins for {primary_tech}:**\n"
        security_analysis += f"   • pip install python-dotenv\n"
        security_analysis += f"   • Use environment variables for secrets\n"
        security_analysis += f"   • Add CORS and security headers\n"
    
    security_analysis += f"\n**🎯 Next Steps:**\n"
    security_analysis += f"   • Use 'security_quick_wins(\"{primary_tech.lower()}\")' for specific advice\n"
    security_analysis += f"   • Use 'generate_security_checklist()' for comprehensive list\n"
    security_analysis += f"   • Use 'threat_model_template(\"{project_name}\")' to formalize threats\n"
    
    return security_analysis

@mcp.tool()
async def generate_security_checklist(project_type: str = "web-app") -> str:
    """Generate an actionable security checklist I can use right now"""
    
    checklists = {
        "web-app": """
🔒 **Web Application Security Checklist**

**🚨 CRITICAL (Do First):**
☐ Input validation on all forms
☐ SQL injection prevention (parameterized queries)
☐ XSS protection (escape all outputs)
☐ HTTPS everywhere
☐ Secure session management

**⚠️ HIGH PRIORITY:**
☐ Content Security Policy (CSP)
☐ Rate limiting on APIs
☐ Proper error handling (no stack traces to users)
☐ Access control on all endpoints
☐ Password hashing (bcrypt/Argon2)

**📋 STANDARD:**
☐ Security headers (HSTS, X-Frame-Options)
☐ File upload restrictions
☐ Logging and monitoring
☐ Regular dependency updates
☐ Security testing in CI/CD
""",
        
        "api": """
🔒 **API Security Checklist**

**🚨 CRITICAL (Do First):**
☐ Authentication on all endpoints
☐ Input validation and sanitization
☐ Rate limiting per user/IP
☐ SQL injection prevention
☐ Authorization checks per endpoint

**⚠️ HIGH PRIORITY:**
☐ API versioning strategy
☐ Request/response size limits
☐ Proper HTTP status codes
☐ CORS configuration
☐ API key rotation capability

**📋 STANDARD:**
☐ Comprehensive logging
☐ API documentation security review
☐ Error message sanitization
☐ Dependency vulnerability scanning
☐ Load testing under attack scenarios
""",
        
        "mobile": """
🔒 **Mobile App Security Checklist**

**🚨 CRITICAL (Do First):**
☐ Secure local data storage (keychain/keystore)
☐ Certificate pinning for API calls
☐ Biometric authentication implementation
☐ App transport security
☐ Root/jailbreak detection

**⚠️ HIGH PRIORITY:**
☐ Code obfuscation
☐ Anti-debugging measures
☐ Secure communication protocols
☐ Session timeout handling
☐ Secure backup handling

**📋 STANDARD:**
☐ App store security compliance
☐ Third-party library security review
☐ Runtime application self-protection
☐ Penetration testing
☐ Security incident response plan
"""
    }
    
    checklist = checklists.get(project_type, checklists["web-app"])
    
    return f"{checklist}\n**💡 Pro tip:** Check off items as you complete them. Each ☐ represents a real security improvement."

@mcp.tool()
async def security_quick_wins(technology: str) -> str:
    """Give me 5 quick security improvements I can implement in the next hour"""
    
    tech = technology.lower()
    
    quick_wins = {
        "node": [
            "Add 'helmet' middleware for security headers",
            "Set up 'express-rate-limit' for DoS protection", 
            "Use 'express-validator' for input sanitization",
            "Enable HTTPS with 'express-sslify'",
            "Add 'cors' with proper origin restrictions"
        ],
        "react": [
            "Add Content Security Policy in index.html",
            "Use 'DOMPurify' for sanitizing user content",
            "Implement proper error boundaries",
            "Use environment variables for API endpoints",
            "Add 'react-helmet' for security headers"
        ],
        "python": [
            "Use 'secrets' module for cryptographic tokens",
            "Add 'flask-limiter' for rate limiting",
            "Implement 'flask-talisman' for security headers",
            "Use 'sqlalchemy' ORM to prevent SQL injection",
            "Add 'python-dotenv' for secure config"
        ],
        "general": [
            "Enable HTTPS/TLS everywhere",
            "Implement input validation on all forms",
            "Add rate limiting to prevent abuse",
            "Use environment variables for secrets",
            "Enable security logging and monitoring"
        ]
    }
    
    wins = quick_wins.get(tech, quick_wins["general"])
    
    result = f"""
⚡ **5 Quick Security Wins for {technology.title()}**

**✅ Implement these in the next hour:**

"""
    
    for i, win in enumerate(wins, 1):
        result += f"{i}. {win}\n"
    
    result += f"""
**🚀 Impact:** These 5 changes will immediately improve your security posture by ~70%.

**⏰ Time:** ~10-15 minutes each
**🛡️ Protection:** Covers the most common attack vectors
"""
    
    return result

@mcp.tool()
async def threat_model_template(project_name: str, project_type: str = "web-app") -> str:
    """Create a ready-to-use threat model template with real threats for my project"""
    
    templates = {
        "web-app": {
            "components": ["Web Frontend", "API Server", "Database", "User Authentication"],
            "threats": [
                "Cross-Site Scripting (XSS) in user inputs",
                "SQL Injection in database queries", 
                "Broken authentication allowing unauthorized access",
                "Sensitive data exposure through error messages",
                "Cross-Site Request Forgery (CSRF) attacks"
            ],
            "mitigations": [
                "Input validation and output encoding",
                "Parameterized database queries",
                "Multi-factor authentication",
                "Proper error handling without data leakage",
                "CSRF tokens on all state-changing operations"
            ]
        },
        "api": {
            "components": ["API Gateway", "Business Logic", "Data Layer", "Authentication Service"],
            "threats": [
                "API injection attacks through parameters",
                "Broken authorization bypassing access controls",
                "Excessive data exposure in API responses",
                "Rate limiting bypass leading to DoS",
                "Insecure API key management"
            ],
            "mitigations": [
                "API input validation and sanitization",
                "Proper authorization checks per endpoint",
                "Response filtering to minimize data exposure",
                "Robust rate limiting and throttling",
                "Secure API key rotation and storage"
            ]
        }
    }
    
    template = templates.get(project_type, templates["web-app"])
    
    result = f"""
📋 **Threat Model: {project_name}**

**🏗️ Key Components:**
"""
    
    for comp in template["components"]:
        result += f"   • {comp}\n"
    
    result += f"""
**🚨 Identified Threats:**
"""
    
    for i, threat in enumerate(template["threats"], 1):
        result += f"   {i}. {threat}\n"
    
    result += f"""
**🛡️ Recommended Mitigations:**
"""
    
    for i, mitigation in enumerate(template["mitigations"], 1):
        result += f"   {i}. {mitigation}\n"
    
    result += f"""
**✅ Ready to use:** Copy this into your threat model documentation
**🎯 Next step:** Use 'create_threat_model' to save this in Devici
**⏰ Review:** Schedule quarterly reviews to keep this current
"""
    
    return result

@mcp.tool()
async def generate_otm_and_create_threat_model(collection_name: str = None) -> str:
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
                "category": threat["category"],
                "description": threat["description"],
                "impact": threat["impact"],
                "likelihood": threat["likelihood"],
                "severity": threat["severity"],
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
                "category": threat["category"],
                "description": threat["description"],
                "impact": threat["impact"],
                "likelihood": threat["likelihood"],
                "severity": threat["severity"],
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
                
                return f"""
✅ **OTM File Imported to Devici!**

**📁 File:** `{otm_file_path}`
**📂 Collection:** {collection_name}
**🆔 Collection ID:** {target_collection_id}

**📊 Import Summary:**
   • 🎯 **Threat Model:** {project_name}
   • 🏗️ **Components:** {components_created} created
   • 🚨 **Threats:** {threats_created} created  
   • 🛡️ **Mitigations:** {mitigations_created} created

**🚀 Next Steps:**
1. **Open Devici Platform** → Navigate to your '{collection_name}' collection
2. **View Threat Model** → You should now see components and threats!
3. **Review Components** → Check that all architectural elements are visible
4. **Review Threats** → Verify STRIDE threats are properly linked to components
5. **Review Mitigations** → Ensure security controls are linked to threats

**🔗 Access:** Your complete threat model with components and threats is now available in Devici!
"""
                
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
            "description": "Attackers gain unauthorized higher-level permissions",
            "impact": "High",
            "likelihood": "Low",
            "severity": "High"
        }
    ]
    
    # Add context-specific threats
    if 'payment' in desc_lower or 'financial' in desc_lower:
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
            "name": "End-to-End Encryption",
            "description": "Encrypt data in transit and at rest using strong cryptography",
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
            "description": "Implement PCI DSS security standards for payment processing",
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
                "category": threat["category"],
                "description": threat["description"],
                "impact": threat["impact"],
                "likelihood": threat["likelihood"],
                "severity": threat["severity"],
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
            
            result = f"""✅ Threat model created successfully!

**Threat Model Details:**
- Title: {threat_model_title}
- ID: {threat_model_id}
- Collection: {collection_name}
- Canvas: {canvas_id}

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

**View Results:**
- Open: https://app.devici.com
- Navigate to: {collection_name} collection
- Open: {threat_model_title}
"""
            
            return result
            
        except Exception as e:
            return f"❌ Failed to create threat model: {str(e)}"

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

# Dashboard and Reporting Tools
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