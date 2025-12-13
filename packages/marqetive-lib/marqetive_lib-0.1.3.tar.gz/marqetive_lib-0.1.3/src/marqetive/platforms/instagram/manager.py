"""Instagram post manager for handling post operations."""

import logging
from typing import Any

from marqetive.core.base_manager import BasePostManager
from marqetive.platforms.instagram.client import InstagramClient
from marqetive.platforms.instagram.factory import InstagramAccountFactory
from marqetive.platforms.models import AuthCredentials, Post, PostCreateRequest

logger = logging.getLogger(__name__)


class InstagramPostManager(BasePostManager):
    """Manager for Instagram post operations.

    Coordinates post creation, media uploads, and progress tracking for Instagram.

    Example:
        >>> manager = InstagramPostManager()
        >>> credentials = AuthCredentials(
        ...     platform="instagram",
        ...     access_token="token",
        ...     additional_data={"instagram_business_account_id": "123"}
        ... )
        >>> request = PostCreateRequest(content="Hello Instagram!")
        >>> post = await manager.execute_post(credentials, request)
        >>> print(f"Media ID: {post.post_id}")
    """

    def __init__(
        self,
        account_factory: InstagramAccountFactory | None = None,
    ) -> None:
        """Initialize Instagram post manager.

        Args:
            account_factory: Instagram account factory (creates default if None).
        """
        if account_factory is None:
            account_factory = InstagramAccountFactory()

        super().__init__(account_factory=account_factory)

    @property
    def platform_name(self) -> str:
        """Get platform name."""
        return "instagram"

    async def _execute_post_impl(
        self,
        client: Any,
        request: PostCreateRequest,
        credentials: AuthCredentials,  # noqa: ARG002
    ) -> Post:
        """Execute Instagram post creation.

        Args:
            client: InstagramClient instance.
            request: Post creation request.
            credentials: Instagram credentials.

        Returns:
            Created Post object.
        """
        if not isinstance(client, InstagramClient):
            raise TypeError(f"Expected InstagramClient, got {type(client)}")

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
            message="Creating Instagram post...",
        )

        # Use the client to create the post
        post = await client.create_post(request)

        return post
