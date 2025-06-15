"""
AI Manager Hub - Central coordination system for all AI components.

This module provides the main coordination point for all AI systems,
managing the lifecycle of AI entities, system registration, and
cross-system communication through events.
"""

import logging
from collections.abc import Callable
from typing import Any

from yendoria.components.ai_components import (
    BehaviorTreeComponent,
    FactionComponent,
    MemoryComponent,
    MotivationComponent,
    PersonalityComponent,
    ReputationComponent,
)
from yendoria.components.ai_events import AIEvent, AIEventType
from yendoria.components.component_manager import ComponentManager
from yendoria.systems.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class AISystemRegistry:
    """Registry for AI subsystems and their capabilities."""

    def __init__(self) -> None:
        self.systems: dict[str, Any] = {}
        self.system_priorities: dict[str, int] = {}
        self.event_handlers: dict[AIEventType, list[Callable[[AIEvent], None]]] = {}

    def register_system(
        self,
        name: str,
        system: Any,
        priority: int = 0,
        event_types: list[AIEventType] | None = None,
    ) -> None:
        """Register an AI system with the hub."""
        self.systems[name] = system
        self.system_priorities[name] = priority

        # Register event handlers if provided
        if event_types and hasattr(system, "handle_ai_event"):
            for event_type in event_types:
                if event_type not in self.event_handlers:
                    self.event_handlers[event_type] = []
                self.event_handlers[event_type].append(system.handle_ai_event)

        logger.info(f"Registered AI system: {name} (priority: {priority})")

    def unregister_system(self, name: str) -> None:
        """Unregister an AI system."""
        if name in self.systems:
            system = self.systems[name]

            # Remove event handlers
            for handlers in self.event_handlers.values():
                if hasattr(system, "handle_ai_event"):
                    handlers[:] = [h for h in handlers if h != system.handle_ai_event]

            del self.systems[name]
            del self.system_priorities[name]
            logger.info(f"Unregistered AI system: {name}")

    def get_system(self, name: str) -> Any:
        """Get a registered system by name."""
        return self.systems.get(name)

    def get_systems_by_priority(self) -> list[tuple[str, Any]]:
        """Get all systems sorted by priority (highest first)."""
        return sorted(
            self.systems.items(),
            key=lambda x: self.system_priorities[x[0]],
            reverse=True,
        )


