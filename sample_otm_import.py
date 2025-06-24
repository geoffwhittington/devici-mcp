#!/usr/bin/env python3
"""
Sample Code: OTM Import to Devici

This script demonstrates how to import an Open Threat Model (OTM) file 
into Devici using the MCP tools. It shows the complete process with 
detailed logging of what works and what doesn't.
"""

import asyncio
import json
import os
from src.devici_mcp_server.api_client import create_client_from_env

async def sample_otm_import():
    """Complete example of OTM import process with detailed logging."""
    
    print("🚀 OTM Import Sample - Step by Step")
    print("=" * 60)
    
    # Step 1: Show the OTM file structure
    otm_file = "./web-app-security-workflow.otm"
    
    print("📄 Step 1: Reading OTM File")
    print("-" * 30)
    
    with open(otm_file, 'r') as f:
        otm_content = json.load(f)
    
    print(f"File: {otm_file}")
    print(f"Project: {otm_content.get('project', {}).get('name', 'Unknown')}")
    print(f"Components: {len(otm_content.get('components', []))}")
    print(f"Threats: {len(otm_content.get('threats', []))}")
    print(f"Mitigations: {len(otm_content.get('mitigations', []))}")
    
    # Show component details
    print("\n📦 Components to Import:")
    for i, comp in enumerate(otm_content.get('components', []), 1):
        print(f"  {i}. {comp.get('name', 'Unnamed')}: {comp.get('description', 'No description')}")
    
    # Show threat details
    print("\n🚨 Threats to Import:")
    for i, threat in enumerate(otm_content.get('threats', []), 1):
        print(f"  {i}. {threat.get('name', 'Unnamed')}: {threat.get('description', 'No description')}")
    
    # Step 2: Connect to Devici API
    print(f"\n🔗 Step 2: Connecting to Devici API")
    print("-" * 30)
    
    async with create_client_from_env() as client:
        print("✅ Successfully authenticated with Devici")
        
        # Step 3: Find target collection
        print(f"\n📁 Step 3: Finding Target Collection")
        print("-" * 30)
        
        collections = await client.get_collections(limit=10)
        sandbox_collection = None
        
        for collection in collections.get('items', []):
            if collection.get('title', '').lower() == 'sandbox':
                sandbox_collection = collection
                break
        
        if sandbox_collection:
            collection_id = sandbox_collection['id']
            print(f"✅ Found Sandbox collection: {collection_id}")
        else:
            print("❌ Sandbox collection not found")
            return
        
        # Step 4: Create threat model
        print(f"\n🎯 Step 4: Creating Threat Model")
        print("-" * 30)
        
        project = otm_content.get("project", {})
        threat_model_data = {
            "title": project.get("name", "OTM Import Test"),
            "description": project.get("description", "Imported from OTM file"),
            "collectionId": collection_id
        }
        
        threat_model = await client.create_threat_model(threat_model_data)
        threat_model_id = threat_model.get("id")
        print(f"✅ Created threat model: {threat_model_id}")
        
        if not threat_model_id:
            print("❌ Failed to create threat model")
            return
        
        # Get canvas ID
        tm_details = await client.get_threat_model(threat_model_id)
        canvas_id = tm_details.get("canvases", [None])[0]
        print(f"✅ Canvas ID: {canvas_id}")
        
        # Step 5: Import Components
        print(f"\n🏗️ Step 5: Importing Components")
        print("-" * 30)
        
        component_mapping = {}
        components_created = 0
        
        for i, component in enumerate(otm_content.get("components", []), 1):
            try:
                component_data = {
                    "title": component.get("name", f"Component {i}"),
                    "description": component.get("description", ""),
                    "type": component.get("type", "generic"),
                }
                
                if canvas_id:
                    component_data["canvasId"] = canvas_id
                
                print(f"  Creating: {component_data['title']}")
                created_component = await client.create_component(component_data)
                component_id = created_component.get("component") or created_component.get("id")
                
                if component_id:
                    component_mapping[component.get("id")] = component_id
                    components_created += 1
                    print(f"  ✅ Created component: {component_id}")
                    
                    # Attempt to add to canvas (this is where it currently fails)
                    try:
                        await client._add_component_to_canvas(component_id, canvas_id, i-1)
                        print(f"  ✅ Added to canvas successfully")
                    except Exception as canvas_error:
                        print(f"  ⚠️ Canvas add failed: {canvas_error}")
                else:
                    print(f"  ❌ Failed to get component ID")
                    
            except Exception as e:
                print(f"  ❌ Component creation failed: {e}")
        
        print(f"\n📊 Components Summary: {components_created}/{len(otm_content.get('components', []))} created")
        
        # Step 6: Import Threats (currently fails)
        print(f"\n🚨 Step 6: Importing Threats")
        print("-" * 30)
        
        threats_created = 0
        
        for threat in otm_content.get("threats", []):
            try:
                threat_data = {
                    "title": threat.get("name", "Untitled Threat"),
                    "description": threat.get("description", ""),
                    "priority": threat.get("severity", "medium").lower(),
                    "status": "open",
                    "source": f"OTM Import: {threat.get('type', 'Unknown')}",
                    "is_custom": True
                }
                
                print(f"  Attempting: {threat_data['title']}")
                created_threat = await client.create_threat(threat_data)
                threats_created += 1
                print(f"  ✅ Created threat")
                
            except Exception as e:
                print(f"  ❌ Threat creation failed: {e}")
        
        print(f"\n📊 Threats Summary: {threats_created}/{len(otm_content.get('threats', []))} created")
        
        # Step 7: Final Status
        print(f"\n🎯 Final Import Status")
        print("=" * 60)
        print(f"✅ Threat Model: Created ({threat_model_id})")
        print(f"✅ Components: {components_created}/{len(otm_content.get('components', []))} imported")
        print(f"❌ Threats: {threats_created}/{len(otm_content.get('threats', []))} imported")
        print(f"❌ Canvas Visibility: Components exist but not visible on canvas")
        
        print(f"\n📍 Where to find your imported data:")
        print(f"1. Go to https://app.devici.com")
        print(f"2. Navigate to Sandbox collection")
        print(f"3. Open threat model: '{threat_model_data['title']}'")
        print(f"4. Components are created but may not be visible on canvas")
        
        # Step 8: Verify what was actually created
        print(f"\n🔍 Verification")
        print("-" * 30)
        
        # Check if components exist in the system
        all_components = await client.get_components(limit=20)
        recent_components = [
            c for c in all_components.get('items', []) 
            if threat_model_id and threat_model_id in str(c.get('canvas', {}))
        ]
        
        print(f"Components in system: {len(recent_components)}")
        for comp in recent_components:
            print(f"  - {comp.get('title', 'Unknown')}")
        
        # Check canvas state
        canvas = await client.get_canvas(canvas_id)
        canvas_nodes = len(canvas.get('data', {}).get('nodes', []))
        print(f"Canvas nodes: {canvas_nodes}")

if __name__ == "__main__":
    asyncio.run(sample_otm_import()) 