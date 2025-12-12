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

        # Print config to stderr for MCP inspector visibility
        print("=== RAG AGENT CONFIG ===", file=sys.stderr)
        print(f"Base URL: {config.LIGHTRAG_API_BASE_URL}", file=sys.stderr)
        print(f"API Key: {config.LIGHTRAG_API_KEY[:20]}...{config.LIGHTRAG_API_KEY[-10:] if config.LIGHTRAG_API_KEY else 'NOT SET'}", file=sys.stderr)
        print(f"Auth Mode: {config.AUTH_MODE}", file=sys.stderr)
        if config.AUTH_USER:
            print(f"Auth User: {config.AUTH_USER}", file=sys.stderr)
        print("=== END CONFIG ===", file=sys.stderr)
        
        logger.info("Starting RAG Agent MCP server")
        logger.info(
            f"RAG Agent API server is expected to be already running and available at: {config.LIGHTRAG_API_BASE_URL}"
        )
        if config.LIGHTRAG_API_KEY:
            logger.info("API key is configured")
        else:
            logger.warning("No API key provided")
        
        # Log authentication mode
        if config.AUTH_MODE == "jwt":
            logger.info(f"Auth mode: Anon Key + JWT for user: {config.AUTH_USER}")
            logger.info(f"Login URL: {config.SUPABASE_AUTH_URL.replace('/auth/v1', '/login')}")
        else:
            logger.info("Auth mode: Service Key (admin privileges)")

        mcp.run(transport="stdio")

    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.exception(f"Error starting server: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
