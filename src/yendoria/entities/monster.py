"""
Monster entity module.

This module contains functions for creating different types of monster entities.
"""

import logging

from yendoria.components.component_manager import (
    ComponentManager,
    get_component_manager,
)
from yendoria.systems.ai_manager import AIManager, get_ai_manager

from ..components.component import BasicMonsterAI, Damage, Graphic, Health, Position
from ..utils.constants import CHAR_ORC, CHAR_TROLL, COLOR_GREEN, COLOR_RED
from .entity import Entity

logger = logging.getLogger(__name__)


def get_managers() -> tuple[ComponentManager, AIManager]:
    return get_component_manager(), get_ai_manager()


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

    # Create the entity via the component manager so it gets a valid ID
    component_manager, ai_manager = get_managers()
    orc = component_manager.create_entity(name="Orc")

    # Add components
    orc.add_component(Position(x, y))
    orc.add_component(Health(max_hp=10))
    orc.add_component(Graphic(char=CHAR_ORC, color=COLOR_RED))
    orc.add_component(BasicMonsterAI())
    orc.add_component(Damage(amount=3))

    # Register with AI manager
    if orc.id is None:
        raise RuntimeError("Entity ID was not set by ComponentManager!")
    ai_manager.register_ai_entity(
        entity_id=orc.id, archetype="aggressive_monster", faction="monsters"
    )

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

    # Create the entity via the component manager so it gets a valid ID
    component_manager, ai_manager = get_managers()
    troll = component_manager.create_entity(name="Troll")

    # Add components
    troll.add_component(Position(x, y))
    troll.add_component(Health(max_hp=16))
    troll.add_component(Graphic(char=CHAR_TROLL, color=COLOR_GREEN))
    troll.add_component(BasicMonsterAI())
    troll.add_component(Damage(amount=4))

    # Register with AI manager
    if troll.id is None:
        raise RuntimeError("Entity ID was not set by ComponentManager!")
    ai_manager.register_ai_entity(
        entity_id=troll.id, archetype="tough_monster", faction="monsters"
    )

    return troll
