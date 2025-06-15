"""
AI System Error Handling Utilities.

This module provides common error handling patterns and utilities
for AI system operations, including context managers and decorators.
"""

import functools
import logging
from collections.abc import Callable, Generator
from contextlib import contextmanager
from typing import Any, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


class AISystemError(Exception):
    """Base exception for AI system errors."""

    pass


class AIEntityNotFoundError(AISystemError):
    """Raised when an AI entity is not found."""

    pass


class AIComponentError(AISystemError):
    """Raised when there's an issue with AI components."""

    pass


class AIConfigurationError(AISystemError):
    """Raised when there's an issue with AI configuration."""

    pass


@contextmanager
def ai_operation_context(operation_name: str) -> Generator[None, None, None]:
    """
    Context manager for AI operations with consistent error handling.

    Args:
        operation_name: Name of the operation for logging
    """
    logger.debug(f"Starting AI operation: {operation_name}")
    try:
        yield
        logger.debug(f"Completed AI operation: {operation_name}")
    except Exception as e:
        logger.error(f"Error in AI operation '{operation_name}': {e}")
        raise AISystemError(f"Failed to execute {operation_name}: {e}") from e


def handle_ai_errors(
    operation_name: str, default_return: Any = None, reraise: bool = False
) -> Callable[[F], F]:
    """
    Decorator for AI operations with consistent error handling.

    Args:
        operation_name: Name of the operation for logging
        default_return: Default value to return on error
        reraise: Whether to reraise the exception after logging
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {operation_name}: {e}")
                if reraise:
                    raise
                return default_return

        return wrapper  # type: ignore

    return decorator


def safe_ai_operation(
    func: F,
    *args: Any,
    operation_name: str = "AI operation",
    default_return: Any = None,
    **kwargs: Any,
) -> Any:
    """
    Safely execute an AI operation with error handling.

    Args:
        func: Function to execute
        *args: Arguments for the function
        operation_name: Name of the operation for logging
        default_return: Default value to return on error
        **kwargs: Keyword arguments for the function
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error in {operation_name}: {e}")
        return default_return


@contextmanager
def suppress_ai_errors(operation_name: str) -> Generator[None, None, None]:
    """
    Context manager that suppresses AI errors and logs them.

    Args:
        operation_name: Name of the operation for logging
    """
    try:
        yield
    except Exception as e:
        logger.warning(f"Suppressed error in {operation_name}: {e}")


def validate_entity_id(entity_id: str | None) -> str:
    """
    Validate that an entity ID is valid.

    Args:
        entity_id: The entity ID to validate

    Returns:
        The validated entity ID

    Raises:
        AIEntityNotFoundError: If the entity ID is invalid
    """
    if not entity_id or not isinstance(entity_id, str):
        raise AIEntityNotFoundError(f"Invalid entity ID: {entity_id}")
    return entity_id


def ensure_ai_component(
    component_manager: Any, entity_id: str, component_type: type
) -> Any:
    """
    Ensure an entity has a specific AI component.

    Args:
        component_manager: The component manager
        entity_id: The entity ID
        component_type: The component type to check

    Returns:
        The component instance

    Raises:
        AIComponentError: If the component is missing
    """
    try:
        component = component_manager.get_component(entity_id, component_type)
        if component is None:
            raise AIComponentError(
                f"Entity {entity_id} missing required component "
                f"{component_type.__name__}"
            )
        return component
    except Exception as e:
        raise AIComponentError(
            f"Failed to get component {component_type.__name__} "
            f"for entity {entity_id}: {e}"
        ) from e


class AIOperationMetrics:
    """Simple metrics collection for AI operations."""

    def __init__(self) -> None:
        self.operation_counts: dict[str, int] = {}
        self.error_counts: dict[str, int] = {}
        self.operation_times: dict[str, float] = {}  # For timing operations

    def record_operation(self, operation_name: str) -> None:
        """Record a successful operation."""
        current_count = self.operation_counts.get(operation_name, 0)
        self.operation_counts[operation_name] = current_count + 1

    def record_error(self, operation_name: str) -> None:
        """Record an error in an operation."""
        self.error_counts[operation_name] = self.error_counts.get(operation_name, 0) + 1

    @contextmanager
    def operation_timer(self, operation_name: str) -> Generator[None, None, None]:
        """Context manager for timing operations."""
        import time

        start_time = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start_time
            self.operation_times[operation_name] = duration
            self.record_operation(operation_name)

    def get_stats(self) -> dict[str, Any]:
        """Get operation statistics."""
        return {
            "operations": dict(self.operation_counts),
            "errors": dict(self.error_counts),
            "operation_times": dict(self.operation_times),
            "total_operations": sum(self.operation_counts.values()),
            "total_errors": sum(self.error_counts.values()),
        }

    def reset(self) -> None:
        """Reset all metrics."""
        self.operation_counts.clear()
        self.error_counts.clear()


# Global metrics instance
_ai_metrics = AIOperationMetrics()


def get_ai_metrics() -> AIOperationMetrics:
    """Get the global AI metrics instance."""
    return _ai_metrics


def ai_error_handler(operation_name: str) -> Callable[[F], F]:
    """
    Decorator for AI operations with consistent error handling.

    Args:
        operation_name: Name of the operation for logging and metrics

    Returns:
        Decorated function with error handling
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            metrics = get_ai_metrics()
            try:
                logger.debug(f"Starting AI operation: {operation_name}")
                result = func(*args, **kwargs)
                metrics.record_operation(operation_name)
                logger.debug(f"Completed AI operation: {operation_name}")
                return result
            except Exception as e:
                metrics.record_error(operation_name)
                logger.error(f"Error in AI operation '{operation_name}': {e}")
                raise

        return wrapper  # type: ignore

    return decorator
