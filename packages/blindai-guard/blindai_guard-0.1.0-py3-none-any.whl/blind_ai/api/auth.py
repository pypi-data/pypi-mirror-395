"""Authentication middleware for Blind AI API.

Provides API key validation for SaaS mode.
"""

import os
import secrets
from typing import Optional

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

# API key header name
API_KEY_HEADER = "X-API-Key"

# Environment variable for valid API keys (comma-separated for multiple keys)
API_KEYS_ENV = "BLIND_AI_API_KEYS"

# Header security scheme
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)


def get_api_keys() -> set[str]:
    """Get valid API keys from environment.
    
    Returns:
        Set of valid API keys
    """
    keys_str = os.getenv(API_KEYS_ENV, "")
    if not keys_str:
        return set()
    return {k.strip() for k in keys_str.split(",") if k.strip()}


def is_auth_enabled() -> bool:
    """Check if authentication is enabled.
    
    Auth is enabled if BLIND_AI_API_KEYS environment variable is set.
    
    Returns:
        True if auth is required
    """
    return bool(os.getenv(API_KEYS_ENV))


async def verify_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """Verify API key from request header.
    
    Args:
        api_key: API key from X-API-Key header
        
    Returns:
        Validated API key
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    # Skip auth if not enabled (local/dev mode)
    if not is_auth_enabled():
        return "local-mode"
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Include 'X-API-Key' header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    valid_keys = get_api_keys()
    
    # Constant-time comparison to prevent timing attacks
    key_valid = any(secrets.compare_digest(api_key, valid_key) for valid_key in valid_keys)
    
    if not key_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return api_key


def generate_api_key(prefix: str = "blind_") -> str:
    """Generate a new API key.
    
    Args:
        prefix: Prefix for the API key
        
    Returns:
        New API key in format: prefix + 32 random hex chars
    """
    return f"{prefix}{secrets.token_hex(16)}"
