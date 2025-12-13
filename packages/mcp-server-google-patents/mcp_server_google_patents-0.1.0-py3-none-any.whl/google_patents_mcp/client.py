import os
import requests
from typing import Optional, Dict, Any, List

class GooglePatentsClient:
    """Client for interacting with Google Patents via SerpApi."""

    BASE_URL = "https://serpapi.com/search"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the client.

        Args:
            api_key: SerpApi API key. If not provided, looks for SERPAPI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            raise ValueError("SerpApi API key is required. Set SERPAPI_API_KEY env var or pass it to the constructor.")

    def search(self, query: str, num: int = 10, page: int = 1, **kwargs) -> Dict[str, Any]:
        """
        Search for patents using Google Patents API.

        Args:
            query: Search query (e.g., "coffee").
            num: Number of results per page (1-100).
            page: Page number.
            **kwargs: Additional parameters supported by SerpApi (e.g., sort, clustered, etc.).

        Returns:
            Dictionary containing the search results.
        """
        params = {
            "engine": "google_patents",
            "q": query,
            "num": num,
            "page": page,
            "api_key": self.api_key,
            "output": "json",
            **kwargs
        }
        
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()

    def get_details(self, patent_id: str, **kwargs) -> Dict[str, Any]:
        """
        Get details of a specific patent using Google Patents Details API.

        Args:
            patent_id: Patent ID (e.g., "US11734097B1").
            **kwargs: Additional parameters supported by SerpApi.

        Returns:
            Dictionary containing the patent details.
        """
        params = {
            "engine": "google_patents_details",
            "patent_id": patent_id,
            "api_key": self.api_key,
            "output": "json",
            **kwargs
        }

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
