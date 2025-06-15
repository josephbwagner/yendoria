"""
Enhanced Entity Component System for AI support.

This module provides enhanced ECS functionality needed for the AI system,
including component queries, entity management, and AI-specific components.
"""

import logging
from collections import defaultdict
from typing import TypeVar

from ..entities.entity import Entity
from .component import Component

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Component)


class ComponentManager:
    """
    Enhanced component manager with query capabilities for AI systems.

    Provides efficient component queries needed for AI system updates,
    such as finding all entities with specific component combinations.
    """

    def __init__(self):
        """Initialize the component manager."""
        self._entities: dict[str, Entity] = {}
        self._component_indices: dict[type[Component], set[str]] = defaultdict(set)
        self._entity_counter = 0

    def create_entity(self, name: str | None = None, is_player: bool = False) -> Entity:
        """
        Create a new entity and register it with the manager.

        Args:
            name: Display name for the entity
            is_player: Whether this entity is the player

        Returns:
            The newly created entity
        """
        if name is None:
            name = f"Entity_{self._entity_counter}"

        entity_id = f"entity_{self._entity_counter}"
        self._entity_counter += 1

        entity = Entity(name, is_player)
        entity.id = entity_id
        self._entities[entity_id] = entity

        logger.debug(f"Created entity {entity_id}: {name}")
        return entity

    def destroy_entity(self, entity_id: str) -> None:
        """
        Remove an entity and all its components.

        Args:
            entity_id: ID of the entity to remove
        """
        if entity_id not in self._entities:
            logger.warning(f"Attempted to destroy non-existent entity {entity_id}")
            return

        # Remove from component indices
        for component_type in self._component_indices:
            self._component_indices[component_type].discard(entity_id)

        # Remove entity
        del self._entities[entity_id]
        logger.debug(f"Destroyed entity {entity_id}")

    def add_component(self, entity_id: str, component: Component) -> None:
        """
        Add a component to an entity and update indices.

        Args:
            entity_id: ID of the entity
            component: Component to add
        """
        if entity_id not in self._entities:
            logger.error(f"Cannot add component to non-existent entity {entity_id}")
            return

        entity = self._entities[entity_id]
        entity.add_component(component)

        # Update component index
        component_type = type(component)
        self._component_indices[component_type].add(entity_id)

        logger.debug(f"Added {component_type.__name__} to entity {entity_id}")

    def remove_component(self, entity_id: str, component_type: type[T]) -> T | None:
        """
        Remove a component from an entity.

        Args:
            entity_id: ID of the entity
            component_type: Type of component to remove

        Returns:
            The removed component, or None if not found
        """
        if entity_id not in self._entities:
            logger.error(
                f"Cannot remove component from non-existent entity {entity_id}"
            )
            return None

        entity = self._entities[entity_id]
        component_name = component_type.__name__.lower()

        if entity.has_component(component_name):
            component = entity.get_component(component_name)
            entity.remove_component(component_name)

            # Update component index
            self._component_indices[component_type].discard(entity_id)

            logger.debug(f"Removed {component_type.__name__} from entity {entity_id}")
            if component and isinstance(component, component_type):
                return component

        return None

    def get_component(self, entity_id: str, component_type: type[T]) -> T | None:
        """
        Get a component from an entity.

        Args:
            entity_id: ID of the entity
            component_type: Type of component to get

        Returns:
            The component if found, None otherwise
        """
        if entity_id not in self._entities:
            return None

        entity = self._entities[entity_id]
        component_name = component_type.__name__.lower()
        component = entity.get_component(component_name)
        if component and isinstance(component, component_type):
            return component
        return None

    def get_entity(self, entity_id: str) -> Entity | None:
        """
        Get an entity by ID.

        Args:
            entity_id: ID of the entity

        Returns:
            The entity if found, None otherwise
        """
        return self._entities.get(entity_id)

    def query_entities(self, *component_types: type[Component]) -> list[Entity]:
        """
        Find all entities that have ALL of the specified components.

        This is the core function used by AI systems to find entities
        they need to operate on.

        Args:
            component_types: Component types that entities must have

        Returns:
            List of entities with all specified components
        """
        if not component_types:
            return list(self._entities.values())

        # Start with entities that have the first component type
        if component_types[0] not in self._component_indices:
            return []

        result_entity_ids = self._component_indices[component_types[0]].copy()

        # Intersect with entities that have each subsequent component type
        for component_type in component_types[1:]:
            if component_type not in self._component_indices:
                return []
            result_entity_ids &= self._component_indices[component_type]

        # Return the actual entities
        return [
            self._entities[entity_id]
            for entity_id in result_entity_ids
            if entity_id in self._entities
        ]

    def query_entities_with_any(
        self, *component_types: type[Component]
    ) -> list[Entity]:
        """
        Find all entities that have ANY of the specified components.

        Args:
            component_types: Component types to search for

        Returns:
            List of entities with any of the specified components
        """
        if not component_types:
            return []

        result_entity_ids: set[str] = set()

        for component_type in component_types:
            if component_type in self._component_indices:
                result_entity_ids |= self._component_indices[component_type]

        return [
            self._entities[entity_id]
            for entity_id in result_entity_ids
            if entity_id in self._entities
        ]

    def get_entities_by_name(self, name: str) -> list[Entity]:
        """
        Find entities by name (useful for debugging and testing).

        Args:
            name: Entity name to search for

        Returns:
            List of entities with the specified name
        """
        return [entity for entity in self._entities.values() if entity.name == name]

    def get_all_entities(self) -> list[Entity]:
        """
        Get all entities in the system.

        Returns:
            List of all entities
        """
        return list(self._entities.values())

    def get_entity_count(self) -> int:
        """
        Get the total number of entities.

        Returns:
            Number of entities in the system
        """
        return len(self._entities)

    def get_component_count(self, component_type: type[Component]) -> int:
        """
        Get the number of entities with a specific component type.

        Args:
            component_type: Component type to count

        Returns:
            Number of entities with the specified component
        """
        return len(self._component_indices.get(component_type, set()))

    def has_component(self, entity_id: str, component_type: type[Component]) -> bool:
        """
        Check if an entity has a specific component type.

        Args:
            entity_id: ID of the entity
            component_type: Type of component to check for

        Returns:
            True if entity has the component, False otherwise
        """
        if entity_id not in self._entities:
            return False

        entity = self._entities[entity_id]
        component_name = component_type.__name__.lower()
        return entity.has_component(component_name)

    def get_entities_with_component(
        self, component_type: type[Component]
    ) -> list[Entity]:
        """
        Find all entities that have a specific component type.

        Args:
            component_type: Component type to search for

        Returns:
            List of entities with the specified component
        """
        if component_type not in self._component_indices:
            return []

        entity_ids = self._component_indices[component_type]
        return [
            self._entities[entity_id]
            for entity_id in entity_ids
            if entity_id in self._entities
        ]


# Component manager singleton registry
class ComponentManagerRegistry:
    """Registry for managing component manager singleton."""

    _instance: ComponentManager | None = None

    @classmethod
    def get_instance(cls) -> ComponentManager:
        """Get the singleton component manager instance."""
        if cls._instance is None:
            cls._instance = ComponentManager()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> ComponentManager:
        """Reset and return a new component manager instance."""
        cls._instance = ComponentManager()
        return cls._instance


def get_component_manager() -> ComponentManager:
    """
    Get the global component manager instance.

    Returns:
        The global component manager
    """
    return ComponentManagerRegistry.get_instance()


def initialize_component_manager() -> ComponentManager:
    """
    Initialize a new global component manager.

    Returns:
        The new component manager
    """
    return ComponentManagerRegistry.reset_instance()
