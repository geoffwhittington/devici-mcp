#!/usr/bin/env python3
"""
Minimal test script for Devici vendor to demonstrate OTM import endpoint issue.

ISSUE: Export OTM works, but no corresponding import endpoint found.
- GET /threat-models/{id}/export/otm ✅ Works (200 OK)
- POST /threat-models/{id}/import/otm ❌ 404 Not Found
- All other logical import variations return 404

Expected: Ability to POST OTM JSON to import/update a threat model.
"""

import requests
import json
import os

# Configuration
CLIENT_ID = os.getenv('DEVICI_CLIENT_ID', 'your_client_id')
CLIENT_SECRET = os.getenv('DEVICI_CLIENT_SECRET', 'your_client_secret')
THREAT_MODEL_ID = "cd977df6-9cad-4cfa-9259-b4725cc0cda4"  # Replace with your threat model ID

def authenticate():
    """Get OAuth token"""
    response = requests.post(
        "https://api.devici.com/api/v1/auth",
        json={"clientId": CLIENT_ID, "secret": CLIENT_SECRET}
    )
    return response.json()["access_token"]

def test_export_import():
    """Test that export works but import doesn't"""
    token = authenticate()
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    print("🔍 Testing Export (should work):")
    export_url = f"https://api.devici.com/api/v1/threat-models/{THREAT_MODEL_ID}/export/otm"
    export_response = requests.get(export_url, headers=headers)
    print(f"GET {export_url}")
    print(f"Status: {export_response.status_code}")
    print(f"Response length: {len(export_response.text)} chars")
    
    # Use a minimal OTM payload for testing import
    sample_otm = {
        "otmVersion": "0.2.0",
        "project": {
            "name": "Test Import",
            "description": "Testing OTM import endpoint"
        },
        "components": [],
        "threats": [],
        "mitigations": []
    }
    
    if export_response.status_code == 200:
        print("✅ Export endpoint exists!")
        
        # Try to use actual export data if available, otherwise use sample
        try:
            if export_response.text.strip():
                otm_data = export_response.json()
                print("📄 Using exported OTM data")
            else:
                otm_data = sample_otm
                print("📄 Export was empty, using sample OTM data")
        except:
            otm_data = sample_otm
            print("📄 Export was not valid JSON, using sample OTM data")
        
        print(f"\n🔍 Testing Import Endpoints (all expected to fail with 404):")
        import_endpoints = [
            f"/threat-models/{THREAT_MODEL_ID}/import/otm",
            f"/threat-models/{THREAT_MODEL_ID}/otm", 
            f"/threat-models/import/otm",
        ]
        
        for endpoint in import_endpoints:
            import_url = f"https://api.devici.com/api/v1{endpoint}"
            import_response = requests.post(import_url, json=otm_data, headers=headers)
            print(f"POST {import_url} → {import_response.status_code}")
            
            if import_response.status_code not in [404, 405]:
                print(f"🎉 Found potential import endpoint! Status: {import_response.status_code}")
                if import_response.text:
                    print(f"Response: {import_response.text[:200]}...")
                return
        
        print(f"\n❌ ISSUE: No working import endpoint found (all returned 404).")
        print(f"📋 QUESTION FOR VENDOR: What is the correct endpoint to POST OTM JSON?")
        print(f"📋 Expected: If GET /threat-models/{{id}}/export/otm works,")
        print(f"           then POST /threat-models/{{id}}/import/otm should work too.")
    
    else:
        print(f"❌ Export failed: {export_response.status_code}")
        print(f"Response: {export_response.text[:200]}...")

if __name__ == "__main__":
    test_export_import() 