"""Configuration for the MCP Server Builder."""

from typing import Final

from pydantic import BaseModel, Field, field_validator

from .utils.url_validator import URLValidationError, validate_urls

# Python 3.13 type alias (PEP 695)
type UrlList = list[str]


class Config(BaseModel):
    """Server configuration with validated llms.txt sources.

    Attributes:
        llm_texts_url: List of llms.txt URLs to index for documentation
        timeout: HTTP request timeout in seconds
        user_agent: User agent string for HTTP requests
    """

    llm_texts_url: UrlList = Field(
        default_factory=lambda: [
            "https://modelcontextprotocol.io/llms.txt",
            "https://gofastmcp.com/llms.txt",
        ],
        description="Curated list of llms.txt files to index at startup",
    )
    timeout: float = Field(
        default=30.0, gt=0, description="HTTP request timeout in seconds"
    )
    user_agent: str = Field(
        default="mcp-server-builder/1.0", description="User agent for HTTP requests"
    )

    @field_validator("llm_texts_url")
    @classmethod
    def validate_llm_urls(cls, v: UrlList) -> UrlList:
        """Validate URLs after initialization."""
        try:
            return validate_urls(v)
        except URLValidationError as e:
            raise ValueError(f"Invalid URLs in configuration: {e}") from e


# Global configuration instance
doc_config: Final[Config] = Config()
