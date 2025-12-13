# Google Patents MCP Server

This is a Model Context Protocol (MCP) server that provides access to Google Patents data using SerpApi.

## Configuration

You need a SerpApi API key to use this server. Set the `SERPAPI_API_KEY` environment variable.

## Tools

- `search_patents(query: str, num: int = 10, page: int = 1)`: Search for patents.
- `get_patent_details(patent_id: str)`: Get details of a specific patent.

## Installation

```bash
pip install mcp-server-google-patents
```

## Usage

Run the server:

```bash
mcp-server-google-patents
```
