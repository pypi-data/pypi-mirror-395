"""Cache management for documentation index and pages."""

from typing import Final

from ..config import doc_config
from . import doc_fetcher, text_processor
from .doc_fetcher import Page
from .indexer import Doc, IndexSearch

# Python 3.13 type aliases (PEP 695)
type UrlCache = dict[str, Page | None]
type UrlTitles = dict[str, str]

# Global state
_INDEX: IndexSearch | None = None
_URL_CACHE: UrlCache = {}
_URL_TITLES: UrlTitles = {}
_LINKS_LOADED: bool = False

SNIPPET_HYDRATE_MAX: Final[int] = 5


def load_links_only() -> None:
    """Parse llms.txt files and index curated titles without fetching content.

    This function initializes the search index with document titles and URLs from
    configured llms.txt files. Content is not fetched during initialization for
    faster startup times.
    """
    global _INDEX, _LINKS_LOADED, _URL_TITLES, _URL_CACHE

    if _INDEX is None:
        _INDEX = IndexSearch()

    for src in doc_config.llm_texts_url:
        for title, url in doc_fetcher.parse_llms_txt(src):
            # Record curated display title and placeholder cache
            _URL_TITLES[url] = title
            _URL_CACHE.setdefault(url, None)

            # Normalize title for display and indexing
            display_title = text_processor.normalize(title)
            index_title = text_processor.index_title_variants(display_title, url)

            # Index with empty content for fast startup
            _INDEX.add(
                Doc(
                    uri=url,
                    display_title=display_title,
                    content="",
                    index_title=index_title,
                )
            )

    _LINKS_LOADED = True


def ensure_ready() -> None:
    """Ensure the search index is initialized and ready for use.

    Calls load_links_only() if the index hasn't been loaded yet.
    This is the main entry point for index initialization.
    """
    if not _LINKS_LOADED:
        load_links_only()


def ensure_page(url: str) -> Page | None:
    """Ensure a page is cached, fetching it if necessary.

    Args:
        url: The URL of the page to ensure is cached

    Returns:
        The cached or newly fetched Page object, or None if fetch failed
    """
    page = _URL_CACHE.get(url)
    if page is not None:
        return page

    try:
        raw = doc_fetcher.fetch_and_clean(url)
        display_title = text_processor.format_display_title(url, raw.title, _URL_TITLES)
        page = Page(url=url, title=display_title, content=raw.content)
        _URL_CACHE[url] = page
        return page
    except Exception:
        return None


def get_index() -> IndexSearch | None:
    """Get the current search index instance.

    Returns:
        The initialized IndexSearch instance, or None if not yet loaded
    """
    return _INDEX


def get_url_cache() -> UrlCache:
    """Get the URL cache dictionary.

    Returns:
        Dictionary mapping URLs to cached Page objects (or None if not fetched)
    """
    return _URL_CACHE


def get_url_titles() -> UrlTitles:
    """Get the curated URL titles mapping.

    Returns:
        Dictionary mapping URLs to their curated display titles from llms.txt
    """
    return _URL_TITLES
