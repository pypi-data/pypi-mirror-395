from mcp.server.fastmcp import FastMCP
from .client import GooglePatentsClient
import os
from typing import Optional

# Initialize FastMCP server
mcp = FastMCP("google-patents")

def get_client() -> GooglePatentsClient:
    """Helper to get an authenticated client."""
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY environment variable is not set.")
    return GooglePatentsClient(api_key=api_key)

@mcp.tool()
def search_patents(query: str, num: int = 10, page: int = 1) -> str:
    """
    Search for patents using Google Patents.

    Args:
        query: The search query (e.g., "artificial intelligence").
        num: Number of results to return (default 10).
        page: Page number (default 1).

    Returns:
        JSON string containing the search results.
    """
    client = get_client()
    results = client.search(query=query, num=num, page=page)
    return str(results)

@mcp.tool()
def get_patent_details(patent_id: str) -> str:
    """
    Get detailed information about a specific patent.

    Args:
        patent_id: The unique ID of the patent (e.g., "US1234567B2").

    Returns:
        JSON string containing the patent details.
    """
    client = get_client()
    results = client.get_details(patent_id=patent_id)
    return str(results)

if __name__ == "__main__":
    mcp.run()
