#!/usr/bin/env python3
"""
SIMPLE: Just POST the raw JSON file - try with /v1
"""
import json
import asyncio
import httpx
from src.devici_mcp_server.api_client import create_client_from_env
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
            
            response = httpx.post(auth_url, json=auth_data)
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

def get_threat_model(threat_model_id):
    """
    Fetch an existing threat model by ID from Devici API.
    """
    access_token = get_access_token()
    if not access_token:
        return None

    base_url = os.getenv('DEVICI_API_BASE_URL', 'https://api.devici.com/api/v1')
    url = f"{base_url}/threat-models/{threat_model_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = httpx.get(url, headers=headers)
        print(f"GET {url} -> {response.status_code}")
        if response.status_code == 200:
            print("✅ Threat model fetched successfully.")
            return response.json()
        else:
            print(f"❌ Failed to fetch threat model: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error fetching threat model: {e}")
        return None

def get_first_collection_id():
    """
    Fetch the first available collection ID from the Devici API.
    If none exist, create a new collection and return its ID.
    """
    access_token = get_access_token()
    if not access_token:
        return None

    base_url = os.getenv('DEVICI_API_BASE_URL', 'https://api.devici.com/api/v1')
    url = f"{base_url}/collections?page=1&limit=10"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = httpx.get(url, headers=headers)
        print(f"GET {url} -> {response.status_code}")
        if response.status_code == 200:
            collections = response.json()
            if isinstance(collections, list) and collections:
                collection_id = collections[0].get("id")
                print(f"✅ Using collectionId: {collection_id}")
                return collection_id
            elif isinstance(collections, dict) and "collections" in collections and collections["collections"]:
                collection_id = collections["collections"][0].get("id")
                print(f"✅ Using collectionId: {collection_id}")
                return collection_id
            else:
                print("❌ No collections found in API response. Attempting to create a new collection...")
                # Try to create a new collection
                create_url = f"{base_url}/collections"
                collection_payload = {
                    "title": "Auto-created Collection",
                    "description": "Created automatically by import script"
                }
                try:
                    create_resp = httpx.post(create_url, json=collection_payload, headers=headers)
                    print(f"POST {create_url} -> {create_resp.status_code}")
                    if create_resp.status_code in [200, 201]:
                        created = create_resp.json()
                        # The response may be a dict with the new collection's id
                        collection_id = created.get("id")
                        if not collection_id and "collection" in created:
                            collection_id = created["collection"].get("id")
                        if collection_id:
                            print(f"✅ Created and using collectionId: {collection_id}")
                            return collection_id
                        else:
                            print("❌ Could not parse collectionId from create response.")
                            return None
                    else:
                        print(f"❌ Failed to create collection: {create_resp.text}")
                        return None
                except Exception as ce:
                    print(f"❌ Error creating collection: {ce}")
                    return None
        else:
            print(f"❌ Failed to fetch collections: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error fetching collections: {e}")
        return None

def import_otm_to_threat_model(otm_file_path, threat_model_id):
    """
    Import an OTM JSON to a specific threat model using the documented endpoint.
    If collectionId is missing, fetch one from the API and add it.
    """
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

    # Ensure collectionId is present, or fetch one if missing
    if "collectionId" not in otm_data:
        print("ℹ️ OTM data missing collectionId. Attempting to fetch one from the API...")
        collection_id = get_first_collection_id()
        if not collection_id:
            print("❌ Could not retrieve a collectionId. Aborting import.")
            return False
        otm_data["collectionId"] = collection_id
        print(f"📁 Added collectionId: {collection_id}")

    base_url = os.getenv('DEVICI_API_BASE_URL', 'https://api.devici.com/api/v1')
    url = f"{base_url}/threat-models/otm/{threat_model_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    print(f"POST {url} (data size: {len(json.dumps(otm_data))} bytes)")
    try:
        response = httpx.post(url, json=otm_data, headers=headers)
        print(f"📈 Status Code: {response.status_code}")
        if response.text:
            try:
                response_json = response.json()
                print(f"📋 Response: {json.dumps(response_json, indent=2)}")
            except Exception:
                print(f"📋 Response Text: {response.text}")
        if response.status_code in [200, 201]:
            print("✅ OTM import successful!")
            return True
        else:
            print("❌ OTM import failed.")
            return False
    except Exception as e:
        print(f"❌ Error importing OTM: {e}")
        return False

if __name__ == "__main__":
    # Example threat model ID and OTM file
    threat_model_id = "cd977df6-9cad-4cfa-9259-b4725cc0cda4"  # Replace with your actual threat model ID
    otm_file = "Draft threat model_otm_report.json"  # Replace with your OTM file path

    # Fetch and display the existing threat model
    print(f"🔍 Fetching threat model: {threat_model_id}")
    threat_model = get_threat_model(threat_model_id)
    if threat_model:
        print(f"Threat Model Name: {threat_model.get('name', 'Unknown')}")
    else:
        print("Failed to fetch threat model. Aborting import.")
        exit(1)

    # Import the OTM to the threat model
    if os.path.exists(otm_file):
        print(f"🎯 Importing OTM to threat model: {threat_model_id}")
        success = import_otm_to_threat_model(otm_file, threat_model_id)
        if success:
            print("🎉 Import completed successfully!")
        else:
            print("💥 Import failed - check logs above")
    else:
        print(f"❌ OTM file not found: {otm_file}")
