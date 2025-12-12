from fastmcp import FastMCP

mcp = FastMCP("Test")

def my_func(x: int) -> int:
    return x + 1

try:
    print("Trying mcp.tool(my_func)...")
    mcp.tool(my_func)
    print("Success!")
except Exception as e:
    print(f"Failed: {e}")

try:
    print("Trying mcp.add_tool(my_func)...")
    mcp.add_tool(my_func)
    print("Success!")
except Exception as e:
    print(f"Failed: {e}")
