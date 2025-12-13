"""Instagram account factory for managing credentials and client creation."""

import logging
from collections.abc import Callable

from marqetive.core.account_factory import BaseAccountFactory
from marqetive.platforms.exceptions import PlatformAuthError
from marqetive.platforms.instagram.client import InstagramClient
from marqetive.platforms.models import AccountStatus, AuthCredentials
from marqetive.utils.oauth import refresh_instagram_token

logger = logging.getLogger(__name__)


class InstagramAccountFactory(BaseAccountFactory):
    """Factory for creating and managing Instagram accounts and clients.

    Example:
        >>> factory = InstagramAccountFactory()
        >>> credentials = AuthCredentials(
        ...     platform="instagram",
        ...     access_token="token"
        ... )
        >>> client = await factory.create_authenticated_client(credentials)
        >>> async with client:
        ...     post = await client.create_post(request)
    """

    def __init__(
        self,
        on_status_update: Callable[[str, AccountStatus], None] | None = None,
    ) -> None:
        """Initialize Instagram account factory.

        Args:
            on_status_update: Optional callback when account status changes.
        """
        super().__init__(on_status_update=on_status_update)

    @property
    def platform_name(self) -> str:
        """Get platform name."""
        return "instagram"

    async def refresh_token(self, credentials: AuthCredentials) -> AuthCredentials:
        """Refresh Instagram long-lived access token.

        Args:
            credentials: Current credentials.

        Returns:
            Updated credentials with refreshed token.

        Raises:
            PlatformAuthError: If refresh fails.
        """
        logger.info("Refreshing Instagram access token...")
        return await refresh_instagram_token(credentials)

    async def create_client(self, credentials: AuthCredentials) -> InstagramClient:
        """Create Instagram API client.

        Args:
            credentials: Valid Instagram credentials.

        Returns:
            InstagramClient instance.

        Raises:
            PlatformAuthError: If credentials are invalid.
        """
        if not credentials.access_token:
            raise PlatformAuthError(
                "Access token is required",
                platform=self.platform_name,
            )

        # Instagram needs instagram_business_account_id in additional_data
        instagram_business_account_id = credentials.additional_data.get(
            "instagram_business_account_id"
        )
        if not instagram_business_account_id:
            raise PlatformAuthError(
                "instagram_business_account_id is required in additional_data",
                platform=self.platform_name,
            )

        return InstagramClient(credentials=credentials)

    async def validate_credentials(self, credentials: AuthCredentials) -> bool:
        """Validate Instagram credentials by making a test API call.

        Args:
            credentials: Credentials to validate.

        Returns:
            True if credentials are valid, False otherwise.
        """
        try:
            client = await self.create_client(credentials)
            async with client:
                # Try to verify credentials
                return await client.is_authenticated()
        except Exception as e:
            logger.error(f"Error validating Instagram credentials: {e}")
            return False
