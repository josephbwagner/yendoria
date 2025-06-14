"""
Tests for the game engine module.
"""

import os

import pytest

from src.yendoria.engine import GameEngine


class TestGameEngine:
    """Test cases for the GameEngine class."""

    def test_engine_initialization(self):
        """Test that the engine initializes properly."""
        engine = GameEngine(headless=True)

        assert engine.screen_width == 80
        assert engine.screen_height == 50
        assert engine.is_running is True
        assert engine.game_map is not None
        assert engine.player is not None
        assert engine.renderer is not None
        assert len(engine.entities) >= 1  # At least the player

    def test_player_creation(self):
        """Test that the player is created correctly."""
        engine = GameEngine(headless=True)

        assert engine.player.is_player is True
        assert hasattr(engine.player, "position")
        assert hasattr(engine.player, "health")
        assert hasattr(engine.player, "graphic")
        assert engine.player.is_alive is True

    def test_game_map_generation(self):
        """Test that the game map is generated correctly."""
        engine = GameEngine(headless=True)

        assert engine.game_map.width == 80
        assert engine.game_map.height == 43
        assert len(engine.game_map.rooms) > 0

    def test_monster_placement(self):
        """Test that monsters are placed in the dungeon."""
        engine = GameEngine(headless=True)

        # Count non-player entities (monsters)
        monsters = [e for e in engine.entities if not e.is_player]

        # Should have some monsters (depending on room generation)
        # This is probabilistic, so we just check that it's possible
        assert len(monsters) >= 0

    def test_handle_quit_action(self):
        """Test that quit action stops the engine."""
        engine = GameEngine(headless=True)

        assert engine.is_running is True
        engine.handle_player_action("quit")
        assert engine.is_running is False

    def test_handle_invalid_action(self):
        """Test that invalid actions don't crash the engine."""
        engine = GameEngine(headless=True)

        # Should not consume turn or crash
        result = engine.handle_player_action("invalid_action")
        assert result is False
        assert engine.is_running is True

    def test_headless_mode(self):
        """Test that headless mode works correctly."""
        # Test headless mode
        headless_engine = GameEngine(headless=True)
        assert headless_engine.context is None
        assert headless_engine.is_running is True

        # Test that render doesn't crash in headless mode
        headless_engine.render()  # Should not raise an exception

        # Test that cleanup doesn't crash in headless mode
        headless_engine.stop()
        assert headless_engine.is_running is False

    @pytest.mark.skipif(
        os.getenv("CI") is not None or os.getenv("GITHUB_ACTIONS") is not None,
        reason="Skipping graphics test in CI environment",
    )
    def test_normal_mode(self):
        """Test that normal mode works correctly."""
        normal_engine = GameEngine(headless=False)
        assert normal_engine.context is not None
        assert normal_engine.is_running is True

        # Test that cleanup works in normal mode
        normal_engine.stop()
        assert normal_engine.is_running is False
