"""LinkedIn API client implementation.

This module provides a concrete implementation of the SocialMediaPlatform
ABC for LinkedIn, using the LinkedIn Marketing API and Share API.

API Documentation: https://learn.microsoft.com/en-us/linkedin/
"""

from datetime import datetime
from typing import Any, cast

import httpx
from pydantic import HttpUrl

from marqetive.core.base import ProgressCallback, SocialMediaPlatform
from marqetive.core.exceptions import (
    MediaUploadError,
    PlatformAuthError,
    PlatformError,
    PostNotFoundError,
    ValidationError,
)
from marqetive.core.models import (
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
from marqetive.platforms.linkedin.media import LinkedInMediaManager, MediaAsset


class LinkedInClient(SocialMediaPlatform):
    """LinkedIn API client.

    This client implements the SocialMediaPlatform interface for LinkedIn,
    using the LinkedIn Share API and Marketing API. It supports creating
    posts (shares), managing comments, and uploading media.

    Note:
        - Requires LinkedIn Developer app with appropriate permissions
        - Requires OAuth 2.0 authentication
        - Supports both personal profiles and organization pages
        - Rate limits vary by API endpoint

    Example:
        >>> credentials = AuthCredentials(
        ...     platform="linkedin",
        ...     access_token="your_access_token",
        ...     user_id="urn:li:person:abc123"
        ... )
        >>> async with LinkedInClient(credentials) as client:
        ...     request = PostCreateRequest(
        ...         content="Excited to share our latest update!",
        ...         link="https://example.com"
        ...     )
        ...     post = await client.create_post(request)
    """

    def __init__(
        self,
        credentials: AuthCredentials,
        timeout: float = 30.0,
        api_version: str = "v2",
        progress_callback: ProgressCallback | None = None,
    ) -> None:
        """Initialize LinkedIn client.

        Args:
            credentials: LinkedIn authentication credentials
            timeout: Request timeout in seconds
            api_version: LinkedIn API version
            progress_callback: Optional callback for progress updates during
                long-running operations like media uploads.

        Raises:
            PlatformAuthError: If credentials are invalid
        """
        base_url = f"https://api.linkedin.com/{api_version}"
        super().__init__(
            platform_name="linkedin",
            credentials=credentials,
            base_url=base_url,
            timeout=timeout,
            progress_callback=progress_callback,
        )
        self.author_urn = (
            credentials.user_id
        )  # urn:li:person:xxx or urn:li:organization:xxx
        self.api_version = api_version

        # Media manager (initialized in __aenter__)
        self._media_manager: LinkedInMediaManager | None = None

    async def __aenter__(self) -> "LinkedInClient":
        """Async context manager entry."""
        await super().__aenter__()

        # Initialize media manager
        if not self.author_urn:
            raise PlatformAuthError(
                "LinkedIn author URN (user_id) is required in credentials",
                platform=self.platform_name,
            )

        self._media_manager = LinkedInMediaManager(
            person_urn=self.author_urn,
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
        """Perform LinkedIn authentication flow.

        Note: This method assumes you already have a valid OAuth 2.0 access token.
        For the full OAuth flow, use LinkedIn's OAuth 2.0 implementation.

        Returns:
            Current credentials if valid.

        Raises:
            PlatformAuthError: If authentication fails.
        """
        if await self.is_authenticated():
            return self.credentials

        raise PlatformAuthError(
            "Invalid or expired credentials. Please re-authenticate via LinkedIn OAuth 2.0.",
            platform=self.platform_name,
        )

    async def refresh_token(self) -> AuthCredentials:
        """Refresh LinkedIn access token.

        LinkedIn access tokens typically expire after 60 days. Use the
        refresh token to obtain a new access token.

        Returns:
            Updated credentials with new access token.

        Raises:
            PlatformAuthError: If token refresh fails.
        """
        if not self.credentials.refresh_token:
            raise PlatformAuthError(
                "No refresh token available",
                platform=self.platform_name,
            )

        # Note: LinkedIn OAuth token refresh requires making a request to
        # https://www.linkedin.com/oauth/v2/accessToken
        # This is simplified for demonstration
        raise PlatformAuthError(
            "Token refresh not yet implemented. Please re-authenticate.",
            platform=self.platform_name,
        )

    async def is_authenticated(self) -> bool:
        """Check if LinkedIn credentials are valid.

        Returns:
            True if authenticated and token is valid.
        """
        if not self.api_client:
            raise RuntimeError("Client must be used as async context manager")

        try:
            # Verify credentials by fetching user profile
            await self.api_client.get("/me")
            return True
        except httpx.HTTPError:
            return False

    # ==================== Post CRUD Methods ====================

    async def create_post(self, request: PostCreateRequest) -> Post:
        """Create and publish a LinkedIn post (share).

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

        if not request.content:
            raise ValidationError(
                "LinkedIn posts require content",
                platform=self.platform_name,
                field="content",
            )

        # Validate content length (3000 characters for posts)
        if len(request.content) > 3000:
            raise ValidationError(
                f"Post content exceeds 3000 characters ({len(request.content)} characters)",
                platform=self.platform_name,
                field="content",
            )

        try:
            # Build share payload
            share_payload: dict[str, Any] = {
                "author": self.author_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": request.content},
                        "shareMediaCategory": "NONE",
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
            }

            # Add media if provided
            if request.media_ids:
                share_payload["specificContent"]["com.linkedin.ugc.ShareContent"][
                    "shareMediaCategory"
                ] = "IMAGE"
                share_payload["specificContent"]["com.linkedin.ugc.ShareContent"][
                    "media"
                ] = [
                    {"status": "READY", "media": media_id}
                    for media_id in request.media_ids
                ]

            # Add link if provided
            if request.link:
                share_payload["specificContent"]["com.linkedin.ugc.ShareContent"][
                    "shareMediaCategory"
                ] = "ARTICLE"
                share_payload["specificContent"]["com.linkedin.ugc.ShareContent"][
                    "media"
                ] = [
                    {
                        "status": "READY",
                        "originalUrl": request.link,
                    }
                ]

            # Create the share
            response = await self.api_client.post("/ugcPosts", data=share_payload)

            post_id = response.data["id"]

            # Fetch full post details
            return await self.get_post(post_id)

        except httpx.HTTPError as e:
            raise PlatformError(
                f"Failed to create LinkedIn post: {e}",
                platform=self.platform_name,
            ) from e

    async def get_post(self, post_id: str) -> Post:
        """Retrieve a LinkedIn post by ID.

        Args:
            post_id: LinkedIn post URN (e.g., urn:li:share:123).

        Returns:
            Post object with current data.

        Raises:
            PostNotFoundError: If post doesn't exist.
        """
        if not self.api_client:
            raise RuntimeError("Client must be used as async context manager")

        try:
            response = await self.api_client.get(f"/ugcPosts/{post_id}")
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
        """Update a LinkedIn post.

        Note: LinkedIn has limited support for editing posts. Only certain
        fields can be updated, and there are time restrictions.

        Args:
            post_id: LinkedIn post URN.
            request: Post update request.

        Raises:
            PlatformError: If post cannot be edited.
        """
        raise PlatformError(
            "LinkedIn does not support editing published posts",
            platform=self.platform_name,
        )

    async def delete_post(self, post_id: str) -> bool:
        """Delete a LinkedIn post.

        Args:
            post_id: LinkedIn post URN.

        Returns:
            True if deletion was successful.

        Raises:
            PostNotFoundError: If post doesn't exist.
        """
        if not self.api_client:
            raise RuntimeError("Client must be used as async context manager")

        try:
            # LinkedIn uses DELETE method for removing posts
            if not self.api_client._client:
                raise RuntimeError("API client not initialized")

            await self.api_client._client.delete(f"{self.base_url}/ugcPosts/{post_id}")
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
        offset: int = 0,
    ) -> list[Comment]:
        """Retrieve comments for a LinkedIn post.

        Args:
            post_id: LinkedIn post URN.
            limit: Maximum number of comments to retrieve.
            offset: Number of comments to skip.

        Returns:
            List of Comment objects.
        """
        if not self.api_client:
            raise RuntimeError("Client must be used as async context manager")

        try:
            # LinkedIn Social API endpoint for comments
            response = await self.api_client.get(
                f"/socialActions/{post_id}/comments",
                params={
                    "count": limit,
                    "start": offset,
                },
            )

            comments = []
            for comment_data in response.data.get("elements", []):
                comments.append(self._parse_comment(comment_data, post_id))

            return comments

        except httpx.HTTPError as e:
            raise PlatformError(
                f"Failed to fetch comments: {e}",
                platform=self.platform_name,
            ) from e

    async def create_comment(self, post_id: str, content: str) -> Comment:
        """Add a comment to a LinkedIn post.

        Args:
            post_id: LinkedIn post URN.
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

        # LinkedIn comment length limit
        if len(content) > 1250:
            raise ValidationError(
                f"Comment exceeds 1250 characters ({len(content)} characters)",
                platform=self.platform_name,
                field="content",
            )

        try:
            comment_payload = {
                "actor": self.author_urn,
                "message": {"text": content},
                "object": post_id,
            }

            response = await self.api_client.post(
                f"/socialActions/{post_id}/comments",
                data=comment_payload,
            )

            comment_id = response.data["id"]

            # Fetch full comment details
            comment_response = await self.api_client.get(
                f"/socialActions/{post_id}/comments/{comment_id}"
            )

            return self._parse_comment(comment_response.data, post_id)

        except httpx.HTTPError as e:
            raise PlatformError(
                f"Failed to create comment: {e}",
                platform=self.platform_name,
            ) from e

    async def delete_comment(self, comment_id: str) -> bool:
        """Delete a LinkedIn comment.

        Args:
            comment_id: LinkedIn comment URN.

        Returns:
            True if deletion was successful.
        """
        if not self.api_client:
            raise RuntimeError("Client must be used as async context manager")

        try:
            if not self.api_client._client:
                raise RuntimeError("API client not initialized")

            # Extract post ID from comment URN if needed
            # Note: This is simplified; actual implementation may vary
            await self.api_client._client.delete(
                f"{self.base_url}/comments/{comment_id}"
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
        """Upload media to LinkedIn.

        Automatically handles images, videos, and documents with progress tracking.

        Args:
            media_url: URL or file path of the media.
            media_type: Type of media ("image", "video", or "document").
            alt_text: Alternative text for accessibility.

        Returns:
            MediaAttachment object with LinkedIn media URN.

        Raises:
            MediaUploadError: If upload fails.
            RuntimeError: If client not used as context manager.

        Example:
            >>> async with LinkedInClient(credentials) as client:
            ...     media = await client.upload_media(
            ...         "/path/to/image.jpg",
            ...         "image",
            ...         alt_text="Company logo"
            ...     )
        """
        if not self._media_manager:
            raise RuntimeError("Client must be used as async context manager")

        try:
            # Convert URL to string if needed
            file_path = str(media_url)

            # Upload based on type
            if media_type.lower() == "image":
                asset = await self._media_manager.upload_image(
                    file_path, alt_text=alt_text
                )
            elif media_type.lower() == "video":
                asset = await self._media_manager.upload_video(
                    file_path, wait_for_processing=True
                )
            elif media_type.lower() == "document":
                asset = await self._media_manager.upload_document(file_path)
            else:
                raise ValidationError(
                    f"Unsupported media type: {media_type}. "
                    "Must be 'image', 'video', or 'document'",
                    platform=self.platform_name,
                    field="media_type",
                )

            return MediaAttachment(
                media_id=asset.asset_id,
                media_type=(
                    MediaType.IMAGE
                    if media_type.lower() == "image"
                    else (
                        MediaType.VIDEO
                        if media_type.lower() == "video"
                        else MediaType.IMAGE
                    )  # Document
                ),
                url=cast(HttpUrl, media_url),
                alt_text=alt_text,
            )

        except Exception as e:
            raise MediaUploadError(
                f"Failed to upload media: {e}",
                platform=self.platform_name,
                media_type=media_type,
            ) from e

    async def upload_image(
        self,
        file_path: str,
        *,
        alt_text: str | None = None,
    ) -> MediaAsset:
        """Upload an image to LinkedIn.

        Convenience method for image uploads.

        Args:
            file_path: Path to image file or URL.
            alt_text: Alternative text for accessibility.

        Returns:
            MediaAsset with asset ID.

        Example:
            >>> async with LinkedInClient(credentials) as client:
            ...     asset = await client.upload_image("photo.jpg")
        """
        if not self._media_manager:
            raise RuntimeError("Client must be used as async context manager")

        return await self._media_manager.upload_image(file_path, alt_text=alt_text)

    async def upload_video(
        self,
        file_path: str,
        *,
        wait_for_processing: bool = True,
    ) -> MediaAsset:
        """Upload a video to LinkedIn.

        Convenience method for video uploads.

        Args:
            file_path: Path to video file or URL.
            wait_for_processing: Wait for video processing to complete.

        Returns:
            MediaAsset with asset ID.

        Example:
            >>> async with LinkedInClient(credentials) as client:
            ...     asset = await client.upload_video("video.mp4")
        """
        if not self._media_manager:
            raise RuntimeError("Client must be used as async context manager")

        return await self._media_manager.upload_video(
            file_path, wait_for_processing=wait_for_processing
        )

    async def upload_document(
        self,
        file_path: str,
        *,
        title: str | None = None,
    ) -> MediaAsset:
        """Upload a document/PDF to LinkedIn.

        Convenience method for document uploads.

        Args:
            file_path: Path to PDF file or URL.
            title: Document title.

        Returns:
            MediaAsset with asset ID.

        Example:
            >>> async with LinkedInClient(credentials) as client:
            ...     asset = await client.upload_document("report.pdf")
        """
        if not self._media_manager:
            raise RuntimeError("Client must be used as async context manager")

        return await self._media_manager.upload_document(file_path, title=title)

    # ==================== Helper Methods ====================

    def _parse_post(self, data: dict[str, Any]) -> Post:
        """Parse LinkedIn API response into Post model.

        Args:
            data: Raw API response data.

        Returns:
            Post object.
        """
        content = ""
        if "specificContent" in data:
            share_content = data["specificContent"].get(
                "com.linkedin.ugc.ShareContent", {}
            )
            commentary = share_content.get("shareCommentary", {})
            content = commentary.get("text", "")

        # Extract timestamps
        created_timestamp = data.get("created", {}).get("time", 0)
        created_at = (
            datetime.fromtimestamp(created_timestamp / 1000)
            if created_timestamp
            else datetime.now()
        )

        return Post(
            post_id=data["id"],
            platform=self.platform_name,
            content=content,
            media=[],  # Media parsing would go here
            status=(
                PostStatus.PUBLISHED
                if data.get("lifecycleState") == "PUBLISHED"
                else PostStatus.DRAFT
            ),
            created_at=created_at,
            author_id=data.get("author"),
            raw_data=data,
        )

    def _parse_comment(self, data: dict[str, Any], post_id: str) -> Comment:
        """Parse LinkedIn API response into Comment model.

        Args:
            data: Raw API response data.
            post_id: ID of the post this comment belongs to.

        Returns:
            Comment object.
        """
        content = data.get("message", {}).get("text", "")
        created_timestamp = data.get("created", {}).get("time", 0)
        created_at = (
            datetime.fromtimestamp(created_timestamp / 1000)
            if created_timestamp
            else datetime.now()
        )

        return Comment(
            comment_id=data["id"],
            post_id=post_id,
            platform=self.platform_name,
            content=content,
            author_id=data.get("actor", "unknown"),
            created_at=created_at,
            status=CommentStatus.VISIBLE,
            raw_data=data,
        )
