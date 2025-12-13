"""Base account factory for managing platform credentials and client creation.

This module provides an abstract base class for platform-specific account
factories that handle credential management, token refresh, and client creation.
"""

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from marqetive.platforms.exceptions import PlatformAuthError
from marqetive.platforms.models import AccountStatus, AuthCredentials

logger = logging.getLogger(__name__)


class BaseAccountFactory(ABC):
    """Abstract base class for platform account factories.

    Account factories manage the lifecycle of platform credentials including:
    - Token expiry checking and automatic refresh
    - Account status management
    - Platform-specific client creation

    Subclasses must implement:
    - refresh_token(): Platform-specific token refresh logic
    - create_client(): Create platform-specific API client
    - validate_credentials(): Check if credentials are valid

    Example:
        >>> class TwitterAccountFactory(BaseAccountFactory):
        ...     async def refresh_token(self, credentials):
        ...         # Implement Twitter OAuth token refresh
        ...         pass
        ...
        ...     async def create_client(self, credentials):
        ...         return TwitterClient(credentials=credentials)
        ...
        ...     async def validate_credentials(self, credentials):
        ...         # Check if credentials work
        ...         pass
    """

    def __init__(
        self,
        on_status_update: Callable[[str, AccountStatus], None] | None = None,
    ) -> None:
        """Initialize the account factory.

        Args:
            on_status_update: Optional callback when account status changes.
                            Called with (user_id, new_status).
        """
        self.on_status_update = on_status_update

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Get the name of the platform this factory manages.

        Returns:
            Platform name (e.g., "twitter", "linkedin").
        """
        pass

    @abstractmethod
    async def refresh_token(self, credentials: AuthCredentials) -> AuthCredentials:
        """Refresh the OAuth access token.

        Args:
            credentials: Current credentials with expired token.

        Returns:
            Updated credentials with new token.

        Raises:
            PlatformAuthError: If token refresh fails.
        """
        pass

    @abstractmethod
    async def create_client(self, credentials: AuthCredentials) -> Any:
        """Create a platform-specific API client.

        Args:
            credentials: Valid credentials for the platform.

        Returns:
            Platform-specific API client instance.

        Raises:
            PlatformAuthError: If credentials are invalid.
        """
        pass

    @abstractmethod
    async def validate_credentials(self, credentials: AuthCredentials) -> bool:
        """Validate that credentials are working.

        Args:
            credentials: Credentials to validate.

        Returns:
            True if credentials are valid, False otherwise.
        """
        pass

    async def get_credentials(
        self,
        credentials: AuthCredentials,
        auto_refresh: bool = True,
    ) -> AuthCredentials:
        """Get credentials, refreshing if necessary.

        This method checks if credentials are expired and automatically
        refreshes them if auto_refresh is True.

        Args:
            credentials: Current credentials.
            auto_refresh: Whether to automatically refresh expired tokens.

        Returns:
            Valid credentials (refreshed if necessary).

        Raises:
            PlatformAuthError: If refresh fails or credentials are invalid.
        """
        # Check if token needs refresh
        if credentials.needs_refresh():
            if not auto_refresh:
                logger.warning(
                    f"Credentials for {credentials.platform} are expired "
                    "but auto_refresh is disabled"
                )
                return credentials

            logger.info(
                f"Token expired for {credentials.platform}, attempting refresh..."
            )
            try:
                refreshed_creds = await self.refresh_token(credentials)
                refreshed_creds.mark_valid()

                # Notify status update
                if self.on_status_update and refreshed_creds.user_id:
                    self.on_status_update(refreshed_creds.user_id, AccountStatus.VALID)

                logger.info(f"Successfully refreshed token for {credentials.platform}")
                return refreshed_creds

            except PlatformAuthError as e:
                # Determine if this is an OAuth error requiring reconnection
                if "oauth" in str(e).lower() or "authorization" in str(e).lower():
                    credentials.mark_reconnection_required()
                    if self.on_status_update and credentials.user_id:
                        self.on_status_update(
                            credentials.user_id, AccountStatus.RECONNECTION_REQUIRED
                        )
                    logger.error(
                        f"OAuth error refreshing token for {credentials.platform}: {e}"
                    )
                else:
                    credentials.mark_error()
                    if self.on_status_update and credentials.user_id:
                        self.on_status_update(credentials.user_id, AccountStatus.ERROR)
                    logger.error(
                        f"Error refreshing token for {credentials.platform}: {e}"
                    )
                raise

        return credentials

    async def create_authenticated_client(
        self,
        credentials: AuthCredentials,
        auto_refresh: bool = True,
    ) -> Any:
        """Create an authenticated client, refreshing credentials if needed.

        This is the main method to use for getting a ready-to-use client.

        Args:
            credentials: Platform credentials.
            auto_refresh: Whether to automatically refresh expired tokens.

        Returns:
            Authenticated platform client.

        Raises:
            PlatformAuthError: If authentication fails.
        """
        # Get valid credentials (refresh if needed)
        valid_creds = await self.get_credentials(credentials, auto_refresh=auto_refresh)

        # Create client
        client = await self.create_client(valid_creds)

        return client

    def _update_status(self, user_id: str | None, status: AccountStatus) -> None:
        """Internal method to update account status.

        Args:
            user_id: User ID for the account.
            status: New status.
        """
        if self.on_status_update and user_id:
            try:
                self.on_status_update(user_id, status)
            except Exception as e:
                logger.error(f"Error calling status update callback: {e}")
