#!/usr/bin/env python3
"""Test script to verify MCP server tools and schemas"""
import sys
import json
import asyncio
from typing import Any

# Add parent directory to path
sys.path.insert(0, '/home/lysander-z-f-q/PycharmProjects/sj_ai_patent')

from mcp_server.server import mcp

async def verify():
    print("=" * 60)
    print("MCP Server Tool Verification")
    print("=" * 60)

    try:
        # FastMCP list_tools is async
        # FastMCP might not expose list_tools directly in all versions
        # It seems we should use the internal tool list or the list_tools capability
        if hasattr(mcp, 'list_tools'):
            tools = await mcp.list_tools()
        elif hasattr(mcp, 'get_tools'):
             tools = await mcp.get_tools()
        else:
            # Fallback to accessing the tool list directly if possible (for older fastmcp)
            # This is a hack for verification
            print("Could not find list_tools or get_tools, trying direct access...")
            tools = []
            if hasattr(mcp, '_tool_manager'):
                 # This might be a dict
                 tools_dict = mcp._tool_manager._tools
                 # Mock tool objects for printing
                 class MockTool:
                     def __init__(self, name, func):
                         self.name = name
                         self.description = func.__doc__
                         self.inputSchema = getattr(func, "__annotations__", {})
                 
                 tools = [MockTool(k, v) for k, v in tools_dict.items()]
        
        print(f"\nFound {len(tools)} tools:")
        
        for tool in tools:
            if isinstance(tool, str):
                print(f"\n🔹 Tool: {tool}")
                # Try to get more info if possible
                if hasattr(mcp, '_tool_manager') and tool in mcp._tool_manager._tools:
                    func = mcp._tool_manager._tools[tool]
                    print(f"   Description: {func.__doc__}")
                    # Try to print annotations as a proxy for schema
                    if hasattr(func, "__annotations__"):
                        print(f"   Annotations: {func.__annotations__}")
            else:
                print(f"\n🔹 Tool: {tool.name}")
                print(f"   Description: {tool.description}")
                print("   Schema:")
                # Pretty print the schema
                try:
                    print(json.dumps(tool.inputSchema, indent=4, ensure_ascii=False))
                except:
                    print(f"   Could not print schema for {tool.name}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(verify())
