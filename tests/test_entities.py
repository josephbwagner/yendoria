"""
Tests for the entity system.
"""

from src.yendoria.components.component import Health, Position
from src.yendoria.entities.entity import Entity
from src.yendoria.entities.monster import create_orc, create_troll
from src.yendoria.entities.player import create_player


class TestEntity:
    """Test cases for the Entity class."""

    def test_entity_creation(self):
        """Test basic entity creation."""
        entity = Entity("Test Entity")

        assert entity.name == "Test Entity"
        assert entity.is_player is False
        assert entity.is_alive is True  # No health component

    def test_component_system(self):
        """Test adding and accessing components."""
        entity = Entity("Test")
        position = Position(5, 10)

        entity.add_component(position)

        assert hasattr(entity, "position")
        assert entity.position.x == 5
        assert entity.position.y == 10
        assert entity.has_component("position")
        assert entity.get_component("position") is position

    def test_component_removal(self):
        """Test removing components."""
        entity = Entity("Test")
        position = Position(0, 0)

        entity.add_component(position)
        assert entity.has_component("position")

        entity.remove_component("position")
        assert not entity.has_component("position")
        assert not hasattr(entity, "position")


class TestPlayer:
    """Test cases for player creation and behavior."""

    def test_player_creation(self):
        """Test player entity creation."""
        player = create_player(10, 15)

        assert player.is_player is True
        assert player.name == "Player"
        assert hasattr(player, "position")
        assert hasattr(player, "health")
        assert hasattr(player, "graphic")

        assert player.position.x == 10
        assert player.position.y == 15
        assert player.health.max_hp == 30
        assert player.health.current_hp == 30
        assert player.is_alive is True


class TestMonsters:
    """Test cases for monster creation."""

    def test_orc_creation(self):
        """Test orc monster creation."""
        orc = create_orc(5, 8)

        assert orc.name == "Orc"
        assert orc.is_player is False
        assert hasattr(orc, "position")
        assert hasattr(orc, "health")
        assert hasattr(orc, "graphic")
        assert hasattr(orc, "basicmonsterai")

        assert orc.position.x == 5
        assert orc.position.y == 8
        assert orc.health.max_hp == 10
        assert hasattr(orc, "damage")
        assert orc.damage.amount == 3

    def test_troll_creation(self):
        """Test troll monster creation."""
        troll = create_troll(3, 7)

        assert troll.name == "Troll"
        assert troll.is_player is False
        assert hasattr(troll, "position")
        assert hasattr(troll, "health")
        assert hasattr(troll, "graphic")
        assert hasattr(troll, "basicmonsterai")

        assert troll.position.x == 3
        assert troll.position.y == 7
        assert troll.health.max_hp == 16
        assert hasattr(troll, "damage")
        assert troll.damage.amount == 4


class TestComponents:
    """Test cases for individual components."""

    def test_position_component(self):
        """Test position component functionality."""
        pos = Position(10, 20)

        assert pos.x == 10
        assert pos.y == 20

        pos.move(5, -3)
        assert pos.x == 15
        assert pos.y == 17

    def test_health_component(self):
        """Test health component functionality."""
        health = Health(20)

        assert health.max_hp == 20
        assert health.current_hp == 20
        assert health.is_alive is True

        # Test damage
        damage_dealt = health.take_damage(5)
        assert damage_dealt == 5
        assert health.current_hp == 15
        assert health.is_alive is True

        # Test healing
        healing_done = health.heal(3)
        assert healing_done == 3
        assert health.current_hp == 18

        # Test fatal damage
        health.take_damage(20)
        assert health.current_hp == 0
        assert health.is_alive is False

    def test_health_component_edge_cases(self):
        """Test health component edge cases."""
        health = Health(10)

        # Test over-healing
        health.current_hp = 8
        healing_done = health.heal(5)
        assert healing_done == 2  # Can only heal to max
        assert health.current_hp == 10

        # Test over-damage
        damage_dealt = health.take_damage(15)
        assert damage_dealt == 10  # Can only deal current HP
        assert health.current_hp == 0
