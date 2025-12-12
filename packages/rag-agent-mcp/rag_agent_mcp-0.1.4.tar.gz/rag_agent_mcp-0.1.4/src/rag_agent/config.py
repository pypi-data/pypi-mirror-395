"""
Configuration module for RAG Agent MCP server.

Supports three authentication modes:
1. API Key mode (legacy): Only --api-key is provided
2. Kong Basic Auth mode: --user is NOT an email (e.g., "supabase")
3. Supabase Auth mode: --user IS an email (e.g., "user@example.com")

Authentication type is automatically determined by checking if --user contains "@":
- Contains "@" → Supabase Auth (JWT token)
- Does not contain "@" → Kong Basic Auth (HTTP Basic Authentication)
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
# - "none": No user authentication (API Key only)
# - "basic": Kong Basic Auth (user is not email)
# - "supabase": Supabase Auth JWT (user is email)
def _is_email(value: str) -> bool:
    """Check if value looks like an email address."""
    if not value:
        return False
    # Simple email pattern check
    return "@" in value and "." in value.split("@")[-1]

if AUTH_USER and AUTH_USER_PASSWORD and LIGHTRAG_API_KEY:
    if _is_email(AUTH_USER):
        AUTH_MODE = "supabase"
    else:
        AUTH_MODE = "basic"
else:
    AUTH_MODE = "none"

# Legacy compatibility
SUPABASE_USER = AUTH_USER
SUPABASE_USER_PASSWORD = AUTH_USER_PASSWORD
SUPABASE_AUTH_ENABLED = AUTH_MODE == "supabase"
BASIC_AUTH_ENABLED = AUTH_MODE == "basic"

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
