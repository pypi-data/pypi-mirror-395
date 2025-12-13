"""MCP documentation search and retrieval tools."""

from typing import Any, Literal

from ..utils import cache, text_processor

# Source type for filtering
SourceFilter = Literal["mcp", "fastmcp"] | None

# Domain to source mapping
_DOMAIN_SOURCE_MAP: dict[str, str] = {
    "modelcontextprotocol.io": "mcp",
    "gofastmcp.com": "fastmcp",
}


def _get_source_from_url(url: str) -> str:
    """Extract source identifier from URL domain."""
    for domain, source in _DOMAIN_SOURCE_MAP.items():
        if domain in url:
            return source
    return "unknown"


def _matches_source_filter(url: str, source_filter: SourceFilter) -> bool:
    """Check if URL matches the source filter."""
    if source_filter is None:
        return True
    return _get_source_from_url(url) == source_filter


def search_mcp_docs(
    query: str, k: int = 5, source: SourceFilter = None
) -> list[dict[str, Any]]:
    """Search MCP protocol AND FastMCP framework documentation with ranked results.

    This tool searches across both documentation sources simultaneously:

    **MCP Protocol (modelcontextprotocol.io):**
    - Official protocol specification and architecture
    - Transports (stdio, streamable HTTP)
    - Tools, Resources, and Prompts primitives
    - Lifecycle, capabilities negotiation, and security

    **FastMCP Framework (gofastmcp.com):**
    - Python framework for building MCP servers
    - Decorators, type hints, and Pydantic integration
    - Authentication, deployment, and production patterns
    - Client SDK and cloud deployment

    Use this to find documentation for building MCP servers with either approach.

    Args:
        query: Search query string (e.g., "tool input schema", "stdio transport")
        k: Maximum number of results to return (default: 5)
        source: Optional filter - "mcp" for protocol docs only, "fastmcp" for
                framework docs only. If None, searches both sources.

    Returns:
        List of dictionaries containing:
        - url: Document URL
        - title: Display title
        - score: Relevance score (higher is better)
        - snippet: Contextual content preview
        - source: Documentation source ("mcp" or "fastmcp")
    """
    cache.ensure_ready()
    index = cache.get_index()

    if index is None:
        return []

    # Request more results if filtering, to ensure we get k results after filtering
    search_k = k * 3 if source else k
    results = index.search(query, k=search_k)

    # Apply source filter if specified
    if source:
        results = [(score, doc) for score, doc in results if _matches_source_filter(doc.uri, source)]

    # Limit to requested k after filtering
    results = results[:k]

    url_cache = cache.get_url_cache()

    # Hydrate top results with content for snippets
    top = results[: min(len(results), cache.SNIPPET_HYDRATE_MAX)]
    for _, doc in top:
        cached = url_cache.get(doc.uri)
        if cached is None or not cached.content:
            cache.ensure_page(doc.uri)

    # Build response with snippets and source
    return_docs: list[dict[str, Any]] = []
    for score, doc in results:
        page = url_cache.get(doc.uri)
        snippet = text_processor.make_snippet(page, doc.display_title)
        return_docs.append(
            {
                "url": doc.uri,
                "title": doc.display_title,
                "score": round(score, 3),
                "snippet": snippet,
                "source": _get_source_from_url(doc.uri),
            }
        )

    return return_docs


def fetch_mcp_doc(uri: str) -> dict[str, Any]:
    """Fetch full document content by URL from MCP protocol or FastMCP framework docs.

    Retrieves complete documentation content from URLs found via search_mcp_docs
    or provided directly. Works with both documentation sources:

    **Supported domains:**
    - modelcontextprotocol.io - Official MCP protocol specification
    - gofastmcp.com - FastMCP Python framework documentation

    Use this to get full documentation pages when search snippets aren't
    sufficient, including:
    - Complete protocol specifications and API references
    - Full tutorial and example code
    - Configuration, authentication, and deployment instructions

    Args:
        uri: Document URI (http/https URLs from supported domains)

    Returns:
        Dictionary containing:
        - url: Canonical document URL
        - title: Document title
        - content: Full document text content
        - source: Documentation source ("mcp" or "fastmcp")
        - error: Error message (only present if fetch failed)
    """
    cache.ensure_ready()

    page = cache.ensure_page(uri)
    if page is None:
        return {"error": "fetch failed", "url": uri, "source": _get_source_from_url(uri)}

    return {
        "url": page.url,
        "title": page.title,
        "content": page.content,
        "source": _get_source_from_url(page.url),
    }
