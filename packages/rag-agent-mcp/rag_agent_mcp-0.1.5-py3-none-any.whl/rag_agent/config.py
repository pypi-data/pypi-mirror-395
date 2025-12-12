"""
Configuration module for RAG Agent MCP server.

Supports two authentication modes:
1. Service Key mode: Only --api-key is provided (admin privileges, no JWT needed)
2. Anon Key + JWT mode: --api-key (anon key) + --user + --user-password provided
   - Calls /login endpoint to obtain JWT token
   - User-level permissions

Authentication type is automatically determined:
- Only --api-key provided → Service Key mode (admin)
- --api-key + --user + --user-password provided → Anon Key + JWT mode (user-level)
"""

import argparse
import re
from urllib.parse import urlparse

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 9621
DEFAULT_API_KEY = ""


def parse_args():
    """Parse command line arguments for RAG Agent MCP server."""
    parser = argparse.ArgumentParser(description="RAG Agent MCP Server")
    parser.add_argument(
        "--host", 
        default=DEFAULT_HOST, 
        help=f"Supabase URL or RAG Agent API host (default: {DEFAULT_HOST})"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"API port (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--api-key", 
        default=DEFAULT_API_KEY, 
        help="Supabase anon key or RAG Agent API key (required)"
    )
    parser.add_argument(
        "--user",
        default=None,
        help="Supabase Auth user (email or username for admin)"
    )
    parser.add_argument(
        "--user-password",
        default=None,
        help="Supabase Auth user password"
    )
    return parser.parse_args()


args = parse_args()

# Basic configuration
LIGHTRAG_API_HOST = args.host
LIGHTRAG_API_PORT = args.port
LIGHTRAG_API_KEY = args.api_key

# User authentication configuration
AUTH_USER = args.user
AUTH_USER_PASSWORD = args.user_password

# Determine authentication mode
# - "service_key": Service Key mode (admin privileges, only api-key needed)
# - "jwt": Anon Key + JWT mode (user-level, requires login)
if AUTH_USER and AUTH_USER_PASSWORD and LIGHTRAG_API_KEY:
    # User credentials provided → JWT mode
    AUTH_MODE = "jwt"
else:
    # Only api-key provided → Service Key mode
    AUTH_MODE = "service_key"

# Legacy compatibility (for backward compatibility with existing code)
SUPABASE_USER = AUTH_USER
SUPABASE_USER_PASSWORD = AUTH_USER_PASSWORD
SUPABASE_AUTH_ENABLED = AUTH_MODE == "jwt"
BASIC_AUTH_ENABLED = False  # No longer used

# Build base URL
# If host starts with http:// or https://, use it directly (may already include port)
# Otherwise, construct the URL with scheme and port
if LIGHTRAG_API_HOST.startswith("http://") or LIGHTRAG_API_HOST.startswith("https://"):
    _base_host = LIGHTRAG_API_HOST.rstrip("/")
    # Check if host already contains a port (e.g., http://host:80)
    _parsed = urlparse(_base_host)
    _host_has_port = _parsed.port is not None
    
    if _host_has_port:
        # Host already has port, use as-is
        LIGHTRAG_API_BASE_URL = f"{_base_host}/rag/v1"
        SUPABASE_AUTH_URL = f"{_base_host}/auth/v1"
    elif LIGHTRAG_API_PORT in (80, 443):
        # Standard ports, don't append
        LIGHTRAG_API_BASE_URL = f"{_base_host}/rag/v1"
        SUPABASE_AUTH_URL = f"{_base_host}/auth/v1"
    else:
        # Append non-standard port
        LIGHTRAG_API_BASE_URL = f"{_base_host}:{LIGHTRAG_API_PORT}/rag/v1"
        SUPABASE_AUTH_URL = f"{_base_host}:{LIGHTRAG_API_PORT}/auth/v1"
else:
    LIGHTRAG_API_BASE_URL = f"http://{LIGHTRAG_API_HOST}:{LIGHTRAG_API_PORT}/rag/v1"
    SUPABASE_AUTH_URL = f"http://{LIGHTRAG_API_HOST}:{LIGHTRAG_API_PORT}/auth/v1"
