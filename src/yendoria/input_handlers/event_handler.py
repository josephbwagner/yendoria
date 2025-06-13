"""
Event handling system for Yendoria.

This module handles input events from the player including movement,
actions, and system commands like quitting the game.
"""

import tcod.event

from ..utils.constants import MOVE_KEYS


class EventHandler(tcod.event.EventDispatch[None]):
    """
    Main event handler for the game.

    Handles keyboard and other input events, returning appropriate
    actions for the game engine to process.
    """

    def __init__(self):
        """Initialize the event handler."""
        super().__init__()

    def ev_quit(self, event: tcod.event.Quit) -> str | None:
        """
        Handle quit events (like clicking the X button).

        Args:
            event: The quit event

        Returns:
            str: "quit" action
        """
        return "quit"

    def ev_keydown(self, event: tcod.event.KeyDown) -> str | None:
        """
        Handle key press events.

        Args:
            event: The key down event

        Returns:
            str or None: Action string if action should be taken
        """
        key = event.sym

        # Movement keys
        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            return f"move {dx} {dy}"

        # System commands
        if key == tcod.event.KeySym.ESCAPE:
            return "quit"

        # No action for this key
        return None


class GameEventHandler(EventHandler):
    """
    Event handler for the main game state.

    Extends the base event handler with game-specific actions.
    """

    def ev_keydown(self, event: tcod.event.KeyDown) -> str | None:
        """
        Handle key press events during normal gameplay.

        Args:
            event: The key down event

        Returns:
            str or None: Action string if action should be taken
        """
        # First check base handler
        action = super().ev_keydown(event)
        if action:
            return action

        # Additional game actions can be added here
        # For example:
        # if key == tcod.event.KeySym.i:
        #     return "inventory"
        # if key == tcod.event.KeySym.g:
        #     return "pickup"

        return None


def handle_events() -> str | None:
    """
    Process all pending events and return the first action.

    Returns:
        str or None: Action string if an action should be taken
    """
    handler = GameEventHandler()

    for event in tcod.event.wait():
        action = handler.dispatch(event)
        if action:
            return action

    return None
