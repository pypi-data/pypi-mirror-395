"""TikTok post manager for handling video post operations."""

import logging
from typing import Any

from marqetive.core.base_manager import BasePostManager
from marqetive.platforms.models import AuthCredentials, Post, PostCreateRequest
from marqetive.platforms.tiktok.client import TikTokClient
from marqetive.platforms.tiktok.factory import TikTokAccountFactory

logger = logging.getLogger(__name__)


class TikTokPostManager(BasePostManager):
    """Manager for TikTok video post operations.

    This manager coordinates the multi-step process of posting a video to
    TikTok, including media upload, processing, and the final publishing step.
    It provides progress tracking throughout the operation.
    """

    def __init__(
        self,
        account_factory: TikTokAccountFactory | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> None:
        """Initialize the TikTok post manager.

        Args:
            account_factory: An instance of TikTokAccountFactory. If not provided,
                             a default one will be created.
            client_id: TikTok App client ID (for the default factory).
            client_secret: TikTok App client secret (for the default factory).
        """
        if account_factory is None:
            account_factory = TikTokAccountFactory(
                client_id=client_id,
                client_secret=client_secret,
            )
        super().__init__(account_factory=account_factory)

    @property
    def platform_name(self) -> str:
        """Get the platform name."""
        return "tiktok"

    async def _execute_post_impl(
        self,
        client: Any,
        request: PostCreateRequest,
        credentials: AuthCredentials,  # noqa: ARG002
    ) -> Post:
        """Execute the TikTok video post creation process.

        Args:
            client: An authenticated TikTokClient instance.
            request: The post creation request.
            credentials: The credentials used for authentication.

        Returns:
            The created Post object representing the TikTok video.

        Raises:
            TypeError: If the provided client is not a TikTokClient.
            InterruptedError: If the operation is cancelled.
        """
        if not isinstance(client, TikTokClient):
            raise TypeError(f"Expected TikTokClient, got {type(client)}")

        # The TikTok posting process is primarily about the video upload.
        # The client's create_post method handles the upload and publish steps.
        # We can wrap it here to provide progress updates.

        self._progress_tracker.emit_start(
            "execute_post", total=100, message="Starting TikTok post..."
        )

        if self.is_cancelled():
            raise InterruptedError("Post creation was cancelled before start.")

        # Media upload progress can be tracked inside the client, but for simplicity,
        # we'll emit high-level progress here.
        self._progress_tracker.emit_progress(
            "execute_post",
            progress=10,
            total=100,
            message="Uploading video to TikTok...",
        )

        # The `create_post` method in the client will handle the full flow:
        # 1. Upload media
        # 2. Publish post
        # 3. Fetch final post data
        # A more advanced implementation might involve callbacks from the client
        # to the manager for more granular progress updates.
        post = await client.create_post(request)

        if self.is_cancelled():
            # If cancellation happened during the client call, we might need cleanup.
            # For now, we just raise.
            raise InterruptedError("Post creation was cancelled during execution.")

        self._progress_tracker.emit_progress(
            "execute_post",
            progress=90,
            total=100,
            message="Finalizing post...",
        )

        self._progress_tracker.emit_complete(
            "execute_post", message="TikTok post published successfully!"
        )

        return post
