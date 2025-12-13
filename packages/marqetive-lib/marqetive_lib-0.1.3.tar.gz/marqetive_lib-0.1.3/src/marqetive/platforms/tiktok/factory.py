"""TikTok account factory for managing credentials and client creation."""

import logging
import os
from collections.abc import Callable
from datetime import datetime, timedelta

from marqetive.core.account_factory import BaseAccountFactory
from marqetive.platforms.exceptions import PlatformAuthError
from marqetive.platforms.models import AccountStatus, AuthCredentials
from marqetive.platforms.tiktok.client import TikTokClient
from marqetive.utils.oauth import fetch_tiktok_token, refresh_tiktok_token

logger = logging.getLogger(__name__)


class TikTokAccountFactory(BaseAccountFactory):
    """Factory for creating and managing TikTok accounts and clients.

    This factory handles the instantiation of TikTokClients, manages OAuth
    credentials, and provides a mechanism for token refreshing.
    """

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        on_status_update: Callable[[str, AccountStatus], None] | None = None,
    ) -> None:
        """Initialize TikTok account factory.

        Args:
            client_id: TikTok App client ID (uses TIKTOK_CLIENT_ID env if None).
            client_secret: TikTok App client secret (uses TIKTOK_CLIENT_SECRET env if None).
            on_status_update: Optional callback when account status changes.
        """
        super().__init__(on_status_update=on_status_update)
        self.client_id = client_id or os.getenv("TIKTOK_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("TIKTOK_CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            logger.warning(
                "TikTok client_id/client_secret not provided. "
                "Token refresh may not work."
            )

    @property
    def platform_name(self) -> str:
        """Get the platform name."""
        return "tiktok"

    async def get_credentials_from_auth_code(
        self,
        auth_code: str,
        redirect_uri: str,
        code_verifier: str | None = None,
    ) -> AuthCredentials:
        """Get credentials from an authorization code.

        This method exchanges an authorization code for an access token and
        formats it into the standard AuthCredentials object.

        Args:
            auth_code: The authorization code received from TikTok.
            redirect_uri: The redirect URI used in the initial auth request.
            code_verifier: The PKCE code verifier, if used.

        Returns:
            An AuthCredentials object for the user.

        Raises:
            PlatformAuthError: If the token exchange fails.
        """
        if not self.client_id or not self.client_secret:
            raise PlatformAuthError(
                "TikTok client_id and client_secret are required.",
                platform=self.platform_name,
            )

        token_data = await fetch_tiktok_token(
            code=auth_code,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=redirect_uri,
            code_verifier=code_verifier,
        )

        expires_at = None
        if "expires_in" in token_data:
            expires_at = datetime.now() + timedelta(seconds=token_data["expires_in"])

        refresh_expires_at = None
        if "refresh_expires_in" in token_data:
            refresh_expires_at = datetime.now() + timedelta(
                seconds=token_data["refresh_expires_in"]
            )

        credentials = AuthCredentials(
            platform=self.platform_name,
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            expires_at=expires_at,
            scope=token_data.get("scope", []),
            additional_data={
                "open_id": token_data["open_id"],
                "token_type": token_data.get("token_type"),
                "refresh_expires_at": refresh_expires_at,
            },
        )
        return credentials

    async def refresh_token(self, credentials: AuthCredentials) -> AuthCredentials:
        """Refresh a TikTok OAuth2 access token.

        Args:
            credentials: The current credentials containing the refresh token.

        Returns:
            Updated credentials with a new access token.

        Raises:
            PlatformAuthError: If refresh fails or credentials are missing.
        """
        if not self.client_id or not self.client_secret:
            raise PlatformAuthError(
                "TikTok client_id and client_secret are required for token refresh.",
                platform=self.platform_name,
            )

        if not credentials.refresh_token:
            raise PlatformAuthError(
                "No refresh token available for TikTok.", platform=self.platform_name
            )

        logger.info("Refreshing TikTok access token...")
        # This function would call the actual TikTok token refresh endpoint
        return await refresh_tiktok_token(
            credentials, self.client_id, self.client_secret
        )

    async def create_client(self, credentials: AuthCredentials) -> TikTokClient:
        """Create a TikTok API client.

        Args:
            credentials: Valid TikTok authentication credentials.

        Returns:
            An instance of TikTokClient.

        Raises:
            PlatformAuthError: If credentials are incomplete or invalid.
        """
        if not credentials.access_token:
            raise PlatformAuthError(
                "Access token is required for TikTok.", platform=self.platform_name
            )
        if (
            not credentials.additional_data
            or "open_id" not in credentials.additional_data
        ):
            raise PlatformAuthError(
                "'open_id' must be provided in additional_data for TikTok.",
                platform=self.platform_name,
            )

        return TikTokClient(credentials=credentials)

    async def validate_credentials(self, credentials: AuthCredentials) -> bool:
        """Validate TikTok credentials by making a test API call.

        Args:
            credentials: The credentials to validate.

        Returns:
            True if the credentials are valid, False otherwise.
        """
        try:
            client = await self.create_client(credentials)
            async with client:
                return await client.is_authenticated()
        except PlatformAuthError as e:
            logger.warning(f"TikTok credential validation failed: {e}")
            return False
        except Exception as e:
            logger.error(
                f"An unexpected error occurred during TikTok credential validation: {e}"
            )
            return False
