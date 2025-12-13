"""Platform registry for managing platform manager instances.

This module provides a singleton registry pattern for registering and accessing
platform managers across the application.
"""

import threading
from typing import Any, TypeVar

from marqetive.platforms.models import AuthCredentials

# Type variable for manager classes
ManagerType = TypeVar("ManagerType")


class PlatformRegistry:
    """Singleton registry for platform managers.

    The registry maintains a mapping of platform names to their manager classes
    and provides caching of manager instances to avoid unnecessary recreation.

    Thread-safe implementation using threading.Lock.

    Example:
        >>> from marqetive.platforms.twitter.manager import TwitterPostManager
        >>> registry = PlatformRegistry()
        >>> registry.register_platform("twitter", TwitterPostManager)
        >>> manager = registry.get_manager("twitter", credentials=creds)
    """

    _instance: "PlatformRegistry | None" = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls) -> "PlatformRegistry":
        """Ensure only one instance exists (singleton pattern)."""
        if cls._instance is None:
            with cls._lock:
                # Double-check locking pattern
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize the registry."""
        # Only initialize once
        if self._initialized:
            return

        self._platforms: dict[str, type] = {}
        self._manager_cache: dict[str, Any] = {}
        self._cache_lock = threading.Lock()
        self._initialized = True

    def register_platform(self, platform_name: str, manager_class: type) -> None:
        """Register a platform manager class.

        Args:
            platform_name: Name of the platform (e.g., "twitter", "linkedin").
            manager_class: The manager class to register.

        Raises:
            ValueError: If platform is already registered.

        Example:
            >>> registry.register_platform("twitter", TwitterPostManager)
        """
        if platform_name in self._platforms:
            raise ValueError(f"Platform '{platform_name}' is already registered")

        self._platforms[platform_name] = manager_class

    def unregister_platform(self, platform_name: str) -> None:
        """Unregister a platform and clear its cached instances.

        Args:
            platform_name: Name of the platform to unregister.

        Example:
            >>> registry.unregister_platform("twitter")
        """
        with self._cache_lock:
            self._platforms.pop(platform_name, None)
            # Clear cached instances for this platform
            keys_to_remove = [
                k for k in self._manager_cache if k.startswith(f"{platform_name}:")
            ]
            for key in keys_to_remove:
                self._manager_cache.pop(key)

    def get_manager(
        self,
        platform_name: str,
        use_cache: bool = True,
        **kwargs: Any,
    ) -> Any:
        """Get or create a manager instance for the specified platform.

        Args:
            platform_name: Name of the platform (e.g., "twitter", "linkedin").
            use_cache: Whether to use cached instance (default: True).
            **kwargs: Arguments to pass to the manager constructor.

        Returns:
            Manager instance for the platform.

        Raises:
            ValueError: If platform is not registered.

        Example:
            >>> manager = registry.get_manager("twitter", credentials=creds)
            >>> post = await manager.execute_post(...)
        """
        if platform_name not in self._platforms:
            available = ", ".join(self.get_available_platforms())
            raise ValueError(
                f"Platform '{platform_name}' is not registered. "
                f"Available platforms: {available}"
            )

        # Generate cache key from platform name and kwargs
        cache_key = self._generate_cache_key(platform_name, **kwargs)

        if use_cache:
            with self._cache_lock:
                if cache_key in self._manager_cache:
                    return self._manager_cache[cache_key]

        # Create new manager instance
        manager_class = self._platforms[platform_name]
        manager = manager_class(**kwargs)

        if use_cache:
            with self._cache_lock:
                self._manager_cache[cache_key] = manager

        return manager

    def get_available_platforms(self) -> list[str]:
        """Get list of all registered platform names.

        Returns:
            List of platform names.

        Example:
            >>> platforms = registry.get_available_platforms()
            >>> print(platforms)
            ['twitter', 'linkedin', 'instagram', 'tiktok']
        """
        return list(self._platforms.keys())

    def clear_cache(self) -> None:
        """Clear all cached manager instances.

        Example:
            >>> registry.clear_cache()
        """
        with self._cache_lock:
            self._manager_cache.clear()

    def _generate_cache_key(self, platform_name: str, **kwargs: Any) -> str:
        """Generate a cache key for manager instance.

        Args:
            platform_name: Name of the platform.
            **kwargs: Manager constructor arguments.

        Returns:
            Cache key string.
        """
        # For credentials, use account_id if available
        if "credentials" in kwargs:
            creds = kwargs["credentials"]
            if isinstance(creds, AuthCredentials) and creds.user_id:
                return f"{platform_name}:user_id:{creds.user_id}"

        # Default to platform name only
        return platform_name


# Global registry instance
_global_registry: PlatformRegistry | None = None
_global_lock = threading.Lock()


def get_registry() -> PlatformRegistry:
    """Get the global platform registry instance.

    Returns:
        Global PlatformRegistry instance.

    Example:
        >>> registry = get_registry()
        >>> manager = registry.get_manager("twitter", credentials=creds)
    """
    global _global_registry

    if _global_registry is None:
        with _global_lock:
            if _global_registry is None:
                _global_registry = PlatformRegistry()

    return _global_registry


def register_platform(platform_name: str, manager_class: type) -> None:
    """Register a platform in the global registry.

    Convenience function that uses the global registry.

    Args:
        platform_name: Name of the platform.
        manager_class: The manager class to register.

    Example:
        >>> from marqetive.platforms.twitter.manager import TwitterPostManager
        >>> register_platform("twitter", TwitterPostManager)
    """
    registry = get_registry()
    registry.register_platform(platform_name, manager_class)


def get_manager_for_platform(platform_name: str, **kwargs: Any) -> Any:
    """Get a manager instance for the specified platform.

    Convenience function that uses the global registry.

    Args:
        platform_name: Name of the platform.
        **kwargs: Arguments to pass to the manager constructor.

    Returns:
        Manager instance for the platform.

    Example:
        >>> manager = get_manager_for_platform("twitter", credentials=creds)
        >>> post = await manager.execute_post(...)
    """
    registry = get_registry()
    return registry.get_manager(platform_name, **kwargs)


def get_available_platforms() -> list[str]:
    """Get list of all registered platforms.

    Convenience function that uses the global registry.

    Returns:
        List of platform names.

    Example:
        >>> platforms = get_available_platforms()
        >>> print(platforms)
        ['twitter', 'linkedin', 'instagram']
    """
    registry = get_registry()
    return registry.get_available_platforms()
