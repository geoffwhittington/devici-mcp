# Devici MCP Server

A Model Context Protocol (MCP) server for threat modeling with Devici. Generate threat models from code and get instant clickable URLs for team collaboration.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Quick Install

```bash
uvx git+https://github.com/geoffwhittington/devici-mcp.git
```

## Configuration

Get your API credentials from Devici: **Settings** > **API Access**

Set environment variables:
```bash
export DEVICI_API_BASE_URL="https://api.devici.com/v1"
export DEVICI_CLIENT_ID="your-client-id-here"
export DEVICI_CLIENT_SECRET="your-client-secret-here"
```

## MCP Client Setup

### Claude Desktop
Add to `~/.config/claude-desktop/claude_desktop_config.json`:
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

### Cursor
Same configuration in Cursor MCP settings.

## Real Use Cases

### 1. **PRIMARY USE CASE: Analyze Current Project**
**Scenario:** You're working on a project and want to generate a threat model from your actual codebase.

**Ask your AI assistant:**
```
"Analyze my current project and create a threat model in Devici. I want URLs to share with my team."
```

**What it does:**
- Scans your project files (package.json, requirements.txt, etc.)
- Detects technologies (React, Node.js, Python, databases)
- Identifies architecture patterns (frontend, backend, database, APIs)
- Generates components, data flows, and STRIDE threats
- Creates threat model in Devici with instant URLs

**Result:**
- Complete threat model based on your actual code
- Clickable Devici URLs for immediate team access
- Architecture diagram with detected components
- STRIDE threats specific to your tech stack

### 2. **Create OTM File for Local Review**
**Scenario:** You want to generate a threat model from your project but review it locally before importing to Devici.

**Ask your AI assistant:**
```
"Create an OTM file from my current project for local review."
```

**What it does:**
- Scans your project files and detects architecture
- Generates complete OTM file with components, threats, and mitigations
- Saves file locally (e.g., `my-project-devici-ready.otm`)
- Validates against OTM schema

**Result:**
- Local OTM file ready for review
- Can be opened with text editor or OTM viewers
- Ready for import to Devici when approved

### 3. **Import Reviewed OTM File**
**Scenario:** You've reviewed your OTM file locally and want to import it to Devici.

**Ask your AI assistant:**
```
"Import my reviewed OTM file 'my-project-devici-ready.otm' to the 'Security Reviews' collection."
```

**Result:**
- Imports your reviewed OTM file to Devici
- Creates threat model with all components and threats
- Provides instant clickable URLs for team access

### 4. **Visualize OTM File as Diagram**
**Scenario:** You have an OTM file and want to see a visual diagram before importing to Devici.

**Ask your AI assistant:**
```
"Show me a Mermaid diagram of my OTM file 'my-project-devici-ready.otm'."
```

**What it does:**
- Reads your OTM file and extracts components, data flows, and trust zones
- Generates a Mermaid diagram showing architecture
- Color-codes different component types (web apps, databases, external services)
- Shows data flows between components
- Provides threat summary by category

**Result:**
- Interactive Mermaid diagram of your threat model
- Visual verification of architecture before import
- Clear overview of components and relationships

### 5. Software Developer Starting Fresh Threat Model
**Scenario:** You're building a new e-commerce app and need to start security discussions with your team.

**Ask your AI assistant:**
```
"Create a threat model for my e-commerce platform. It's a React frontend with Node.js API, PostgreSQL database, and Stripe payments. I need URLs to share with my security team."
```

**Result:** 
- Creates complete threat model with components and STRIDE threats
- Returns instant clickable Devici URLs
- Ready to share with security team

### 6. Security Team Reviewing Microservices
**Scenario:** Security team needs to assess a complex microservices architecture.

**Ask your AI assistant:**
```
"Generate a threat model for our Kubernetes microservices architecture. We have an API Gateway, Redis cache, and MongoDB. Tech stack includes Docker, Kubernetes, Redis, MongoDB, and Nginx."
```

**Result:**
- Generates detailed OTM file with all components
- Maps security boundaries and data flows
- Identifies key threat vectors

### 7. DevOps Creating Infrastructure Threat Model
**Scenario:** Need to model cloud infrastructure for compliance audit.

**Ask your AI assistant:**
```
"Create a threat model for our AWS production infrastructure. Include load balancer, web servers, database cluster, and S3 storage."
```

**Result:**
- Visual components on Devici canvas
- Infrastructure-specific threats
- Compliance-ready documentation

### 8. Team Lead Importing Existing Analysis
**Scenario:** You have an existing OTM file from another tool and want to import it.

**Ask your AI assistant:**
```
"Import my existing threat model file 'my-analysis.otm' into the 'Security Reviews' collection in Devici."
```

**Result:**
- Imports all components, threats, and mitigations
- Places in specified collection
- Provides direct URLs for team access

### 9. Developer Getting Project Overview
**Scenario:** New team member needs to understand existing threat models.

**Ask your AI assistant:**
```
"Show me all threat models in the 'Web Applications' collection."
```

**Result:**
- Lists all threat models in collection
- Shows creation dates and owners
- Quick access to relevant models

### 10. Security Engineer Adding Specific Threats
**Scenario:** Need to add custom threats to existing components.

**Ask your AI assistant:**
```
"Add a high-priority SQL injection threat to the user input component. It should be categorized as Tampering in STRIDE."
```

**Result:**
- Adds threat linked to specific component
- Categorized with STRIDE methodology
- Prioritized for remediation

## Key Features

- **Instant URLs:** Get clickable Devici links for immediate team sharing
- **Code Analysis:** Generate threat models from project descriptions
- **STRIDE Integration:** Automatic threat categorization
- **OTM Support:** Full Open Threat Model standard compliance
- **Team Collaboration:** Built for developer → security team workflows