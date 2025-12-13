"""TikTok-specific models for post creation.

This module defines TikTok-specific data models for creating video posts,
including privacy settings and content toggles.
"""

from enum import StrEnum

from pydantic import BaseModel, Field


class PrivacyLevel(StrEnum):
    """Privacy level options for TikTok posts.

    Attributes:
        PUBLIC: Visible to everyone
        FRIENDS: Visible to mutual followers/friends only
        PRIVATE: Visible only to the author (for unaudited apps)
    """

    PUBLIC = "PUBLIC_TO_EVERYONE"
    FRIENDS = "MUTUAL_FOLLOW_FRIENDS"
    PRIVATE = "SELF_ONLY"


class TikTokPostRequest(BaseModel):
    """TikTok-specific post creation request.

    TikTok only supports video posts. Videos must be between 3 seconds
    and 10 minutes, and under 4GB in size.

    Attributes:
        title: Video title/caption (max 2200 characters)
        video_url: URL to video file (required)
        video_id: Pre-uploaded video ID
        privacy_level: Privacy setting (PUBLIC, FRIENDS, PRIVATE)
        disable_comment: Disable comments on the video
        disable_duet: Disable duet feature
        disable_stitch: Disable stitch feature
        video_cover_timestamp_ms: Timestamp in ms for auto-generated cover
        brand_content_toggle: Mark as branded/sponsored content
        brand_organic_toggle: Mark as organic branded content
        schedule_time: Unix timestamp to schedule post (10 mins to 10 days ahead)

    Example:
        >>> # Public video post
        >>> request = TikTokPostRequest(
        ...     title="Check out this dance!",
        ...     video_url="https://example.com/dance.mp4",
        ...     privacy_level=PrivacyLevel.PUBLIC
        ... )

        >>> # Private video with features disabled
        >>> request = TikTokPostRequest(
        ...     title="Personal video",
        ...     video_url="https://example.com/video.mp4",
        ...     privacy_level=PrivacyLevel.PRIVATE,
        ...     disable_comment=True,
        ...     disable_duet=True,
        ...     disable_stitch=True
        ... )

        >>> # Branded content
        >>> request = TikTokPostRequest(
        ...     title="Sponsored review",
        ...     video_url="https://example.com/review.mp4",
        ...     privacy_level=PrivacyLevel.PUBLIC,
        ...     brand_content_toggle=True
        ... )
    """

    title: str | None = None
    video_url: str | None = None
    video_id: str | None = None
    privacy_level: PrivacyLevel = PrivacyLevel.PRIVATE
    disable_comment: bool = False
    disable_duet: bool = False
    disable_stitch: bool = False
    video_cover_timestamp_ms: int | None = None
    brand_content_toggle: bool = False
    brand_organic_toggle: bool = False
    schedule_time: int | None = Field(default=None, description="Unix timestamp")
