"""
Admin Authentication Module

This module provides authentication functionality for the admin panel,
including password verification with constant-time comparison and
token-based session management.

Requirements: 2.1, 2.2, 2.3, 2.5
"""

import hashlib
import logging
import os
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .admin_models import AdminAuthResponse


logger = logging.getLogger(__name__)

# Token configuration
TOKEN_EXPIRY_HOURS = 24
TOKEN_PREFIX = "admin_"

# Security scheme for admin endpoints
admin_bearer_security = HTTPBearer(auto_error=False)

# In-memory token store (in production, consider using Redis or similar)
# Format: {token_hash: {"expires_at": datetime, "created_at": datetime}}
_admin_tokens: dict[str, dict[str, datetime]] = {}


def _get_admin_password() -> str:
    """
    Retrieve the admin password from environment variable.

    Returns:
        The configured admin password, or a default value if not set.
    """
    return os.environ.get("ADMIN_PASSWORD", "admin123")


def verify_admin_password(password: str) -> bool:
    """
    Verify the provided password against the configured admin password.

    Uses constant-time comparison to prevent timing attacks.

    Args:
        password: The password to verify.

    Returns:
        True if the password matches, False otherwise.

    Requirements: 2.2, 2.5
    """
    admin_password = _get_admin_password()

    # Use secrets.compare_digest for constant-time comparison
    # to prevent timing attacks
    is_valid = secrets.compare_digest(password.encode("utf-8"), admin_password.encode("utf-8"))

    if is_valid:
        logger.info("[ADMIN AUTH] Password verification successful")
    else:
        logger.warning("[ADMIN AUTH] Password verification failed")

    return is_valid


def create_admin_token() -> AdminAuthResponse:
    """
    Create a new admin session token.

    Generates a cryptographically secure token and stores it with
    an expiration timestamp.

    Returns:
        AdminAuthResponse with the token and expiration details.

    Requirements: 2.2
    """
    # Generate a secure random token
    raw_token = secrets.token_urlsafe(32)
    token = f"{TOKEN_PREFIX}{raw_token}"

    # Calculate expiration time
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=TOKEN_EXPIRY_HOURS)

    # Store token hash (not the raw token) for security
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    _admin_tokens[token_hash] = {
        "expires_at": expires_at,
        "created_at": now,
    }

    logger.info(f"[ADMIN AUTH] Created new admin token, expires at {expires_at.isoformat()}")

    # Clean up expired tokens periodically
    _cleanup_expired_tokens()

    return AdminAuthResponse(
        success=True,
        token=token,
        expires_at=expires_at,
    )


def validate_admin_token(token: str) -> bool:
    """
    Validate an admin session token.

    Checks if the token exists and has not expired.

    Args:
        token: The token to validate.

    Returns:
        True if the token is valid and not expired, False otherwise.

    Requirements: 2.4
    """
    if not token:
        return False

    # Hash the token to look it up
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()

    token_data = _admin_tokens.get(token_hash)
    if not token_data:
        logger.debug("[ADMIN AUTH] Token not found in store")
        return False

    # Check expiration
    now = datetime.now(timezone.utc)
    if now >= token_data["expires_at"]:
        logger.info("[ADMIN AUTH] Token has expired")
        # Remove expired token
        del _admin_tokens[token_hash]
        return False

    logger.debug("[ADMIN AUTH] Token validation successful")
    return True


def invalidate_admin_token(token: str) -> bool:
    """
    Invalidate (logout) an admin session token.

    Args:
        token: The token to invalidate.

    Returns:
        True if the token was found and removed, False otherwise.

    Requirements: 2.4
    """
    if not token:
        return False

    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()

    if token_hash in _admin_tokens:
        del _admin_tokens[token_hash]
        logger.info("[ADMIN AUTH] Admin token invalidated (logout)")
        return True

    return False


def _cleanup_expired_tokens() -> None:
    """
    Remove expired tokens from the store.

    This is called periodically during token creation to prevent
    memory buildup from expired tokens.
    """
    now = datetime.now(timezone.utc)
    expired_hashes = [
        token_hash for token_hash, data in _admin_tokens.items() if now >= data["expires_at"]
    ]

    for token_hash in expired_hashes:
        del _admin_tokens[token_hash]

    if expired_hashes:
        logger.debug(f"[ADMIN AUTH] Cleaned up {len(expired_hashes)} expired token(s)")


async def get_admin_user(
    bearer_credentials: HTTPAuthorizationCredentials | None = Depends(admin_bearer_security),
) -> str:
    """
    FastAPI dependency to validate admin authentication.

    This dependency should be used on admin endpoints that require
    authentication (all except /status and /auth/verify).

    Args:
        bearer_credentials: The Bearer token from the Authorization header.

    Returns:
        A string identifier for the authenticated admin user.

    Raises:
        HTTPException: 401 if authentication fails.

    Requirements: 7.1
    """
    if not bearer_credentials:
        logger.warning("[ADMIN AUTH] No authorization credentials provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = bearer_credentials.credentials

    if not validate_admin_token(token):
        logger.warning("[ADMIN AUTH] Invalid or expired admin token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired admin token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return "admin"


def authenticate_admin(password: str) -> AdminAuthResponse:
    """
    Authenticate an admin user with password and return a session token.

    This is the main entry point for admin authentication, combining
    password verification and token creation.

    Args:
        password: The admin password to verify.

    Returns:
        AdminAuthResponse with success status and token if authenticated.

    Requirements: 2.1, 2.2, 2.3
    """
    if verify_admin_password(password):
        return create_admin_token()

    return AdminAuthResponse(
        success=False,
        token=None,
        expires_at=None,
    )
