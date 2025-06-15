"""
AI Engine Integration - Bridge between GameEngine and AI systems.

This module provides the integration layer between the main game engine
and the AI system, handling initialization, updates, and event bridging.
"""

import logging
from typing import Any

from yendoria.components.ai_components import BehaviorTreeComponent
from yendoria.components.ai_events import (
    AIEventType,
    create_entity_spawned_event,
    create_turn_started_event,
)
from yendoria.components.component_manager import get_component_manager
from yendoria.entities.entity import Entity
from yendoria.modding import EventBus, EventType, GameEvent
from yendoria.systems.ai_behavior_basic import BasicAIBehaviorSystem
from yendoria.systems.ai_manager import AIManager, init_ai_manager
from yendoria.systems.config_manager import initialize_config_manager

logger = logging.getLogger(__name__)


class AIEngineIntegration:
    """
    Integration layer between GameEngine and AI systems.

    This class handles:
    - AI system initialization and lifecycle
    - Event bridging between game events and AI events
    - Entity registration with AI systems
    - AI update coordination
    """

    def __init__(self, game_event_bus: EventBus) -> None:
        """
        Initialize the AI integration layer.

        Args:
            game_event_bus: The main game event bus for bridging events
        """
        self.game_event_bus = game_event_bus
        self.ai_manager: AIManager | None = None
        self.component_manager = get_component_manager()

        # Track AI-enabled entities
        self.ai_entities: set[str] = set()

        # Integration state
        self.initialized = False
        self.turn_count = 0

        logger.info("AI Engine Integration initialized")

    def initialize_ai_systems(self) -> None:
        """Initialize all AI systems and set up event bridging."""
        try:
            logger.info("Initializing AI systems...")

            # Initialize AI systems
            config_manager = initialize_config_manager()
            self.ai_manager = init_ai_manager(self.component_manager, config_manager)

            # Register core AI systems
            behavior_system = BasicAIBehaviorSystem(self.component_manager)
            self.ai_manager.register_system(
                "behavior",
                behavior_system,
                priority=10,
                event_types=[
                    AIEventType.REPUTATION_CHANGED,
                    AIEventType.CONFLICT_STARTED,
                    AIEventType.FACTION_RELATIONSHIP_CHANGED,
                ],
            )

            # Set up event bridging
            self._setup_event_bridging()

            self.initialized = True
            logger.info("AI systems initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize AI systems: {e}")
            raise

    def _setup_event_bridging(self) -> None:
        """Set up event bridging between game events and AI events."""
        if not self.ai_manager:
            return

        # Bridge game events to AI events
        self.game_event_bus.subscribe(EventType.ENTITY_SPAWN, self._on_entity_spawn)
        self.game_event_bus.subscribe(EventType.ENTITY_DEATH, self._on_entity_death)
        self.game_event_bus.subscribe(EventType.TURN_START, self._on_turn_start)
        self.game_event_bus.subscribe(EventType.TURN_END, self._on_turn_end)
        self.game_event_bus.subscribe(EventType.COMBAT_START, self._on_combat_start)

        logger.info("Event bridging set up successfully")

    def _on_entity_spawn(self, event: GameEvent) -> None:
        """Handle entity spawn events."""
        if not self.ai_manager:
            return

        entity = event.data.get("entity")
        entity_type = event.data.get("entity_type", "unknown")
        position = event.data.get("position", (0, 0))

        if entity and entity_type != "player":
            # Register monster entities with AI system
            entity_id = entity.id  # Use object id as unique identifier

            # Determine archetype based on entity type
            archetype_map = {
                "orc": "aggressive_monster",
                "troll": "tough_monster",
                "goblin": "sneaky_monster",
            }

            archetype = archetype_map.get(entity_type, "basic_monster")
            faction = "monsters"  # Default faction for monsters

            # Register with AI manager
            self.ai_manager.register_ai_entity(
                entity_id, archetype=archetype, faction=faction
            )
            self.ai_entities.add(entity_id)

            # Store entity reference for later lookups
            entity._ai_entity_id = entity_id

            # Post AI event
            ai_event = create_entity_spawned_event(
                entity_id=entity_id,
                entity_type=entity_type,
                location=position,
                faction_id=faction,
            )
            self.ai_manager.post_event(ai_event)

            logger.debug(
                f"Registered entity {entity_id} ({entity_type}) with AI system"
            )

    def _on_entity_death(self, event: GameEvent) -> None:
        """Handle entity death events."""
        if not self.ai_manager:
            return

        entity = event.data.get("entity")
        if entity and hasattr(entity, "_ai_entity_id"):
            entity_id = entity._ai_entity_id

            # Unregister from AI manager
            self.ai_manager.unregister_ai_entity(entity_id)
            self.ai_entities.discard(entity_id)

            logger.debug(f"Unregistered entity {entity_id} from AI system")

    def _on_turn_start(self, event: GameEvent) -> None:
        """Handle turn start events."""
        if not self.ai_manager:
            return

        self.turn_count = event.data.get("turn_count", 0)

        # Post AI turn start event
        ai_event = create_turn_started_event(
            turn_number=self.turn_count, active_entities=len(self.ai_entities)
        )
        self.ai_manager.post_event(ai_event)

    def _on_turn_end(self, event: GameEvent) -> None:
        """Handle turn end events."""
        if not self.ai_manager:
            return

        # Process any remaining AI events at turn end
        self.ai_manager.process_events()

    def _on_combat_start(self, event: GameEvent) -> None:
        """Handle combat start events."""
        if not self.ai_manager:
            return

        # Could trigger AI events for combat responses
        logger.debug("Combat started - AI systems notified")

    def register_entity_with_ai(
        self,
        entity: Entity,
        entity_type: str,
        archetype: str | None = None,
        faction: str | None = None,
    ) -> None:
        """
        Manually register an entity with the AI system.

        Args:
            entity: The entity to register
            entity_type: Type of entity (for archetype mapping)
            archetype: Specific AI archetype (optional)
            faction: Faction to assign (optional)
        """
        if not self.ai_manager:
            logger.warning("AI manager not initialized - cannot register entity")
            return

        entity_id = entity.id

        # Use provided archetype or map from entity type
        if not archetype:
            archetype_map = {
                "guard": "guard",
                "merchant": "merchant",
                "bandit": "bandit",
                "villager": "villager",
            }
            archetype = archetype_map.get(entity_type, "basic_npc")

        # Use provided faction or default
        if not faction:
            faction_map = {
                "guard": "town_guard",
                "merchant": "merchants_guild",
                "bandit": "raiders",
                "villager": "civilians",
            }
            faction = faction_map.get(entity_type, "neutral")

        # Register with AI manager
        if entity_id is None:
            logger.warning("Entity has no 'id'; cannot register with AI system")
            return
        self.ai_manager.register_ai_entity(
            entity_id, archetype=archetype, faction=faction
        )
        self.ai_entities.add(entity_id)

        # Store reference
        entity._ai_entity_id = entity_id

        logger.info(
            f"Manually registered entity {entity_id} ({entity_type}) with AI system"
        )

    def update_ai_systems(self, delta_time: float = 1.0) -> None:
        """
        Update all AI systems.

        Args:
            delta_time: Time elapsed since last update (defaults to 1 turn)
        """
        if not self.ai_manager or not self.initialized:
            return

        try:
            # Update the AI manager (which updates all registered systems)
            self.ai_manager.update(delta_time)

        except Exception as e:
            logger.error(f"Error updating AI systems: {e}")

    def get_ai_action_for_entity(self, entity: Entity) -> str | None:
        """
        Get the next AI action for an entity.

        Args:
            entity: The entity to get an action for

        Returns:
            String action name or None if no action available
        """
        if not self.ai_manager or not hasattr(entity, "_ai_entity_id"):
            return None

        entity_id = entity._ai_entity_id

        if not entity_id:
            return None

        # Check if entity has behavior tree component
        behavior_tree = self.component_manager.get_component(
            entity_id, BehaviorTreeComponent
        )

        if behavior_tree and behavior_tree.current_action:
            return behavior_tree.current_action

        # Default action for entities without specific behavior
        return "wander"

    def get_ai_stats(self) -> dict[str, Any]:
        """Get AI system statistics."""
        if not self.ai_manager:
            return {"status": "not_initialized"}

        stats = self.ai_manager.get_performance_stats()
        stats.update(
            {
                "integration_status": "active" if self.initialized else "inactive",
                "ai_entities_tracked": len(self.ai_entities),
                "turn_count": self.turn_count,
            }
        )

        return stats

    def shutdown(self) -> None:
        """Shutdown the AI integration layer."""
        logger.info("Shutting down AI Engine Integration")

        if self.ai_manager:
            self.ai_manager.shutdown()

        self.ai_entities.clear()
        self.initialized = False

        logger.info("AI Engine Integration shutdown complete")


def get_ai_integration() -> AIEngineIntegration | None:
    """Get the AI integration singleton instance."""
    from yendoria.systems.ai_singleton_registry import (
        get_ai_integration as _get_ai_integration,
    )

    try:
        return _get_ai_integration()
    except RuntimeError:
        return None


def init_ai_integration(game_event_bus: EventBus) -> AIEngineIntegration:
    """Initialize the AI integration singleton."""
    from yendoria.systems.ai_singleton_registry import set_ai_integration

    ai_integration = AIEngineIntegration(game_event_bus)
    return set_ai_integration(ai_integration)


def shutdown_ai_integration() -> None:
    """Shutdown the AI integration singleton."""
    from yendoria.systems.ai_singleton_registry import clear_ai_integration

    clear_ai_integration()
