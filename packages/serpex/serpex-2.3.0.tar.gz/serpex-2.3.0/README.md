# serpex

Official Python SDK for the Serpex SERP API - Fetch search results in JSON format.

## Installation

```bash
pip install serpex
```

Or with poetry:

```bash
poetry add serpex
```

## Quick Start

```python
from serpex import SerpexClient

# Initialize the client with your API key
client = SerpexClient('your-api-key-here')

# Search with auto-routing (recommended for simple use cases)
results = client.search({
    'q': 'python tutorial',
    'engine': 'auto'
})

# Or using SearchParams object for type safety
from serpex import SearchParams

params = SearchParams(q='python tutorial', engine='auto')
results = client.search(params)

print(results.results[0].title)
```

## API Reference

### SerpexClient

#### Constructor

```python
SerpexClient(api_key: str, base_url: str = "https://api.serpex.dev")
```

- `api_key`: Your API key from the Serpex dashboard
- `base_url`: Optional base URL (defaults to 'https://api.serpex.dev')

#### Methods

##### `extract(params: ExtractParams | Dict[str, Any]) -> ExtractResponse`

Extract content from web pages and convert them to LLM-ready markdown data. Accepts up to 10 URLs per request.

```python
# Using dictionary (simple approach)
results = client.extract({
    'urls': [
        'https://example.com',
        'https://httpbin.org'
    ]
})

# Using ExtractParams object (type-safe approach)
from serpex import ExtractParams

params = ExtractParams(urls=[
    'https://example.com',
    'https://httpbin.org'
])
results = client.extract(params)
```

## Extract Parameters

The `ExtractParams` dataclass supports extraction parameters:

```python
@dataclass
class ExtractParams:
    # Required: URLs to extract (max 10)
    urls: List[str]
```

## Extract Response Format

```python
@dataclass
class ExtractResponse:
    success: bool
    results: List[ExtractResult]
    metadata: ExtractMetadata

@dataclass
class ExtractResult:
    url: str
    success: bool
    markdown: Optional[str] = None
    error: Optional[str] = None
    status_code: Optional[int] = None

@dataclass
class ExtractMetadata:
    total_urls: int
    processed_urls: int
    successful_crawls: int
    failed_crawls: int
    credits_used: int
    response_time: int
    timestamp: str
```

## Search Parameters

The `SearchParams` dataclass supports all search parameters:

```python
@dataclass
class SearchParams:
    # Required: search query
    q: str

    # Optional: Engine selection (defaults to 'auto')
    engine: Optional[str] = 'auto'

    # Optional: Search category ('web' for general search, 'news' for news articles - always returns latest news)
    category: Optional[str] = 'web'  # Supports: 'web', 'news'

    # Optional: Time range filter (only applicable for 'web' category, ignored for 'news')
    time_range: Optional[str] = 'all'

    # Optional: Response format
    format: Optional[str] = 'json'
```

### News Search Example

News search always returns the latest news articles. The `time_range` parameter is ignored for news searches.

```python
# Search for latest news articles
news_results = client.search({
    'q': 'artificial intelligence',
    'engine': 'google',
    'category': 'news'  # Always returns latest news
})

print(news_results.results[0].title)
print(news_results.results[0].published_date)
```

````

## Supported Engines

- **auto**: Automatically routes to the best available search engine
- **google**: Google's primary search engine
- **bing**: Microsoft's search engine
- **duckduckgo**: Privacy-focused search engine
- **brave**: Privacy-first search engine
- **yahoo**: Yahoo search engine
- **yandex**: Russian search engine

## Response Format

```python
@dataclass
class SearchResponse:
    metadata: SearchMetadata
    id: str
    query: str
    engines: List[str]
    results: List[SearchResult]
    answers: List[Any]
    corrections: List[str]
    infoboxes: List[Any]
    suggestions: List[str]
````

## Error Handling

The SDK raises `SerpApiException` for API errors:

```python
from serpex import SerpexClient, SerpApiException

try:
    results = client.search(SearchParams(q='test query'))
except SerpApiException as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
    print(f"Details: {e.details}")
```

## Examples

### Basic Search

```python
results = client.search({
    'q': 'coffee shops near me'
})
```

### Advanced Search with Filters

```python
results = client.search({
    'q': 'latest AI news',
    'engine': 'google',
    'time_range': 'day',
    'category': 'web'
})
```

### Using SearchParams Object

```python
from serpex import SearchParams

params = SearchParams(
    q='machine learning',
    engine='auto',
    time_range='month'
)
results = client.search(params)
```

### Extract Web Content to LLM-Ready Data

#### Extract from a Single URL

```python
# Extract content from one website
result = client.extract({
    'urls': ['https://example.com']
})

if result.results[0].success:
    print(f"✅ Extracted {len(result.results[0].markdown)} characters")
    print("Markdown content:", result.results[0].markdown[:200] + "...")
```

#### Extract from Multiple URLs (up to 10 at once)

```python
# Extract content from multiple websites (up to 10 URLs)
extract_results = client.extract({
    'urls': [
        'https://example.com',
        'https://httpbin.org',
        'https://github.com'
    ]
})

print(f"Successfully extracted {extract_results.metadata.successful_crawls} pages")
print(f"Total credits used: {extract_results.metadata.credits_used}")

for result in extract_results.results:
    if result.success:
        print(f"✅ {result.url}: {len(result.markdown)} characters")
        # Use result.markdown for LLM processing
    else:
        print(f"❌ {result.url}: {result.error}")
```

#### Sample Response

```python
# Example response structure
{
    'success': True,
    'results': [
        {
            'url': 'https://example.com',
            'success': True,
            'markdown': '# Example Domain\n\nThis domain is for use in...',
            'status_code': 200
        }
    ],
    'metadata': {
        'total_urls': 1,
        'processed_urls': 1,
        'successful_crawls': 1,
        'failed_crawls': 0,
        'credits_used': 3,
        'response_time': 255,
        'timestamp': '2025-11-13T10:30:00.000Z'
    }
}
```

### Using ExtractParams Object

```python
from serpex import ExtractParams

params = ExtractParams(urls=[
    'https://example.com',
    'https://httpbin.org'
])
results = client.extract(params)
```

## Requirements

- Python 3.8+
- requests

## License

MIT
