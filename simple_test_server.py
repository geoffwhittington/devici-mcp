#!/usr/bin/env python3
"""
Simple test MCP server to verify Cursor connection.
"""

from mcp.server.fastmcp import FastMCP

# Create simple MCP server
mcp = FastMCP("simple-test")

@mcp.tool()
def hello_world() -> str:
    """A simple hello world tool for testing."""
    return "Hello from MCP!"

@mcp.tool()  
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

if __name__ == "__main__":
    print("Starting simple test MCP server...")
    mcp.run() 