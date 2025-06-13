"""
Entity module for Yendoria.

This module contains the Entity class which serves as a container
for components in the Entity Component System architecture.
"""

from ..components.component import Component


class Entity:
    """
    A generic entity in the game world.

    Entities are containers for components. The specific behavior
    and properties of an entity are determined by its components.

    Attributes:
        name (str): Display name of the entity
        is_player (bool): True if this entity is the player
    """

    def __init__(self, name: str = "Entity", is_player: bool = False):
        """
        Initialize a new entity.

        Args:
            name: Display name for the entity
            is_player: Whether this entity represents the player
        """
        self.name = name
        self.is_player = is_player
        self._components: dict[str, Component] = {}

    def add_component(self, component: Component) -> None:
        """
        Add a component to this entity.

        Args:
            component: The component to add
        """
        component.entity = self
        component_type = type(component).__name__.lower()
        self._components[component_type] = component

        # Add as attribute for easy access
        setattr(self, component_type, component)

    def get_component(self, component_type: str) -> Component | None:
        """
        Get a component by type name.

        Args:
            component_type: Name of the component type (case insensitive)

        Returns:
            The component if found, None otherwise
        """
        return self._components.get(component_type.lower())

    def has_component(self, component_type: str) -> bool:
        """
        Check if entity has a specific component type.

        Args:
            component_type: Name of the component type (case insensitive)

        Returns:
            True if entity has the component, False otherwise
        """
        return component_type.lower() in self._components

    def remove_component(self, component_type: str) -> None:
        """
        Remove a component from this entity.

        Args:
            component_type: Name of the component type to remove
        """
        component_type = component_type.lower()
        if component_type in self._components:
            del self._components[component_type]
            if hasattr(self, component_type):
                delattr(self, component_type)

    @property
    def is_alive(self) -> bool:
        """
        Check if the entity is alive.

        Returns:
            True if entity has health component and current HP > 0
        """
        if hasattr(self, "health"):
            return bool(self.health.is_alive)
        return True  # Entities without health are considered always alive

    def __repr__(self) -> str:
        """String representation of the entity."""
        return f"Entity(name='{self.name}', is_player={self.is_player})"
