"""
Tests for input handling and event processing.
"""

from unittest.mock import Mock, patch

try:
    import tcod.event
except ImportError:
    # Create mock for tcod.event if not available
    class MockEvent:
        pass

    class MockTcodEvent:
        Event = MockEvent
        Quit = MockEvent
        KeyDown = MockEvent
        KeySym = type(
            "KeySym",
            (),
            {
                "ESCAPE": 27,
                "UP": 273,
                "DOWN": 274,
                "LEFT": 276,
                "RIGHT": 275,
                "a": 97,
            },
        )

    tcod = type("tcod", (), {"event": MockTcodEvent})

from src.yendoria.input_handlers.event_handler import (
    BaseEventHandler,
    GameEventHandler,
    handle_events,
)
from src.yendoria.utils.constants import MOVE_KEYS


class TestEventHandler:
    """Test cases for event handler protocol."""

    def test_event_handler_protocol(self):
        """Test that EventHandler is a protocol."""

        # Test that we can create a class that implements the protocol
        class TestHandler:
            def handle_events(self, event: tcod.event.Event) -> str | None:
                return "test"

        handler = TestHandler()
        assert callable(handler.handle_events)


class TestBaseEventHandler:
    """Test cases for BaseEventHandler."""

    def setUp(self):
        """Set up test fixtures."""
        self.handler = BaseEventHandler()

    def test_handle_quit_event(self):
        """Test handling quit events."""
        handler = BaseEventHandler()
        quit_event = tcod.event.Quit()

        result = handler.handle_events(quit_event)
        assert result == "quit"

    def test_handle_escape_key(self):
        """Test handling escape key."""
        handler = BaseEventHandler()
        escape_event = tcod.event.KeyDown(
            sym=tcod.event.KeySym.ESCAPE,
            scancode=tcod.event.Scancode.ESCAPE,
            mod=tcod.event.Modifier.NONE,
        )

        result = handler.handle_events(escape_event)
        assert result == "quit"

    def test_handle_movement_keys(self):
        """Test handling movement keys."""
        handler = BaseEventHandler()

        # Test all movement keys
        for key_sym, (dx, dy) in MOVE_KEYS.items():
            key_event = tcod.event.KeyDown(
                sym=key_sym,
                scancode=tcod.event.Scancode.W,  # Use a default scancode
                mod=tcod.event.Modifier.NONE,
            )
            result = handler.handle_events(key_event)
            assert result == f"move {dx} {dy}"

    def test_handle_unknown_key(self):
        """Test handling unknown keys."""
        handler = BaseEventHandler()
        unknown_event = tcod.event.KeyDown(
            sym=tcod.event.KeySym.F1,  # F1 is not a movement key
            scancode=tcod.event.Scancode.F1,
            mod=tcod.event.Modifier.NONE,
        )

        result = handler.handle_events(unknown_event)
        assert result is None

    def test_handle_unknown_event(self):
        """Test handling unknown event types."""
        handler = BaseEventHandler()

        # Create a mock event that's not Quit or KeyDown
        mock_event = Mock(spec=tcod.event.Event)

        result = handler.handle_events(mock_event)
        assert result is None

    def test_ev_quit_method(self):
        """Test ev_quit method directly."""
        handler = BaseEventHandler()
        quit_event = tcod.event.Quit()

        result = handler.ev_quit(quit_event)
        assert result == "quit"

    def test_ev_keydown_method(self):
        """Test ev_keydown method directly."""
        handler = BaseEventHandler()

        # Test movement key
        key_event = tcod.event.KeyDown(
            sym=tcod.event.KeySym.UP,
            scancode=tcod.event.Scancode.UP,
            mod=tcod.event.Modifier.NONE,
        )
        result = handler.ev_keydown(key_event)
        assert result == "move 0 -1"

        # Test escape key
        escape_event = tcod.event.KeyDown(
            sym=tcod.event.KeySym.ESCAPE,
            scancode=tcod.event.Scancode.ESCAPE,
            mod=tcod.event.Modifier.NONE,
        )
        result = handler.ev_keydown(escape_event)
        assert result == "quit"

        # Test unknown key
        unknown_event = tcod.event.KeyDown(
            sym=tcod.event.KeySym.F1,
            scancode=tcod.event.Scancode.F1,
            mod=tcod.event.Modifier.NONE,
        )
        result = handler.ev_keydown(unknown_event)
        assert result is None


