"""Progress tracking system for long-running operations.

This module provides models and utilities for tracking progress of operations
like media uploads, post creation, and other long-running tasks.
"""

from collections.abc import Callable
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ProgressStatus(str, Enum):
    """Status of a progress event."""

    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProgressEvent(BaseModel):
    """Represents a progress event for an operation.

    Attributes:
        operation: Name of the operation (e.g., "upload_media", "create_post").
        progress: Current progress value (e.g., bytes uploaded).
        total: Total expected value (e.g., total bytes).
        status: Current status of the operation.
        message: Optional human-readable message.
        metadata: Additional operation-specific data.
        timestamp: When this event occurred.

    Example:
        >>> event = ProgressEvent(
        ...     operation="upload_media",
        ...     progress=500,
        ...     total=1000,
        ...     status=ProgressStatus.IN_PROGRESS,
        ...     message="Uploading image..."
        ... )
        >>> print(f"Progress: {event.percentage}%")
        Progress: 50.0%
    """

    operation: str
    progress: int | float
    total: int | float | None = None
    status: ProgressStatus
    message: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)

    @property
    def percentage(self) -> float:
        """Calculate progress as a percentage.

        Returns:
            Progress percentage (0-100), or 0 if total is None.
        """
        if self.total is None or self.total == 0:
            return 0.0
        return (self.progress / self.total) * 100

    def is_complete(self) -> bool:
        """Check if operation is complete.

        Returns:
            True if status is COMPLETED, False otherwise.
        """
        return self.status == ProgressStatus.COMPLETED

    def is_failed(self) -> bool:
        """Check if operation failed.

        Returns:
            True if status is FAILED, False otherwise.
        """
        return self.status == ProgressStatus.FAILED


# Type alias for progress callback functions
ProgressCallback = Callable[[ProgressEvent], None]


class ProgressTracker:
    """Tracks and emits progress events for operations.

    Manages multiple progress callbacks and provides utilities for
    emitting progress events with consistent formatting.

    Example:
        >>> tracker = ProgressTracker()
        >>> tracker.add_callback(lambda e: print(f"{e.operation}: {e.percentage}%"))
        >>>
        >>> tracker.emit_start("upload_media")
        >>> tracker.emit_progress("upload_media", 500, 1000, "Uploading...")
        >>> tracker.emit_complete("upload_media", "Upload complete")
    """

    def __init__(self) -> None:
        """Initialize progress tracker."""
        self._callbacks: list[ProgressCallback] = []

    def add_callback(self, callback: ProgressCallback) -> None:
        """Add a progress callback.

        Args:
            callback: Function to call when progress events occur.

        Example:
            >>> def my_callback(event: ProgressEvent) -> None:
            ...     print(f"{event.operation}: {event.percentage}%")
            >>>
            >>> tracker.add_callback(my_callback)
        """
        self._callbacks.append(callback)

    def remove_callback(self, callback: ProgressCallback) -> None:
        """Remove a progress callback.

        Args:
            callback: Callback to remove.
        """
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def clear_callbacks(self) -> None:
        """Remove all callbacks."""
        self._callbacks.clear()

    def emit(self, event: ProgressEvent) -> None:
        """Emit a progress event to all callbacks.

        Args:
            event: Progress event to emit.
        """
        import contextlib

        for callback in self._callbacks:
            with contextlib.suppress(Exception):
                # Silently ignore callback errors to prevent disrupting operations
                callback(event)

    def emit_start(
        self,
        operation: str,
        total: int | float | None = None,
        message: str | None = None,
        **metadata: Any,
    ) -> None:
        """Emit an operation start event.

        Args:
            operation: Name of the operation.
            total: Total expected value (optional).
            message: Optional message.
            **metadata: Additional metadata.

        Example:
            >>> tracker.emit_start("upload_media", total=1024000,
            ...                    message="Starting upload...")
        """
        event = ProgressEvent(
            operation=operation,
            progress=0,
            total=total,
            status=ProgressStatus.STARTED,
            message=message or f"Starting {operation}",
            metadata=metadata,
        )
        self.emit(event)

    def emit_progress(
        self,
        operation: str,
        progress: int | float,
        total: int | float | None = None,
        message: str | None = None,
        **metadata: Any,
    ) -> None:
        """Emit a progress update event.

        Args:
            operation: Name of the operation.
            progress: Current progress value.
            total: Total expected value (optional).
            message: Optional message.
            **metadata: Additional metadata.

        Example:
            >>> tracker.emit_progress("upload_media", 512000, 1024000,
            ...                       message="Uploading...")
        """
        event = ProgressEvent(
            operation=operation,
            progress=progress,
            total=total,
            status=ProgressStatus.IN_PROGRESS,
            message=message,
            metadata=metadata,
        )
        self.emit(event)

    def emit_complete(
        self,
        operation: str,
        message: str | None = None,
        **metadata: Any,
    ) -> None:
        """Emit an operation complete event.

        Args:
            operation: Name of the operation.
            message: Optional message.
            **metadata: Additional metadata.

        Example:
            >>> tracker.emit_complete("upload_media",
            ...                       message="Upload successful!")
        """
        event = ProgressEvent(
            operation=operation,
            progress=100,
            total=100,
            status=ProgressStatus.COMPLETED,
            message=message or f"{operation} completed",
            metadata=metadata,
        )
        self.emit(event)

    def emit_failed(
        self,
        operation: str,
        error: str | Exception,
        **metadata: Any,
    ) -> None:
        """Emit an operation failed event.

        Args:
            operation: Name of the operation.
            error: Error message or exception.
            **metadata: Additional metadata.

        Example:
            >>> try:
            ...     # Some operation
            ...     pass
            ... except Exception as e:
            ...     tracker.emit_failed("upload_media", e)
        """
        message = str(error) if isinstance(error, Exception) else error
        event = ProgressEvent(
            operation=operation,
            progress=0,
            total=100,
            status=ProgressStatus.FAILED,
            message=message,
            metadata=metadata,
        )
        self.emit(event)

    def emit_cancelled(
        self,
        operation: str,
        message: str | None = None,
        **metadata: Any,
    ) -> None:
        """Emit an operation cancelled event.

        Args:
            operation: Name of the operation.
            message: Optional message.
            **metadata: Additional metadata.

        Example:
            >>> tracker.emit_cancelled("upload_media",
            ...                        message="Upload cancelled by user")
        """
        event = ProgressEvent(
            operation=operation,
            progress=0,
            total=100,
            status=ProgressStatus.CANCELLED,
            message=message or f"{operation} cancelled",
            metadata=metadata,
        )
        self.emit(event)
