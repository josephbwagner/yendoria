"""
Constants used throughout Yendoria.

This module contains all game constants including colors, dimensions,
and key mappings for Yendoria.
"""

import tcod

# Screen dimensions
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# Map dimensions
MAP_WIDTH = 80
MAP_HEIGHT = 43

# UI dimensions
UI_HEIGHT = 7

# Room generation parameters
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

# Probability constants
MONSTER_SPAWN_CHANCE = 0.8  # 80% chance to spawn monster in room
ORC_SPAWN_CHANCE = 0.8  # 80% chance for orc, 20% for troll
TUNNEL_DIRECTION_CHANCE = 0.5  # 50% chance for horizontal-first tunnel

# Game mechanics constants
MOVE_COMMAND_PARTS = 3  # Expected parts in move command

# Colors using tuple format (compatible with newer tcod)
# Map colors
COLOR_DARK_WALL = (0, 0, 100)
COLOR_DARK_GROUND = (50, 50, 150)
COLOR_LIGHT_WALL = (130, 110, 50)
COLOR_LIGHT_GROUND = (200, 180, 50)

# Entity colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)

# Character representations
CHAR_PLAYER = ord("@")
CHAR_ORC = ord("o")
CHAR_TROLL = ord("T")
CHAR_WALL = ord("#")
CHAR_FLOOR = ord(".")

# Game settings
FPS = 60

# Key mappings for movement and actions
MOVE_KEYS = {
    # Arrow keys
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    # Numpad
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_9: (1, -1),
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_3: (1, 1),
    # WASD keys
    tcod.event.KeySym.W: (0, -1),
    tcod.event.KeySym.S: (0, 1),
    tcod.event.KeySym.A: (-1, 0),
    tcod.event.KeySym.D: (1, 0),
    # Vim keys
    tcod.event.KeySym.H: (-1, 0),
    tcod.event.KeySym.J: (0, 1),
    tcod.event.KeySym.K: (0, -1),
    tcod.event.KeySym.L: (1, 0),
    tcod.event.KeySym.Y: (-1, -1),
    tcod.event.KeySym.U: (1, -1),
    tcod.event.KeySym.B: (-1, 1),
    tcod.event.KeySym.N: (1, 1),
}
