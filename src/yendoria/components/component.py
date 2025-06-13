"""
Base component class for the Entity Component System.

This module provides the base Component class that all game components
inherit from, as well as specific component implementations.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities.entity import Entity
    from ..game_map.game_map import GameMap


class Component:
    """
    Base class for all components in the ECS system.

    Components store data and state but no behavior logic.
    Systems operate on entities that have specific components.
    """

    def __init__(self, entity: "Entity | None" = None):
        """
        Initialize the component.

        Args:
            entity: The entity this component belongs to
        """
        self.entity = entity


class Position(Component):
    """
    Component for entity position on the game map.

    Attributes:
        x (int): X coordinate
        y (int): Y coordinate
    """

    def __init__(self, x: int, y: int, entity: "Entity | None" = None):
        super().__init__(entity)
        self.x = x
        self.y = y

    def move(self, dx: int, dy: int) -> None:
        """Move the entity by the given offset."""
        self.x += dx
        self.y += dy


class Health(Component):
    """
    Component for entity health and hit points.

    Attributes:
        current_hp (int): Current hit points
        max_hp (int): Maximum hit points
    """

    def __init__(self, max_hp: int, entity: "Entity | None" = None):
        super().__init__(entity)
        self.max_hp = max_hp
        self.current_hp = max_hp

    @property
    def is_alive(self) -> bool:
        """Check if the entity is alive."""
        return self.current_hp > 0

    def take_damage(self, amount: int) -> int:
        """
        Take damage and return actual damage dealt.

        Args:
            amount: Damage amount

        Returns:
            int: Actual damage dealt (may be less if kills entity)
        """
        damage_dealt = min(amount, self.current_hp)
        self.current_hp -= damage_dealt
        return damage_dealt

    def heal(self, amount: int) -> int:
        """
        Heal damage and return actual healing done.

        Args:
            amount: Healing amount

        Returns:
            int: Actual healing done (may be less if at max HP)
        """
        healing_done = min(amount, self.max_hp - self.current_hp)
        self.current_hp += healing_done
        return healing_done


class Graphic(Component):
    """
    Component for entity visual representation.

    Attributes:
        char (int): Character code to display
        color (Tuple[int, int, int]): RGB color tuple
    """

    def __init__(self, char: int, color: tuple, entity: "Entity | None" = None):
        super().__init__(entity)
        self.char = char
        self.color = color


class AI(Component):
    """
    Base AI component for entity behavior.

    This is a base class that specific AI behaviors should inherit from.
    """

    def perform(self, game_map: "GameMap", entities: list["Entity"]) -> None:
        """
        Perform AI action. Override in subclasses.

        Args:
            game_map: The current game map
            entities: List of all entities in the game
        """
        pass


class BasicMonsterAI(AI):
    """
    Basic AI that moves towards and attacks the player.
    """

    def perform(self, game_map: "GameMap", entities: list["Entity"]) -> None:
        """
        Move towards player if visible, attack if adjacent.

        Args:
            game_map: The current game map
            entities: List of all entities in the game
        """
        if not self.entity or not hasattr(self.entity, "position"):
            return

        # Find the player
        player = None
        for entity in entities:
            if hasattr(entity, "is_player") and entity.is_player:
                player = entity
                break

        if not player or not hasattr(player, "position"):
            return

        # Check if player is visible
        monster_pos = self.entity.position
        player_pos = player.position

        if not game_map.visible[monster_pos.x, monster_pos.y]:
            return  # Monster can't see, don't act

        # Calculate distance to player
        dx = player_pos.x - monster_pos.x
        dy = player_pos.y - monster_pos.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance

        if distance <= 1:
            # Adjacent to player - attack
            if hasattr(player, "health") and hasattr(self.entity, "damage"):
                damage = getattr(self.entity, "damage", 1)
                player.health.take_damage(damage)
        else:
            # Move towards player
            # Normalize movement to -1, 0, or 1
            move_x = 0 if dx == 0 else (1 if dx > 0 else -1)
            move_y = 0 if dy == 0 else (1 if dy > 0 else -1)

            new_x = monster_pos.x + move_x
            new_y = monster_pos.y + move_y

            # Check if move is valid
            if game_map.is_walkable(new_x, new_y):
                # Check if tile is occupied by another entity
                occupied = False
                for entity in entities:
                    if (
                        hasattr(entity, "position")
                        and entity != self.entity
                        and entity.position.x == new_x
                        and entity.position.y == new_y
                    ):
                        occupied = True
                        break

                if not occupied:
                    monster_pos.move(move_x, move_y)


class Damage(Component):
    """
    Component for entity damage dealing capability.

    Attributes:
        amount (int): Amount of damage this entity deals
    """

    def __init__(self, amount: int, entity: "Entity | None" = None):
        super().__init__(entity)
        self.amount = amount
