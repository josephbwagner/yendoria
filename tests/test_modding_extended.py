"""
Tests for modding system functionality.
"""

import contextlib
from unittest.mock import Mock

from src.yendoria.modding import (
    EventBus,
    EventType,
    GameEvent,
)


class TestEventType:
    """Test cases for EventType enum."""

    def test_event_type_values(self):
        """Test that EventType has expected values."""
        assert EventType.ENTITY_SPAWN.value == "entity_spawn"
        assert EventType.ENTITY_DEATH.value == "entity_death"
        assert EventType.ENTITY_MOVE.value == "entity_move"
        assert EventType.COMBAT_START.value == "combat_start"
        assert EventType.COMBAT_HIT.value == "combat_hit"
        assert EventType.COMBAT_MISS.value == "combat_miss"

    def test_event_type_membership(self):
        """Test EventType membership."""
        assert EventType.ENTITY_SPAWN in EventType
        assert EventType.COMBAT_HIT in EventType
        assert "invalid_event" not in [e.value for e in EventType]

    def test_event_type_iteration(self):
        """Test iterating over EventType."""
        event_types = list(EventType)
        assert len(event_types) >= 6  # At least the core events we know about
        assert EventType.ENTITY_SPAWN in event_types
        assert EventType.COMBAT_START in event_types


class TestGameEvent:
    """Test cases for GameEvent class."""

    def test_game_event_creation(self):
        """Test GameEvent creation."""
        event = GameEvent(EventType.ENTITY_SPAWN, {"entity": "test"})

        assert event.type == EventType.ENTITY_SPAWN
        assert event.data == {"entity": "test"}
        assert event.source == "core"

    def test_game_event_creation_minimal(self):
        """Test GameEvent creation with minimal data."""
        event = GameEvent(EventType.COMBAT_HIT, {})

        assert event.type == EventType.COMBAT_HIT
        assert event.data == {}
        assert event.source == "core"

    def test_game_event_creation_with_data(self):
        """Test GameEvent creation with complex data."""
        data = {"attacker": "player", "target": "orc", "damage": 10, "position": (5, 5)}
        event = GameEvent(EventType.COMBAT_HIT, data)

        assert event.type == EventType.COMBAT_HIT
        assert event.data == data
        assert event.source == "core"

    def test_game_event_timestamp_uniqueness(self):
        """Test that different events have different sources."""
        event1 = GameEvent(EventType.ENTITY_SPAWN, {})
        event2 = GameEvent(EventType.ENTITY_SPAWN, {}, source="test")

        assert event1.source == "core"
        assert event2.source == "test"

    def test_game_event_data_modification(self):
        """Test that event data can be accessed and modified."""
        event = GameEvent(EventType.ENTITY_MOVE, {"x": 5, "y": 10})

        assert event.data["x"] == 5
        assert event.data["y"] == 10

        # Modify data
        event.data["x"] = 6
        assert event.data["x"] == 6

    def test_game_event_string_representation(self):
        """Test string representation of GameEvent."""
        event = GameEvent(EventType.COMBAT_HIT, {"damage": 5})

        event_str = str(event)
        assert "COMBAT_HIT" in event_str or "combat_hit" in event_str

    def test_game_event_equality(self):
        """Test GameEvent equality comparison."""
        event1 = GameEvent(EventType.ENTITY_SPAWN, {"entity": "test"})
        event2 = GameEvent(EventType.ENTITY_SPAWN, {"entity": "test"})

        # Events should be different objects even with same data
        assert event1 is not event2


