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

def main():
    """Run the MCP server"""
    mcp.run()

