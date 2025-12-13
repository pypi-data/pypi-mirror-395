"""Instagram Graph API client implementation.

This module provides a concrete implementation of the SocialMediaPlatform
ABC for Instagram, using the Instagram Graph API.

API Documentation: https://developers.facebook.com/docs/instagram-api
"""

from datetime import datetime
from typing import Any, Literal, cast

import httpx
from pydantic import HttpUrl

from marqetive.platforms.base import ProgressCallback, SocialMediaPlatform
from marqetive.platforms.exceptions import (
    MediaUploadError,
    PlatformAuthError,
    PlatformError,
    PostNotFoundError,
    ValidationError,
)
from marqetive.platforms.instagram.media import (
    InstagramMediaManager,
    MediaItem,
)
from marqetive.platforms.models import (
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


class InstagramClient(SocialMediaPlatform):
    """Instagram Graph API client.

    This client implements the SocialMediaPlatform interface for Instagram,
    using the Instagram Graph API. It supports posts (feed posts), stories,
    and reels, along with comments and media management.

    Note:
        - Requires a Facebook App with Instagram Graph API permissions
        - Requires an Instagram Business or Creator account
        - Access tokens must have appropriate scopes (instagram_basic,
          instagram_content_publish, etc.)

    Example:
        >>> credentials = AuthCredentials(
        ...     platform="instagram",
        ...     access_token="your_token",
        ...     user_id="instagram_business_account_id"
        ... )
        >>> async with InstagramClient(credentials) as client:
        ...     request = PostCreateRequest(
        ...         content="Check out our new product!",
        ...         media_urls=["https://example.com/image.jpg"]
        ...     )
        ...     post = await client.create_post(request)
    """

    def __init__(
        self,
        credentials: AuthCredentials,
        timeout: float = 30.0,
        api_version: str = "v21.0",
        progress_callback: ProgressCallback | None = None,
    ) -> None:
        """Initialize Instagram client.

        Args:
            credentials: Instagram authentication credentials
            timeout: Request timeout in seconds
            api_version: Instagram Graph API version
            progress_callback: Optional callback for progress updates during
                long-running operations like media uploads.

        Raises:
            PlatformAuthError: If credentials are invalid
        """
        base_url = f"https://graph.instagram.com/{api_version}"
        super().__init__(
            platform_name="instagram",
            credentials=credentials,
            base_url=base_url,
            timeout=timeout,
            progress_callback=progress_callback,
        )
        self.instagram_account_id = credentials.user_id
        self.api_version = api_version

        # Media manager (initialized in __aenter__)
        self._media_manager: InstagramMediaManager | None = None

    async def __aenter__(self) -> "InstagramClient":
        """Async context manager entry."""
        await super().__aenter__()

        # Initialize media manager
        if not self.instagram_account_id:
            raise PlatformAuthError(
                "Instagram account ID (user_id) is required in credentials",
                platform=self.platform_name,
            )

        self._media_manager = InstagramMediaManager(
            ig_user_id=self.instagram_account_id,
            access_token=self.credentials.access_token,
            api_version=self.api_version,
            timeout=self.timeout,
        )

        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        # Cleanup media manager
        if self._media_manager:
            await self._media_manager.__aexit__(exc_type, exc_val, exc_tb)
            self._media_manager = None

        await super().__aexit__(exc_type, exc_val, exc_tb)

    # ==================== Authentication Methods ====================

    async def authenticate(self) -> AuthCredentials:
        """Perform Instagram authentication flow.

        Note: Instagram uses Facebook OAuth. This method assumes you already
        have a long-lived access token. For the full OAuth flow, use Facebook's
        OAuth implementation.

        Returns:
            Current credentials if valid.

        Raises:
            PlatformAuthError: If authentication fails.
        """
        if await self.is_authenticated():
            return self.credentials

        raise PlatformAuthError(
            "Invalid or expired credentials. Please re-authenticate via Facebook OAuth.",
            platform=self.platform_name,
        )

    async def refresh_token(self) -> AuthCredentials:
        """Refresh Instagram access token.

        Instagram long-lived tokens can be refreshed to extend their validity
        from 60 days to another 60 days.

        Returns:
            Updated credentials with new access token.

        Raises:
            PlatformAuthError: If token refresh fails.
        """
        if not self.api_client:
            raise RuntimeError("Client must be used as async context manager")

        try:
            response = await self.api_client.get(
                "/refresh_access_token",
                params={
                    "grant_type": "ig_refresh_token",
                    "access_token": self.credentials.access_token,
                },
            )

            data = response.data
            self.credentials.access_token = data["access_token"]
            # Instagram tokens typically expire in 60 days
            self.credentials.expires_at = datetime.fromtimestamp(
                datetime.now().timestamp() + data.get("expires_in", 5184000)
            )

            return self.credentials

        except httpx.HTTPError as e:
            raise PlatformAuthError(
                f"Token refresh failed: {e}",
                platform=self.platform_name,
            ) from e

    async def is_authenticated(self) -> bool:
        """Check if Instagram credentials are valid.

        Returns:
            True if authenticated and token is valid.
        """
        if not self.api_client:
            raise RuntimeError("Client must be used as async context manager")

        try:
            # Verify credentials by fetching account info
            await self.api_client.get(
                f"/{self.instagram_account_id}",
                params={
                    "fields": "id,username",
                    "access_token": self.credentials.access_token,
                },
            )
            return True
        except httpx.HTTPError:
            return False

    # ==================== Post CRUD Methods ====================

    async def create_post(self, request: PostCreateRequest) -> Post:
        """Create and publish an Instagram post.

        Instagram requires a two-step process:
        1. Create a media container
        2. Publish the container

        Args:
            request: Post creation request.

        Returns:
            Created Post object.

        Raises:
            ValidationError: If request is invalid.
            MediaUploadError: If media upload fails.
        """
        if not self.api_client:
            raise RuntimeError("Client must be used as async context manager")

        if not request.media_urls and not request.media_ids:
            raise ValidationError(
                "Instagram posts require at least one media attachment",
                platform=self.platform_name,
                field="media",
            )

        # Step 1: Create media container
        container_params: dict[str, Any] = {
            "access_token": self.credentials.access_token,
        }

        if request.media_urls:
            container_params["image_url"] = request.media_urls[0]

        if request.content:
            container_params["caption"] = request.content

        try:
            # Create container
            container_response = await self.api_client.post(
                f"/{self.instagram_account_id}/media",
                data=container_params,
            )
            container_id = container_response.data["id"]

            # Step 2: Publish container
            publish_response = await self.api_client.post(
                f"/{self.instagram_account_id}/media_publish",
                data={
                    "creation_id": container_id,
                    "access_token": self.credentials.access_token,
                },
            )
            post_id = publish_response.data["id"]

            # Fetch full post details
            return await self.get_post(post_id)

        except httpx.HTTPError as e:
            raise MediaUploadError(
                f"Failed to create Instagram post: {e}",
                platform=self.platform_name,
            ) from e

    async def get_post(self, post_id: str) -> Post:
        """Retrieve an Instagram post by ID.

        Args:
            post_id: Instagram media ID.

        Returns:
            Post object with current data.

        Raises:
            PostNotFoundError: If post doesn't exist.
        """
        if not self.api_client:
            raise RuntimeError("Client must be used as async context manager")

        try:
            response = await self.api_client.get(
                f"/{post_id}",
                params={
                    "fields": "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count",
                    "access_token": self.credentials.access_token,
                },
            )

            data = response.data
            return self._parse_post(data)

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise PostNotFoundError(
                    post_id=post_id,
                    platform=self.platform_name,
                    status_code=404,
                ) from e
            raise PlatformError(
                f"Failed to fetch post: {e}",
                platform=self.platform_name,
            ) from e
        except httpx.HTTPError as e:
            raise PlatformError(
                f"Failed to fetch post: {e}",
                platform=self.platform_name,
            ) from e

    async def update_post(
        self,
        post_id: str,  # noqa: ARG002
        request: PostUpdateRequest,  # noqa: ARG002
    ) -> Post:
        """Update an Instagram post.

        Note: Instagram does not support editing published posts. This method
        will raise an error.

        Args:
            post_id: Instagram media ID.
            request: Post update request.

        Raises:
            PlatformError: Instagram doesn't support post editing.
        """
        raise PlatformError(
            "Instagram does not support editing published posts",
            platform=self.platform_name,
        )

    async def delete_post(self, post_id: str) -> bool:
        """Delete an Instagram post.

        Args:
            post_id: Instagram media ID.

        Returns:
            True if deletion was successful.

        Raises:
            PostNotFoundError: If post doesn't exist.
        """
        if not self.api_client:
            raise RuntimeError("Client must be used as async context manager")

        try:
            await self.api_client.post(
                f"/{post_id}",
                data={
                    "access_token": self.credentials.access_token,
                },
            )
            return True

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise PostNotFoundError(
                    post_id=post_id,
                    platform=self.platform_name,
                    status_code=404,
                ) from e
            raise PlatformError(
                f"Failed to delete post: {e}",
                platform=self.platform_name,
            ) from e
        except httpx.HTTPError as e:
            raise PlatformError(
                f"Failed to delete post: {e}",
                platform=self.platform_name,
            ) from e

    # ==================== Comment Methods ====================

    async def get_comments(
        self,
        post_id: str,
        limit: int = 50,
        offset: int = 0,  # noqa: ARG002
    ) -> list[Comment]:
        """Retrieve comments for an Instagram post.

        Args:
            post_id: Instagram media ID.
            limit: Maximum number of comments to retrieve.
            offset: Number of comments to skip.

        Returns:
            List of Comment objects.
        """
        if not self.api_client:
            raise RuntimeError("Client must be used as async context manager")

        try:
            response = await self.api_client.get(
                f"/{post_id}/comments",
                params={
                    "fields": "id,text,username,timestamp,like_count",
                    "access_token": self.credentials.access_token,
                    "limit": limit,
                },
            )

            comments = []
            for comment_data in response.data.get("data", []):
                comments.append(self._parse_comment(comment_data, post_id))

            return comments

        except httpx.HTTPError as e:
            raise PlatformError(
                f"Failed to fetch comments: {e}",
                platform=self.platform_name,
            ) from e

    async def create_comment(self, post_id: str, content: str) -> Comment:
        """Add a comment to an Instagram post.

        Args:
            post_id: Instagram media ID.
            content: Text content of the comment.

        Returns:
            Created Comment object.

        Raises:
            ValidationError: If comment content is invalid.
        """
        if not self.api_client:
            raise RuntimeError("Client must be used as async context manager")

        if not content or len(content) == 0:
            raise ValidationError(
                "Comment content cannot be empty",
                platform=self.platform_name,
                field="content",
            )

        try:
            response = await self.api_client.post(
                f"/{post_id}/comments",
                data={
                    "message": content,
                    "access_token": self.credentials.access_token,
                },
            )

            comment_id = response.data["id"]

            # Fetch full comment details
            comment_response = await self.api_client.get(
                f"/{comment_id}",
                params={
                    "fields": "id,text,username,timestamp,like_count",
                    "access_token": self.credentials.access_token,
                },
            )

            return self._parse_comment(comment_response.data, post_id)

        except httpx.HTTPError as e:
            raise PlatformError(
                f"Failed to create comment: {e}",
                platform=self.platform_name,
            ) from e

    async def delete_comment(self, comment_id: str) -> bool:
        """Delete an Instagram comment.

        Args:
            comment_id: Instagram comment ID.

        Returns:
            True if deletion was successful.
        """
        if not self.api_client:
            raise RuntimeError("Client must be used as async context manager")

        try:
            await self.api_client.post(
                f"/{comment_id}",
                data={
                    "access_token": self.credentials.access_token,
                },
            )
            return True

        except httpx.HTTPError as e:
            raise PlatformError(
                f"Failed to delete comment: {e}",
                platform=self.platform_name,
            ) from e

    # ==================== Media Methods ====================

    async def upload_media(
        self,
        media_url: str,
        media_type: str,
        alt_text: str | None = None,
    ) -> MediaAttachment:
        """Upload media to Instagram.

        Note: Instagram requires media to be hosted on a publicly accessible
        URL. This method creates a media container that can be used for
        publishing.

        Args:
            media_url: Public URL of the media file.
            media_type: Type of media (image or video).
            alt_text: Alternative text for accessibility.

        Returns:
            MediaAttachment object with container ID.

        Raises:
            MediaUploadError: If upload fails.
        """
        if not self.api_client:
            raise RuntimeError("Client must be used as async context manager")

        params: dict[str, Any] = {
            "access_token": self.credentials.access_token,
        }

        if media_type.lower() == "image":
            params["image_url"] = media_url
        elif media_type.lower() == "video":
            params["video_url"] = media_url
            params["media_type"] = "VIDEO"
        else:
            raise ValidationError(
                f"Unsupported media type: {media_type}",
                platform=self.platform_name,
                field="media_type",
            )

        try:
            response = await self.api_client.post(
                f"/{self.instagram_account_id}/media",
                data=params,
            )

            container_id = response.data["id"]

            return MediaAttachment(
                media_id=container_id,
                media_type=(
                    MediaType.IMAGE
                    if media_type.lower() == "image"
                    else MediaType.VIDEO
                ),
                url=cast(HttpUrl, media_url),
                alt_text=alt_text,
            )

        except httpx.HTTPError as e:
            raise MediaUploadError(
                f"Failed to upload media: {e}",
                platform=self.platform_name,
                media_type=media_type,
            ) from e

    async def create_carousel(
        self,
        media_urls: list[str],
        caption: str | None = None,
        *,
        alt_texts: list[str] | None = None,
        location_id: str | None = None,
    ) -> Post:
        """Create an Instagram carousel post (2-10 images).

        Args:
            media_urls: List of image URLs (2-10 items).
            caption: Post caption.
            alt_texts: Optional alt texts for each image.
            location_id: Optional location ID.

        Returns:
            Published Post object.

        Raises:
            ValidationError: If inputs are invalid.
            MediaUploadError: If creation fails.
            RuntimeError: If client not used as context manager.

        Example:
            >>> async with InstagramClient(credentials) as client:
            ...     post = await client.create_carousel(
            ...         media_urls=[
            ...             "https://example.com/img1.jpg",
            ...             "https://example.com/img2.jpg",
            ...         ],
            ...         caption="Beautiful carousel post!"
            ...     )
        """
        if not self._media_manager:
            raise RuntimeError("Client must be used as async context manager")

        # Convert to MediaItem objects
        media_items = []
        for idx, url in enumerate(media_urls):
            alt_text = None
            if alt_texts and idx < len(alt_texts):
                alt_text = alt_texts[idx]
            media_items.append(MediaItem(url=url, type="image", alt_text=alt_text))

        # Create containers
        container_ids = await self._media_manager.create_feed_containers(
            media_items,
            caption=caption,
            location_id=location_id,
        )

        # Publish
        result = await self._media_manager.publish_container(container_ids[0])

        # Fetch and return post
        return await self.get_post(result.media_id)

    async def create_reel(
        self,
        video_url: str,
        caption: str | None = None,
        *,
        cover_url: str | None = None,
        share_to_feed: bool = True,
    ) -> Post:
        """Create an Instagram Reel (video).

        Args:
            video_url: URL of video file.
            caption: Reel caption.
            cover_url: Optional thumbnail image URL.
            share_to_feed: Share reel to main feed.

        Returns:
            Published Post object.

        Raises:
            MediaUploadError: If creation fails.
            RuntimeError: If client not used as context manager.

        Example:
            >>> async with InstagramClient(credentials) as client:
            ...     reel = await client.create_reel(
            ...         video_url="https://example.com/video.mp4",
            ...         caption="Check out this reel!",
            ...         share_to_feed=True
            ...     )
        """
        if not self._media_manager:
            raise RuntimeError("Client must be used as async context manager")

        # Create reel container
        container_id = await self._media_manager.create_reel_container(
            video_url,
            caption=caption,
            cover_url=cover_url,
            share_to_feed=share_to_feed,
            wait_for_processing=True,
        )

        # Publish
        result = await self._media_manager.publish_container(container_id)

        # Fetch and return post
        return await self.get_post(result.media_id)

    async def create_story(
        self,
        media_url: str,
        media_type: Literal["image", "video"],
    ) -> Post:
        """Create an Instagram Story.

        Args:
            media_url: URL of media file.
            media_type: Type of media ("image" or "video").

        Returns:
            Published Post object.

        Raises:
            MediaUploadError: If creation fails.
            RuntimeError: If client not used as context manager.

        Example:
            >>> async with InstagramClient(credentials) as client:
            ...     story = await client.create_story(
            ...         media_url="https://example.com/story.jpg",
            ...         media_type="image"
            ...     )
        """
        if not self._media_manager:
            raise RuntimeError("Client must be used as async context manager")

        # Create story container
        container_id = await self._media_manager.create_story_container(
            media_url,
            media_type,
            wait_for_processing=(media_type == "video"),
        )

        # Publish
        result = await self._media_manager.publish_container(container_id)

        # Fetch and return post
        return await self.get_post(result.media_id)

    # ==================== Helper Methods ====================

    def _parse_post(self, data: dict[str, Any]) -> Post:
        """Parse Instagram API response into Post model.

        Args:
            data: Raw API response data.

        Returns:
            Post object.
        """
        media_type_map = {
            "IMAGE": MediaType.IMAGE,
            "VIDEO": MediaType.VIDEO,
            "CAROUSEL_ALBUM": MediaType.CAROUSEL,
        }

        media = []
        if data.get("media_url"):
            media.append(
                MediaAttachment(
                    media_id=data["id"],
                    media_type=media_type_map.get(
                        data.get("media_type", "IMAGE"),
                        MediaType.IMAGE,
                    ),
                    url=data["media_url"],
                )
            )

        return Post(
            post_id=data["id"],
            platform=self.platform_name,
            content=data.get("caption"),
            media=media,
            status=PostStatus.PUBLISHED,
            url=data.get("permalink"),
            created_at=datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")),
            likes_count=data.get("like_count", 0),
            comments_count=data.get("comments_count", 0),
            raw_data=data,
        )

    def _parse_comment(self, data: dict[str, Any], post_id: str) -> Comment:
        """Parse Instagram API response into Comment model.

        Args:
            data: Raw API response data.
            post_id: ID of the post this comment belongs to.

        Returns:
            Comment object.
        """
        return Comment(
            comment_id=data["id"],
            post_id=post_id,
            platform=self.platform_name,
            content=data.get("text", ""),
            author_username=data.get("username"),
            author_id=data.get("user", {}).get("id", ""),
            created_at=datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")),
            likes_count=data.get("like_count", 0),
            status=CommentStatus.VISIBLE,
            raw_data=data,
        )
