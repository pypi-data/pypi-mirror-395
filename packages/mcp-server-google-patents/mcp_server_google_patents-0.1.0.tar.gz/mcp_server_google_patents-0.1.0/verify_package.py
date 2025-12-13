import os
import sys
from unittest.mock import MagicMock, patch

# Add current directory to path so we can import the package
sys.path.append(os.getcwd())

def test_imports():
    print("Testing imports...")
    try:
        from google_patents_mcp import GooglePatentsClient, mcp
        print("Imports successful.")
    except ImportError as e:
        print(f"Import failed: {e}")
        sys.exit(1)

def test_client_init():
    print("Testing client initialization...")
    from google_patents_mcp import GooglePatentsClient
    
    # Test with explicit key
    client = GooglePatentsClient(api_key="test_key")
    assert client.api_key == "test_key"
    print("Client init with explicit key successful.")

    # Test with missing key (should raise error if env var not set)
    if "SERPAPI_API_KEY" in os.environ:
        del os.environ["SERPAPI_API_KEY"]
    
    try:
        GooglePatentsClient()
        print("Error: Client should have raised ValueError for missing key.")
        sys.exit(1)
    except ValueError:
        print("Client correctly raised ValueError for missing key.")

def test_server_tools():
    print("Testing server tool definitions...")
    from google_patents_mcp.server import search_patents, get_patent_details
    
    # Check if tools are decorated correctly (FastMCP internals might be hard to check, 
    # but we can check if functions exist and have correct signatures)
    assert callable(search_patents)
    assert callable(get_patent_details)
    print("Server tools are defined.")

if __name__ == "__main__":
    test_imports()
    test_client_init()
    test_server_tools()
    print("Verification passed!")
