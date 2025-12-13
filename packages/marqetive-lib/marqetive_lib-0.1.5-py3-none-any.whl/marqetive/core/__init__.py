"""Core functionality for MarqetiveLib."""

from marqetive.core.base import ProgressCallback, SocialMediaPlatform
from marqetive.core.client import APIClient
from marqetive.core.exceptions import (
    InvalidFileTypeError,
    MediaUploadError,
    PlatformAuthError,
    PlatformError,
    PostNotFoundError,
    RateLimitError,
    ValidationError,
)
from marqetive.core.models import (
    AccountStatus,
    AuthCredentials,
    Comment,
    CommentStatus,
    MediaAttachment,
    MediaType,
    PlatformResponse,
    Post,
    PostCreateRequest,
    PostStatus,
    PostUpdateRequest,
)

__all__ = [
    # Client
    "APIClient",
    # Base class
    "SocialMediaPlatform",
    "ProgressCallback",
    # Models
    "AccountStatus",
    "AuthCredentials",
    "Comment",
    "CommentStatus",
    "MediaAttachment",
    "MediaType",
    "PlatformResponse",
    "Post",
    "PostCreateRequest",
    "PostStatus",
    "PostUpdateRequest",
    # Exceptions
    "InvalidFileTypeError",
    "MediaUploadError",
    "PlatformAuthError",
    "PlatformError",
    "PostNotFoundError",
    "RateLimitError",
    "ValidationError",
]