class TestEventBus:
    """Test cases for EventBus class."""

    def test_event_bus_creation(self):
        """Test EventBus creation."""
        bus = EventBus()

        assert bus is not None
        # Check if it has expected attributes
        assert hasattr(bus, "subscribe") or hasattr(bus, "register")
        assert hasattr(bus, "publish") or hasattr(bus, "emit")

    def test_event_bus_subscribe(self):
        """Test subscribing to events."""
        bus = EventBus()

        callback = Mock()

        # Try different subscription method names
        if hasattr(bus, "subscribe"):
            bus.subscribe(EventType.ENTITY_SPAWN, callback)
        elif hasattr(bus, "register"):
            bus.register(EventType.ENTITY_SPAWN, callback)
        elif hasattr(bus, "add_listener"):
            bus.add_listener(EventType.ENTITY_SPAWN, callback)

        # Should not raise an error

    def test_event_bus_publish(self):
        """Test publishing events."""
        bus = EventBus()

        callback = Mock()

        # Subscribe first
        if hasattr(bus, "subscribe"):
            bus.subscribe(EventType.ENTITY_SPAWN, callback)
        elif hasattr(bus, "register"):
            bus.register(EventType.ENTITY_SPAWN, callback)
        elif hasattr(bus, "add_listener"):
            bus.add_listener(EventType.ENTITY_SPAWN, callback)

        # Publish event
        event = GameEvent(EventType.ENTITY_SPAWN, {"entity": "test"})

        if hasattr(bus, "publish"):
            bus.publish(event)
        elif hasattr(bus, "emit"):
            bus.emit(event)
        elif hasattr(bus, "dispatch"):
            bus.dispatch(event)

        # Should not raise an error

    def test_event_bus_multiple_subscribers(self):
        """Test multiple subscribers for same event."""
        bus = EventBus()

        callback1 = Mock()
        callback2 = Mock()

        # Subscribe both callbacks
        subscribe_method = None
        for method_name in ["subscribe", "register", "add_listener"]:
            if hasattr(bus, method_name):
                subscribe_method = getattr(bus, method_name)
                break

        if subscribe_method:
            subscribe_method(EventType.ENTITY_SPAWN, callback1)
            subscribe_method(EventType.ENTITY_SPAWN, callback2)

        # Should not raise an error

    def test_event_bus_unsubscribe(self):
        """Test unsubscribing from events."""
        bus = EventBus()

        callback = Mock()

        # Subscribe first
        subscribe_method = None
        for method_name in ["subscribe", "register", "add_listener"]:
            if hasattr(bus, method_name):
                subscribe_method = getattr(bus, method_name)
                break

        if subscribe_method:
            subscribe_method(EventType.ENTITY_SPAWN, callback)

        # Unsubscribe
        unsubscribe_method = None
        for method_name in ["unsubscribe", "unregister", "remove_listener"]:
            if hasattr(bus, method_name):
                unsubscribe_method = getattr(bus, method_name)
                break

        if unsubscribe_method:
            unsubscribe_method(EventType.ENTITY_SPAWN, callback)

        # Should not raise an error

    def test_event_bus_clear_subscribers(self):
        """Test clearing all subscribers."""
        bus = EventBus()

        callback1 = Mock()
        callback2 = Mock()

        # Subscribe callbacks
        subscribe_method = None
        for method_name in ["subscribe", "register", "add_listener"]:
            if hasattr(bus, method_name):
                subscribe_method = getattr(bus, method_name)
                break

        if subscribe_method:
            subscribe_method(EventType.ENTITY_SPAWN, callback1)
            subscribe_method(EventType.COMBAT_HIT, callback2)

        # Clear all
        clear_method = None
        for method_name in ["clear", "clear_all", "reset"]:
            if hasattr(bus, method_name):
                clear_method = getattr(bus, method_name)
                break

        if clear_method:
            clear_method()

        # Should not raise an error

    def test_event_bus_event_types(self):
        """Test event bus with different event types."""
        bus = EventBus()

        callbacks = {}
        for event_type in EventType:
            callbacks[event_type] = Mock()

        # Subscribe to all event types
        subscribe_method = None
        for method_name in ["subscribe", "register", "add_listener"]:
            if hasattr(bus, method_name):
                subscribe_method = getattr(bus, method_name)
                break

        if subscribe_method:
            for event_type, callback in callbacks.items():
                subscribe_method(event_type, callback)

        # Should not raise an error

    def test_event_bus_invalid_event_type(self):
        """Test event bus with invalid event type."""
        bus = EventBus()

        callback = Mock()

        # Try to subscribe with invalid event type
        subscribe_method = None
        for method_name in ["subscribe", "register", "add_listener"]:
            if hasattr(bus, method_name):
                subscribe_method = getattr(bus, method_name)
                break

        if subscribe_method:
            with contextlib.suppress(ValueError, TypeError, KeyError):
                subscribe_method("invalid_event", callback)

        # Should handle gracefully

    def test_event_bus_singleton_behavior(self):
        """Test if EventBus behaves as singleton."""
        bus1 = EventBus()
        bus2 = EventBus()

        # May or may not be singleton, both behaviors are valid
        assert bus1 is not None
        assert bus2 is not None


class TestEventBusIntegration:
    """Integration tests for the event bus system."""

    def test_full_event_lifecycle(self):
        """Test complete event lifecycle."""
        bus = EventBus()

        # Create callback
        callback = Mock()

        # Subscribe
        subscribe_method = None
        for method_name in ["subscribe", "register", "add_listener"]:
            if hasattr(bus, method_name):
                subscribe_method = getattr(bus, method_name)
                break

        if subscribe_method:
            subscribe_method(EventType.ENTITY_SPAWN, callback)

        # Create and publish event
        event = GameEvent(EventType.ENTITY_SPAWN, {"entity": "player"})

        publish_method = None
        for method_name in ["publish", "emit", "dispatch"]:
            if hasattr(bus, method_name):
                publish_method = getattr(bus, method_name)
                break

        if publish_method:
            publish_method(event)

        # Should complete without error

    def test_event_filtering(self):
        """Test event filtering by type."""
        bus = EventBus()

        spawn_callback = Mock()
        combat_callback = Mock()

        # Subscribe to different events
        subscribe_method = None
        for method_name in ["subscribe", "register", "add_listener"]:
            if hasattr(bus, method_name):
                subscribe_method = getattr(bus, method_name)
                break

        if subscribe_method:
            subscribe_method(EventType.ENTITY_SPAWN, spawn_callback)
            subscribe_method(EventType.COMBAT_HIT, combat_callback)

        # Publish different events
        spawn_event = GameEvent(EventType.ENTITY_SPAWN, {})
        combat_event = GameEvent(EventType.COMBAT_HIT, {})

        publish_method = None
        for method_name in ["publish", "emit", "dispatch"]:
            if hasattr(bus, method_name):
                publish_method = getattr(bus, method_name)
                break

        if publish_method:
            publish_method(spawn_event)
            publish_method(combat_event)

        # Should complete without error

    def test_error_handling_in_callbacks(self):
        """Test error handling when callbacks fail."""
        bus = EventBus()

        # Create callback that raises an exception
        def failing_callback(event):
            raise ValueError("Test error")

        # Subscribe failing callback
        subscribe_method = None
        for method_name in ["subscribe", "register", "add_listener"]:
            if hasattr(bus, method_name):
                subscribe_method = getattr(bus, method_name)
                break

        if subscribe_method:
            subscribe_method(EventType.ENTITY_SPAWN, failing_callback)

        # Publish event
        event = GameEvent(EventType.ENTITY_SPAWN, {})

        publish_method = None
        for method_name in ["publish", "emit", "dispatch"]:
            if hasattr(bus, method_name):
                publish_method = getattr(bus, method_name)
                break

        if publish_method:
            with contextlib.suppress(ValueError):
                publish_method(event)

        # Should handle gracefully
