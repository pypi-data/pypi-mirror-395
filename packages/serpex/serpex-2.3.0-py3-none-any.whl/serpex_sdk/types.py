"""
Type definitions for the Serpex SERP API Python SDK.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Represents a single search result."""

    title: str
    url: str
    snippet: str
    position: int
    engine: str
    published_date: Optional[str] = None
    img_src: Optional[str] = None
    duration: Optional[str] = None
    score: Optional[float] = None


@dataclass
class SearchMetadata:
    """Metadata for search results."""

    number_of_results: int
    response_time: int
    timestamp: str
    credits_used: int
    category: Optional[str] = None  # Optional category field for news searches


@dataclass
class SearchResponse:
    """Complete search response."""

    metadata: SearchMetadata
    id: str
    query: str
    engines: List[str]
    results: List[SearchResult]
    answers: List[Any]
    corrections: List[str]
    infoboxes: List[Any]
    suggestions: List[str]


@dataclass
class ExtractResult:
    """Represents a single extraction result."""

    url: str
    success: bool
    markdown: Optional[str] = None
    error: Optional[str] = None
    error_type: Optional[str] = None
    status_code: Optional[int] = None
    crawled_at: Optional[str] = None
    extraction_mode: Optional[str] = None


@dataclass
class ExtractMetadata:
    """Metadata for extraction results."""

    total_urls: int
    processed_urls: int
    successful_crawls: int
    failed_crawls: int
    credits_used: int
    response_time: int
    timestamp: str


@dataclass
class ExtractResponse:
    """Complete extraction response."""

    success: bool
    results: List[ExtractResult]
    metadata: ExtractMetadata


@dataclass
class ExtractParams:
    """Parameters for extraction requests."""

    # Required: URLs to extract (max 10)
    urls: List[str]


@dataclass
class SearchParams:
    """Parameters for search requests."""

    # Required: search query
    q: str

    # Optional: Engine selection (defaults to 'auto')
    engine: Optional[str] = "auto"

    # Optional: Search category ('web' for general search, 'news' for news articles - always returns latest news)
    category: Optional[str] = "web"  # Supports: 'web', 'news'

    # Optional: Time range filter (only applicable for 'web' category, ignored for 'news')
    time_range: Optional[str] = "all"

    # Optional: Response format
    format: Optional[str] = "json"
