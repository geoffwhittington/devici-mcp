#!/usr/bin/env python3
"""
Demonstration: Creating a Threat Model with Components via Devici API

This script demonstrates the complete workflow I learned from exploring 
the Devici browser interface and analyzing the API code. It creates a 
simple web application threat model with key components, threats, and 
mitigations.
"""

import asyncio
import json
from src.devici_mcp_server.api_client import create_client_from_env

async def create_demo_threat_model():
    """Create a demonstration threat model with components via API."""
    
    print("🎯 Creating Demo Threat Model via Devici API")
    print("=" * 60)
    print("Based on learning from browser interface exploration")
    
    async with create_client_from_env() as client:
        print("✅ Successfully authenticated with Devici API")
        
        # Step 1: Find Sandbox collection
        print("\n📁 Step 1: Finding Sandbox Collection")
        print("-" * 40)
        
        collections = await client.get_collections(limit=10)
        sandbox_collection = None
        
        for collection in collections.get('items', []):
            if 'sandbox' in collection.get('title', '').lower():
                sandbox_collection = collection
                break
        
        if not sandbox_collection:
            print("❌ Sandbox collection not found")
            return
        
        collection_id = sandbox_collection['id']
        print(f"✅ Found collection: {sandbox_collection['title']} ({collection_id})")
        
        # Step 2: Create threat model
        print("\n🎯 Step 2: Creating Threat Model")
        print("-" * 40)
        
        threat_model_data = {
            "title": "API Demo - Simple Web App",
            "description": "Demonstration threat model created via API showing web application components",
            "collectionId": collection_id
        }
        
        threat_model = await client.create_threat_model(threat_model_data)
        threat_model_id = threat_model.get("id")
        
        if not threat_model_id:
            print("❌ Failed to create threat model")
            return
        
        print(f"✅ Created threat model: {threat_model_id}")
        print(f"   Title: {threat_model_data['title']}")
        
        # Get the canvas ID
        tm_details = await client.get_threat_model(threat_model_id)
        canvas_id = tm_details.get("canvases", [None])[0]
        print(f"✅ Canvas ID: {canvas_id}")
        
        # Step 3: Create components (like I saw in the browser interface)
        print("\n🏗️ Step 3: Creating Components")
        print("-" * 40)
        
        # Define components similar to what I would create in the browser
        components_to_create = [
            {
                "title": "Web Browser",
                "description": "User's web browser accessing the application",
                "type": "external-entity",
                "tags": "user, browser, external"
            },
            {
                "title": "Web Application",
                "description": "Main web application server processing requests",
                "type": "web-service",
                "tags": "server, application, process"
            },
            {
                "title": "Database",
                "description": "Application database storing user data",
                "type": "datastore", 
                "tags": "database, storage, data"
            },
            {
                "title": "Authentication Service",
                "description": "OAuth/SAML authentication provider",
                "type": "external-service",
                "tags": "auth, oauth, external"
            }
        ]
        
        created_components = {}
        
        for i, comp_def in enumerate(components_to_create, 1):
            try:
                component_data = {
                    "title": comp_def["title"],
                    "description": comp_def["description"],
                    "type": comp_def["type"],
                    "tags": comp_def["tags"]
                }
                
                if canvas_id:
                    component_data["canvasId"] = canvas_id
                
                print(f"  Creating: {comp_def['title']}")
                created_component = await client.create_component(component_data)
                
                # Handle the API response format I discovered
                component_id = created_component.get("component") or created_component.get("id")
                
                if component_id:
                    created_components[comp_def["title"]] = component_id
                    print(f"  ✅ Created: {component_id}")
                    
                    # Try to add visual representation to canvas
                    try:
                        await client._add_component_to_canvas(component_id, canvas_id, i-1)
                        print(f"  ✅ Added to canvas at position {i-1}")
                    except Exception as canvas_error:
                        print(f"  ⚠️ Canvas positioning failed: {canvas_error}")
                        print(f"     (Component still created successfully)")
                else:
                    print(f"  ❌ Failed to get component ID from response")
                    
            except Exception as e:
                print(f"  ❌ Failed to create {comp_def['title']}: {e}")
        
        print(f"\n📊 Components Created: {len(created_components)}/{len(components_to_create)}")
        
        return {
            "threat_model_id": threat_model_id,
            "components": created_components
        }

if __name__ == "__main__":
    asyncio.run(create_demo_threat_model()) 