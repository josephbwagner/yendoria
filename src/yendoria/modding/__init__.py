"""
Event system foundation for Yendoria modding support.

This module provides the core event bus system that will allow mods
to hook into game events and extend functionality.
"""

import logging
from collections import defaultdict
from collections.abc import Callable
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Core game events that mods can hook into."""

    # Entity events
    ENTITY_SPAWN = "entity_spawn"
    ENTITY_DEATH = "entity_death"
    ENTITY_MOVE = "entity_move"

    # Combat events
    COMBAT_START = "combat_start"
    COMBAT_HIT = "combat_hit"
    COMBAT_MISS = "combat_miss"

    # Map events
    LEVEL_GENERATE = "level_generate"
    LEVEL_ENTER = "level_enter"
    ROOM_GENERATE = "room_generate"

    # Player events
    PLAYER_LEVEL_UP = "player_level_up"
    PLAYER_DEATH = "player_death"

    # Item events
    ITEM_PICKUP = "item_pickup"
    ITEM_USE = "item_use"
    ITEM_DROP = "item_drop"

    # UI events
    TURN_START = "turn_start"
    TURN_END = "turn_end"


class GameEvent:
    """
    Represents a game event that can be modified by mods.

    Attributes:
        type: The type of event
        data: Event-specific data
        cancellable: Whether mods can cancel this event
        cancelled: Whether the event has been cancelled
        source: What triggered this event (for debugging)
    """

    def __init__(
        self,
        event_type: EventType,
        data: dict[str, Any],
        cancellable: bool = False,
        source: str = "core",
    ):
        self.type = event_type
        self.data = data
        self.cancellable = cancellable
        self.cancelled = False
        self.source = source

    def cancel(self) -> None:
        """Cancel this event if it's cancellable."""
        if self.cancellable:
            self.cancelled = True
        else:
            logger.warning(f"Attempted to cancel non-cancellable event: {self.type}")

    def __repr__(self) -> str:
        return f"GameEvent({self.type}, cancelled={self.cancelled})"


class EventBus:
    """
    Central event system for the game.

    Allows mods and core systems to register event handlers
    and emit events throughout the game lifecycle.
    """

    def __init__(self):
        self.handlers: dict[EventType, list[Callable]] = defaultdict(list)
        self.event_history: list[GameEvent] = []
        self.max_history = 1000  # Prevent memory bloat

    def subscribe(
        self, event_type: EventType, handler: Callable[[GameEvent], None]
    ) -> None:
        """
        Register a handler function for a specific event type.

        Args:
            event_type: The type of event to listen for
            handler: Function that takes a GameEvent and returns None
        """
        self.handlers[event_type].append(handler)
        logger.debug(f"Registered handler for {event_type}")

    def unsubscribe(self, event_type: EventType, handler: Callable) -> None:
        """Remove a handler for a specific event type."""
        if handler in self.handlers[event_type]:
            self.handlers[event_type].remove(handler)
            logger.debug(f"Unregistered handler for {event_type}")

    def emit(self, event: GameEvent) -> GameEvent:
        """
        Fire an event to all registered handlers.

        Args:
            event: The event to emit

        Returns:
            The event (possibly modified by handlers)
        """
        # Store in history
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)

        # Call all handlers for this event type
        for handler in self.handlers[event.type]:
            try:
                handler(event)
                # If event was cancelled by a handler, stop processing
                if event.cancelled and event.cancellable:
                    logger.debug(f"Event {event.type} was cancelled by handler")
                    break
            except Exception as e:
                logger.error(f"Error in event handler for {event.type}: {e}")
                # Continue processing other handlers even if one fails

        return event

    def emit_simple(
        self,
        event_type: EventType,
        data: dict[str, Any] | None = None,
        cancellable: bool = False,
    ) -> GameEvent:
        """
        Convenience method to emit an event with minimal setup.

        Args:
            event_type: The type of event
            data: Event data (optional)
            cancellable: Whether the event can be cancelled

        Returns:
            The emitted event
        """
        if data is None:
            data = {}

        event = GameEvent(event_type, data, cancellable)
        return self.emit(event)

    def get_event_history(self, event_type: EventType | None = None) -> list[GameEvent]:
        """
        Get recent event history, optionally filtered by type.

        Args:
            event_type: Filter by this event type (optional)

        Returns:
            List of recent events
        """
        if event_type is None:
            return self.event_history.copy()
        else:
            return [e for e in self.event_history if e.type == event_type]

    def clear_handlers(self) -> None:
        """Clear all event handlers (useful for testing/cleanup)."""
        self.handlers.clear()
        logger.debug("Cleared all event handlers")


# Global event bus instance
# This will be used throughout the game
game_events = EventBus()


# Example event handler functions that could be used by mods
def log_entity_spawns(event: GameEvent) -> None:
    """Example handler that logs when entities spawn."""
    entity = event.data.get("entity")
    if entity:
        logger.info(f"Entity spawned: {entity.name} at {entity.position}")


def prevent_player_death(event: GameEvent) -> None:
    """Example handler that prevents player death (god mode mod)."""
    if event.data.get("entity_type") == "player":
        logger.info("Player death prevented by mod!")
        event.cancel()


# Usage examples:
if __name__ == "__main__":
    # Example of how the event system would be used

    # Register some handlers
    game_events.subscribe(EventType.ENTITY_SPAWN, log_entity_spawns)
    game_events.subscribe(EventType.PLAYER_DEATH, prevent_player_death)

    # Emit some events
    spawn_event = game_events.emit_simple(
        EventType.ENTITY_SPAWN, {"entity": {"name": "Orc", "position": (10, 5)}}
    )

    death_event = game_events.emit_simple(
        EventType.PLAYER_DEATH,
        {"entity_type": "player", "cause": "orc_attack"},
        cancellable=True,
    )

    print(f"Death event cancelled: {death_event.cancelled}")
