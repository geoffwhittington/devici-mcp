#!/usr/bin/env python3
"""
Simple MCP client test to verify the server is working.
"""

import asyncio
import subprocess
import json
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters


async def test_mcp_server():
    """Test connecting to the MCP server and listing tools."""
    print("🔍 Testing MCP Server Connection...")
    
    # Server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "devici_mcp_server"],
        env={
            "PYTHONPATH": "src",
            "DEVICI_API_BASE_URL": "https://api.devici.com/api/v1",
            "DEVICI_CLIENT_ID": "4a4rbdka5m6ed6dmi0iliequm7", 
            "DEVICI_CLIENT_SECRET": "1og9ao144hoigto1ji7eak87baununi1s38l6s5u64k0jp5qi80c",
            "DEBUG": "true"
        }
    )
    
    try:
        # Connect to server
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize
                await session.initialize()
                print("✅ Successfully connected to MCP server")
                
                # List tools
                tools_response = await session.list_tools()
                tools = tools_response.tools
                
                print(f"✅ Found {len(tools)} tools:")
                for tool in tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                if len(tools) == 0:
                    print("❌ No tools found - this indicates a problem")
                    return False
                else:
                    print("🎉 MCP server is working correctly!")
                    return True
                    
    except Exception as e:
        print(f"❌ Failed to connect to MCP server: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_mcp_server())
    exit(0 if success else 1) 