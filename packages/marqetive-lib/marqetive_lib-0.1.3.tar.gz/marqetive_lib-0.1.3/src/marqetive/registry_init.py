"""Registry initialization for platform managers.

This module provides the initialization function that registers all available
platform managers with the global registry.
"""

import logging

from marqetive.core.registry import register_platform
from marqetive.platforms.instagram.manager import InstagramPostManager
from marqetive.platforms.linkedin.manager import LinkedInPostManager
from marqetive.platforms.tiktok.manager import TikTokPostManager
from marqetive.platforms.twitter.manager import TwitterPostManager

logger = logging.getLogger(__name__)

_initialized = False


def initialize_platform_registry() -> None:
    """Initialize the platform registry with all available platforms.

    This function registers all platform managers (Twitter, LinkedIn, Instagram, TikTok)
    with the global registry. It should be called once at application startup.

    This function is idempotent - calling it multiple times is safe.

    Example:
        >>> from marqetive import initialize_platform_registry
        >>> initialize_platform_registry()
        >>> # Now you can use get_manager_for_platform()
        >>> from marqetive import get_manager_for_platform
        >>> manager = get_manager_for_platform("twitter")
    """
    global _initialized

    if _initialized:
        logger.debug("Platform registry already initialized")
        return

    logger.info("Initializing platform registry...")

    # Register all platform managers
    register_platform("twitter", TwitterPostManager)
    register_platform("linkedin", LinkedInPostManager)
    register_platform("instagram", InstagramPostManager)
    register_platform("tiktok", TikTokPostManager)

    _initialized = True
    logger.info("Platform registry initialized with 4 platforms")


def is_registry_initialized() -> bool:
    """Check if registry has been initialized.

    Returns:
        True if initialized, False otherwise.
    """
    return _initialized


def reset_registry() -> None:
    """Reset the initialization flag.

    This is mainly useful for testing. It allows re-initialization of the registry.
    """
    global _initialized
    _initialized = False
