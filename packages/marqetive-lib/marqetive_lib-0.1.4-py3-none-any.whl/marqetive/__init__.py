"""MarqetiveLib: Modern Python utilities for web APIs and social media platforms.

A comprehensive library providing utilities for working with web APIs,
HTTP requests, data processing, and social media platform integrations.

Usage:
    Simple usage with factory:
        >>> from marqetive import get_client, AuthCredentials, PostCreateRequest
        >>> credentials = AuthCredentials(
        ...     platform="twitter",
        ...     access_token="...",
        ...     refresh_token="..."
        ... )
        >>> client = await get_client(credentials)
        >>> async with client:
        ...     post = await client.create_post(PostCreateRequest(content="Hello!"))

    Factory with custom OAuth credentials:
        >>> from marqetive import PlatformFactory, AuthCredentials
        >>> factory = PlatformFactory(
        ...     twitter_client_id="your_client_id",
        ...     twitter_client_secret="your_client_secret"
        ... )
        >>> client = await factory.get_client(credentials)

    Direct client usage:
        >>> from marqetive.platforms.twitter import TwitterClient
        >>> async with TwitterClient(credentials) as client:
        ...     post = await client.create_post(request)

    Basic API client:
        >>> from marqetive import APIClient
        >>> async with APIClient(base_url="https://api.example.com") as client:
        ...     response = await client.get("/endpoint")
"""

# Core API client
from marqetive.core.client import APIClient

# Factory
from marqetive.factory import PlatformFactory, get_client

# Progress callback type
from marqetive.platforms.base import ProgressCallback

# Exceptions
from marqetive.platforms.exceptions import (
    InvalidFileTypeError,
    MediaUploadError,
    PlatformAuthError,
    PlatformError,
    PostNotFoundError,
    RateLimitError,
    ValidationError,
)

# Models
from marqetive.platforms.models import (
    AccountStatus,
    AuthCredentials,
    Comment,
    CommentStatus,
    MediaAttachment,
    MediaType,
    Post,
    PostCreateRequest,
    PostStatus,
    PostUpdateRequest,
)

# Utilities
from marqetive.utils.helpers import format_response

# Retry utilities
from marqetive.utils.retry import STANDARD_BACKOFF, BackoffConfig, retry_async

__version__ = "0.2.0"

__all__ = [
    # Core
    "APIClient",
    # Factory
    "PlatformFactory",
    "get_client",
    # Retry
    "BackoffConfig",
    "STANDARD_BACKOFF",
    "retry_async",
    # Models
    "AuthCredentials",
    "AccountStatus",
    "Post",
    "PostStatus",
    "PostCreateRequest",
    "PostUpdateRequest",
    "Comment",
    "CommentStatus",
    "MediaAttachment",
    "MediaType",
    # Exceptions
    "PlatformError",
    "PlatformAuthError",
    "RateLimitError",
    "PostNotFoundError",
    "MediaUploadError",
    "ValidationError",
    "InvalidFileTypeError",
    # Types
    "ProgressCallback",
    # Utilities
    "format_response",
]
