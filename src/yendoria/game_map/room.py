"""
Room generation for dungeon creation.

This module contains classes for creating rectangular rooms
and managing room placement in the dungeon.
"""

import random
from collections.abc import Iterator

import tcod

from ..utils.constants import TUNNEL_DIRECTION_CHANCE


class RectangularRoom:
    """
    A rectangular room for dungeon generation.

    Args:
        x (int): Top-left x coordinate
        y (int): Top-left y coordinate
        width (int): Room width
        height (int): Room height
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> tuple[int, int]:
        """Return the center coordinates of the room."""
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    @property
    def inner(self) -> tuple[slice, slice]:
        """Return the inner area of the room as slices (excludes walls)."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: "RectangularRoom") -> bool:
        """
        Check if this room intersects with another room.

        Args:
            other: Another RectangularRoom to check intersection with

        Returns:
            bool: True if rooms intersect, False otherwise
        """
        return (
            self.x1 < other.x2
            and self.x2 > other.x1
            and self.y1 < other.y2
            and self.y2 > other.y1
        )


def tunnel_between(
    start: tuple[int, int], end: tuple[int, int]
) -> Iterator[tuple[int, int]]:
    """
    Create an L-shaped tunnel between two points.

    Args:
        start: Starting coordinates (x, y)
        end: Ending coordinates (x, y)

    Yields:
        Tuple[int, int]: Coordinates along the tunnel path
    """
    x1, y1 = start
    x2, y2 = end

    if random.random() < TUNNEL_DIRECTION_CHANCE:  # nosec B311
        # Move horizontally, then vertically
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally
        corner_x, corner_y = x1, y2

    # Generate coordinates for the L-shaped tunnel
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y
