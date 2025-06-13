"""
Player entity module.

This module contains functions for creating and managing the player entity.
"""

from .entity import Entity
from ..components.component import Position, Health, Graphic
from ..utils.constants import CHAR_PLAYER, COLOR_WHITE


def create_player(x: int, y: int) -> Entity:
    """
    Create a new player entity with all necessary components.
    
    Args:
        x: Starting x coordinate
        y: Starting y coordinate
        
    Returns:
        Entity: A fully configured player entity
    """
    player = Entity(name="Player", is_player=True)
    
    # Add components
    player.add_component(Position(x, y))
    player.add_component(Health(max_hp=30))
    player.add_component(Graphic(char=CHAR_PLAYER, color=COLOR_WHITE))
    
    return player


def move_player(player: Entity, dx: int, dy: int, game_map) -> bool:
    """
    Attempt to move the player in the given direction.
    
    Args:
        player: The player entity
        dx: Change in x coordinate
        dy: Change in y coordinate
        game_map: The game map to check for collision
        
    Returns:
        bool: True if move was successful, False otherwise
    """
    if not hasattr(player, 'position'):
        return False
        
    new_x = player.position.x + dx
    new_y = player.position.y + dy
    
    # Check bounds and walkability
    if not game_map.is_walkable(new_x, new_y):
        return False
        
    # Move the player
    player.position.move(dx, dy)
    return True
