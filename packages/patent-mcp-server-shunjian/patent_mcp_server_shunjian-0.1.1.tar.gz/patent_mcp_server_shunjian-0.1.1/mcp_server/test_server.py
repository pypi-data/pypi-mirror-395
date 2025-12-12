from mcp_server.server import mcp

print("Verifying MCP Server Tools...")
try:
    # Access the internal tool list if possible, or just print success if import works
    # FastMCP likely stores tools in a way we can inspect.
    # Let's try to print the keys of the tools.
    # Note: Implementation details of FastMCP might vary, but usually there is a registry.
    # If mcp.list_tools() exists (async), we might need to run it. 
    # For now, let's just check if the object is created and has tools.
    
    # Check for _tools dict (common in some implementations) or similar
    if hasattr(mcp, '_tools'):
        print(f"Found {len(mcp._tools)} tools registered.")
        for name in mcp._tools:
            print(f" - {name}")
    else:
        print("Could not directly inspect tools, but server object created successfully.")

except Exception as e:
    print(f"Error verifying server: {e}")
