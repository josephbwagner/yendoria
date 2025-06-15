"""
Advanced AI Behavior System - Implements sophisticated AI behaviors.

This module provides comprehensive AI behaviors including personality-driven
decisions, memory-based learning, motivation systems, and complex behavior trees.
Use this for entities that need rich, nuanced AI behavior.
"""

import logging
import random
from dataclasses import dataclass
from typing import Any

from yendoria.components.ai_components import (
    BehaviorTreeComponent,
    FactionComponent,
    MemoryComponent,
    MotivationComponent,
    PersonalityComponent,
)
from yendoria.components.ai_events import AIEvent, AIEventType
from yendoria.components.component_manager import ComponentManager
from yendoria.systems.ai_behavior_interface import AIBehaviorSystemInterface
from yendoria.systems.ai_error_handling import ai_error_handler, get_ai_metrics

logger = logging.getLogger(__name__)

# Constants for thresholds to avoid magic numbers
HUNGER_THRESHOLD = 0.7
SAFETY_THRESHOLD = 0.3
COMPANIONSHIP_THRESHOLD = 0.6
CONFIDENCE_THRESHOLD = 0.6
ENEMY_DETECTION_PROBABILITY = 0.1
FOOD_FIND_PROBABILITY = 0.2
ANTISOCIAL_THRESHOLD = 0.3
TERRITORIAL_THRESHOLD = 0.5


@dataclass
class BehaviorContext:
    """Context object to reduce parameter passing in behavior tree functions."""

    entity_id: str
    personality: PersonalityComponent
    motivation: MotivationComponent
    memory: MemoryComponent
    delta_time: float


