"""
Singleton Registry for AI System Components.

This module provides a clean singleton pattern implementation to manage
global state without using global variables directly.
"""

import logging
from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    from yendoria.systems.ai_engine_integration import AIEngineIntegration
    from yendoria.systems.ai_manager import AIManager
    from yendoria.systems.config_manager import ConfigManager

logger = logging.getLogger(__name__)

T = TypeVar("T")


class Singleton(Generic[T]):
    """Generic singleton pattern implementation."""

    def __init__(self) -> None:
        self._instance: T | None = None
        self._initialized = False

    def get_instance(self) -> T | None:
        """Get the singleton instance."""
        return self._instance

    def set_instance(self, instance: T) -> T:
        """Set the singleton instance."""
        if self._instance is not None:
            logger.warning("Replacing existing singleton instance")
        self._instance = instance
        self._initialized = True
        return instance

    def clear_instance(self) -> None:
        """Clear the singleton instance."""
        if self._instance and hasattr(self._instance, "shutdown"):
            try:
                self._instance.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down singleton instance: {e}")
        self._instance = None
        self._initialized = False

    def is_initialized(self) -> bool:
        """Check if the singleton is initialized."""
        return self._initialized

    def require_instance(self) -> T:
        """Get the instance or raise an error if not initialized."""
        if self._instance is None:
            raise RuntimeError("Singleton not initialized")
        return self._instance


# Singleton instances for AI system components
_ai_manager_singleton: Singleton["AIManager"] = Singleton()
_ai_integration_singleton: Singleton["AIEngineIntegration"] = Singleton()
_config_manager_singleton: Singleton["ConfigManager"] = Singleton()


def get_ai_manager() -> "AIManager":
    """Get the AI manager singleton instance."""
    return _ai_manager_singleton.require_instance()


def set_ai_manager(instance: "AIManager") -> "AIManager":
    """Set the AI manager singleton instance."""
    return _ai_manager_singleton.set_instance(instance)


def clear_ai_manager() -> None:
    """Clear the AI manager singleton."""
    _ai_manager_singleton.clear_instance()


def get_ai_integration() -> "AIEngineIntegration":
    """Get the AI integration singleton instance."""
    return _ai_integration_singleton.require_instance()


def set_ai_integration(instance: "AIEngineIntegration") -> "AIEngineIntegration":
    """Set the AI integration singleton instance."""
    return _ai_integration_singleton.set_instance(instance)


def clear_ai_integration() -> None:
    """Clear the AI integration singleton."""
    _ai_integration_singleton.clear_instance()


def get_config_manager() -> "ConfigManager":
    """Get the config manager singleton instance."""
    return _config_manager_singleton.require_instance()


def set_config_manager(instance: "ConfigManager") -> "ConfigManager":
    """Set the config manager singleton instance."""
    return _config_manager_singleton.set_instance(instance)


def clear_config_manager() -> None:
    """Clear the config manager singleton."""
    _config_manager_singleton.clear_instance()


def shutdown_all_singletons() -> None:
    """Shutdown all AI system singletons."""
    logger.info("Shutting down all AI system singletons")
    clear_ai_integration()
    clear_ai_manager()
    clear_config_manager()
    logger.info("All AI system singletons shut down")


# Initialization convenience functions for compatibility
def initialize_ai_manager(*args: Any, **kwargs: Any) -> "AIManager":
    """Initialize and set up AI manager singleton."""
    from yendoria.systems.ai_manager import AIManager

    instance = AIManager(*args, **kwargs)
    return set_ai_manager(instance)


def initialize_config_manager(*args: Any, **kwargs: Any) -> "ConfigManager":
    """Initialize and set up config manager singleton."""
    from yendoria.systems.config_manager import ConfigManager

    instance = ConfigManager(*args, **kwargs)
    return set_config_manager(instance)
