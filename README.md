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

### 1. Software Developer Starting Threat Model
**Scenario:** You're building a new e-commerce app and need to start security discussions with your team.

```
create_developer_threat_model(
    "E-commerce Platform",
    "React frontend with Node.js API, PostgreSQL database, and Stripe payments",
    "React, Node.js, PostgreSQL, Stripe"
)
```

**Result:** 
- Creates complete threat model with components and STRIDE threats
- Returns instant clickable Devici URLs
- Ready to share with security team

### 2. Security Team Reviewing Microservices
**Scenario:** Security team needs to assess a complex microservices architecture.

```
create_otm_from_description(
    "Kubernetes microservices with API Gateway, Redis cache, and MongoDB",
    "Docker, Kubernetes, Redis, MongoDB, Nginx"
)
```

**Result:**
- Generates detailed OTM file with all components
- Maps security boundaries and data flows
- Identifies key threat vectors

### 3. DevOps Creating Infrastructure Threat Model
**Scenario:** Need to model cloud infrastructure for compliance audit.

```
create_complete_threat_model_with_components(
    "AWS Production Infrastructure",
    "Infrastructure",
    "load balancer, web servers, database cluster, S3 storage"
)
```

**Result:**
- Visual components on Devici canvas
- Infrastructure-specific threats
- Compliance-ready documentation

### 4. Team Lead Importing Existing Analysis
**Scenario:** You have an existing OTM file from another tool and want to import it.

```
import_otm_to_devici("my-analysis.otm", "Security Reviews")
```

**Result:**
- Imports all components, threats, and mitigations
- Places in specified collection
- Provides direct URLs for team access

### 5. Developer Getting Project Overview
**Scenario:** New team member needs to understand existing threat models.

```
show_my_threat_models("Web Applications")
```

**Result:**
- Lists all threat models in collection
- Shows creation dates and owners
- Quick access to relevant models

### 6. Security Engineer Adding Specific Threats
**Scenario:** Need to add custom threats to existing components.

```
create_threat_for_component(
    "SQL Injection via User Input",
    "component-id-123",
    "Unvalidated user input could allow SQL injection attacks",
    "high",
    "Tampering"
)
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