class AdvancedAIBehaviorSystem(AIBehaviorSystemInterface):
    """
    Advanced AI behavior system that implements sophisticated decision-making.

    This system provides:
    - Personality-driven behavior decisions
    - Memory-based learning and adaptation
    - Complex motivation and need systems
    - Full behavior tree processing
    - Social interaction modeling
    - Faction-aware behavior

    Use this system for important NPCs, boss enemies, or any entity
    that needs rich, believable AI behavior.
    """

    def __init__(self, component_manager: ComponentManager) -> None:
        """
        Initialize the behavior system.

        Args:
            component_manager: ECS component manager
        """
        self.component_manager = component_manager

        # Behavior state tracking
        self.entity_goals: dict[str, dict[str, Any]] = {}
        self.entity_timers: dict[str, dict[str, float]] = {}

    @property
    def name(self) -> str:
        """Get the name of this AI behavior system."""
        return "Advanced AI Behavior System"

    @ai_error_handler("update AI behavior")
    def update(self, delta_time: float) -> None:
        """
        Update AI behavior for all entities.

        Args:
            delta_time: Time elapsed since last update
        """
        metrics = get_ai_metrics()
        with metrics.operation_timer("behavior_update"):
            # Get all entities with AI components
            ai_entities = []
            try:
                ai_entities = self.component_manager.get_entities_with_component(
                    BehaviorTreeComponent
                )
            except Exception as e:
                logger.warning(f"Error getting entities with AI components: {e}")
                return

            for entity in ai_entities:
                if entity.id is None:
                    continue
                try:
                    self._update_entity_behavior(entity.id, delta_time)
                except Exception as e:
                    logger.error(f"Error updating behavior for entity {entity.id}: {e}")
                    metrics.record_error("entity_update_error")

    def _update_entity_behavior(self, entity_id: str, delta_time: float) -> None:
        """Update behavior for a single entity."""
        # Get entity components
        behavior_tree = self.component_manager.get_component(
            entity_id, BehaviorTreeComponent
        )
        personality = self.component_manager.get_component(
            entity_id, PersonalityComponent
        )
        motivation = self.component_manager.get_component(
            entity_id, MotivationComponent
        )
        memory = self.component_manager.get_component(entity_id, MemoryComponent)

        if not behavior_tree:
            return

        # Skip entities that don't have required components
        if not all([personality, motivation, memory]):
            return

        # Ensure we have the required components (mypy satisfaction)
        assert personality is not None  # nosec B101
        assert motivation is not None  # nosec B101
        assert memory is not None  # nosec B101

        # Update timers
        if entity_id not in self.entity_timers:
            self.entity_timers[entity_id] = {}

        # Create behavior context to reduce parameter passing
        context = BehaviorContext(
            entity_id=entity_id,
            personality=personality,
            motivation=motivation,
            memory=memory,
            delta_time=delta_time,
        )

        # Process behavior tree
        self._process_behavior_tree(behavior_tree, context)

    def _process_behavior_tree(
        self,
        behavior_tree: BehaviorTreeComponent,
        context: BehaviorContext,
    ) -> None:
        """Process the entity's behavior tree."""
        if not behavior_tree.tree_data:
            return

        # Simple behavior tree execution
        # In a full implementation, this would be a proper BT interpreter
        root_node = behavior_tree.tree_data.get("root")
        if root_node:
            self._execute_behavior_node(root_node, context)

    def _execute_behavior_node(
        self,
        node: dict[str, Any],
        context: BehaviorContext,
    ) -> bool:
        """
        Execute a behavior tree node.

        Returns:
            True if the node succeeded, False otherwise
        """
        node_type = node.get("type", "unknown")

        # Map node types to their execution methods
        node_handlers = {
            "selector": self._execute_selector_node,
            "sequence": self._execute_sequence_node,
            "action": self._execute_action_node,
            "condition": self._execute_condition_node,
        }

        handler = node_handlers.get(node_type)
        return handler(node, context) if handler else False

    def _execute_selector_node(
        self, node: dict[str, Any], context: BehaviorContext
    ) -> bool:
        """Execute a selector node - try each child until one succeeds."""
        for child in node.get("children", []):
            if self._execute_behavior_node(child, context):
                return True
        return False

    def _execute_sequence_node(
        self, node: dict[str, Any], context: BehaviorContext
    ) -> bool:
        """Execute a sequence node - all children must succeed."""
        for child in node.get("children", []):
            if not self._execute_behavior_node(child, context):
                return False
        return True

    def _execute_action_node(
        self, node: dict[str, Any], context: BehaviorContext
    ) -> bool:
        """Execute an action node."""
        return self._execute_action(action_node=node, context=context)

    def _execute_condition_node(
        self, node: dict[str, Any], context: BehaviorContext
    ) -> bool:
        """Execute a condition node."""
        return self._evaluate_condition(condition_node=node, context=context)

    def _execute_action(
        self,
        action_node: dict[str, Any],
        context: BehaviorContext,
    ) -> bool:
        """Execute a behavior action."""
        action_type = action_node.get("action", "unknown")

        if action_type == "wander":
            return self._action_wander(context.entity_id, context.personality)
        elif action_type == "seek_food":
            return self._action_seek_food(context.entity_id, context.motivation)
        elif action_type == "socialize":
            return self._action_socialize(
                context.entity_id, context.personality, context.memory
            )
        elif action_type == "guard_territory":
            return self._action_guard_territory(context.entity_id, context.motivation)
        elif action_type == "flee":
            return self._action_flee(context.entity_id, context.personality)
        else:
            logger.warning(f"Unknown action type: {action_type}")
            return False

    def _evaluate_condition(
        self,
        condition_node: dict[str, Any],
        context: BehaviorContext,
    ) -> bool:
        """Evaluate a behavior condition."""
        condition_type = condition_node.get("condition", "unknown")

        if condition_type == "is_hungry":
            return (
                context.motivation.survival_needs.get("hunger", 0.0) > HUNGER_THRESHOLD
            )
        elif condition_type == "is_threatened":
            return (
                context.motivation.survival_needs.get("safety", 1.0) < SAFETY_THRESHOLD
            )
        elif condition_type == "is_lonely":
            return (
                context.motivation.social_needs.get("companionship", 0.0)
                > COMPANIONSHIP_THRESHOLD
            )
        elif condition_type == "is_confident":
            return context.personality.get_trait("courage", 0.5) > CONFIDENCE_THRESHOLD
        elif condition_type == "has_enemy_nearby":
            # In a real implementation, this would check spatial queries
            return random.random() < ENEMY_DETECTION_PROBABILITY  # nosec B311
        else:
            logger.warning(f"Unknown condition type: {condition_type}")
            return False

    # Action implementations
    def _action_wander(self, entity_id: str, personality: PersonalityComponent) -> bool:
        """Make the entity wander around."""
        # Personality affects wandering behavior
        movement_chance = 0.3 + (personality.get_trait("restlessness") * 0.4)

        if random.random() < movement_chance:  # nosec B311
            logger.debug(f"Entity {entity_id} is wandering")
            # In a real implementation, this would modify position components
            return True
        return False

    def _action_seek_food(
        self, entity_id: str, motivation: MotivationComponent
    ) -> bool:
        """Make the entity seek food."""
        logger.debug(f"Entity {entity_id} is seeking food")

        # Simulate food finding
        if random.random() < FOOD_FIND_PROBABILITY:  # nosec B311
            # Found food - reduce hunger
            motivation.survival_needs["hunger"] = max(
                0.0, motivation.survival_needs.get("hunger", 0.0) - 0.3
            )
            return True
        return False

    def _action_socialize(
        self, entity_id: str, personality: PersonalityComponent, memory: MemoryComponent
    ) -> bool:
        """Make the entity attempt to socialize."""
        if personality.get_trait("sociability", 0.5) < ANTISOCIAL_THRESHOLD:
            return False  # Too antisocial

        logger.debug(f"Entity {entity_id} is attempting to socialize")

        # Add social memory - since we have MemoryComponent, we can use its knowledge
        if "social_interactions" not in memory.knowledge:
            memory.knowledge["social_interactions"] = []

        memory.knowledge["social_interactions"].append(
            {
                "type": "attempted_socialization",
                "timestamp": 0.0,  # Would be game time
                "success": random.random() < personality.get_trait("charisma"),  # nosec B311
            }
        )

        return True

    def _action_guard_territory(
        self, entity_id: str, motivation: MotivationComponent
    ) -> bool:
        """Make the entity guard its territory."""
        territorial_drive = motivation.survival_needs.get("territory", 0.0)

        if territorial_drive > TERRITORIAL_THRESHOLD:
            logger.debug(f"Entity {entity_id} is guarding territory")
            return True
        return False

    def _action_flee(self, entity_id: str, personality: PersonalityComponent) -> bool:
        """Make the entity flee from danger."""
        flee_chance = 1.0 - personality.get_trait("courage", 0.5)

        if random.random() < flee_chance:  # nosec B311
            logger.debug(f"Entity {entity_id} is fleeing")
            return True
        return False

    def handle_event(self, event: AIEvent) -> None:
        """Handle AI events that affect behavior."""
        if event.ai_event_type == AIEventType.REPUTATION_CHANGED:
            self._handle_reputation_change(event)
        elif event.ai_event_type == AIEventType.CONFLICT_STARTED:
            self._handle_conflict_start(event)
        elif event.ai_event_type == AIEventType.FACTION_RELATION_CHANGED:
            self._handle_faction_relation_change(event)

    def _handle_reputation_change(self, event: AIEvent) -> None:
        """Handle reputation change events."""
        entity_id = event.data.get("entity_id")
        if entity_id and entity_id in self.entity_goals:
            # Reputation changes might affect social goals
            logger.debug(f"Reputation change affects entity {entity_id}")

    def _handle_conflict_start(self, event: AIEvent) -> None:
        """Handle conflict start events."""
        faction_a = event.data.get("faction_a")
        faction_b = event.data.get("faction_b")

        # Find entities in these factions and adjust their behavior
        faction_entities = []
        try:
            faction_entities = self.component_manager.get_entities_with_component(
                FactionComponent
            )
        except Exception as e:
            logger.warning(f"Error getting faction entities: {e}")
            return

        for entity in faction_entities:
            if entity.id is None:
                continue
            faction = self.component_manager.get_component(entity.id, FactionComponent)
            if faction and faction.faction_id in [faction_a, faction_b]:
                # Increase aggression/alertness
                motivation = self.component_manager.get_component(
                    entity.id, MotivationComponent
                )
                if motivation:
                    motivation.survival_needs["safety"] = max(
                        0.0, motivation.survival_needs.get("safety", 1.0) - 0.2
                    )

    def _handle_faction_relation_change(self, event: AIEvent) -> None:
        """Handle faction relation change events."""
        logger.debug("Faction relations changed - updating entity behaviors")

    def shutdown(self) -> None:
        """Clean shutdown of the behavior system."""
        logger.info("Shutting down Basic AI Behavior System")
        self.entity_goals.clear()
        self.entity_timers.clear()

    def get_performance_stats(self) -> dict[str, Any]:
        """Get performance statistics for the advanced AI system."""
        return {
            "entities_with_goals": len(self.entity_goals),
            "entities_with_timers": len(self.entity_timers),
            "system_type": "advanced",
            "features": [
                "personality_system",
                "memory_system",
                "motivation_system",
                "behavior_trees",
                "faction_awareness",
            ],
        }
