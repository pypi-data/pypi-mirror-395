"""
Serpex SERP API Python SDK

Official Python SDK for the Serpex SERP API - Fetch search results in JSON format.
"""

from .client import SerpexClient
from .exceptions import SerpApiException
from .types import SearchParams, SearchResponse, ExtractParams, ExtractResponse

__version__ = "1.0.0"
__all__ = ["SerpexClient", "SerpApiException", "SearchParams", "SearchResponse"]