class AIManager:
    """
    Central AI management hub that coordinates all AI systems.

    The AIManager serves as the main interface for AI operations,
    handling entity lifecycle, system coordination, and event distribution.
    """

    def __init__(
        self,
        component_manager: ComponentManager,
        config_manager: ConfigManager | None = None,
    ) -> None:
        """
        Initialize the AI Manager.

        Args:
            component_manager: The ECS component manager
            config_manager: Configuration manager (uses global if None)
        """
        self.component_manager = component_manager
        # Initialize configuration manager
        if config_manager is None:
            from yendoria.systems.ai_singleton_registry import get_config_manager

            try:
                self.config_manager = get_config_manager()
            except RuntimeError:
                # Config manager not initialized - this is OK for some use cases
                logger.warning("Config manager not available, using defaults")
                from yendoria.systems.config_manager import ConfigManager

                self.config_manager = ConfigManager()
        else:
            self.config_manager = config_manager
        self.registry = AISystemRegistry()

        # Configuration caches
        self._faction_configs: dict[str, dict[str, Any]] = {}
        self._archetype_configs: dict[str, dict[str, Any]] = {}
        self._behavior_tree_configs: dict[str, dict[str, Any]] = {}

        # AI entity tracking
        self.ai_entities: set[str] = set()
        self.faction_memberships: dict[str, str] = {}  # entity_id -> faction_id

        # Event system
        self.event_queue: list[AIEvent] = []
        self.event_handlers: dict[AIEventType, list[Callable[[AIEvent], None]]] = {}

        # For compatibility with external code
        self.systems = self.registry.systems

        # Performance metrics
        self.performance_stats: dict[str, Any] = {
            "events_processed": 0,
            "ai_entities_active": 0,
            "systems_registered": 0,
        }

        self._initialize()

    def _initialize(self) -> None:
        """Initialize the AI manager with default configurations."""
        try:
            # Load AI configurations
            self._load_configurations()

            # Register default event handlers
            self._register_default_handlers()

            logger.info("AI Manager initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize AI Manager: {e}")
            raise

    def _load_configurations(self) -> None:
        """Load all AI-related configurations."""
        try:
            # Load and flatten faction configurations
            factions = self.config_manager.load_config("ai/factions.json", watch=False)
            self._faction_configs = factions.get("factions", factions)

            # Load and flatten archetype configurations
            archetypes = self.config_manager.load_config(
                "ai/archetypes.json", watch=False
            )
            self._archetype_configs = archetypes.get("archetypes", archetypes)

            # Load and flatten behavior tree configurations
            behavior_trees = self.config_manager.load_config(
                "ai/behavior_trees.json", watch=False
            )
            self._behavior_tree_configs = behavior_trees.get(
                "behavior_trees", behavior_trees
            )

            logger.info("AI configurations loaded successfully")

        except Exception as e:
            logger.warning(f"Failed to load some AI configurations: {e}")

    def _register_default_handlers(self) -> None:
        """Register default event handlers for core AI events."""
        # Register handlers in the registry system
        for event_type in AIEventType:
            if event_type not in self.registry.event_handlers:
                self.registry.event_handlers[event_type] = []

    # Entity Management
    def register_ai_entity(
        self, entity_id: str, archetype: str | None = None, faction: str | None = None
    ) -> None:
        """
        Register an entity as AI-controlled.

        Args:
            entity_id: Unique identifier for the entity
            archetype: AI archetype to apply (optional)
            faction: Faction to assign entity to (optional)
        """
        try:
            # Add to AI entity set
            self.ai_entities.add(entity_id)

            # Ensure entity has required AI components
            self._ensure_ai_components(entity_id)

            # Apply archetype if specified
            if archetype:
                self._apply_archetype(entity_id, archetype)

            # Assign to faction if specified
            if faction:
                self._assign_faction(entity_id, faction)

            # Update performance stats
            self.performance_stats["ai_entities_active"] = len(self.ai_entities)

            logger.debug(f"Registered AI entity: {entity_id}")

        except Exception as e:
            logger.error(f"Failed to register AI entity {entity_id}: {e}")
            raise

    def unregister_ai_entity(self, entity_id: str) -> None:
        """Remove an entity from AI control."""
        if entity_id in self.ai_entities:
            self.ai_entities.remove(entity_id)

            # Remove faction membership
            if entity_id in self.faction_memberships:
                del self.faction_memberships[entity_id]

            # Update performance stats
            self.performance_stats["ai_entities_active"] = len(self.ai_entities)

            logger.debug(f"Unregistered AI entity: {entity_id}")

    def _ensure_ai_components(self, entity_id: str) -> None:
        """Ensure an entity has all required AI components."""
        # Add basic AI components if not present
        components_to_add = [
            (MemoryComponent, MemoryComponent()),
            (PersonalityComponent, PersonalityComponent()),
        ]

        for component_type, default_instance in components_to_add:
            if not self.component_manager.has_component(entity_id, component_type):
                self.component_manager.add_component(entity_id, default_instance)

    def _apply_archetype(self, entity_id: str, archetype_name: str) -> None:
        """Apply an AI archetype configuration to an entity."""
        if archetype_name not in self._archetype_configs:
            logger.warning(f"Unknown archetype: {archetype_name}")
            return

        archetype = self._archetype_configs[archetype_name]

        # Apply personality traits
        if "personality" in archetype:
            personality = PersonalityComponent()
            for trait, value in archetype["personality"].items():
                if hasattr(personality, trait):
                    setattr(personality, trait, value)
            self.component_manager.add_component(entity_id, personality)

        # Apply behavior tree
        if "behavior_tree" in archetype:
            tree_name = archetype["behavior_tree"]
            if tree_name in self._behavior_tree_configs:
                behavior_tree = BehaviorTreeComponent(
                    tree_data=self._behavior_tree_configs[tree_name]
                )
                self.component_manager.add_component(entity_id, behavior_tree)

        # Apply motivations
        if "motivations" in archetype:
            motivation = MotivationComponent()
            for key, value in archetype["motivations"].items():
                if hasattr(motivation, key):
                    setattr(motivation, key, value)
            self.component_manager.add_component(entity_id, motivation)

        logger.debug(f"Applied archetype '{archetype_name}' to entity {entity_id}")

    def _assign_faction(self, entity_id: str, faction_id: str) -> None:
        """Assign an entity to a faction."""
        if faction_id not in self._faction_configs:
            logger.warning(f"Unknown faction: {faction_id}")
            return

        # Add faction component
        faction_data = self._faction_configs[faction_id]
        from yendoria.components.ai_components import FactionConfig

        config = FactionConfig(
            name=faction_data.get("name", faction_id),
            description=faction_data.get("description", ""),
            relations=faction_data.get("relations", {}),
            territory=faction_data.get("territory", []),
        )
        faction = FactionComponent(faction_id=faction_id, config=config)
        self.component_manager.add_component(entity_id, faction)

        # Track membership
        self.faction_memberships[entity_id] = faction_id

        # Initialize reputation with other factions
        reputation = ReputationComponent()
        for other_faction, relation_value in faction_data.get("relations", {}).items():
            reputation.faction_standings[other_faction] = relation_value
        self.component_manager.add_component(entity_id, reputation)

        logger.debug(f"Assigned entity {entity_id} to faction {faction_id}")

    # Event System
    def post_event(self, event: AIEvent) -> None:
        """Post an AI event to the system."""
        self.event_queue.append(event)
        logger.debug(f"Posted AI event: {event.ai_event_type}")

    def process_events(self) -> None:
        """Process all queued AI events."""
        events_processed = 0

        while self.event_queue:
            event = self.event_queue.pop(0)
            self._handle_event(event)
            events_processed += 1

        if events_processed > 0:
            self.performance_stats["events_processed"] += events_processed
            logger.debug(f"Processed {events_processed} AI events")

    def _handle_event(self, event: AIEvent) -> None:
        """Handle a single AI event."""
        # Call registered handlers from the registry
        handlers = self.registry.event_handlers.get(event.ai_event_type, [])

        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in event handler for {event.ai_event_type}: {e}")

    def handle_ai_event(self, event: AIEvent) -> None:
        """Handle a single AI event (compatibility alias)."""
        self._handle_event(event)

    # System Registration
    def register_system(
        self,
        name: str,
        system: Any,
        priority: int = 0,
        event_types: list[AIEventType] | None = None,
    ) -> None:
        """Register an AI subsystem."""
        self.registry.register_system(name, system, priority, event_types)
        self.performance_stats["systems_registered"] = len(self.registry.systems)

    def unregister_system(self, name: str) -> None:
        """Unregister an AI subsystem."""
        self.registry.unregister_system(name)
        self.performance_stats["systems_registered"] = len(self.registry.systems)

    def get_system(self, name: str) -> Any:
        """Get a registered system by name."""
        return self.registry.get_system(name)

    # Configuration Access
    def get_faction_config(self, faction_id: str) -> dict[str, Any] | None:
        """Get configuration for a specific faction."""
        return self._faction_configs.get(faction_id)

    def get_archetype_config(self, archetype_name: str) -> dict[str, Any] | None:
        """Get configuration for a specific archetype."""
        return self._archetype_configs.get(archetype_name)

    def get_behavior_tree_config(self, tree_name: str) -> dict[str, Any] | None:
        """Get configuration for a specific behavior tree."""
        return self._behavior_tree_configs.get(tree_name)

    # Query Interface
    def get_ai_entities(self) -> set[str]:
        """Get all AI-controlled entities."""
        return self.ai_entities.copy()

    def get_faction_members(self, faction_id: str) -> list[str]:
        """Get all entities belonging to a faction."""
        return [
            entity_id
            for entity_id, faction in self.faction_memberships.items()
            if faction == faction_id
        ]

    def get_entity_faction(self, entity_id: str) -> str | None:
        """Get the faction of an entity."""
        return self.faction_memberships.get(entity_id)

    # Performance and Diagnostics
    def get_performance_stats(self) -> dict[str, Any]:
        """Get AI system performance statistics."""
        return self.performance_stats.copy()

    def update(self, delta_time: float) -> None:
        """
        Update the AI manager (called each game tick).

        Args:
            delta_time: Time elapsed since last update
        """
        # Process queued events
        self.process_events()

        # Update registered systems in priority order
        for name, system in self.registry.get_systems_by_priority():
            if hasattr(system, "update"):
                try:
                    system.update(delta_time)
                except Exception as e:
                    logger.error(f"Error updating AI system '{name}': {e}")

    def shutdown(self) -> None:
        """Clean shutdown of the AI manager."""
        logger.info("Shutting down AI Manager")

        # Shutdown registered systems
        for name, system in self.registry.systems.items():
            if hasattr(system, "shutdown"):
                try:
                    system.shutdown()
                except Exception as e:
                    logger.error(f"Error shutting down AI system '{name}': {e}")

        # Clear all data
        self.ai_entities.clear()
        self.faction_memberships.clear()
        self.event_queue.clear()
        self.registry.systems.clear()
        self.registry.event_handlers.clear()

        logger.info("AI Manager shutdown complete")


def init_ai_manager(
    component_manager: ComponentManager, config_manager: ConfigManager | None = None
) -> AIManager:
    """Initialize the AI manager singleton."""
    from yendoria.systems.ai_singleton_registry import set_ai_manager

    ai_manager = AIManager(component_manager, config_manager)
    return set_ai_manager(ai_manager)


def get_ai_manager() -> AIManager:
    """Get the AI manager singleton instance."""
    from yendoria.systems.ai_singleton_registry import get_ai_manager as _get_ai_manager

    return _get_ai_manager()


def shutdown_ai_manager() -> None:
    """Shutdown the AI manager singleton."""
    from yendoria.systems.ai_singleton_registry import clear_ai_manager

    clear_ai_manager()
