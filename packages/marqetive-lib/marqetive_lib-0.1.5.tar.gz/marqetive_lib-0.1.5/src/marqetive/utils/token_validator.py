"""Token validation utilities for checking credential validity.

This module provides utilities for validating OAuth tokens and determining
if they need to be refreshed.
"""

import re
from datetime import datetime, timedelta
from typing import Any

from marqetive.core.models import AuthCredentials


def is_token_expired(
    expires_at: datetime | None,
    threshold_minutes: int = 5,
) -> bool:
    """Check if a token has expired or will expire soon.

    Args:
        expires_at: Token expiration timestamp.
        threshold_minutes: Consider expired if expires within this many minutes.

    Returns:
        True if token is expired or will expire soon, False otherwise.

    Example:
        >>> from datetime import datetime, timedelta
        >>> expires = datetime.now() + timedelta(minutes=3)
        >>> is_token_expired(expires, threshold_minutes=5)
        True
        >>> expires = datetime.now() + timedelta(hours=1)
        >>> is_token_expired(expires, threshold_minutes=5)
        False
    """
    if expires_at is None:
        # No expiry means token doesn't expire
        return False

    threshold = datetime.now() + timedelta(minutes=threshold_minutes)
    return expires_at <= threshold


def needs_refresh(
    credentials: AuthCredentials,
    threshold_minutes: int = 5,  # noqa: ARG001
) -> bool:
    """Check if credentials need to be refreshed.

    Args:
        credentials: Credentials to check.
        threshold_minutes: Expiry threshold in minutes.

    Returns:
        True if refresh is needed, False otherwise.

    Example:
        >>> creds = AuthCredentials(
        ...     platform="twitter",
        ...     access_token="token",
        ...     expires_at=datetime.now() + timedelta(minutes=2)
        ... )
        >>> needs_refresh(creds)
        True
    """
    return credentials.needs_refresh()


def validate_token_format(token: str, min_length: int = 10) -> bool:
    """Validate basic token format.

    Checks if token looks valid (not empty, meets minimum length).

    Args:
        token: Token string to validate.
        min_length: Minimum acceptable token length.

    Returns:
        True if token format is valid, False otherwise.

    Example:
        >>> validate_token_format("abc123xyz")
        False
        >>> validate_token_format("a" * 50)
        True
    """
    if not token or not isinstance(token, str):
        return False

    # Remove whitespace
    token = token.strip()

    # Check minimum length
    if len(token) < min_length:
        return False

    # Check for obviously invalid tokens
    return token.lower() not in ["none", "null", "undefined", ""]


def validate_bearer_token(token: str) -> bool:
    """Validate Bearer token format.

    Args:
        token: Bearer token to validate.

    Returns:
        True if token appears valid, False otherwise.

    Example:
        >>> validate_bearer_token("ya29.a0AfH6SMB...")
        True
        >>> validate_bearer_token("invalid")
        False
    """
    # Bearer tokens are typically base64-like strings
    if not validate_token_format(token, min_length=20):
        return False

    # Check for suspicious patterns
    return not re.search(r"[<>\"']", token)


def calculate_token_ttl(expires_at: datetime | None) -> timedelta | None:
    """Calculate time-to-live for a token.

    Args:
        expires_at: Token expiration timestamp.

    Returns:
        Time remaining until expiration, or None if no expiry.

    Example:
        >>> from datetime import datetime, timedelta
        >>> expires = datetime.now() + timedelta(hours=1)
        >>> ttl = calculate_token_ttl(expires)
        >>> ttl.total_seconds() > 3500  # Approximately 1 hour
        True
    """
    if expires_at is None:
        return None

    now = datetime.now()
    if expires_at <= now:
        return timedelta(0)

    return expires_at - now


def should_proactively_refresh(
    credentials: AuthCredentials,
    refresh_threshold_minutes: int = 5,
) -> bool:
    """Determine if token should be proactively refreshed.

    Checks if token will expire soon and if refresh token is available.

    Args:
        credentials: Credentials to check.
        refresh_threshold_minutes: Refresh if expires within this many minutes.

    Returns:
        True if should proactively refresh, False otherwise.

    Example:
        >>> creds = AuthCredentials(
        ...     platform="twitter",
        ...     access_token="token",
        ...     refresh_token="refresh",
        ...     expires_at=datetime.now() + timedelta(minutes=3)
        ... )
        >>> should_proactively_refresh(creds)
        True
    """
    # Need refresh token to refresh
    if not credentials.refresh_token:
        return False

    # Check if expiring soon
    return is_token_expired(credentials.expires_at, refresh_threshold_minutes)


def is_credentials_complete(credentials: AuthCredentials) -> bool:
    """Check if credentials have all required fields.

    Args:
        credentials: Credentials to validate.

    Returns:
        True if credentials are complete, False otherwise.

    Example:
        >>> creds = AuthCredentials(
        ...     platform="twitter",
        ...     access_token="token"
        ... )
        >>> is_credentials_complete(creds)
        True
    """
    # Must have platform and access token
    if not credentials.platform or not credentials.access_token:
        return False

    # Access token must be valid format
    return validate_token_format(credentials.access_token)


def get_token_health_status(credentials: AuthCredentials) -> dict[str, Any]:
    """Get comprehensive health status of credentials.

    Args:
        credentials: Credentials to analyze.

    Returns:
        Dictionary with health information.

    Example:
        >>> creds = AuthCredentials(
        ...     platform="twitter",
        ...     access_token="token",
        ...     expires_at=datetime.now() + timedelta(hours=1)
        ... )
        >>> status = get_token_health_status(creds)
        >>> status["is_valid"]
        True
        >>> status["needs_refresh"]
        False
    """
    ttl = calculate_token_ttl(credentials.expires_at)

    return {
        "is_valid": credentials.is_valid(),
        "is_expired": credentials.is_expired(),
        "needs_refresh": credentials.needs_refresh(),
        "has_refresh_token": credentials.refresh_token is not None,
        "time_to_expiry_seconds": ttl.total_seconds() if ttl else None,
        "should_proactively_refresh": should_proactively_refresh(credentials),
        "status": credentials.status.value,
        "is_complete": is_credentials_complete(credentials),
    }
