"""
Tests for player entity functionality.
"""

from unittest.mock import Mock

from src.yendoria.components.component import Graphic, Health, Position
from src.yendoria.entities.entity import Entity
from src.yendoria.entities.player import create_player, move_player
from src.yendoria.utils.constants import CHAR_PLAYER, COLOR_WHITE


class TestPlayerCreation:
    """Test cases for player creation."""

    def test_create_player_basic(self):
        """Test basic player creation."""
        player = create_player(5, 10)

        assert isinstance(player, Entity)
        assert player.name == "Player"
        assert player.is_player is True

    def test_create_player_components(self):
        """Test that player has correct components."""
        player = create_player(5, 10)

        # Check position component
        assert hasattr(player, "position")
        assert isinstance(player.position, Position)
        assert player.position.x == 5
        assert player.position.y == 10

        # Check health component
        assert hasattr(player, "health")
        assert isinstance(player.health, Health)
        assert player.health.max_hp == 30
        assert player.health.current_hp == 30

        # Check graphic component
        assert hasattr(player, "graphic")
        assert isinstance(player.graphic, Graphic)
        assert player.graphic.char == CHAR_PLAYER
        assert player.graphic.color == COLOR_WHITE

    def test_create_player_different_positions(self):
        """Test player creation at different positions."""
        player1 = create_player(0, 0)
        player2 = create_player(100, 200)

        assert player1.position.x == 0
        assert player1.position.y == 0
        assert player2.position.x == 100
        assert player2.position.y == 200


class TestPlayerMovement:
    """Test cases for player movement."""

    def test_move_player_success(self):
        """Test successful player movement."""
        player = create_player(5, 5)

        # Mock game map
        game_map = Mock()
        game_map.is_walkable.return_value = True

        # Test movement
        result = move_player(player, 1, 0, game_map)

        assert result is True
        assert player.position.x == 6
        assert player.position.y == 5
        game_map.is_walkable.assert_called_once_with(6, 5)

    def test_move_player_blocked(self):
        """Test blocked player movement."""
        player = create_player(5, 5)

        # Mock game map with blocked tile
        game_map = Mock()
        game_map.is_walkable.return_value = False

        # Test movement
        result = move_player(player, 1, 0, game_map)

        assert result is False
        assert player.position.x == 5  # Should not move
        assert player.position.y == 5
        game_map.is_walkable.assert_called_once_with(6, 5)

    def test_move_player_no_position(self):
        """Test movement with player without position component."""
        player = Entity("Test")  # No position component

        game_map = Mock()

        result = move_player(player, 1, 0, game_map)

        assert result is False
        game_map.is_walkable.assert_not_called()

    def test_move_player_multiple_directions(self):
        """Test player movement in multiple directions."""
        player = create_player(10, 10)

        game_map = Mock()
        game_map.is_walkable.return_value = True

        # Test all directions
        directions = [
            (0, -1),  # North
            (1, 0),  # East
            (0, 1),  # South
            (-1, 0),  # West
            (1, 1),  # Southeast
            (-1, -1),  # Northwest
        ]

        for dx, dy in directions:
            initial_x, initial_y = player.position.x, player.position.y
            result = move_player(player, dx, dy, game_map)

            assert result is True
            assert player.position.x == initial_x + dx
            assert player.position.y == initial_y + dy

    def test_move_player_boundaries(self):
        """Test movement at map boundaries."""
        player = create_player(0, 0)

        game_map = Mock()
        game_map.is_walkable.return_value = False  # Simulate boundary

        # Try to move outside boundary
        result = move_player(player, -1, -1, game_map)

        assert result is False
        assert player.position.x == 0
        assert player.position.y == 0
        game_map.is_walkable.assert_called_once_with(-1, -1)

    def test_move_player_zero_movement(self):
        """Test movement with zero displacement."""
        player = create_player(5, 5)

        game_map = Mock()
        game_map.is_walkable.return_value = True

        result = move_player(player, 0, 0, game_map)

        assert result is True
        assert player.position.x == 5
        assert player.position.y == 5
        game_map.is_walkable.assert_called_once_with(5, 5)


class TestPlayerHealth:
    """Test cases for player health mechanics."""

    def test_player_health_initialization(self):
        """Test that player starts with full health."""
        player = create_player(0, 0)

        assert player.health.current_hp == 30
        assert player.health.max_hp == 30
        assert player.health.is_alive is True

    def test_player_take_damage(self):
        """Test player taking damage."""
        player = create_player(0, 0)

        damage_dealt = player.health.take_damage(10)

        assert damage_dealt == 10
        assert player.health.current_hp == 20
        assert player.health.is_alive is True

    def test_player_death(self):
        """Test player death from damage."""
        player = create_player(0, 0)

        damage_dealt = player.health.take_damage(50)  # More than max hp

        assert damage_dealt == 30  # Only dealt what hp was available
        assert player.health.current_hp == 0
        assert player.health.is_alive is False

    def test_player_healing(self):
        """Test player healing."""
        player = create_player(0, 0)

        # Take damage first
        player.health.take_damage(15)
        assert player.health.current_hp == 15

        # Heal
        healing_done = player.health.heal(10)

        assert healing_done == 10
        assert player.health.current_hp == 25
        assert player.health.is_alive is True

    def test_player_heal_beyond_max(self):
        """Test healing beyond max HP."""
        player = create_player(0, 0)

        # Take small damage
        player.health.take_damage(5)
        assert player.health.current_hp == 25

        # Try to heal more than needed
        healing_done = player.health.heal(20)

        assert healing_done == 5  # Only healed what was needed
        assert player.health.current_hp == 30
        assert player.health.is_alive is True
