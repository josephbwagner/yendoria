"""
AI Behavior System Interface - Common interface for all AI behavior systems.

This module defines the interface that all AI behavior systems must implement,
ensuring consistency and interchangeability between different AI implementations.
"""

from abc import ABC, abstractmethod
from typing import Any

from yendoria.components.ai_events import AIEvent
from yendoria.components.component_manager import ComponentManager


class AIBehaviorSystemInterface(ABC):
    """
    Abstract base class for all AI behavior systems.

    This interface ensures that all AI behavior implementations
    provide the same basic functionality for integration with
    the AI Manager and Game Engine.
    """

    def __init__(self, component_manager: ComponentManager) -> None:
        """
        Initialize the AI behavior system.

        Args:
            component_manager: ECS component manager for entity/component access
        """
        self.component_manager = component_manager

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """
        Update AI behavior for all managed entities.

        Args:
            delta_time: Time elapsed since last update in seconds
        """
        pass

    @abstractmethod
    def handle_event(self, event: AIEvent) -> None:
        """
        Handle AI-related events that may affect behavior.

        Args:
            event: The AI event to process
        """
        pass

    @abstractmethod
    def get_performance_stats(self) -> dict[str, Any]:
        """
        Get performance statistics for monitoring and debugging.

        Returns:
            Dictionary containing performance metrics
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the name of this AI behavior system.

        Returns:
            Human-readable name of the system
        """
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """
        Clean shutdown of the behavior system.

        Should release resources and clean up state.
        """
        pass
