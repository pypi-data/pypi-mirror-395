"""Twitter post manager for handling post operations."""

import logging
from typing import Any

from marqetive.core.base_manager import BasePostManager
from marqetive.platforms.models import AuthCredentials, Post, PostCreateRequest
from marqetive.platforms.twitter.client import TwitterClient
from marqetive.platforms.twitter.factory import TwitterAccountFactory

logger = logging.getLogger(__name__)


class TwitterPostManager(BasePostManager):
    """Manager for Twitter/X post operations.

    Coordinates post creation, media uploads, and progress tracking for Twitter.

    Example:
        >>> manager = TwitterPostManager()
        >>> credentials = AuthCredentials(
        ...     platform="twitter",
        ...     access_token="token",
        ...     refresh_token="refresh"
        ... )
        >>> request = PostCreateRequest(content="Hello Twitter!")
        >>> post = await manager.execute_post(credentials, request)
        >>> print(f"Tweet ID: {post.post_id}")
    """

    def __init__(
        self,
        account_factory: TwitterAccountFactory | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> None:
        """Initialize Twitter post manager.

        Args:
            account_factory: Twitter account factory (creates default if None).
            client_id: Twitter OAuth client ID (for default factory).
            client_secret: Twitter OAuth client secret (for default factory).
        """
        if account_factory is None:
            account_factory = TwitterAccountFactory(
                client_id=client_id,
                client_secret=client_secret,
            )

        super().__init__(account_factory=account_factory)

    @property
    def platform_name(self) -> str:
        """Get platform name."""
        return "twitter"

    async def _execute_post_impl(
        self,
        client: Any,
        request: PostCreateRequest,
        credentials: AuthCredentials,  # noqa: ARG002
    ) -> Post:
        """Execute Twitter post creation.

        Args:
            client: TwitterClient instance.
            request: Post creation request.
            credentials: Twitter credentials.

        Returns:
            Created Post object.
        """
        if not isinstance(client, TwitterClient):
            raise TypeError(f"Expected TwitterClient, got {type(client)}")

        # Handle media uploads with progress tracking
        media_ids: list[str] = []
        if request.media_urls:
            self._progress_tracker.emit_start(
                "upload_media",
                total=len(request.media_urls),
                message=f"Uploading {len(request.media_urls)} media files...",
            )

            for idx, media_url in enumerate(request.media_urls):
                if self.is_cancelled():
                    raise InterruptedError("Post creation was cancelled")

                self._progress_tracker.emit_progress(
                    "upload_media",
                    progress=idx,
                    total=len(request.media_urls),
                    message=f"Uploading media {idx + 1}/{len(request.media_urls)}...",
                )

                # Twitter media upload is simplified in the client
                # In production, this would use tweepy's media upload
                media_attachment = await client.upload_media(
                    media_url=media_url,
                    media_type="image",  # Default to image
                    alt_text=None,
                )
                media_ids.append(media_attachment.media_id)

            self._progress_tracker.emit_complete(
                "upload_media",
                message="All media uploaded successfully",
            )

        # Create post with progress tracking
        self._progress_tracker.emit_progress(
            "execute_post",
            progress=50,
            total=100,
            message="Creating tweet...",
        )

        # Use the client to create the post
        post = await client.create_post(request)

        return post
