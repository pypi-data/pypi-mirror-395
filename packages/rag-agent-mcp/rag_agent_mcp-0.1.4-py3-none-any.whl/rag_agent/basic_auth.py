"""
Basic Auth module for RAG Agent MCP server.

This module handles HTTP Basic Authentication for Kong gateway.
"""

import base64
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class BasicAuthClient:
    """Client for HTTP Basic Authentication.
    
    Generates Authorization header for Kong gateway authentication.
    """
    
    user: str
    password: str
    
    def __post_init__(self):
        """Initialize Basic Auth client."""
        logger.info(f"Initialized Basic Auth client for user: {self.user}")
    
    @property
    def authorization_header(self) -> str:
        """Get the Authorization header value for Basic Auth.
        
        Returns:
            str: Authorization header value (e.g., "Basic dXNlcjpwYXNz")
        """
        credentials = f"{self.user}:{self.password}"
        encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        return f"Basic {encoded}"
    
    def get_headers(self) -> dict:
        """Get headers dict with Authorization.
        
        Returns:
            dict: Headers dictionary with Authorization
        """
        return {"Authorization": self.authorization_header}
    
    async def close(self) -> None:
        """Clean up resources (no-op for Basic Auth)."""
        logger.info("Basic Auth client closed")
