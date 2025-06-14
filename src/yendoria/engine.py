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
from .modding import EventBus, EventType  # Add event system import
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
        is_running (bool): Whether the game is currently running
    """

    context: tcod.context.Context | None

    def __init__(
        self,
        width: int = SCREEN_WIDTH,
        height: int = SCREEN_HEIGHT,
        headless: bool = False,
    ):
        """
        Initialize the game engine.

        Args:
            width: Screen width in characters
            height: Screen height in characters
            headless: If True, skip graphics initialization for testing
        """
        self.screen_width = width
        self.screen_height = height

        # Initialize tcod context only if not in headless mode
        if not headless:
            tileset = self._load_system_font()

            self.context = tcod.context.new(
                columns=width,
                rows=height,
                title="Yendoria",
                vsync=True,
                tileset=tileset,
            )
        else:
            self.context = None

        # Initialize game systems
        self.renderer = RenderingSystem()
        self.game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
        self.entities: list[Entity] = []
        self.event_bus = EventBus()  # Add event system for modding
        self.is_running = True

        # Generate the dungeon and create entities
        self._setup_game()

    def _load_system_font(self) -> tcod.tileset.Tileset | None:
        """
        Try to load a system monospace font for the tileset.

        Returns:
            A loaded tileset, or None if no suitable font is found
        """
        try:
            import os
            import platform

            # Choose a font based on the operating system
            system = platform.system()
            font_path = None

            if system == "Darwin":  # macOS
                # Try SF Mono (modern macOS) first
                if os.path.exists("/System/Library/Fonts/SFNSMono.ttf"):
                    font_path = "/System/Library/Fonts/SFNSMono.ttf"
                elif os.path.exists("/System/Library/Fonts/Monaco.ttf"):
                    font_path = "/System/Library/Fonts/Monaco.ttf"
            elif system == "Windows":
                if os.path.exists("C:\\Windows\\Fonts\\consola.ttf"):
                    font_path = "C:\\Windows\\Fonts\\consola.ttf"  # Consolas
                elif os.path.exists("C:\\Windows\\Fonts\\cour.ttf"):
                    font_path = "C:\\Windows\\Fonts\\cour.ttf"  # Courier New
            else:  # Linux and others
                # Try common Linux monospace fonts
                linux_fonts = [
                    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
                    "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
                ]
                for font in linux_fonts:
                    if os.path.exists(font):
                        font_path = font
                        break

            # Load the font if it exists
            if font_path and os.path.exists(font_path):
                return tcod.tileset.load_truetype_font(font_path, 16, 16)

        except (OSError, ImportError, TypeError, ValueError):
            # If any font loading error occurs, fall back to no tileset
            # Specific exceptions: file not found, import issues, invalid parameters
            pass  # nosec B110

        return None

    def _setup_game(self) -> None:
        """Set up the initial game state."""
        # Generate dungeon
        player_x, player_y = self.game_map.generate_dungeon()

        # Emit level generation event
        self.event_bus.emit_simple(
            EventType.LEVEL_GENERATE,
            {
                "map": self.game_map,
                "player_start": (player_x, player_y),
                "rooms": self.game_map.rooms,
            },
        )

        # Create player
        self.player = create_player(player_x, player_y)
        self.entities.append(self.player)

        # Emit player spawn event
        self.event_bus.emit_simple(
            EventType.ENTITY_SPAWN,
            {
                "entity": self.player,
                "position": (player_x, player_y),
                "entity_type": "player",
            },
        )

        # Place monsters in rooms (except the first room where player starts)
        for room in self.game_map.rooms[1:]:
            # 80% chance to place a monster in each room
            if random.random() < MONSTER_SPAWN_CHANCE:  # nosec B311
                monster_x, monster_y = room.center

                # 80% chance for orc, 20% chance for troll
                if random.random() < ORC_SPAWN_CHANCE:  # nosec B311
                    monster = create_orc(monster_x, monster_y)
                    monster_type = "orc"
                else:
                    monster = create_troll(monster_x, monster_y)
                    monster_type = "troll"

                self.entities.append(monster)

                # Emit monster spawn event
                self.event_bus.emit_simple(
                    EventType.ENTITY_SPAWN,
                    {
                        "entity": monster,
                        "position": (monster_x, monster_y),
                        "entity_type": monster_type,
                        "room": room,
                    },
                )

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
                    player_pos = self.player.get_component("position")
                    if (
                        not player_pos
                        or not hasattr(player_pos, "x")
                        or not hasattr(player_pos, "y")
                    ):
                        return False
                    target_x = player_pos.x + dx
                    target_y = player_pos.y + dy

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
                        return self._handle_combat(target_monster, target_x, target_y)

                    # Try to move
                    elif move_player(self.player, dx, dy, self.game_map):
                        # Emit player movement event for mods
                        position = getattr(self.player, "position", None)
                        if position:
                            self.event_bus.emit_simple(
                                EventType.ENTITY_MOVE,
                                {
                                    "entity": self.player,
                                    "old_position": (position.x - dx, position.y - dy),
                                    "new_position": (position.x, position.y),
                                    "is_player": True,
                                    "movement": (dx, dy),
                                },
                            )
                        self.update_fov()
                        return True  # Movement consumes turn

                except ValueError:
                    pass

        return False  # No turn consumed

    def _handle_combat(
        self, target_monster: Entity, target_x: int, target_y: int
    ) -> bool:
        """Handle combat between player and monster.

        Args:
            target_monster: The monster being attacked
            target_x: Target x coordinate
            target_y: Target y coordinate

        Returns:
            bool: True if combat occurred
        """
        # Emit combat start event
        combat_event = self.event_bus.emit_simple(
            EventType.COMBAT_START,
            {
                "attacker": self.player,
                "defender": target_monster,
                "position": (target_x, target_y),
            },
            cancellable=True,
        )

        has_health = hasattr(target_monster, "health")
        if not combat_event.cancelled and has_health:
            # Attack the monster
            damage = 5  # Player damage
            health_comp = getattr(target_monster, "health", None)
            original_hp = health_comp.current_hp if health_comp else 0

            # Emit combat hit event
            self.event_bus.emit_simple(
                EventType.COMBAT_HIT,
                {
                    "attacker": self.player,
                    "defender": target_monster,
                    "damage": damage,
                    "original_hp": original_hp,
                },
            )

            if health_comp:
                health_comp.take_damage(damage)

            # Check if monster died
            if not target_monster.is_alive:
                # Emit entity death event
                self.event_bus.emit_simple(
                    EventType.ENTITY_DEATH,
                    {
                        "entity": target_monster,
                        "killer": self.player,
                        "position": (target_x, target_y),
                        "cause": "combat",
                    },
                )
                self.entities.remove(target_monster)

        return True  # Combat consumes turn

    def update_monsters(self) -> None:
        """Update all monster AI."""
        for entity in self.entities:
            if entity != self.player and hasattr(entity, "ai"):
                entity.ai.perform(self.game_map, self.entities)

    def handle_events(self) -> bool:
        """Handle input events.

        Returns:
            bool: True if player took a turn-consuming action
        """
        action = handle_events()
        if action:
            # Player took an action
            return self.handle_player_action(action)
        return False

    def update(self) -> None:
        """Update game state."""
        # Check if player is still alive
        if not self.player.is_alive:
            # Emit player death event
            position = getattr(self.player, "position", None)
            death_pos = (position.x, position.y) if position else (0, 0)
            self.event_bus.emit_simple(
                EventType.PLAYER_DEATH,
                {
                    "entity": self.player,
                    "position": death_pos,
                    "cause": "combat",  # Could be expanded for different causes
                },
            )
            self.is_running = False

    def render(self) -> None:
        """Render the current game state."""
        self.renderer.render_all(self.game_map, self.entities, self.player)
        if self.context is not None:
            self.renderer.present(self.context)

    def run(self) -> None:
        """Main game loop."""
        try:
            while self.is_running:
                # Emit turn start event
                turn_count = getattr(self, "_turn_count", 0)
                self.event_bus.emit_simple(
                    EventType.TURN_START,
                    {"player": self.player, "turn_count": turn_count},
                )

                player_acted = self.handle_events()
                self.update()

                # If player acted, update monsters and advance turn
                if player_acted:
                    self.update_monsters()
                    turn_count += 1
                    self._turn_count = turn_count

                    # Emit turn end event
                    self.event_bus.emit_simple(
                        EventType.TURN_END,
                        {"player": self.player, "turn_count": turn_count},
                    )

                self.render()
        finally:
            # Clean up
            if self.context is not None:
                self.context.close()

    def stop(self) -> None:
        """Stop the game."""
        self.is_running = False
