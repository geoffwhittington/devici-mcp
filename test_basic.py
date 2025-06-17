#!/usr/bin/env python3
"""
Very basic test to verify the Devici MCP Server can be imported.
"""

def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        from src.devici_mcp_server import DeviciMCPServer
        from src.devici_mcp_server.api_client import DeviciAPIClient, DeviciConfig
        from src.devici_mcp_server.server import DeviciMCPServer as ServerClass
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


if __name__ == "__main__":
    print("Running basic import test for Devici MCP Server...")
    print("=" * 50)
    
    if test_imports():
        print("🎉 Basic test passed! The Devici MCP Server is ready to use.")
        print("\nTo use the server:")
        print("1. Copy env.example to .env and add your Devici API credentials")
        print("2. Run: python -m src.devici_mcp_server")
    else:
        print("❌ Basic test failed")
        exit(1) 