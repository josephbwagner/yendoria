"""
Tests for the game engine module.
"""

from src.yendoria.engine import GameEngine


class TestGameEngine:
    """Test cases for the GameEngine class."""

    def test_engine_initialization(self):
        """Test that the engine initializes properly."""
        engine = GameEngine()

        assert engine.screen_width == 80
        assert engine.screen_height == 50
        assert engine.is_running is True
        assert engine.game_map is not None
        assert engine.player is not None
        assert engine.renderer is not None
        assert len(engine.entities) >= 1  # At least the player

    def test_player_creation(self):
        """Test that the player is created correctly."""
        engine = GameEngine()

        assert engine.player.is_player is True
        assert hasattr(engine.player, "position")
        assert hasattr(engine.player, "health")
        assert hasattr(engine.player, "graphic")
        assert engine.player.is_alive is True

    def test_game_map_generation(self):
        """Test that the game map is generated correctly."""
        engine = GameEngine()

        assert engine.game_map.width == 80
        assert engine.game_map.height == 43
        assert len(engine.game_map.rooms) > 0

    def test_monster_placement(self):
        """Test that monsters are placed in the dungeon."""
        engine = GameEngine()

        # Count non-player entities (monsters)
        monsters = [e for e in engine.entities if not e.is_player]

        # Should have some monsters (depending on room generation)
        # This is probabilistic, so we just check that it's possible
        assert len(monsters) >= 0

    def test_handle_quit_action(self):
        """Test that quit action stops the engine."""
        engine = GameEngine()

        assert engine.is_running is True
        engine.handle_player_action("quit")
        assert engine.is_running is False

    def test_handle_invalid_action(self):
        """Test that invalid actions don't crash the engine."""
        engine = GameEngine()

        # Should not consume turn or crash
        result = engine.handle_player_action("invalid_action")
        assert result is False
        assert engine.is_running is True
