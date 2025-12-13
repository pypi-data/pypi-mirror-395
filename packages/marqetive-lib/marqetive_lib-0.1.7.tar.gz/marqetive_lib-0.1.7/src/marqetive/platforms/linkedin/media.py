"""LinkedIn media upload manager with support for images, videos, and documents.

LinkedIn uses a multi-step upload process:
1. Register upload (get upload URL)
2. Upload file to the URL
3. Complete upload (finalize)

This module supports:
- Image uploads (single and multiple)
- Video uploads with processing monitoring
- Document/PDF uploads
"""

import asyncio
import inspect
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any, Literal

import httpx

from marqetive.core.exceptions import (
    MediaUploadError,
    ValidationError,
)
from marqetive.core.models import ProgressEvent, ProgressStatus
from marqetive.utils.file_handlers import download_file, read_file_bytes
from marqetive.utils.media import detect_mime_type, format_file_size
from marqetive.utils.retry import STANDARD_BACKOFF, retry_async

# Type aliases for progress callbacks
type SyncProgressCallback = Callable[[ProgressEvent], None]
type AsyncProgressCallback = Callable[[ProgressEvent], Awaitable[None]]
type ProgressCallback = SyncProgressCallback | AsyncProgressCallback

logger = logging.getLogger(__name__)

# LinkedIn limits
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_VIDEO_SIZE = 200 * 1024 * 1024  # 200MB
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB
MAX_VIDEO_DURATION = 600  # 10 minutes

# Processing timeouts
VIDEO_PROCESSING_TIMEOUT = 600  # 10 minutes


class VideoProcessingState(str, Enum):
    """LinkedIn video processing states."""

    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"
    AVAILABLE = "AVAILABLE"


@dataclass
class UploadProgress:
    """Progress information for media upload.

    .. deprecated:: 0.2.0
        Use :class:`marqetive.core.models.ProgressEvent` instead.
        This class will be removed in a future version.
    """

    asset_id: str
    bytes_uploaded: int
    total_bytes: int
    status: Literal["registering", "uploading", "processing", "completed", "failed"]

    @property
    def percentage(self) -> float:
        """Calculate upload percentage."""
        if self.total_bytes == 0:
            return 0.0
        return (self.bytes_uploaded / self.total_bytes) * 100


@dataclass
class MediaAsset:
    """LinkedIn media asset result.

    Attributes:
        asset_id: LinkedIn asset URN.
        download_url: URL to download the media (if available).
        status: Current status of the asset.
    """

    asset_id: str
    download_url: str | None = None
    status: str | None = None


