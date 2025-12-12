# Patent MCP Server

A Model Context Protocol (MCP) server that provides patent search and analysis tools using the Baiten Patent API.

## Features

- 专利检索 (Patent Search)
- 权利要求查询 (Claims Retrieval)
- 说明书查询 (Specification Retrieval)
- 法律状态查询 (Legal Status Check)
- 专利附图获取 (Patent Images)
- 相似专利查询 (Similar Patents)

## Installation

```bash
pip install patent-mcp-server
```

Or use with uvx:

```bash
uvx patent-mcp-server
```

## Configuration

Create a `.env` file with your Baiten API credentials:

```env
PATENT_DB_APPKEY=your_app_key
PATENT_DB_SECRET=your_secret
PATENT_DB_BASEURL=http://open.baiten.cn
```

## Usage

### Run as MCP Server

```bash
patent-mcp-server
```

### Use with MCP Clients

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "patent-functions": {
      "command": "uvx",
      "args": ["patent-mcp-server"]
    }
  }
}
```

## Available Tools

1. **custom_search** - Search patents
2. **get_claims** - Get patent claims
3. **extract_claims** - Extract claim text
4. **get_patent_images** - Get patent images
5. **extract_image_urls** - Extract image URLs
6. **get_law_status** - Get legal status
7. **extract_law_status** - Extract legal status info
8. **get_similar_patents** - Find similar patents
9. **get_specification** - Get specification
10. **extract_specification** - Extract specification sections

## License

MIT
