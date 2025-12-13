"""Instagram platform integration."""

from marqetive.platforms.instagram.client import InstagramClient
from marqetive.platforms.instagram.factory import InstagramAccountFactory
from marqetive.platforms.instagram.manager import InstagramPostManager

__all__ = ["InstagramClient", "InstagramAccountFactory", "InstagramPostManager"]
