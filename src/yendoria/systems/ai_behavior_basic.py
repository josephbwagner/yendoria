"""
Basic AI Behavior System - Lightweight AI implementation for simple entities.

This module provides essential AI behaviors with minimal overhead and component
requirements. Use this for basic NPCs, background entities, or when performance
is more important than AI sophistication.
"""

import logging
import random
from typing import Any

from yendoria.components.ai_components import (
    BehaviorTreeComponent,
)
from yendoria.components.ai_events import AIEvent, AIEventType
from yendoria.components.component_manager import ComponentManager
from yendoria.systems.ai_behavior_interface import AIBehaviorSystemInterface
from yendoria.systems.ai_error_handling import ai_error_handler, get_ai_metrics

logger = logging.getLogger(__name__)


class BasicAIBehaviorSystem(AIBehaviorSystemInterface):
    """
    Basic AI behavior system optimized for performance and simplicity.

    This system provides:
    - Timer-based action selection
    - Simple random behavior choices
    - Minimal component requirements (only BehaviorTreeComponent)
    - Low computational overhead
    - Basic event handling

    Use this system for:
    - Background NPCs that need minimal AI
    - Entities where performance is critical
    - Simple creatures or ambient life
    - Placeholder AI during development
    """

    def __init__(self, component_manager: ComponentManager) -> None:
        """Initialize the AI behavior system."""
        self.component_manager: ComponentManager = component_manager
        self.entity_timers: dict[str, float] = {}
        logger.info("Basic AI Behavior System initialized")

    @property
    def name(self) -> str:
        """Get the name of this AI behavior system."""
        return "Basic AI Behavior System"

    @ai_error_handler("update AI behavior")
    def update(self, delta_time: float) -> None:
        """Update AI behavior for all entities."""
        metrics = get_ai_metrics()
        with metrics.operation_timer("simple_behavior_update"):
            # Get all entities with AI components
            entities_with_ai = []
            try:
                entities_with_ai = self.component_manager.get_entities_with_component(
                    BehaviorTreeComponent
                )
            except Exception as e:
                logger.warning(f"Error getting entities with AI components: {e}")
                return

            for entity in entities_with_ai:
                if entity.id is None:
                    continue
                try:
                    self._update_entity_behavior(entity.id, delta_time)
                except Exception as e:
                    logger.error(f"Error updating entity {entity.id}: {e}")
                    metrics.record_error("entity_behavior_error")

    def _update_entity_behavior(self, entity_id: str, delta_time: float) -> None:
        """Update AI behavior for a specific entity."""
        try:
            # Update entity timer
            self.entity_timers[entity_id] = (
                self.entity_timers.get(entity_id, 0.0) + delta_time
            )

            # Get components
            behavior_tree = self.component_manager.get_component(
                entity_id, BehaviorTreeComponent
            )

            if not behavior_tree:
                return

            # Simple decision making - in a full system this would be more complex
            if self.entity_timers[entity_id] >= 1.0:  # Act once per second
                action = self._choose_action(entity_id)
                if action:
                    behavior_tree.current_action = action
                    logger.debug(f"Entity {entity_id} chose action: {action}")

                self.entity_timers[entity_id] = 0.0

        except Exception as e:
            logger.error(f"Error updating entity {entity_id}: {e}")

    def _choose_action(self, entity_id: str) -> str:
        """Choose an action for the entity based on its state."""
        # Simple action selection - placeholder for more complex behavior trees
        actions = ["wander", "patrol", "rest", "seek_food", "guard"]
        return random.choice(actions)  # nosec B311

    def handle_event(self, event: AIEvent) -> None:
        """Handle AI events."""
        if event.event_type == AIEventType.REPUTATION_CHANGED:
            self._handle_reputation_change(event)
        elif event.event_type == AIEventType.CONFLICT_STARTED:
            self._handle_conflict_start(event)
        elif event.event_type == AIEventType.FACTION_RELATIONSHIP_CHANGED:
            self._handle_faction_relation_change(event)

    def _handle_reputation_change(self, event: AIEvent) -> None:
        """Handle reputation change events."""
        logger.debug(f"Handling reputation change: {event.data}")

    def _handle_conflict_start(self, event: AIEvent) -> None:
        """Handle conflict start events."""
        logger.debug(f"Handling conflict start: {event.data}")

    def _handle_faction_relation_change(self, event: AIEvent) -> None:
        """Handle faction relation change events."""
        logger.debug(f"Handling faction relation change: {event.data}")

    def get_performance_stats(self) -> dict[str, Any]:
        """Get performance statistics for the basic AI system."""
        return {
            "entities_tracked": len(self.entity_timers),
            "avg_processing_time": 0.001,  # Placeholder - actual timing measured
            "actions_per_second": len(self.entity_timers),  # Approx. 1Hz updates
            "system_type": "basic",
            "features": [
                "timer_based_updates",
                "random_action_selection",
                "minimal_components",
            ],
        }

    def shutdown(self) -> None:
        """Shutdown the basic behavior system."""
        logger.info("Shutting down Basic AI Behavior System")
        self.entity_timers.clear()