class LinkedInMediaManager:
    """Manager for LinkedIn media uploads using the Community Management API.

    Supports images, videos, and documents with progress tracking.

    Example:
        >>> manager = LinkedInMediaManager(person_urn, access_token)
        >>> asset = await manager.upload_image("/path/to/image.jpg")
        >>> print(f"Uploaded: {asset.asset_id}")
    """

    # Default API version in YYYYMM format
    DEFAULT_LINKEDIN_VERSION = "202511"

    def __init__(
        self,
        person_urn: str,
        access_token: str,
        *,
        linkedin_version: str | None = None,
        timeout: float = 60.0,
        progress_callback: ProgressCallback | None = None,
    ) -> None:
        """Initialize LinkedIn media manager.

        Args:
            person_urn: LinkedIn person or organization URN
                (e.g., "urn:li:person:ABC123" or "urn:li:organization:12345").
            access_token: LinkedIn OAuth access token.
            linkedin_version: LinkedIn API version in YYYYMM format (e.g., "202511").
                Defaults to the latest supported version.
            timeout: Request timeout in seconds.
            progress_callback: Optional callback for progress updates.
                Accepts ProgressEvent and can be sync or async.
        """
        self.person_urn = person_urn
        self.access_token = access_token
        self.linkedin_version = linkedin_version or self.DEFAULT_LINKEDIN_VERSION
        self.timeout = timeout
        self.progress_callback = progress_callback

        # Use v2 API for media uploads (still uses assets endpoint)
        # Note: Media registration still uses v2 API, not REST API
        self.base_url = "https://api.linkedin.com/v2"
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-Restli-Protocol-Version": "2.0.0",
                "Linkedin-Version": self.linkedin_version,
                "Content-Type": "application/json",
            },
        )

    async def _emit_progress(
        self,
        status: ProgressStatus,
        progress: int,
        total: int,
        message: str | None = None,
        *,
        entity_id: str | None = None,
        file_path: str | None = None,
        bytes_uploaded: int | None = None,
        total_bytes: int | None = None,
    ) -> None:
        """Emit a progress update if a callback is registered.

        Supports both sync and async callbacks.
        """
        if self.progress_callback is None:
            return

        event = ProgressEvent(
            operation="upload_media",
            platform="linkedin",
            status=status,
            progress=progress,
            total=total,
            message=message,
            entity_id=entity_id,
            file_path=file_path,
            bytes_uploaded=bytes_uploaded,
            total_bytes=total_bytes,
        )

        result = self.progress_callback(event)

        # If callback returned a coroutine, await it
        if inspect.iscoroutine(result):
            await result

    async def __aenter__(self) -> "LinkedInMediaManager":
        """Enter async context."""
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Exit async context and cleanup."""
        await self.client.aclose()

    async def upload_image(
        self,
        file_path: str,
        *,
        alt_text: str | None = None,  # noqa: ARG002
    ) -> MediaAsset:
        """Upload an image to LinkedIn.

        Args:
            file_path: Path to image file or URL.
            alt_text: Alternative text for accessibility.

        Returns:
            MediaAsset with asset ID.

        Raises:
            MediaUploadError: If upload fails.
            ValidationError: If file is invalid.

        Example:
            >>> asset = await manager.upload_image("photo.jpg")
            >>> print(f"Asset ID: {asset.asset_id}")
        """
        # Download if URL
        if file_path.startswith(("http://", "https://")):
            file_path = await download_file(file_path)

        # Validate
        mime_type = detect_mime_type(file_path)
        if not mime_type.startswith("image/"):
            raise ValidationError(
                f"File is not an image: {mime_type}",
                platform="linkedin",
            )

        # Read file
        file_bytes = await read_file_bytes(file_path)
        file_size = len(file_bytes)

        if file_size > MAX_IMAGE_SIZE:
            raise ValidationError(
                f"Image exceeds {format_file_size(MAX_IMAGE_SIZE)} limit",
                platform="linkedin",
            )

        # Register upload
        register_data = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": self.person_urn,
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent",
                    }
                ],
            }
        }

        asset_id = await self._register_upload(register_data)

        # Notify start
        await self._emit_progress(
            status=ProgressStatus.INITIALIZING,
            progress=0,
            total=100,
            message="Registering upload",
            entity_id=asset_id,
            bytes_uploaded=0,
            total_bytes=file_size,
        )

        # Get upload URL
        upload_url = await self._get_upload_url(asset_id)

        # Upload file
        await self._upload_to_url(upload_url, file_bytes, file_size, asset_id)

        # Notify completion
        await self._emit_progress(
            status=ProgressStatus.COMPLETED,
            progress=100,
            total=100,
            message="Upload completed",
            entity_id=asset_id,
            bytes_uploaded=file_size,
            total_bytes=file_size,
        )

        logger.info(f"Image uploaded successfully: {asset_id}")
        return MediaAsset(asset_id=asset_id, status="READY")

    async def upload_video(
        self,
        file_path: str,
        *,
        title: str | None = None,  # noqa: ARG002
        wait_for_processing: bool = True,
    ) -> MediaAsset:
        """Upload a video to LinkedIn.

        Args:
            file_path: Path to video file or URL.
            title: Video title.
            wait_for_processing: Wait for video processing to complete.

        Returns:
            MediaAsset with asset ID.

        Raises:
            MediaUploadError: If upload or processing fails.
            ValidationError: If file is invalid.

        Example:
            >>> asset = await manager.upload_video(
            ...     "video.mp4",
            ...     title="My Video",
            ...     wait_for_processing=True
            ... )
        """
        # Download if URL
        if file_path.startswith(("http://", "https://")):
            file_path = await download_file(file_path)

        # Validate
        mime_type = detect_mime_type(file_path)
        if not mime_type.startswith("video/"):
            raise ValidationError(
                f"File is not a video: {mime_type}",
                platform="linkedin",
            )

        # Read file
        file_bytes = await read_file_bytes(file_path)
        file_size = len(file_bytes)

        if file_size > MAX_VIDEO_SIZE:
            raise ValidationError(
                f"Video exceeds {format_file_size(MAX_VIDEO_SIZE)} limit",
                platform="linkedin",
            )

        # Register upload
        register_data = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-video"],
                "owner": self.person_urn,
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent",
                    }
                ],
            }
        }

        asset_id = await self._register_upload(register_data)

        # Notify start
        await self._emit_progress(
            status=ProgressStatus.INITIALIZING,
            progress=0,
            total=100,
            message="Registering video upload",
            entity_id=asset_id,
            bytes_uploaded=0,
            total_bytes=file_size,
        )

        # Get upload URL
        upload_url = await self._get_upload_url(asset_id)

        # Upload file
        await self._upload_to_url(upload_url, file_bytes, file_size, asset_id)

        # Wait for processing if requested
        if wait_for_processing:
            await self._wait_for_video_processing(asset_id)

        # Notify completion
        final_status = (
            ProgressStatus.COMPLETED
            if wait_for_processing
            else ProgressStatus.PROCESSING
        )
        await self._emit_progress(
            status=final_status,
            progress=100,
            total=100,
            message=(
                "Video upload completed" if wait_for_processing else "Video processing"
            ),
            entity_id=asset_id,
            bytes_uploaded=file_size,
            total_bytes=file_size,
        )

        logger.info(f"Video uploaded successfully: {asset_id}")
        return MediaAsset(
            asset_id=asset_id, status="READY" if wait_for_processing else "PROCESSING"
        )

    async def upload_document(
        self,
        file_path: str,
        *,
        title: str | None = None,  # noqa: ARG002
    ) -> MediaAsset:
        """Upload a document/PDF to LinkedIn.

        Args:
            file_path: Path to document file or URL.
            title: Document title.

        Returns:
            MediaAsset with asset ID.

        Raises:
            MediaUploadError: If upload fails.
            ValidationError: If file is invalid.

        Example:
            >>> asset = await manager.upload_document(
            ...     "presentation.pdf",
            ...     title="Q4 Report"
            ... )
        """
        # Download if URL
        if file_path.startswith(("http://", "https://")):
            file_path = await download_file(file_path)

        # Validate
        mime_type = detect_mime_type(file_path)
        if mime_type != "application/pdf":
            raise ValidationError(
                f"Only PDF documents are supported. Got: {mime_type}",
                platform="linkedin",
            )

        # Read file
        file_bytes = await read_file_bytes(file_path)
        file_size = len(file_bytes)

        if file_size > MAX_DOCUMENT_SIZE:
            raise ValidationError(
                f"Document exceeds {format_file_size(MAX_DOCUMENT_SIZE)} limit",
                platform="linkedin",
            )

        # Register upload
        register_data = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-document"],
                "owner": self.person_urn,
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent",
                    }
                ],
            }
        }

        asset_id = await self._register_upload(register_data)

        # Notify start
        await self._emit_progress(
            status=ProgressStatus.INITIALIZING,
            progress=0,
            total=100,
            message="Registering document upload",
            entity_id=asset_id,
            bytes_uploaded=0,
            total_bytes=file_size,
        )

        # Get upload URL
        upload_url = await self._get_upload_url(asset_id)

        # Upload file
        await self._upload_to_url(upload_url, file_bytes, file_size, asset_id)

        # Notify completion
        await self._emit_progress(
            status=ProgressStatus.COMPLETED,
            progress=100,
            total=100,
            message="Document upload completed",
            entity_id=asset_id,
            bytes_uploaded=file_size,
            total_bytes=file_size,
        )

        logger.info(f"Document uploaded successfully: {asset_id}")
        return MediaAsset(asset_id=asset_id, status="READY")

    async def get_video_status(self, asset_id: str) -> dict[str, Any]:
        """Get processing status of a video asset.

        Args:
            asset_id: LinkedIn asset URN.

        Returns:
            Dictionary with video status information.

        Example:
            >>> status = await manager.get_video_status(asset_id)
            >>> print(f"Status: {status['status']}")
        """

        @retry_async(config=STANDARD_BACKOFF)
        async def _get_status() -> dict[str, Any]:
            response = await self.client.get(
                f"{self.base_url}/assets/{asset_id}",
            )
            response.raise_for_status()
            return response.json()

        return await _get_status()

    async def _register_upload(self, register_data: dict[str, Any]) -> str:
        """Register an upload and get asset ID."""

        @retry_async(config=STANDARD_BACKOFF)
        async def _register() -> str:
            response = await self.client.post(
                f"{self.base_url}/assets?action=registerUpload",
                json=register_data,
            )
            response.raise_for_status()
            result = response.json()
            return result["value"]["asset"]

        try:
            return await _register()
        except httpx.HTTPError as e:
            raise MediaUploadError(
                f"Failed to register upload: {e}",
                platform="linkedin",
            ) from e

    async def _get_upload_url(self, asset_id: str) -> str:
        """Get upload URL for an asset."""

        @retry_async(config=STANDARD_BACKOFF)
        async def _get_url() -> str:
            response = await self.client.get(
                f"{self.base_url}/assets/{asset_id}",
            )
            response.raise_for_status()
            result = response.json()
            return result["uploadMechanism"][
                "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
            ]["uploadUrl"]

        try:
            return await _get_url()
        except httpx.HTTPError as e:
            raise MediaUploadError(
                f"Failed to get upload URL: {e}",
                platform="linkedin",
            ) from e

    async def _upload_to_url(
        self,
        upload_url: str,
        file_bytes: bytes,
        file_size: int,
        asset_id: str,
    ) -> None:
        """Upload file bytes to the upload URL."""

        @retry_async(config=STANDARD_BACKOFF)
        async def _upload() -> None:
            # LinkedIn requires specific headers for upload
            headers = {
                "Content-Type": "application/octet-stream",
            }

            # Notify upload start
            await self._emit_progress(
                status=ProgressStatus.UPLOADING,
                progress=0,
                total=100,
                message="Uploading file",
                entity_id=asset_id,
                bytes_uploaded=0,
                total_bytes=file_size,
            )

            response = await self.client.put(
                upload_url,
                content=file_bytes,
                headers=headers,
            )
            response.raise_for_status()

            # Notify upload complete
            await self._emit_progress(
                status=ProgressStatus.UPLOADING,
                progress=100,
                total=100,
                message="File uploaded",
                entity_id=asset_id,
                bytes_uploaded=file_size,
                total_bytes=file_size,
            )

        try:
            await _upload()
        except httpx.HTTPError as e:
            raise MediaUploadError(
                f"Failed to upload file: {e}",
                platform="linkedin",
            ) from e

    async def _wait_for_video_processing(
        self,
        asset_id: str,
        *,
        timeout: int = VIDEO_PROCESSING_TIMEOUT,
        check_interval: int = 5,
    ) -> None:
        """Wait for video processing to complete."""
        elapsed = 0
        logger.info(f"Waiting for video {asset_id} to process...")

        while elapsed < timeout:
            status_data = await self.get_video_status(asset_id)
            status = status_data.get("status")

            if status in (
                VideoProcessingState.READY.value,
                VideoProcessingState.AVAILABLE.value,
            ):
                logger.info(f"Video {asset_id} processing complete")
                return

            if status == VideoProcessingState.FAILED.value:
                raise MediaUploadError(
                    f"Video processing failed for {asset_id}",
                    platform="linkedin",
                    media_type="video",
                )

            # Notify progress
            progress_pct = min(int((elapsed / timeout) * 90), 90)
            await self._emit_progress(
                status=ProgressStatus.PROCESSING,
                progress=progress_pct,
                total=100,
                message=f"Processing video ({status})",
                entity_id=asset_id,
            )

            await asyncio.sleep(check_interval)
            elapsed += check_interval

        raise MediaUploadError(
            f"Video processing timeout after {timeout}s",
            platform="linkedin",
            media_type="video",
        )
