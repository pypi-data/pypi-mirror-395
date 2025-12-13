"""Twitter account factory for managing credentials and client creation."""

import logging
import os
from collections.abc import Callable

from marqetive.core.account_factory import BaseAccountFactory
from marqetive.platforms.exceptions import PlatformAuthError
from marqetive.platforms.models import AccountStatus, AuthCredentials
from marqetive.platforms.twitter.client import TwitterClient
from marqetive.utils.oauth import refresh_twitter_token

logger = logging.getLogger(__name__)


class TwitterAccountFactory(BaseAccountFactory):
    """Factory for creating and managing Twitter/X accounts and clients.

    Example:
        >>> factory = TwitterAccountFactory(
        ...     client_id="your_client_id",
        ...     client_secret="your_client_secret"
        ... )
        >>> credentials = AuthCredentials(
        ...     platform="twitter",
        ...     access_token="token",
        ...     refresh_token="refresh"
        ... )
        >>> client = await factory.create_authenticated_client(credentials)
        >>> async with client:
        ...     tweet = await client.create_post(request)
    """

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        on_status_update: Callable[[str, AccountStatus], None] | None = None,
    ) -> None:
        """Initialize Twitter account factory.

        Args:
            client_id: Twitter OAuth client ID (uses TWITTER_CLIENT_ID env if None).
            client_secret: Twitter OAuth client secret (uses TWITTER_CLIENT_SECRET env if None).
            on_status_update: Optional callback when account status changes.
        """
        super().__init__(on_status_update=on_status_update)
        self.client_id = client_id or os.getenv("TWITTER_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("TWITTER_CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            logger.warning(
                "Twitter client_id/client_secret not provided. "
                "Token refresh will not work."
            )

    @property
    def platform_name(self) -> str:
        """Get platform name."""
        return "twitter"

    async def refresh_token(self, credentials: AuthCredentials) -> AuthCredentials:
        """Refresh Twitter OAuth2 access token.

        Args:
            credentials: Current credentials with refresh token.

        Returns:
            Updated credentials with new access token.

        Raises:
            PlatformAuthError: If refresh fails or credentials missing.
        """
        if not self.client_id or not self.client_secret:
            raise PlatformAuthError(
                "Twitter client_id and client_secret are required for token refresh",
                platform=self.platform_name,
            )

        if not credentials.refresh_token:
            raise PlatformAuthError(
                "No refresh token available",
                platform=self.platform_name,
            )

        logger.info("Refreshing Twitter access token...")
        return await refresh_twitter_token(
            credentials,
            self.client_id,
            self.client_secret,
        )

    async def create_client(self, credentials: AuthCredentials) -> TwitterClient:
        """Create Twitter API client.

        Args:
            credentials: Valid Twitter credentials.

        Returns:
            TwitterClient instance.

        Raises:
            PlatformAuthError: If credentials are invalid.
        """
        if not credentials.access_token:
            raise PlatformAuthError(
                "Access token is required",
                platform=self.platform_name,
            )

        # Get additional data for Twitter
        additional_data = credentials.additional_data or {}

        # Twitter needs API key/secret for some operations
        api_key = additional_data.get("api_key") or os.getenv("TWITTER_API_KEY")
        api_secret = additional_data.get("api_secret") or os.getenv(
            "TWITTER_API_SECRET"
        )

        # Update additional_data if we have env values
        if api_key:
            additional_data["api_key"] = api_key
        if api_secret:
            additional_data["api_secret"] = api_secret

        credentials.additional_data = additional_data

        return TwitterClient(credentials=credentials)

    async def validate_credentials(self, credentials: AuthCredentials) -> bool:
        """Validate Twitter credentials by making a test API call.

        Args:
            credentials: Credentials to validate.

        Returns:
            True if credentials are valid, False otherwise.
        """
        try:
            client = await self.create_client(credentials)
            async with client:
                # Try to verify credentials by getting current user
                # This is a lightweight call to test authentication
                if client._tweepy_client:
                    me = client._tweepy_client.get_me()
                    return me is not None
                return False
        except Exception as e:
            logger.error(f"Error validating Twitter credentials: {e}")
            return False
