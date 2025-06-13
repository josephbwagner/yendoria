"""
Tile module for Yendoria.

This module defines the Tile class which represents individual tiles
on the game map, including their visual and gameplay properties.
"""

from ..utils.constants import (
    CHAR_FLOOR,
    CHAR_WALL,
    COLOR_DARK_GROUND,
    COLOR_DARK_WALL,
    COLOR_LIGHT_GROUND,
    COLOR_LIGHT_WALL,
    COLOR_WHITE,
)


class Tile:
    """
    A tile on the game map with visual and gameplay properties.

    Attributes:
        walkable (bool): True if entities can walk through this tile
        transparent (bool): True if this tile doesn't block field of view
        dark (TileGraphic): Graphics to use when tile is not visible
        light (TileGraphic): Graphics to use when tile is visible
    """

    def __init__(
        self,
        walkable: bool,
        transparent: bool,
        dark: tuple[int, tuple[int, int, int], tuple[int, int, int]],
        light: tuple[int, tuple[int, int, int], tuple[int, int, int]],
    ):
        self.walkable = walkable
        self.transparent = transparent
        self.dark = dark
        self.light = light


# Pre-defined tile types
floor = Tile(
    walkable=True,
    transparent=True,
    dark=(CHAR_FLOOR, COLOR_WHITE, COLOR_DARK_GROUND),
    light=(CHAR_FLOOR, COLOR_WHITE, COLOR_LIGHT_GROUND),
)

wall = Tile(
    walkable=False,
    transparent=False,
    dark=(CHAR_WALL, COLOR_WHITE, COLOR_DARK_WALL),
    light=(CHAR_WALL, COLOR_WHITE, COLOR_LIGHT_WALL),
)
