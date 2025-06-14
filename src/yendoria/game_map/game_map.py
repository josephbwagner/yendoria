"""
Game map module for Yendoria.

This module contains the GameMap class which manages the game world,
including tiles, dungeon generation, and field of view calculations.
"""

import random

import numpy as np
import tcod

from ..utils.constants import (
    MAP_HEIGHT,
    MAP_WIDTH,
    MAX_ROOMS,
    ROOM_MAX_SIZE,
    ROOM_MIN_SIZE,
)
from .room import RectangularRoom, tunnel_between
from .tile import Tile, floor, wall


class GameMap:
    """
    The game map containing all tiles and providing dungeon generation.

    Attributes:
        width (int): Map width in tiles
        height (int): Map height in tiles
        tiles (np.ndarray): 2D array of Tile objects
        visible (np.ndarray): 2D boolean array for currently visible tiles
        explored (np.ndarray): 2D boolean array for previously seen tiles
        rooms (List[RectangularRoom]): List of generated rooms
    """

    def __init__(self, width: int = MAP_WIDTH, height: int = MAP_HEIGHT):
        """
        Initialize a new game map.

        Args:
            width: Map width in tiles
            height: Map height in tiles
        """
        self.width = width
        self.height = height

        # Initialize the map with walls
        self.tiles = np.full((width, height), fill_value=wall, dtype=Tile)

        # Initialize field of view arrays
        self.visible = np.full((width, height), fill_value=False, dtype=bool)
        self.explored = np.full((width, height), fill_value=False, dtype=bool)

        # List to store generated rooms
        self.rooms: list[RectangularRoom] = []

    def generate_dungeon(self) -> tuple[int, int]:
        """
        Generate a dungeon with rooms and corridors.

        Returns:
            Tuple[int, int]: Starting position (player spawn point)
        """
        for _room_number in range(MAX_ROOMS):
            room_width = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)  # nosec B311
            room_height = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)  # nosec B311

            # Random position within map bounds
            x = random.randint(0, self.width - room_width - 1)  # nosec B311
            y = random.randint(0, self.height - room_height - 1)  # nosec B311

            # Create new room
            new_room = RectangularRoom(x, y, room_width, room_height)

            # Check if room intersects with existing rooms
            if any(new_room.intersects(other_room) for other_room in self.rooms):
                continue  # Skip this room

            # Carve out the room's inner area
            self.tiles[new_room.inner] = floor

            if len(self.rooms) == 0:
                # First room - player starts here
                player_x, player_y = new_room.center
            else:
                # Connect to previous room with tunnel
                for x, y in tunnel_between(self.rooms[-1].center, new_room.center):
                    self.tiles[x, y] = floor

            self.rooms.append(new_room)

        return player_x, player_y

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Check if coordinates are within map bounds.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            bool: True if coordinates are within bounds
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, x: int, y: int) -> bool:
        """
        Check if a tile is walkable.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            bool: True if tile exists and is walkable
        """
        if not self.in_bounds(x, y):
            return False
        return bool(self.tiles[x, y].walkable)

    def update_fov(self, player_x: int, player_y: int, radius: int = 8) -> None:
        """
        Update field of view calculations.

        Args:
            player_x: Player's x coordinate
            player_y: Player's y coordinate
            radius: Sight radius
        """
        # Reset visible tiles
        self.visible[:] = False

        # Create transparency matrix with correct dimensions
        transparency = np.zeros((self.width, self.height), dtype=bool)
        for x in range(self.width):
            for y in range(self.height):
                transparency[x, y] = self.tiles[x, y].transparent

        # Calculate field of view
        self.visible[:] = tcod.map.compute_fov(
            transparency=transparency,
            pov=(player_x, player_y),
            radius=radius,
        )

        # Update explored tiles
        self.explored |= self.visible
