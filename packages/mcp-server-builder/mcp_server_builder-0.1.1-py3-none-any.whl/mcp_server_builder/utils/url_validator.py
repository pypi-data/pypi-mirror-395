"""URL validation for domain restriction."""

from typing import Final


class URLValidationError(Exception):
    """Raised when a URL fails validation."""

    pass


# Immutable domain allowlist using frozenset
DEFAULT_ALLOWED_DOMAINS: Final[frozenset[str]] = frozenset(
    {
        "https://modelcontextprotocol.io/",
        "https://gofastmcp.com/",
        "https://spec.modelcontextprotocol.io/",
    }
)


class URLValidator:
    """Validates URLs against allowed domain prefixes."""

    def __init__(self, allowed_domains: frozenset[str]) -> None:
        """Initialize the URL validator with allowed domain prefixes.

        Args:
            allowed_domains: Frozenset of allowed domain prefixes
        """
        self._allowed = allowed_domains

    def is_url_allowed(self, url: str) -> bool:
        """Check if a URL is allowed based on domain prefixes.

        Args:
            url: The URL to validate

        Returns:
            True if the URL is allowed, False otherwise
        """
        if not url or not isinstance(url, str):
            return False

        return any(url.startswith(prefix) for prefix in self._allowed)

    def validate_urls(self, urls: str | list[str]) -> list[str]:
        """Validate URLs and return valid ones.

        Args:
            urls: Single URL string or list of URLs to validate

        Returns:
            List of validated URLs

        Raises:
            URLValidationError: If any URL is not allowed
        """
        if isinstance(urls, str):
            urls = [urls]

        validated_urls: list[str] = []
        invalid_urls: list[str] = []

        for url in urls:
            if self.is_url_allowed(url):
                validated_urls.append(url)
            else:
                invalid_urls.append(url)

        if invalid_urls:
            allowed_domains = ", ".join(sorted(self._allowed))
            raise URLValidationError(
                f"URLs not allowed: {', '.join(invalid_urls)}. "
                f"Allowed domain prefixes: {allowed_domains}"
            )

        return validated_urls


# Default validator instance
_default_validator: Final[URLValidator] = URLValidator(DEFAULT_ALLOWED_DOMAINS)


def validate_urls(
    urls: str | list[str],
    allowed_domains: frozenset[str] | None = None,
) -> list[str]:
    """Validate URLs based on allowed domains.

    Args:
        urls: Single URL string or list of URLs to validate
        allowed_domains: Optional frozenset of allowed domain prefixes.
                        If None, uses default allowed domains.

    Returns:
        List of validated URLs

    Raises:
        URLValidationError: If any URL is not allowed
    """
    if isinstance(urls, str):
        urls = [urls]

    # Convert relative URLs to absolute URLs (default to modelcontextprotocol.io)
    processed_urls: list[str] = []
    for url in urls:
        if not url.startswith(("http://", "https://")):
            url = f"https://modelcontextprotocol.io{url}"
        processed_urls.append(url)

    if allowed_domains is None:
        return _default_validator.validate_urls(processed_urls)
    else:
        validator = URLValidator(allowed_domains)
        return validator.validate_urls(processed_urls)
