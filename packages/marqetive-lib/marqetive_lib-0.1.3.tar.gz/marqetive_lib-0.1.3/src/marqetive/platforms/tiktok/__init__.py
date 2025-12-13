"""TikTok platform integration."""

from marqetive.platforms.tiktok.client import TikTokClient
from marqetive.platforms.tiktok.factory import TikTokAccountFactory
from marqetive.platforms.tiktok.manager import TikTokPostManager

__all__ = ["TikTokClient", "TikTokAccountFactory", "TikTokPostManager"]
