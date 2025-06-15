#!/usr/bin/env python3
"""Additional tests for the game engine."""

from unittest.mock import Mock, patch

import pytest

from yendoria.engine import GameEngine


class TestGameEngineAdditional:
    """Additional test suite for GameEngine."""

    @pytest.fixture
    def headless_engine(self):
        """Create a headless game engine for testing."""
        return GameEngine(headless=True)

    @pytest.fixture
    def normal_engine(self):
        """Create a normal game engine for testing."""
        with patch("yendoria.engine.tcod.context.new"):
            return GameEngine(headless=False)

    def test_engine_initialization_headless(self, headless_engine):
        """Test engine initialization in headless mode."""
        assert headless_engine.headless is True
        assert headless_engine.context is None
        assert headless_engine.is_running is True
        assert headless_engine.entities is not None
        assert hasattr(headless_engine, "game_map")
        assert hasattr(headless_engine, "player")

    def test_engine_initialization_normal(self, normal_engine):
        """Test engine initialization in normal mode."""
        assert normal_engine.headless is False
        assert normal_engine.is_running is True
        assert hasattr(normal_engine, "entities")
        assert hasattr(normal_engine, "game_map")
        assert hasattr(normal_engine, "player")

    def test_handle_events_empty_list(self, headless_engine):
        """Test handling empty event list."""
        with patch("yendoria.engine.handle_events", return_value=None):
            result = headless_engine.handle_events()
            assert result is False

    def test_handle_events_quit_action(self, headless_engine):
        """Test handling quit action."""
        with (
            patch("yendoria.engine.handle_events", return_value="quit"),
            patch.object(
                headless_engine, "handle_player_action", return_value=True
            ) as mock_handle,
        ):
            result = headless_engine.handle_events()
            mock_handle.assert_called_once_with("quit")
            assert result is True

    def test_handle_events_invalid_action(self, headless_engine):
        """Test handling invalid action."""
        with (
            patch("yendoria.engine.handle_events", return_value="invalid"),
            patch.object(
                headless_engine, "handle_player_action", return_value=False
            ) as mock_handle,
        ):
            result = headless_engine.handle_events()
            mock_handle.assert_called_once_with("invalid")
            assert result is False

    def test_render_normal_mode(self, normal_engine):
        """Test rendering in normal mode."""
        with (
            patch.object(normal_engine.renderer, "render_all") as mock_render,
            patch.object(normal_engine.renderer, "present") as mock_present,
        ):
            normal_engine.render()
            mock_render.assert_called_once_with(
                normal_engine.game_map, normal_engine.entities, normal_engine.player
            )
            mock_present.assert_called_once()

    def test_render_headless_mode(self, headless_engine):
        """Test rendering in headless mode."""
        # Should not raise any exceptions
        headless_engine.render()

    def test_engine_with_ai_integration_disabled(self, headless_engine):
        """Test engine behavior when AI integration is disabled."""
        # Check that ai_integration exists
        assert hasattr(headless_engine, "ai_integration")
        assert headless_engine.ai_integration is not None

    def test_update_monsters_with_ai_integration(self, headless_engine):
        """Test monster updates with AI integration enabled."""
        # Create a mock monster with AI
        mock_monster = Mock()
        mock_monster.ai = Mock()
        headless_engine.entities = [headless_engine.player, mock_monster]

        with patch.object(
            headless_engine.ai_integration, "update_ai_systems", return_value=None
        ) as mock_update:
            headless_engine.update_monsters()
            # AI integration should be updated
            mock_update.assert_called_once()

    def test_update_monsters_without_ai_integration(self, headless_engine):
        """Test monster updates without AI integration."""
        # Temporarily disable AI integration
        original_ai = headless_engine.ai_integration
        headless_engine.ai_integration = None

        try:
            # Should not raise an exception
            headless_engine.update_monsters()
        finally:
            # Restore AI integration
            headless_engine.ai_integration = original_ai

    def test_place_monsters_in_rooms(self, headless_engine):
        """Test placing monsters in generated rooms."""
        # Check that game map has rooms after setup
        assert hasattr(headless_engine.game_map, "rooms")

        # Check that some entities exist (player + potentially monsters)
        assert len(headless_engine.entities) >= 1  # At least the player

    def test_error_handling_in_monster_updates(self, headless_engine):
        """Test error handling during monster updates."""
        # Create a mock monster that raises an exception
        mock_monster = Mock()
        mock_monster.ai.perform.side_effect = Exception("Test error")
        headless_engine.entities = [headless_engine.player, mock_monster]

        # Mock the AI integration to avoid errors
        with patch.object(headless_engine.ai_integration, "update_ai_systems"):
            # Should not raise the exception
            headless_engine.update_monsters()

    def test_update_fov(self, headless_engine):
        """Test field of view updates."""
        # Should not raise any exceptions
        headless_engine.update_fov()

    def test_player_action_handling(self, headless_engine):
        """Test basic player action handling."""
        # Test with a valid movement action
        result = headless_engine.handle_player_action("move_up")
        assert isinstance(result, bool)

    def test_game_state_update(self, headless_engine):
        """Test game state update."""
        # Should not raise any exceptions
        headless_engine.update()

    def test_engine_stop(self, headless_engine):
        """Test stopping the engine."""
        headless_engine.stop()
        assert headless_engine.is_running is False

    def test_combat_system_integration(self, headless_engine):
        """Test combat system integration."""
        # Create a mock monster for combat testing
        mock_monster = Mock()
        mock_monster.position = Mock()
        mock_monster.position.x = 1
        mock_monster.position.y = 1
        mock_monster.is_alive = True

        # Position player near monster
        headless_engine.player.position.x = 0
        headless_engine.player.position.y = 1

        # Test that combat handling exists
        assert hasattr(headless_engine, "_handle_combat")

    def test_event_bus_integration(self, headless_engine):
        """Test event bus integration for modding."""
        assert hasattr(headless_engine, "event_bus")
        assert headless_engine.event_bus is not None

    def test_renderer_integration(self, headless_engine):
        """Test renderer integration."""
        assert hasattr(headless_engine, "renderer")
        assert headless_engine.renderer is not None

    def test_game_map_generation(self, headless_engine):
        """Test that game map is properly generated."""
        assert headless_engine.game_map is not None
        assert hasattr(headless_engine.game_map, "width")
        assert hasattr(headless_engine.game_map, "height")
        assert headless_engine.game_map.width > 0
        assert headless_engine.game_map.height > 0

    def test_player_creation(self, headless_engine):
        """Test that player is properly created."""
        assert headless_engine.player is not None
        assert hasattr(headless_engine.player, "position")
        assert hasattr(headless_engine.player, "is_alive")
        assert headless_engine.player.is_alive

    def test_entity_management(self, headless_engine):
        """Test entity management."""
        initial_count = len(headless_engine.entities)
        assert initial_count >= 1  # At least the player

        # Player should be in entities
        assert headless_engine.player in headless_engine.entities
