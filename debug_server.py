#!/usr/bin/env python3
"""
Debug script for testing Devici MCP Server functionality.
Run this to test individual functions and debug issues.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from devici_mcp_server.api_client import create_client_from_env


async def test_authentication():
    """Test basic authentication with Devici API."""
    print("Testing authentication...")
    try:
        async with create_client_from_env() as client:
            print(f"✅ Authentication successful!")
            print(f"Token type: {client.token_type}")
            print(f"Has access token: {bool(client.access_token)}")
            return True
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False


async def test_basic_endpoints():
    """Test basic API endpoints."""
    print("\nTesting basic endpoints...")
    try:
        async with create_client_from_env() as client:
            # Test getting users
            print("Testing get_users...")
            users = await client.get_users(limit=1)
            print(f"✅ Users endpoint working - returned {len(users.get('data', []))} users")
            
            # Test getting collections
            print("Testing get_collections...")
            collections = await client.get_collections(limit=1)
            print(f"✅ Collections endpoint working - returned {len(collections.get('data', []))} collections")
            
            # Test getting threat models
            print("Testing get_threat_models...")
            threat_models = await client.get_threat_models(limit=1)
            print(f"✅ Threat models endpoint working - returned {len(threat_models.get('data', []))} threat models")
            
            return True
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False


async def test_mcp_tools():
    """Test MCP tool functions."""
    print("\nTesting MCP tool functions...")
    try:
        # Import MCP tools
        from devici_mcp_server.server import get_users, get_collections, get_threat_models
        
        print("Testing get_users tool...")
        result = await get_users(limit=1)
        print(f"✅ get_users tool working - result type: {type(result)}")
        
        print("Testing get_collections tool...")
        result = await get_collections(limit=1)
        print(f"✅ get_collections tool working - result type: {type(result)}")
        
        print("Testing get_threat_models tool...")
        result = await get_threat_models(limit=1)
        print(f"✅ get_threat_models tool working - result type: {type(result)}")
        
        return True
    except Exception as e:
        print(f"❌ MCP tools test failed: {e}")
        return False


def check_environment():
    """Check if environment variables are set."""
    print("Checking environment variables...")
    
    required_vars = [
        "DEVICI_API_BASE_URL",
        "DEVICI_CLIENT_ID", 
        "DEVICI_CLIENT_SECRET"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {'*' * (len(value) - 4)}{value[-4:] if len(value) > 4 else '****'}")
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("\nPlease create a .env file with:")
        for var in missing_vars:
            print(f"{var}=your_value_here")
        return False
    
    return True


async def main():
    """Main debug function."""
    print("🔍 Devici MCP Server Debug Tool")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        return
    
    # Test authentication
    if not await test_authentication():
        return
    
    # Test API endpoints
    if not await test_basic_endpoints():
        return
    
    # Test MCP tools
    if not await test_mcp_tools():
        return
    
    print("\n🎉 All tests passed! Your MCP server should work correctly.")
    print("\nTo debug specific issues:")
    print("1. Check the error messages above")
    print("2. Verify your API credentials")
    print("3. Test individual endpoints")
    print("4. Check network connectivity to Devici API")


if __name__ == "__main__":
    # Load environment from .env file if it exists
    try:
        from dotenv import load_dotenv
        if Path(".env").exists():
            load_dotenv()
            print("📁 Loaded environment from .env file")
        else:
            print("⚠️  No .env file found - using system environment variables")
    except ImportError:
        print("⚠️  python-dotenv not available - using system environment variables")
    
    asyncio.run(main()) 