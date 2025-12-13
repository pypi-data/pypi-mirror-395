"""LinkedIn account factory for managing credentials and client creation."""

import logging
import os
from collections.abc import Callable

from marqetive.core.account_factory import BaseAccountFactory
from marqetive.platforms.exceptions import PlatformAuthError
from marqetive.platforms.linkedin.client import LinkedInClient
from marqetive.platforms.models import AccountStatus, AuthCredentials
from marqetive.utils.oauth import refresh_linkedin_token

logger = logging.getLogger(__name__)


class LinkedInAccountFactory(BaseAccountFactory):
    """Factory for creating and managing LinkedIn accounts and clients.

    Example:
        >>> factory = LinkedInAccountFactory(
        ...     client_id="your_client_id",
        ...     client_secret="your_client_secret"
        ... )
        >>> credentials = AuthCredentials(
        ...     platform="linkedin",
        ...     access_token="token",
        ...     refresh_token="refresh"
        ... )
        >>> client = await factory.create_authenticated_client(credentials)
        >>> async with client:
        ...     post = await client.create_post(request)
    """

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        on_status_update: Callable[[str, AccountStatus], None] | None = None,
    ) -> None:
        """Initialize LinkedIn account factory.

        Args:
            client_id: LinkedIn OAuth client ID (uses LINKEDIN_CLIENT_ID env if None).
            client_secret: LinkedIn OAuth client secret (uses LINKEDIN_CLIENT_SECRET env if None).
            on_status_update: Optional callback when account status changes.
        """
        super().__init__(on_status_update=on_status_update)
        self.client_id = client_id or os.getenv("LINKEDIN_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("LINKEDIN_CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            logger.warning(
                "LinkedIn client_id/client_secret not provided. "
                "Token refresh will not work."
            )

    @property
    def platform_name(self) -> str:
        """Get platform name."""
        return "linkedin"

    async def refresh_token(self, credentials: AuthCredentials) -> AuthCredentials:
        """Refresh LinkedIn OAuth2 access token.

        Args:
            credentials: Current credentials with refresh token.

        Returns:
            Updated credentials with new access token.

        Raises:
            PlatformAuthError: If refresh fails or credentials missing.
        """
        if not self.client_id or not self.client_secret:
            raise PlatformAuthError(
                "LinkedIn client_id and client_secret are required for token refresh",
                platform=self.platform_name,
            )

        if not credentials.refresh_token:
            raise PlatformAuthError(
                "No refresh token available",
                platform=self.platform_name,
            )

        logger.info("Refreshing LinkedIn access token...")
        return await refresh_linkedin_token(
            credentials,
            self.client_id,
            self.client_secret,
        )

    async def create_client(self, credentials: AuthCredentials) -> LinkedInClient:
        """Create LinkedIn API client.

        Args:
            credentials: Valid LinkedIn credentials.

        Returns:
            LinkedInClient instance.

        Raises:
            PlatformAuthError: If credentials are invalid.
        """
        if not credentials.access_token:
            raise PlatformAuthError(
                "Access token is required",
                platform=self.platform_name,
            )

        return LinkedInClient(credentials=credentials)

    async def validate_credentials(self, credentials: AuthCredentials) -> bool:
        """Validate LinkedIn credentials by making a test API call.

        Args:
            credentials: Credentials to validate.

        Returns:
            True if credentials are valid, False otherwise.
        """
        try:
            client = await self.create_client(credentials)
            async with client:
                # Try to verify credentials by getting current user
                # This would need to be implemented in the client
                return await client.is_authenticated()
        except Exception as e:
            logger.error(f"Error validating LinkedIn credentials: {e}")
            return False
