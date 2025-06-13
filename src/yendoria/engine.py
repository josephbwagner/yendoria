"""
Game engine for Yendoria.

This module contains the main GameEngine class that coordinates
all game systems and manages the main game loop.
"""

import random

import tcod

from .entities.entity import Entity
from .entities.monster import create_orc, create_troll
from .entities.player import create_player, move_player
from .game_map.game_map import GameMap
from .input_handlers.event_handler import handle_events
from .systems.rendering import RenderingSystem
from .utils.constants import (
    MAP_HEIGHT,
    MAP_WIDTH,
    MONSTER_SPAWN_CHANCE,
    MOVE_COMMAND_PARTS,
    ORC_SPAWN_CHANCE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class GameEngine:
    """
    Main game engine that coordinates all game systems.

    Attributes:
        game_map (GameMap): The current game map
        entities (List[Entity]): List of all entities in the game
        player (Entity): The player entity
        renderer (RenderingSystem): Rendering system instance
        context (tcod.context.Context): The tcod context for display
        is_running (bool): Whether the game is currently running
    """

    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
        """
        Initialize the game engine.

        Args:
            width: Screen width in characters
            height: Screen height in characters
        """
        self.screen_width = width
        self.screen_height = height

        # Initialize tcod context
        self.context = tcod.context.new(
            columns=width,
            rows=height,
            title="Yendoria",
            vsync=True,
        )

        # Initialize game systems
        self.renderer = RenderingSystem()
        self.game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
        self.entities: list[Entity] = []
        self.is_running = True

        # Generate the dungeon and create entities
        self._setup_game()

    def _setup_game(self) -> None:
        """Set up the initial game state."""
        # Generate dungeon
        player_x, player_y = self.game_map.generate_dungeon()

        # Create player
        self.player = create_player(player_x, player_y)
        self.entities.append(self.player)

        # Place monsters in rooms (except the first room where player starts)
        for room in self.game_map.rooms[1:]:
            # 80% chance to place a monster in each room
            if random.random() < MONSTER_SPAWN_CHANCE:
                monster_x, monster_y = room.center

                # 80% chance for orc, 20% chance for troll
                if random.random() < ORC_SPAWN_CHANCE:
                    monster = create_orc(monster_x, monster_y)
                else:
                    monster = create_troll(monster_x, monster_y)

                self.entities.append(monster)

        # Update field of view for initial state
        self.update_fov()

    def update_fov(self) -> None:
        """Update the field of view based on player position."""
        if hasattr(self.player, "position"):
            self.game_map.update_fov(self.player.position.x, self.player.position.y)

    def handle_player_action(self, action: str) -> bool:
        """
        Handle player actions.

        Args:
            action: Action string from input handler

        Returns:
            bool: True if action consumed player turn, False otherwise
        """
        if action == "quit":
            self.is_running = False
            return False

        elif action.startswith("move"):
            # Parse movement action
            parts = action.split()
            if len(parts) == MOVE_COMMAND_PARTS:
                try:
                    dx = int(parts[1])
                    dy = int(parts[2])

                    # Check for combat
                    target_x = self.player.position.x + dx
                    target_y = self.player.position.y + dy

                    # Look for monster at target position
                    target_monster = None
                    for entity in self.entities:
                        if (
                            hasattr(entity, "position")
                            and entity != self.player
                            and entity.position.x == target_x
                            and entity.position.y == target_y
                        ):
                            target_monster = entity
                            break

                    if target_monster:
                        # Attack the monster
                        if hasattr(target_monster, "health"):
                            damage = 5  # Player damage
                            target_monster.health.take_damage(damage)

                            # Remove dead monsters
                            if not target_monster.is_alive:
                                self.entities.remove(target_monster)

                        return True  # Combat consumes turn
                    # Try to move
                    elif move_player(self.player, dx, dy, self.game_map):
                        self.update_fov()
                        return True  # Movement consumes turn

                except ValueError:
                    pass

        return False  # No turn consumed

    def update_monsters(self) -> None:
        """Update all monster AI."""
        for entity in self.entities:
            if entity != self.player and hasattr(entity, "ai"):
                entity.ai.perform(self.game_map, self.entities)

    def handle_events(self) -> None:
        """Handle input events."""
        action = handle_events()
        if action:
            # Player took an action
            player_turn_taken = self.handle_player_action(action)

            # If player took a turn, update monsters
            if player_turn_taken:
                self.update_monsters()

    def update(self) -> None:
        """Update game state."""
        # Check if player is still alive
        if not self.player.is_alive:
            self.is_running = False

    def render(self) -> None:
        """Render the current game state."""
        self.renderer.render_all(self.game_map, self.entities, self.player)
        self.renderer.present(self.context)

    def run(self) -> None:
        """Main game loop."""
        try:
            while self.is_running:
                self.handle_events()
                self.update()
                self.render()
        finally:
            # Clean up
            self.context.close()

    def stop(self) -> None:
        """Stop the game."""
        self.is_running = False
