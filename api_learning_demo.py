#!/usr/bin/env python3
"""
Complete API Learning Demonstration

This script demonstrates everything I learned from exploring the Devici 
browser interface and analyzing the API code. It shows the complete 
workflow for creating threat models with components, threats, and mitigations.
"""

import asyncio
import json
from src.devici_mcp_server.api_client import create_client_from_env

async def demonstrate_api_learning():
    """Demonstrate the complete threat modeling workflow learned from browser exploration."""
    
    print("🎓 Devici API Learning Demonstration")
    print("=" * 60)
    print("Based on browser interface exploration and API code analysis\n")
    
    async with create_client_from_env() as client:
        print("✅ Successfully authenticated with Devici API")
        
        # Step 1: Find or create collection
        print("\n📁 Step 1: Working with Collections")
        print("-" * 40)
        
        collections = await client.get_collections(limit=10)
        sandbox_collection = None
        
        print(f"Found {len(collections.get('items', []))} collections:")
        for collection in collections.get('items', []):
            title = collection.get('title', 'Untitled')
            print(f"  • {title} ({collection.get('id')})")
            if 'sandbox' in title.lower():
                sandbox_collection = collection
        
        if not sandbox_collection:
            print("❌ No sandbox collection found")
            return
        
        collection_id = sandbox_collection['id']
        print(f"\n✅ Using collection: {sandbox_collection['title']}")
        
        # Step 2: Create threat model
        print("\n🎯 Step 2: Creating Threat Model")
        print("-" * 40)
        
        threat_model_data = {
            "title": "Browser Learning Demo - Web Security",
            "description": "Created after learning the Devici interface through browser exploration",
            "collectionId": collection_id
        }
        
        threat_model = await client.create_threat_model(threat_model_data)
        threat_model_id = threat_model.get("id")
        
        if not threat_model_id:
            print("❌ Failed to create threat model")
            return
        
        print(f"✅ Created threat model: {threat_model_id}")
        
        # Get canvas information
        tm_details = await client.get_threat_model(threat_model_id)
        canvas_id = tm_details.get("canvases", [None])[0]
        print(f"✅ Associated canvas: {canvas_id}")
        
        # Step 3: Create components (based on browser interface types I saw)
        print("\n🏗️ Step 3: Creating Components")
        print("-" * 40)
        print("(Using component types I observed in the browser interface)")
        
        components_to_create = [
            {
                "title": "User Browser",
                "description": "End user's web browser client",
                "type": "external-entity",  # External entity type from browser
                "tags": "user, client, browser"
            },
            {
                "title": "Web Server",
                "description": "Application web server",
                "type": "process",  # Process type from browser toolbar
                "tags": "server, web, application"
            },
            {
                "title": "User Database",
                "description": "Database storing user credentials and data",
                "type": "datastore",  # Datastore type from browser toolbar
                "tags": "database, storage, credentials"
            },
            {
                "title": "Payment Gateway",
                "description": "External payment processing service",
                "type": "external-service",  # External service type
                "tags": "payment, external, api"
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
                
                # Link to canvas for visual display
                if canvas_id:
                    component_data["canvasId"] = canvas_id
                
                print(f"  Creating {comp_def['type']}: {comp_def['title']}")
                created_component = await client.create_component(component_data)
                
                # Handle API response format I discovered during analysis
                component_id = created_component.get("component") or created_component.get("id")
                
                if component_id:
                    created_components[comp_def["title"]] = {
                        "id": component_id,
                        "type": comp_def["type"]
                    }
                    print(f"  ✅ Created: {component_id}")
                    
                    # Attempt visual canvas placement
                    try:
                        await client._add_component_to_canvas(component_id, canvas_id, i-1)
                        print(f"  ✅ Added to canvas at position {i-1}")
                    except Exception as canvas_error:
                        print(f"  ⚠️ Canvas placement issue: {canvas_error}")
                else:
                    print(f"  ❌ Failed to extract component ID")
                    
            except Exception as e:
                print(f"  ❌ Failed to create {comp_def['title']}: {e}")
        
        print(f"\n📊 Components Summary: {len(created_components)}/{len(components_to_create)} created")
        
        # Step 4: Create threats (based on STRIDE methodology I saw referenced)
        print("\n🚨 Step 4: Creating Threats")
        print("-" * 40)
        print("(Using STRIDE categories I observed in the threat creation interface)")
        
        threats_to_create = [
            {
                "title": "Cross-Site Scripting (XSS)",
                "description": "Malicious scripts injected into web pages viewed by users",
                "priority": "high",
                "component": "Web Server",
                "stride_category": "Tampering"
            },
            {
                "title": "SQL Injection",
                "description": "Malicious SQL code injection through input fields",
                "priority": "critical",
                "component": "User Database",
                "stride_category": "Tampering"
            },
            {
                "title": "Payment Data Interception",
                "description": "Unauthorized access to payment information in transit",
                "priority": "critical",
                "component": "Payment Gateway",
                "stride_category": "Information Disclosure"
            },
            {
                "title": "Session Hijacking",
                "description": "Unauthorized user session takeover",
                "priority": "high",
                "component": "User Browser",
                "stride_category": "Spoofing"
            }
        ]
        
        created_threats = {}
        
        for threat_def in threats_to_create:
            try:
                threat_data = {
                    "title": threat_def["title"],
                    "description": threat_def["description"],
                    "priority": threat_def["priority"],
                    "status": "open",
                    "source": f"Browser Demo - {threat_def['stride_category']}",
                    "is_custom": True
                }
                
                # Link to component if it exists
                component_name = threat_def["component"]
                if component_name in created_components:
                    threat_data["component"] = {"id": created_components[component_name]["id"]}
                
                print(f"  Creating {threat_def['stride_category']}: {threat_def['title']}")
                created_threat = await client.create_threat(threat_data)
                
                # Handle API response format
                threat_id = created_threat.get("threat") or created_threat.get("id")
                if threat_id:
                    created_threats[threat_def["title"]] = threat_id
                    print(f"  ✅ Created: {threat_id}")
                else:
                    print(f"  ❌ Failed to get threat ID")
                    
            except Exception as e:
                print(f"  ❌ Failed to create {threat_def['title']}: {e}")
        
        print(f"\n📊 Threats Summary: {len(created_threats)}/{len(threats_to_create)} created")
        
        # Step 5: Create mitigations
        print("\n🛡️ Step 5: Creating Mitigations")
        print("-" * 40)
        
        mitigations_to_create = [
            {
                "title": "Content Security Policy",
                "definition": "Implement CSP headers to prevent XSS attacks",
                "threat": "Cross-Site Scripting (XSS)"
            },
            {
                "title": "Parameterized Queries",
                "definition": "Use prepared statements to prevent SQL injection",
                "threat": "SQL Injection"
            },
            {
                "title": "TLS Encryption",
                "definition": "Encrypt all payment data in transit using TLS 1.3",
                "threat": "Payment Data Interception"
            },
            {
                "title": "Secure Session Management",
                "definition": "Implement secure session tokens with proper expiration",
                "threat": "Session Hijacking"
            }
        ]
        
        created_mitigations = {}
        
        for mitigation_def in mitigations_to_create:
            try:
                mitigation_data = {
                    "title": mitigation_def["title"],
                    "definition": mitigation_def["definition"],
                    "is_custom": True
                }
                
                # Link to threat if it exists
                threat_name = mitigation_def["threat"]
                if threat_name in created_threats:
                    mitigation_data["threat"] = {"id": created_threats[threat_name]}
                
                print(f"  Creating mitigation: {mitigation_def['title']}")
                created_mitigation = await client.create_mitigation(mitigation_data)
                
                # Handle API response format
                mitigation_id = created_mitigation.get("mitigation") or created_mitigation.get("id")
                if mitigation_id:
                    created_mitigations[mitigation_def["title"]] = mitigation_id
                    print(f"  ✅ Created: {mitigation_id}")
                else:
                    print(f"  ❌ Failed to get mitigation ID")
                    
            except Exception as e:
                print(f"  ❌ Failed to create {mitigation_def['title']}: {e}")
        
        print(f"\n📊 Mitigations Summary: {len(created_mitigations)}/{len(mitigations_to_create)} created")
        
        # Step 6: Final summary and learning points
        print("\n🎉 API Learning Demo Complete!")
        print("=" * 60)
        
        print(f"✅ Threat Model Created: {threat_model_id}")
        print(f"✅ Components: {len(created_components)} created")
        print(f"✅ Threats: {len(created_threats)} created") 
        print(f"✅ Mitigations: {len(created_mitigations)} created")
        
        print(f"\n🌐 View Your Results:")
        print(f"1. Open: https://app.devici.com")
        print(f"2. Navigate to: {sandbox_collection['title']} collection")
        print(f"3. Open: '{threat_model_data['title']}'")
        
        print(f"\n📚 Key Learning Points from Browser Exploration:")
        print("• Devici uses a visual canvas system for component placement")
        print("• Component types include: process, datastore, external-entity, external-service")
        print("• STRIDE methodology is integrated into threat categorization")
        print("• Canvas placement requires additional API calls beyond component creation")
        print("• Import functionality supports OTM, DrawIO, and TM7 file formats")
        print("• Visual toolbar provides drag-and-drop component creation in browser")
        
        print(f"\n🔧 API Technical Insights:")
        print("• OAuth2 client credentials flow for authentication")
        print("• Component API returns: {'component': 'id', 'representation': 'canvas_id'}")
        print("• Threat API returns: {'threat': 'id'} or {'id': '...'}")
        print("• Mitigation API returns: {'mitigation': 'id'} or {'id': '...'}")
        print("• Canvas management requires separate API calls for visual positioning")
        print("• Linking is done via ID references in nested objects")
        
        return {
            "threat_model_id": threat_model_id,
            "components": created_components,
            "threats": created_threats,
            "mitigations": created_mitigations,
            "canvas_id": canvas_id
        }

if __name__ == "__main__":
    result = asyncio.run(demonstrate_api_learning())
    if result:
        print(f"\n📝 Demo completed successfully!")
        print(f"Threat Model ID: {result['threat_model_id']}")
    else:
        print(f"\n❌ Demo failed to complete") 