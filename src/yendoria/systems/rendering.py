"""
Rendering system for Yendoria.

This module handles all rendering operations using libtcod,
including map rendering, entity rendering, and UI elements.
"""

from typing import List
import tcod
from ..entities.entity import Entity
from ..game_map.game_map import GameMap
from ..utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT,
    COLOR_WHITE, COLOR_RED, COLOR_GREEN
)


class RenderingSystem:
    """
    Handles all rendering operations for the game.
    
    Attributes:
        console (tcod.Console): Main console for rendering
        map_console (tcod.Console): Console for map rendering
    """
    
    def __init__(self):
        """Initialize the rendering system."""
        self.console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.map_console = tcod.console.Console(MAP_WIDTH, MAP_HEIGHT)
        
    def render_map(self, game_map: GameMap) -> None:
        """
        Render the game map to the map console.
        
        Args:
            game_map: The game map to render
        """
        # Clear the map console
        self.map_console.clear()
        
        # Render tiles
        for x in range(game_map.width):
            for y in range(game_map.height):
                tile = game_map.tiles[x, y]
                
                if game_map.visible[x, y]:
                    # Tile is currently visible - use light graphics
                    char, fg, bg = tile.light
                elif game_map.explored[x, y]:
                    # Tile was previously seen - use dark graphics
                    char, fg, bg = tile.dark
                else:
                    # Tile has never been seen - don't render
                    continue
                    
                self.map_console.print(x, y, chr(char), fg=fg, bg=bg)
                
    def render_entities(self, entities: List[Entity], game_map: GameMap) -> None:
        """
        Render all visible entities to the map console.
        
        Args:
            entities: List of entities to render
            game_map: The game map for visibility checks
        """
        for entity in entities:
            if not hasattr(entity, 'position') or not hasattr(entity, 'graphic'):
                continue
                
            x, y = entity.position.x, entity.position.y
            
            # Only render if tile is visible or entity is the player
            if game_map.visible[x, y] or entity.is_player:
                char = entity.graphic.char
                color = entity.graphic.color
                self.map_console.print(x, y, chr(char), fg=color)
                
    def render_ui(self, player: Entity) -> None:
        """
        Render the user interface elements.
        
        Args:
            player: The player entity for health display
        """
        # Clear UI area (bottom of screen)
        ui_y = MAP_HEIGHT
        for y in range(ui_y, SCREEN_HEIGHT):
            for x in range(SCREEN_WIDTH):
                self.console.print(x, y, " ", bg=COLOR_WHITE)
                
        # Render health bar
        if hasattr(player, 'health'):
            health = player.health
            hp_text = f"HP: {health.current_hp}/{health.max_hp}"
            self.console.print(1, ui_y + 1, hp_text, fg=COLOR_WHITE)
            
            # Health bar
            bar_width = 20
            bar_x = 1
            bar_y = ui_y + 2
            
            # Calculate filled portion
            if health.max_hp > 0:
                filled_length = int(bar_width * health.current_hp / health.max_hp)
            else:
                filled_length = 0
                
            # Draw health bar background
            for x in range(bar_width):
                self.console.print(bar_x + x, bar_y, " ", bg=COLOR_RED)
                
            # Draw filled portion
            for x in range(filled_length):
                self.console.print(bar_x + x, bar_y, " ", bg=COLOR_GREEN)
                
    def render_all(self, game_map: GameMap, entities: List[Entity], player: Entity) -> None:
        """
        Render the complete game state.
        
        Args:
            game_map: The game map to render
            entities: List of all entities to render
            player: The player entity for UI display
        """
        # Clear main console
        self.console.clear()
        
        # Render map and entities to map console
        self.render_map(game_map)
        self.render_entities(entities, game_map)
        
        # Blit map console to main console
        self.map_console.blit(self.console, 0, 0)
        
        # Render UI
        self.render_ui(player)
        
    def present(self, context: tcod.context.Context) -> None:
        """
        Present the rendered frame to the screen.
        
        Args:
            context: The tcod context to present to
        """
        context.present(self.console)
