"""Document fetching and parsing utilities."""

import html
import re
import urllib.request
from typing import Final

from pydantic import BaseModel, Field

from ..config import doc_config
from .url_validator import URLValidationError, validate_urls

# Regex patterns for parsing
_MD_LINK: Final[re.Pattern[str]] = re.compile(r"\[([^\]]+)\]\(([^\)]+)\)")
_HTML_BLOCK: Final[re.Pattern[str]] = re.compile(
    r"(?is)<(script|style|noscript).*?>.*?</\1>"
)
_TAG: Final[re.Pattern[str]] = re.compile(r"(?s)<[^>]+>")
_TITLE_TAG: Final[re.Pattern[str]] = re.compile(r"(?is)<title[^>]*>(.*?)</title>")
_H1_TAG: Final[re.Pattern[str]] = re.compile(r"(?is)<h1[^>]*>(.*?)</h1>")
_META_OG: Final[re.Pattern[str]] = re.compile(
    r'(?is)<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']'
)


class Page(BaseModel):
    """Represents a fetched and cleaned documentation page.

    Attributes:
        url: The source URL of the page
        title: Extracted or derived title of the page
        content: Cleaned text content of the page
    """

    url: str = Field(description="The source URL of the page")
    title: str = Field(description="Page title (extracted or derived)")
    content: str = Field(description="Cleaned text content of the page")


def _get(url: str) -> str:
    """Fetch content from a URL with proper headers and timeout.

    Args:
        url: The URL to fetch

    Returns:
        The decoded text content of the response

    Raises:
        urllib.error.URLError: If the request fails
    """
    req = urllib.request.Request(url, headers={"User-Agent": doc_config.user_agent})
    with urllib.request.urlopen(req, timeout=doc_config.timeout) as r:  # noqa: S310
        return r.read().decode("utf-8", errors="ignore")


def parse_llms_txt(url: str) -> list[tuple[str, str]]:
    """Parse an llms.txt file and extract document links.

    Args:
        url: URL of the llms.txt file to parse

    Returns:
        List of (title, url) tuples extracted from markdown links
    """
    txt = _get(url)
    links: list[tuple[str, str]] = []

    for match in _MD_LINK.finditer(txt):
        title = match.group(1).strip() or match.group(2).strip()
        doc_url = match.group(2).strip()

        try:
            validated_urls = validate_urls(doc_url)
            links.append((title, validated_urls[0]))
        except URLValidationError:
            # Skip invalid URLs silently
            continue

    return links


def _html_to_text(raw_html: str) -> str:
    """Convert HTML to plain text using stdlib only.

    Args:
        raw_html: Raw HTML content to convert

    Returns:
        Plain text with HTML tags removed and entities unescaped
    """
    # Remove script/style blocks
    stripped = _HTML_BLOCK.sub("", raw_html)
    # Drop tags
    stripped = _TAG.sub(" ", stripped)
    # Unescape HTML entities
    stripped = html.unescape(stripped)
    # Normalize whitespace, remove empty lines
    lines = [ln.strip() for ln in stripped.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def _extract_html_title(raw_html: str) -> str | None:
    """Extract title from HTML content using multiple strategies.

    Args:
        raw_html: Raw HTML content to extract title from

    Returns:
        Extracted title string, or None if no title found
    """
    # Try <title> tag
    match = _TITLE_TAG.search(raw_html)
    if match:
        return html.unescape(match.group(1)).strip()

    # Try og:title meta tag
    match = _META_OG.search(raw_html)
    if match:
        return html.unescape(match.group(1)).strip()

    # Try <h1> tag
    match = _H1_TAG.search(raw_html)
    if match:
        inner = _TAG.sub(" ", match.group(1))
        return html.unescape(inner).strip()

    return None


def fetch_and_clean(page_url: str) -> Page:
    """Fetch a web page and return cleaned content.

    Args:
        page_url: URL of the page to fetch

    Returns:
        Page object with URL, title, and cleaned content

    Raises:
        URLValidationError: If the URL is not allowed
    """
    validated_url = validate_urls(page_url)[0]

    raw = _get(validated_url)
    lower = raw.lower()

    # Check if it's HTML content
    if "<html" in lower or "<head" in lower or "<body" in lower:
        extracted_title = _extract_html_title(raw)
        content = _html_to_text(raw)
        title = extracted_title or validated_url.rsplit("/", 1)[-1] or validated_url
        return Page(url=validated_url, title=title, content=content)
    else:
        # Plain text (e.g., markdown)
        title = validated_url.rsplit("/", 1)[-1] or validated_url
        return Page(url=validated_url, title=title, content=raw)
