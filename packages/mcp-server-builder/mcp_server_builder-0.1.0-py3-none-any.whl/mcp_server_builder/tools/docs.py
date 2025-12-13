"""MCP documentation search and retrieval tools."""

from typing import Any

from ..utils import cache, text_processor


def search_mcp_docs(query: str, k: int = 5) -> list[dict[str, Any]]:
    """Search MCP protocol and FastMCP documentation with ranked results.

    This tool provides access to comprehensive MCP documentation including:

    **MCP Protocol:**
    - Architecture and core concepts
    - Transports (stdio, streamable HTTP)
    - Tools, Resources, and Prompts
    - Lifecycle and capabilities negotiation
    - Error handling and security

    **FastMCP Framework:**
    - Python server patterns and decorators
    - Tool definitions with type hints
    - Resource and prompt templates
    - Client integration examples

    Use this to find relevant MCP documentation for building MCP servers.

    Args:
        query: Search query string (e.g., "tool input schema", "stdio transport")
        k: Maximum number of results to return (default: 5)

    Returns:
        List of dictionaries containing:
        - url: Document URL
        - title: Display title
        - score: Relevance score (higher is better)
        - snippet: Contextual content preview
    """
    cache.ensure_ready()
    index = cache.get_index()

    if index is None:
        return []

    results = index.search(query, k=k)
    url_cache = cache.get_url_cache()

    # Hydrate top results with content for snippets
    top = results[: min(len(results), cache.SNIPPET_HYDRATE_MAX)]
    for _, doc in top:
        cached = url_cache.get(doc.uri)
        if cached is None or not cached.content:
            cache.ensure_page(doc.uri)

    # Build response with snippets
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
            }
        )

    return return_docs


def fetch_mcp_doc(uri: str) -> dict[str, Any]:
    """Fetch full document content by URL.

    Retrieves complete MCP or FastMCP documentation content from URLs found
    via search_mcp_docs or provided directly. Use this to get full documentation
    pages including:

    - Complete protocol specifications
    - Detailed API reference documentation
    - Full tutorial and example code
    - Configuration and deployment instructions

    This provides the full content when search snippets aren't sufficient for
    understanding or implementing MCP features.

    Args:
        uri: Document URI (supports http/https URLs)

    Returns:
        Dictionary containing:
        - url: Canonical document URL
        - title: Document title
        - content: Full document text content
        - error: Error message (if fetch failed)
    """
    cache.ensure_ready()

    page = cache.ensure_page(uri)
    if page is None:
        return {"error": "fetch failed", "url": uri}

    return {
        "url": page.url,
        "title": page.title,
        "content": page.content,
    }
