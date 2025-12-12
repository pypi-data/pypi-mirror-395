# /// script
# dependencies = [
#     "fastmcp",
#     "requests",
#     "python-dotenv",
# ]
# ///
import sys
import os
# Add parent directory to path to support both direct execution and module execution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastmcp import FastMCP
from mcp_server.base_function.patent_search import custom_search
from mcp_server.base_function.patent_claim import get_claims, extract_claims
from mcp_server.base_function.patent_images import get_patent_images, extract_image_urls
from mcp_server.base_function.patent_law_status import get_law_status, extract_law_status
from mcp_server.base_function.patent_similar import get_similar_patents
from mcp_server.base_function.patent_specification import get_specification, extract_specification

# Create an MCP server
mcp = FastMCP("Patent Function Server")

# Register tools
mcp.tool(custom_search)
mcp.tool(get_claims)
mcp.tool(extract_claims)
mcp.tool(get_patent_images)
mcp.tool(extract_image_urls)
mcp.tool(get_law_status)
mcp.tool(extract_law_status)
mcp.tool(get_similar_patents)
mcp.tool(get_specification)
mcp.tool(extract_specification)


def main():
    """Entry point for uvx"""
    mcp.run()

if __name__ == "__main__":
    main()

