"""
Entry point for RAG Agent MCP server.
"""

import logging
import sys

from rag_agent import config
from rag_agent.server import mcp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def main():
    """Main function for server startup."""
    try:
        log_level = getattr(logging, "DEBUG")
        logging.getLogger().setLevel(log_level)

        logger.info("Starting RAG Agent MCP server")
        logger.info(
            f"RAG Agent API server is expected to be already running and available at: {config.LIGHTRAG_API_BASE_URL}"
        )
        if config.LIGHTRAG_API_KEY:
            logger.info("API key is configured")
        else:
            logger.warning("No API key provided")
        
        # Log authentication mode
        if config.AUTH_MODE == "supabase":
            logger.info(f"Auth mode: Supabase Auth (JWT) for user: {config.AUTH_USER}")
            logger.info(f"Supabase Auth URL: {config.SUPABASE_AUTH_URL}")
        elif config.AUTH_MODE == "basic":
            logger.info(f"Auth mode: Kong Basic Auth for user: {config.AUTH_USER}")
        else:
            logger.info("Auth mode: API Key only (no user authentication)")

        mcp.run(transport="stdio")

    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.exception(f"Error starting server: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
