"""
Event handling system for Yendoria.

This module handles input events from the player including movement,
actions, and system commands like quitting the game.
"""

from typing import Protocol

import tcod.event

from ..utils.constants import MOVE_KEYS


class EventHandler(Protocol):
    """
    Protocol for event handlers in the game.

    Modern tcod event handling using Protocol instead of deprecated EventDispatch.
    """

    def handle_events(self, event: tcod.event.Event) -> str | None:
        """Handle an event and return an action string or None."""
        ...


class BaseEventHandler:
    """
    Base event handler for the game.

    Handles keyboard and other input events, returning appropriate
    actions for the game engine to process.
    """

    def handle_events(self, event: tcod.event.Event) -> str | None:
        """
        Handle events using modern tcod pattern.

        Args:
            event: The tcod event to handle

        Returns:
            Action string or None
        """
        # Handle quit events
        if isinstance(event, tcod.event.Quit):
            return self.ev_quit(event)

        # Handle keydown events
        if isinstance(event, tcod.event.KeyDown):
            return self.ev_keydown(event)

        return None

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


class GameEventHandler(BaseEventHandler):
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
        action: str | None = handler.handle_events(event)
        if action:
            return action

    return None
