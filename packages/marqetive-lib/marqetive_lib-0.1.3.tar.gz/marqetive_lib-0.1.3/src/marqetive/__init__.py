"""MarqetiveLib: Modern Python utilities for web APIs and social media platforms.

A comprehensive library providing utilities for working with web APIs,
HTTP requests, data processing, and social media platform integrations.

Usage:
    Basic API client:
        >>> from marqetive import APIClient
        >>> async with APIClient(base_url="https://api.example.com") as client:
        ...     response = await client.get("/endpoint")

    Platform managers (high-level):
        >>> from marqetive import initialize_platform_registry, get_manager_for_platform
        >>> from marqetive.platforms.models import AuthCredentials, PostCreateRequest
        >>>
        >>> initialize_platform_registry()
        >>> manager = get_manager_for_platform("twitter")
        >>> credentials = AuthCredentials(platform="twitter", access_token="...")
        >>> request = PostCreateRequest(content="Hello!")
        >>> post = await manager.execute_post(credentials, request)

    Platform clients (low-level):
        >>> from marqetive.platforms.twitter import TwitterClient
        >>> credentials = AuthCredentials(platform="twitter", access_token="...")
        >>> async with TwitterClient(credentials) as client:
        ...     post = await client.create_post(request)
"""

# Core API client
# Account management
from marqetive.core.account_factory import BaseAccountFactory

# Registry and managers
from marqetive.core.base_manager import BasePostManager
from marqetive.core.client import APIClient

# Progress tracking
from marqetive.core.progress import (
    ProgressCallback,
    ProgressEvent,
    ProgressStatus,
    ProgressTracker,
)
from marqetive.core.registry import (
    PlatformRegistry,
    get_available_platforms,
    get_manager_for_platform,
    get_registry,
    register_platform,
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
from marqetive.registry_init import (
    initialize_platform_registry,
    is_registry_initialized,
)

# Utilities
from marqetive.utils.helpers import format_response

# Retry utilities
from marqetive.utils.retry import STANDARD_BACKOFF, BackoffConfig, retry_async

__version__ = "0.1.0"

__all__ = [
    # Core
    "APIClient",
    "format_response",
    # Registry
    "PlatformRegistry",
    "initialize_platform_registry",
    "is_registry_initialized",
    "get_registry",
    "register_platform",
    "get_manager_for_platform",
    "get_available_platforms",
    # Managers and factories
    "BasePostManager",
    "BaseAccountFactory",
    # Progress tracking
    "ProgressEvent",
    "ProgressStatus",
    "ProgressTracker",
    "ProgressCallback",
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
]
