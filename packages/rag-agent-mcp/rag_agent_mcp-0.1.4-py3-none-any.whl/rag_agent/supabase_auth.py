"""
Supabase Auth module for RAG Agent MCP server.

This module handles:
- User login with email/password via Supabase Auth API
- JWT token management (storage, retrieval)
- Automatic token refresh before expiration
"""

import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Optional, Tuple

import httpx

logger = logging.getLogger(__name__)


@dataclass
class AuthToken:
    """Represents a Supabase Auth token pair."""
    access_token: str
    refresh_token: str
    expires_at: float  # Unix timestamp
    user_id: Optional[str] = None
    email: Optional[str] = None


class SupabaseAuthClient:
    """Client for Supabase Auth operations.
    
    Handles user authentication and token lifecycle management.
    """
    
    # Refresh token 5 minutes before expiration
    TOKEN_REFRESH_BUFFER_SECONDS = 300
    
    def __init__(
        self,
        auth_url: str,
        anon_key: str,
        user: str,
        password: str,
    ):
        """Initialize Supabase Auth client.
        
        Args:
            auth_url: Supabase Auth API URL (e.g., https://xxx.supabase.co/auth/v1)
            anon_key: Supabase anon key
            user: User email or username
            password: User password
        """
        self.auth_url = auth_url.rstrip("/")
        self.anon_key = anon_key
        self.user = user
        self.password = password
        self._token: Optional[AuthToken] = None
        self._refresh_task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()
        
        logger.info(f"Initialized Supabase Auth client for user: {user}")
    
    @property
    def is_authenticated(self) -> bool:
        """Check if client has a valid token."""
        return self._token is not None and not self._is_token_expired()
    
    @property
    def access_token(self) -> Optional[str]:
        """Get current access token."""
        return self._token.access_token if self._token else None
    
    def _is_token_expired(self) -> bool:
        """Check if current token is expired or about to expire."""
        if not self._token:
            return True
        return time.time() >= (self._token.expires_at - self.TOKEN_REFRESH_BUFFER_SECONDS)
    
    async def login(self) -> AuthToken:
        """Login with email/password and obtain tokens.
        
        Returns:
            AuthToken: Token information
            
        Raises:
            httpx.HTTPStatusError: If login fails
        """
        url = f"{self.auth_url}/token?grant_type=password"
        
        headers = {
            "apikey": self.anon_key,
            "Content-Type": "application/json",
        }
        
        payload = {
            "email": self.user,
            "password": self.password,
        }
        
        logger.info(f"Attempting Supabase Auth login for user: {self.user}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers,
                timeout=30.0,
            )
            
            if response.status_code != 200:
                error_detail = response.text
                logger.error(f"Login failed with status {response.status_code}: {error_detail}")
                response.raise_for_status()
            
            data = response.json()
            
            # Calculate expiration time
            expires_in = data.get("expires_in", 3600)  # Default 1 hour
            expires_at = time.time() + expires_in
            
            # Extract user info
            user_data = data.get("user", {})
            
            self._token = AuthToken(
                access_token=data["access_token"],
                refresh_token=data.get("refresh_token", ""),
                expires_at=expires_at,
                user_id=user_data.get("id"),
                email=user_data.get("email"),
            )
            
            logger.info(f"Login successful. User ID: {self._token.user_id}, expires in {expires_in}s")
            
            return self._token
    
    async def refresh(self) -> AuthToken:
        """Refresh the access token using refresh token.
        
        Returns:
            AuthToken: New token information
            
        Raises:
            httpx.HTTPStatusError: If refresh fails
        """
        if not self._token or not self._token.refresh_token:
            logger.warning("No refresh token available, performing full login")
            return await self.login()
        
        url = f"{self.auth_url}/token?grant_type=refresh_token"
        
        headers = {
            "apikey": self.anon_key,
            "Content-Type": "application/json",
        }
        
        payload = {
            "refresh_token": self._token.refresh_token,
        }
        
        logger.info("Attempting to refresh Supabase Auth token")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers,
                timeout=30.0,
            )
            
            if response.status_code != 200:
                logger.warning(f"Token refresh failed with status {response.status_code}, performing full login")
                return await self.login()
            
            data = response.json()
            
            # Calculate expiration time
            expires_in = data.get("expires_in", 3600)
            expires_at = time.time() + expires_in
            
            # Extract user info
            user_data = data.get("user", {})
            
            self._token = AuthToken(
                access_token=data["access_token"],
                refresh_token=data.get("refresh_token", self._token.refresh_token),
                expires_at=expires_at,
                user_id=user_data.get("id", self._token.user_id),
                email=user_data.get("email", self._token.email),
            )
            
            logger.info(f"Token refreshed successfully, expires in {expires_in}s")
            
            return self._token
    
    async def ensure_valid_token(self) -> str:
        """Ensure we have a valid access token, refreshing if necessary.
        
        Returns:
            str: Valid access token
        """
        async with self._lock:
            if not self._token:
                await self.login()
            elif self._is_token_expired():
                await self.refresh()
            
            return self._token.access_token
    
    async def start_auto_refresh(self) -> None:
        """Start background task to auto-refresh token before expiration."""
        if self._refresh_task and not self._refresh_task.done():
            logger.debug("Auto-refresh task already running")
            return
        
        async def refresh_loop():
            while True:
                try:
                    if self._token:
                        # Calculate time until we should refresh
                        time_until_refresh = (
                            self._token.expires_at 
                            - time.time() 
                            - self.TOKEN_REFRESH_BUFFER_SECONDS
                        )
                        
                        if time_until_refresh > 0:
                            logger.debug(f"Next token refresh in {time_until_refresh:.0f}s")
                            await asyncio.sleep(time_until_refresh)
                        
                        # Refresh token
                        await self.ensure_valid_token()
                    else:
                        # No token yet, wait a bit and check again
                        await asyncio.sleep(60)
                        
                except asyncio.CancelledError:
                    logger.info("Auto-refresh task cancelled")
                    break
                except Exception as e:
                    logger.error(f"Error in auto-refresh loop: {e}")
                    # Wait before retrying
                    await asyncio.sleep(60)
        
        self._refresh_task = asyncio.create_task(refresh_loop())
        logger.info("Started auto-refresh background task")
    
    async def stop_auto_refresh(self) -> None:
        """Stop the auto-refresh background task."""
        if self._refresh_task:
            self._refresh_task.cancel()
            try:
                await self._refresh_task
            except asyncio.CancelledError:
                pass
            self._refresh_task = None
            logger.info("Stopped auto-refresh background task")
    
    async def close(self) -> None:
        """Clean up resources."""
        await self.stop_auto_refresh()
        self._token = None
        logger.info("Supabase Auth client closed")
