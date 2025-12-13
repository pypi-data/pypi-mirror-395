"""Twitter/X platform integration."""

from marqetive.platforms.twitter.client import TwitterClient
from marqetive.platforms.twitter.factory import TwitterAccountFactory
from marqetive.platforms.twitter.manager import TwitterPostManager

__all__ = ["TwitterClient", "TwitterAccountFactory", "TwitterPostManager"]
