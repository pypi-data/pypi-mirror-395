"""Base manager for platform post operations.

This module provides an abstract base class for managing post operations
across different social media platforms with consistent patterns for
progress tracking, error handling, and state management.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any

from marqetive.core.account_factory import BaseAccountFactory
from marqetive.core.progress import ProgressCallback, ProgressTracker
from marqetive.platforms.exceptions import PlatformError
from marqetive.platforms.models import AuthCredentials, Post, PostCreateRequest

logger = logging.getLogger(__name__)


class BasePostManager(ABC):
    """Abstract base class for platform post managers.

    Managers coordinate the posting process including:
    - Creating authenticated clients via account factories
    - Tracking operation progress
    - Handling errors consistently
    - Supporting cancellation

    Subclasses must implement:
    - _execute_post_impl(): Platform-specific posting logic
    - platform_name: Property returning the platform name

    Example:
        >>> class TwitterPostManager(BasePostManager):
        ...     @property
        ...     def platform_name(self) -> str:
        ...         return "twitter"
        ...
        ...     async def _execute_post_impl(self, client, request):
        ...         return await client.create_post(request)
    """

    def __init__(
        self,
        account_factory: BaseAccountFactory | None = None,
    ) -> None:
        """Initialize the post manager.

        Args:
            account_factory: Account factory for creating clients.
                            If None, subclass must provide default.
        """
        self._account_factory = account_factory
        self._progress_tracker = ProgressTracker()
        self._cancel_event = asyncio.Event()

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Get the name of the platform this manager handles.

        Returns:
            Platform name (e.g., "twitter", "linkedin").
        """
        pass

    @property
    def account_factory(self) -> BaseAccountFactory:
        """Get the account factory.

        Returns:
            Account factory instance.

        Raises:
            RuntimeError: If account factory not set.
        """
        if self._account_factory is None:
            raise RuntimeError(
                f"{self.__class__.__name__} requires an account_factory. "
                "Either pass it to __init__ or override this property."
            )
        return self._account_factory

    def add_progress_callback(self, callback: ProgressCallback) -> None:
        """Add a callback to receive progress updates.

        Args:
            callback: Function that receives ProgressEvent objects.

        Example:
            >>> def my_callback(event):
            ...     print(f"{event.operation}: {event.percentage}%")
            >>>
            >>> manager.add_progress_callback(my_callback)
        """
        self._progress_tracker.add_callback(callback)

    def remove_progress_callback(self, callback: ProgressCallback) -> None:
        """Remove a progress callback.

        Args:
            callback: Callback to remove.
        """
        self._progress_tracker.remove_callback(callback)

    def clear_progress_callbacks(self) -> None:
        """Remove all progress callbacks."""
        self._progress_tracker.clear_callbacks()

    async def execute_post(
        self,
        credentials: AuthCredentials,
        request: PostCreateRequest,
    ) -> Post:
        """Execute post creation with progress tracking and error handling.

        This is the main entry point for creating posts. It handles:
        - Client creation via account factory
        - Progress tracking
        - Cancellation support
        - Consistent error handling

        Args:
            credentials: Platform credentials.
            request: Post creation request.

        Returns:
            Created Post object.

        Raises:
            PlatformError: If post creation fails.
            asyncio.CancelledError: If operation is cancelled.

        Example:
            >>> credentials = AuthCredentials(platform="twitter", ...)
            >>> request = PostCreateRequest(content="Hello world!")
            >>> post = await manager.execute_post(credentials, request)
            >>> print(f"Posted: {post.post_id}")
        """
        # Reset cancel event
        self._cancel_event.clear()

        try:
            # Emit start event
            self._progress_tracker.emit_start(
                "execute_post",
                message=f"Starting post to {self.platform_name}",
                platform=self.platform_name,
            )

            # Check for cancellation
            if self._cancel_event.is_set():
                self._progress_tracker.emit_cancelled("execute_post")
                raise asyncio.CancelledError("Post execution was cancelled")

            # Create authenticated client
            logger.info(f"Creating {self.platform_name} client...")
            client = await self.account_factory.create_authenticated_client(credentials)

            # Check for cancellation
            if self._cancel_event.is_set():
                self._progress_tracker.emit_cancelled("execute_post")
                raise asyncio.CancelledError("Post execution was cancelled")

            # Execute platform-specific posting logic
            logger.info(f"Creating post on {self.platform_name}...")
            post = await self._execute_post_impl(client, request, credentials)

            # Emit completion event
            self._progress_tracker.emit_complete(
                "execute_post",
                message=f"Post created successfully on {self.platform_name}",
                post_id=post.post_id,
                platform=self.platform_name,
            )

            logger.info(
                f"Successfully created post {post.post_id} on {self.platform_name}"
            )
            return post

        except asyncio.CancelledError:
            self._progress_tracker.emit_cancelled(
                "execute_post",
                message=f"Post creation cancelled on {self.platform_name}",
            )
            raise

        except Exception as e:
            error_msg = f"Failed to create post on {self.platform_name}: {str(e)}"
            logger.error(error_msg)
            self._progress_tracker.emit_failed("execute_post", e)

            # Wrap in PlatformError if not already
            if not isinstance(e, PlatformError):
                raise PlatformError(error_msg, platform=self.platform_name) from e
            raise

    @abstractmethod
    async def _execute_post_impl(
        self,
        client: Any,
        request: PostCreateRequest,
        credentials: AuthCredentials,
    ) -> Post:
        """Platform-specific post creation implementation.

        Subclasses must implement this to handle the actual post creation
        logic for their specific platform.

        Args:
            client: Platform-specific authenticated client.
            request: Post creation request.
            credentials: Platform credentials (for context).

        Returns:
            Created Post object.

        Raises:
            PlatformError: If post creation fails.
        """
        pass

    def cancel_post(self) -> None:
        """Cancel the current post operation.

        Sets a cancellation flag that is checked at key points during
        post execution. The operation may not stop immediately.

        Example:
            >>> task = asyncio.create_task(manager.execute_post(...))
            >>> # Later...
            >>> manager.cancel_post()
            >>> try:
            ...     await task
            ... except asyncio.CancelledError:
            ...     print("Operation was cancelled")
        """
        self._cancel_event.set()
        logger.info(f"Cancellation requested for {self.platform_name} post")

    def is_cancelled(self) -> bool:
        """Check if cancellation has been requested.

        Returns:
            True if cancel_post() was called, False otherwise.
        """
        return self._cancel_event.is_set()

    async def get_post_status(
        self,
        credentials: AuthCredentials,
        post_id: str,
    ) -> Post:
        """Get the current status of a post.

        Args:
            credentials: Platform credentials.
            post_id: Platform-specific post ID.

        Returns:
            Post object with current status.

        Raises:
            PlatformError: If fetching post fails.
        """
        try:
            client = await self.account_factory.create_authenticated_client(credentials)
            return await client.get_post(post_id)
        except Exception as e:
            error_msg = f"Failed to get post status from {self.platform_name}: {str(e)}"
            logger.error(error_msg)
            if not isinstance(e, PlatformError):
                raise PlatformError(error_msg, platform=self.platform_name) from e
            raise

    async def delete_post(
        self,
        credentials: AuthCredentials,
        post_id: str,
    ) -> bool:
        """Delete a post.

        Args:
            credentials: Platform credentials.
            post_id: Platform-specific post ID.

        Returns:
            True if deletion was successful.

        Raises:
            PlatformError: If deletion fails.
        """
        try:
            client = await self.account_factory.create_authenticated_client(credentials)
            return await client.delete_post(post_id)
        except Exception as e:
            error_msg = f"Failed to delete post from {self.platform_name}: {str(e)}"
            logger.error(error_msg)
            if not isinstance(e, PlatformError):
                raise PlatformError(error_msg, platform=self.platform_name) from e
            raise
