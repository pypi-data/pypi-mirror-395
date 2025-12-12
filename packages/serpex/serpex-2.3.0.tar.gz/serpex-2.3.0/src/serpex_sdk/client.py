"""
Main client for the Serpex SERP API Python SDK.
"""

import requests
from typing import Optional, Dict, Any, Union
from urllib.parse import urlencode

from .types import (
    SearchResponse,
    SearchParams,
    ExtractResponse,
    ExtractParams,
    ExtractResult,
    ExtractMetadata,
)
from .exceptions import SerpApiException


class SerpexClient:
    """
    Official Python client for the Serpex SERP API.

    Provides methods to interact with the Serpex SERP API for fetching
    search results in JSON format from Google, Bing, DuckDuckGo, and Brave.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.serpex.dev"):
        """
        Initialize the SERP API client.

        Args:
            api_key: Your API key from the Serpex dashboard
            base_url: Base URL for the API (optional, defaults to production)

        Raises:
            ValueError: If api_key is not provided or is not a string
        """
        if not api_key or not isinstance(api_key, str):
            raise ValueError("API key is required and must be a string")

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
        )

    def _make_request(
        self, params: Dict[str, Any], endpoint: str = "/api/search", method: str = "GET"
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the API.

        Args:
            params: Query parameters for GET, or body data for POST
            endpoint: API endpoint
            method: HTTP method ("GET" or "POST")

        Returns:
            JSON response data

        Raises:
            SerpApiException: For API errors
        """
        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == "POST":
                # For POST requests, send params as JSON body
                response = self.session.post(url, json=params, timeout=30)
            else:
                # For GET requests, send params as query parameters
                # Filter out None values and prepare query parameters
                filtered_params = {}
                for key, value in params.items():
                    if value is not None:
                        if isinstance(value, list):
                            # Handle array parameters
                            filtered_params[key] = value
                        else:
                            filtered_params[key] = value

                # Build query string
                query_string = urlencode(filtered_params, doseq=True)
                final_url = f"{url}?{query_string}" if query_string else url
                response = self.session.get(final_url, timeout=30)

            return self._handle_response(response)
        except requests.RequestException as e:
            raise SerpApiException(f"Request failed: {str(e)}")

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and raise appropriate exceptions for errors.

        Args:
            response: Requests response object

        Returns:
            JSON response data

        Raises:
            SerpApiException: For various API errors
        """
        if response.status_code == 401:
            raise SerpApiException("Invalid API key", status_code=401)
        elif response.status_code == 402:
            raise SerpApiException("Insufficient credits", status_code=402)
        elif response.status_code == 429:
            raise SerpApiException("Rate limit exceeded", status_code=429)
        elif response.status_code == 400:
            try:
                data = response.json()
                raise SerpApiException(
                    data.get("error", "Validation error"), status_code=400, details=data
                )
            except ValueError:
                raise SerpApiException("Bad request", status_code=400)
        elif not response.ok:
            try:
                data = response.json()
                raise SerpApiException(
                    data.get("error", f"API error: {response.reason}"),
                    status_code=response.status_code,
                    details=data,
                )
            except ValueError:
                raise SerpApiException(
                    f"API error: {response.reason}", status_code=response.status_code
                )

        try:
            return response.json()
        except ValueError:
            raise SerpApiException("Invalid JSON response from API")

    def search(self, params: Union[SearchParams, Dict[str, Any]]) -> SearchResponse:
        """
        Search using the SERP API.

        Args:
            params: SearchParams object or dictionary with query and options

        Returns:
            SearchResponse object with results

        Raises:
            ValueError: If query is not provided
            SerpApiException: For API errors
        """
        # Convert dict to SearchParams if needed
        if isinstance(params, dict):
            params = SearchParams(**params)

        # Validate required parameters
        if not params.q or not isinstance(params.q, str) or not params.q.strip():
            raise ValueError(
                "Query parameter (q) is required and must be a non-empty string"
            )

        if len(params.q) > 500:
            raise ValueError("Query too long (max 500 characters)")

        # Determine endpoint based on category
        category = params.category or "web"
        endpoint = "/api/search/news" if category == "news" else "/api/search"

        # Prepare request parameters with only supported params
        request_params = {
            "q": params.q,
            "engine": params.engine or "auto",
            "format": params.format or "json",
        }

        # Add category for web search, omit for news (news endpoint doesn't need it)
        if category == "web":
            request_params["category"] = "web"
            request_params["time_range"] = params.time_range or "all"

        data = self._make_request(request_params, endpoint=endpoint)

        # Convert response to SearchResponse object
        from .types import SearchResult, SearchMetadata

        metadata = SearchMetadata(**data["metadata"])
        results = [SearchResult(**result) for result in data["results"]]

        return SearchResponse(
            metadata=metadata,
            id=data["id"],
            query=data["query"],
            engines=data["engines"],
            results=results,
            answers=data.get("answers", []),
            corrections=data.get("corrections", []),
            infoboxes=data.get("infoboxes", []),
            suggestions=data.get("suggestions", []),
        )

    def extract(self, params: Union[ExtractParams, Dict[str, Any]]) -> ExtractResponse:
        """
        Extract content from web pages.

        Args:
            params: ExtractParams object or dictionary with URLs to extract

        Returns:
            ExtractResponse object with extraction results

        Raises:
            ValueError: If URLs are not provided or invalid
            SerpApiException: For API errors
        """
        # Convert dict to ExtractParams if needed
        if isinstance(params, dict):
            params = ExtractParams(**params)

        # Validate required parameters
        if (
            not params.urls
            or not isinstance(params.urls, list)
            or len(params.urls) == 0
        ):
            raise ValueError("URLs list is required and must contain at least one URL")

        if len(params.urls) > 10:
            raise ValueError("Maximum 10 URLs allowed per request")

        # Validate URLs
        invalid_urls = []
        for url in params.urls:
            if not isinstance(url, str):
                invalid_urls.append(url)
                continue
            try:
                from urllib.parse import urlparse

                parsed = urlparse(url)
                if not parsed.scheme or not parsed.netloc:
                    invalid_urls.append(url)
            except:
                invalid_urls.append(url)

        if invalid_urls:
            raise ValueError(f"Invalid URLs provided: {invalid_urls}")

        # Prepare request parameters
        request_params = {"urls": params.urls}

        data = self._make_request(request_params, endpoint="/api/crawl", method="POST")

        # Convert response to ExtractResponse object
        metadata = ExtractMetadata(**data["metadata"])
        results = [ExtractResult(**result) for result in data["results"]]

        return ExtractResponse(
            success=data["success"],
            results=results,
            metadata=metadata,
        )
