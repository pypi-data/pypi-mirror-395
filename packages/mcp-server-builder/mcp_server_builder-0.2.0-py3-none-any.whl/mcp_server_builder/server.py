"""MCP Server Builder - FastMCP server implementation."""

from loguru import logger
from mcp.server.fastmcp import FastMCP

from .tools import docs
from .utils import cache

APP_NAME = "mcp-server-builder"

# Initialize FastMCP server
mcp = FastMCP(APP_NAME)

# Register tools
mcp.tool()(docs.search_mcp_docs)
mcp.tool()(docs.fetch_mcp_doc)


def main() -> None:
    """Main entry point for the MCP server.

    Initializes the document cache and starts the FastMCP server.
    The cache is loaded with document titles only for fast startup,
    with full content fetched on-demand.
    """
    logger.info(f"Starting {APP_NAME}...")

    try:
        cache.ensure_ready()
        logger.info("Cache initialized successfully")
    except Exception as e:
        logger.warning(f"Cache initialization warning: {e}")

    mcp.run()


if __name__ == "__main__":
    main()
