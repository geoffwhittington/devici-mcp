#!/usr/bin/env python3
"""
SIMPLE: Just POST the raw JSON file - try with /v1
"""
import json
import asyncio
import httpx
from src.devici_mcp_server.api_client import create_client_from_env
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_access_token():
    """Get OAuth access token using client credentials"""
    client_id = os.getenv('DEVICI_CLIENT_ID')
    client_secret = os.getenv('DEVICI_CLIENT_SECRET')
    base_url = os.getenv('DEVICI_API_BASE_URL', 'https://api.devici.com/api/v1')
    
    if not client_id or not client_secret:
        print("❌ DEVICI_CLIENT_ID or DEVICI_CLIENT_SECRET not found in environment")
        return None
    
    auth_data = {
        "clientId": client_id,
        "secret": client_secret
    }
    
    # Try different auth endpoint variations
    auth_endpoints = [
        f"{base_url}/auth",  # Try within v1 API first
        base_url.replace('/api/v1', '/auth'),  # Try at root level
        "https://api.devici.com/auth"  # Try explicit root auth
    ]
    
    for auth_url in auth_endpoints:
        try:
            print(f"🔑 Trying auth at: {auth_url}")
            
            response = requests.post(auth_url, json=auth_data)
            print(f"🔑 Auth response status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                auth_response = response.json()
                access_token = auth_response["access_token"]
                print(f"✅ Got access token (length: {len(access_token)})")
                return access_token
            else:
                print(f"❌ Auth failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Auth error: {e}")
    
    print("❌ All auth endpoints failed")
    return None

def post_otm_to_devici(otm_file_path, threat_model_id=None):
    """
    Simple script to POST OTM JSON directly to Devici's OTM import endpoint
    """
    
    # Get access token via OAuth
    access_token = get_access_token()
    if not access_token:
        return False
    
    # Read the OTM file
    try:
        with open(otm_file_path, 'r') as f:
            otm_data = json.load(f)
        print(f"✅ Loaded OTM file: {otm_file_path}")
        print(f"📊 Project: {otm_data.get('project', {}).get('name', 'Unknown')}")
    except Exception as e:
        print(f"❌ Error reading OTM file: {e}")
        return False
    
    # Add collection ID to the OTM data if not present
    if "collectionId" not in otm_data:
        # Use Sandbox collection ID (based on existing threat models we saw)
        sandbox_collection_id = "2eca33f8-4575-4999-90c4-09a67e2ddc7b"
        otm_data["collectionId"] = sandbox_collection_id
        print(f"📁 Added collection ID: {sandbox_collection_id}")
    
    # Test different potential OTM import endpoints based on the docs
    base_url = os.getenv('DEVICI_API_BASE_URL', 'https://api.devici.com/api/v1')
    
    # Try multiple endpoint variations that might exist for OTM import
    endpoints_to_try = [
        "/threat-models/import/otm",
        "/threat-models/otm/import", 
        "/threat-models/import",
        "/otm/import",
        "/import/otm"
    ]
    
    if threat_model_id:
        # Also try endpoints with threat model ID, including the export pattern
        endpoints_to_try.extend([
            f"/threat-models/{threat_model_id}/export/otm",  # Same as export but with POST
            f"/threat-models/{threat_model_id}/import/otm",
            f"/threat-models/{threat_model_id}/otm/import",
            f"/threat-models/{threat_model_id}/import",
            f"/threat-models/{threat_model_id}/otm"  # Just the base OTM endpoint
        ])
    
    # Set up headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print(f"📊 Data size: {len(json.dumps(otm_data))} bytes")
    
    # First, test if the export endpoint works to confirm the correct path pattern
    if threat_model_id:
        export_url = f"{base_url}/threat-models/{threat_model_id}/export/otm"
        print(f"\n🔍 First, testing export endpoint: GET {export_url}")
        
        try:
            export_response = requests.get(export_url, headers=headers)
            print(f"📈 Export Status Code: {export_response.status_code}")
            
            if export_response.status_code == 200:
                print("✅ Export endpoint works! This confirms the path pattern is correct.")
                # Try import variations based on the working export path
                import_variations = [
                    f"/threat-models/{threat_model_id}/import/otm",  # Replace export with import
                    f"/threat-models/{threat_model_id}/otm",        # Just the base path
                    f"/threat-models/{threat_model_id}/import"      # Import without otm
                ]
                # Insert these at the beginning to try first
                for variation in reversed(import_variations):
                    if variation not in [ep for ep in endpoints_to_try]:
                        endpoints_to_try.insert(0, variation)
            else:
                print(f"❌ Export endpoint failed: {export_response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Error testing export: {e}")
    
    for endpoint in endpoints_to_try:
        url = f"{base_url}{endpoint}"
        
        # Try both POST and PUT methods, especially for endpoints with threat model ID
        methods_to_try = ["POST"]
        if threat_model_id and threat_model_id in endpoint:
            methods_to_try = ["POST", "PUT"]  # PUT might be used for updating existing threat models
        
        for method in methods_to_try:
            print(f"\n📡 Trying {method}: {url}")
            
            try:
                # Make the request with the specified method
                response = requests.request(method, url, json=otm_data, headers=headers)
                
                print(f"📈 Status Code: {response.status_code}")
                
                if response.text:
                    try:
                        response_json = response.json()
                        print(f"📋 Response: {json.dumps(response_json, indent=2)}")
                    except:
                        print(f"📋 Response Text: {response.text}")
                
                if response.status_code in [200, 201]:
                    print("✅ OTM import successful!")
                    return True
                elif response.status_code not in [404, 405]:  # 405 = Method Not Allowed
                    # If it's not a 404 or 405, the endpoint might exist but there's another issue
                    print(f"🔍 Endpoint exists but failed with status {response.status_code}")
                    if method == "PUT":  # If PUT failed, still try other endpoints
                        continue
                    else:
                        break  # If POST failed with non-404/405, break from this endpoint
                    
            except Exception as e:
                print(f"❌ Error making request: {e}")
    
    print("❌ All OTM import endpoints failed")
    return False

if __name__ == "__main__":
    # Use an existing threat model ID
    threat_model_id = "cd977df6-9cad-4cfa-9259-b4725cc0cda4"  # First Draft threat model
    
    # Test with the draft threat model file
    otm_file = "Draft threat model_otm_report.json"
    
    if os.path.exists(otm_file):
        print(f"🎯 Testing OTM import to threat model: {threat_model_id}")
        success = post_otm_to_devici(otm_file, threat_model_id)
        
        if success:
            print("🎉 Import completed successfully!")
        else:
            print("💥 Import failed - check logs above")
    else:
        print(f"❌ OTM file not found: {otm_file}") 