class TestGameEventHandler:
    """Test cases for GameEventHandler."""

    def test_inheritance(self):
        """Test that GameEventHandler inherits from BaseEventHandler."""
        handler = GameEventHandler()
        assert isinstance(handler, BaseEventHandler)

    def test_base_functionality(self):
        """Test that base functionality is preserved."""
        handler = GameEventHandler()

        # Test quit event
        quit_event = tcod.event.Quit()
        result = handler.handle_events(quit_event)
        assert result == "quit"

        # Test movement
        key_event = tcod.event.KeyDown(
            sym=tcod.event.KeySym.UP,
            scancode=tcod.event.Scancode.UP,
            mod=tcod.event.Modifier.NONE,
        )
        result = handler.handle_events(key_event)
        assert result == "move 0 -1"

    def test_ev_keydown_calls_super(self):
        """Test that ev_keydown calls super method."""
        handler = GameEventHandler()

        # Test that it returns the same result as base handler
        key_event = tcod.event.KeyDown(
            sym=tcod.event.KeySym.UP,
            scancode=tcod.event.Scancode.UP,
            mod=tcod.event.Modifier.NONE,
        )
        result = handler.ev_keydown(key_event)
        assert result == "move 0 -1"

    def test_ev_keydown_unknown_key(self):
        """Test that unknown keys return None."""
        handler = GameEventHandler()

        # Test unknown key
        unknown_event = tcod.event.KeyDown(
            sym=tcod.event.KeySym.F1,
            scancode=tcod.event.Scancode.F1,
            mod=tcod.event.Modifier.NONE,
        )
        result = handler.ev_keydown(unknown_event)
        assert result is None


class TestHandleEventsFunction:
    """Test cases for the handle_events function."""

    @patch("tcod.event.wait")
    def test_handle_events_with_action(self, mock_wait):
        """Test handle_events returns first action."""
        # Setup mock events
        quit_event = tcod.event.Quit()
        key_event = tcod.event.KeyDown(
            sym=tcod.event.KeySym.UP,
            scancode=tcod.event.Scancode.UP,
            mod=tcod.event.Modifier.NONE,
        )
        mock_wait.return_value = [quit_event, key_event]

        result = handle_events()
        assert result == "quit"

    @patch("tcod.event.wait")
    def test_handle_events_no_action(self, mock_wait):
        """Test handle_events with no actions."""
        # Setup mock events that don't produce actions
        unknown_event = tcod.event.KeyDown(
            sym=tcod.event.KeySym.F1,
            scancode=tcod.event.Scancode.F1,
            mod=tcod.event.Modifier.NONE,
        )
        mock_wait.return_value = [unknown_event]

        result = handle_events()
        assert result is None

    @patch("tcod.event.wait")
    def test_handle_events_empty_events(self, mock_wait):
        """Test handle_events with empty event list."""
        mock_wait.return_value = []

        result = handle_events()
        assert result is None

    @patch("tcod.event.wait")
    def test_handle_events_multiple_events(self, mock_wait):
        """Test handle_events returns first valid action."""
        # Setup mock events - first doesn't produce action, second does
        unknown_event = tcod.event.KeyDown(
            sym=tcod.event.KeySym.F1,
            scancode=tcod.event.Scancode.F1,
            mod=tcod.event.Modifier.NONE,
        )
        move_event = tcod.event.KeyDown(
            sym=tcod.event.KeySym.UP,
            scancode=tcod.event.Scancode.UP,
            mod=tcod.event.Modifier.NONE,
        )
        mock_wait.return_value = [unknown_event, move_event]

        result = handle_events()
        assert result == "move 0 -1"
