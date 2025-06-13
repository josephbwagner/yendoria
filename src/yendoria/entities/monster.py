"""
Monster entity module.

This module contains functions for creating different types of monster entities.
"""

from ..components.component import BasicMonsterAI, Damage, Graphic, Health, Position
from ..utils.constants import CHAR_ORC, CHAR_TROLL, COLOR_GREEN, COLOR_RED
from .entity import Entity


def create_orc(x: int, y: int) -> Entity:
    """
    Create an orc monster entity with basic AI and combat capabilities.

    Args:
        x: Starting x coordinate
        y: Starting y coordinate

    Returns:
        Entity: A fully configured orc entity with Position, Health,
                Graphic, AI, and Damage components
    """
    orc = Entity(name="Orc")

    # Add components
    orc.add_component(Position(x, y))
    orc.add_component(Health(max_hp=10))
    orc.add_component(Graphic(char=CHAR_ORC, color=COLOR_RED))
    orc.add_component(BasicMonsterAI())
    orc.add_component(Damage(amount=3))

    return orc


def create_troll(x: int, y: int) -> Entity:
    """
    Create a troll monster entity with basic AI and combat capabilities.

    Args:
        x: Starting x coordinate
        y: Starting y coordinate

    Returns:
        Entity: A fully configured troll entity with Position, Health,
                Graphic, AI, and Damage components
    """
    troll = Entity(name="Troll")

    # Add components
    troll.add_component(Position(x, y))
    troll.add_component(Health(max_hp=16))
    troll.add_component(Graphic(char=CHAR_TROLL, color=COLOR_GREEN))
    troll.add_component(BasicMonsterAI())
    troll.add_component(Damage(amount=4))

    return troll
