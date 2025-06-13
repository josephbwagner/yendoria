"""
Yendoria game package.

A traditional tile-based roguelike game built with Python and libtcod.
"""

from .engine import GameEngine
from .main import main

__version__ = "0.1.0"
__all__ = ["GameEngine", "main"]
