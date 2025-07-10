"""
Tests for component system functionality.
"""

from unittest.mock import Mock

from src.yendoria.components.component import (
    AI,
    BasicMonsterAI,
    Component,
    Damage,
    Graphic,
    Health,
    Position,
)
from src.yendoria.entities.entity import Entity


class TestComponent:
    """Test cases for base Component class."""

    def test_component_creation(self):
        """Test basic component creation."""
        component = Component()

        assert component.entity is None

    def test_component_with_entity(self):
        """Test component creation with entity."""
        entity = Entity("Test")
        component = Component(entity)

        assert component.entity is entity


class TestPositionComponent:
    """Test cases for Position component."""

    def test_position_creation(self):
        """Test position component creation."""
        position = Position(5, 10)

        assert position.x == 5
        assert position.y == 10
        assert position.entity is None

    def test_position_with_entity(self):
        """Test position component with entity."""
        entity = Entity("Test")
        position = Position(5, 10, entity)

        assert position.x == 5
        assert position.y == 10
        assert position.entity is entity

    def test_position_move(self):
        """Test position movement."""
        position = Position(5, 10)

        position.move(2, -3)

        assert position.x == 7
        assert position.y == 7

    def test_position_move_zero(self):
        """Test position movement with zero displacement."""
        position = Position(5, 10)

        position.move(0, 0)

        assert position.x == 5
        assert position.y == 10

    def test_position_move_negative(self):
        """Test position movement with negative values."""
        position = Position(5, 10)

        position.move(-3, -5)

        assert position.x == 2
        assert position.y == 5


class TestHealthComponent:
    """Test cases for Health component."""

    def test_health_creation(self):
        """Test health component creation."""
        health = Health(50)

        assert health.max_hp == 50
        assert health.current_hp == 50
        assert health.is_alive is True

    def test_health_with_entity(self):
        """Test health component with entity."""
        entity = Entity("Test")
        health = Health(50, entity)

        assert health.max_hp == 50
        assert health.current_hp == 50
        assert health.entity is entity

    def test_health_take_damage(self):
        """Test taking damage."""
        health = Health(50)

        damage_dealt = health.take_damage(20)

        assert damage_dealt == 20
        assert health.current_hp == 30
        assert health.is_alive is True

    def test_health_take_fatal_damage(self):
        """Test taking fatal damage."""
        health = Health(50)

        damage_dealt = health.take_damage(60)  # More than max hp

        assert damage_dealt == 50  # Only dealt what hp was available
        assert health.current_hp == 0
        assert health.is_alive is False

    def test_health_take_zero_damage(self):
        """Test taking zero damage."""
        health = Health(50)

        damage_dealt = health.take_damage(0)

        assert damage_dealt == 0
        assert health.current_hp == 50
        assert health.is_alive is True

    def test_health_heal(self):
        """Test healing."""
        health = Health(50)
        health.current_hp = 30  # Set to damaged state

        healing_done = health.heal(15)

        assert healing_done == 15
        assert health.current_hp == 45
        assert health.is_alive is True

    def test_health_heal_beyond_max(self):
        """Test healing beyond max HP."""
        health = Health(50)
        health.current_hp = 30  # Set to damaged state

        healing_done = health.heal(30)  # More than needed

        assert healing_done == 20  # Only healed what was needed
        assert health.current_hp == 50
        assert health.is_alive is True

    def test_health_heal_at_max(self):
        """Test healing when already at max HP."""
        health = Health(50)

        healing_done = health.heal(10)

        assert healing_done == 0
        assert health.current_hp == 50
        assert health.is_alive is True

    def test_health_heal_zero(self):
        """Test healing with zero amount."""
        health = Health(50)
        health.current_hp = 30

        healing_done = health.heal(0)

        assert healing_done == 0
        assert health.current_hp == 30
        assert health.is_alive is True


class TestGraphicComponent:
    """Test cases for Graphic component."""

    def test_graphic_creation(self):
        """Test graphic component creation."""
        graphic = Graphic(64, (255, 255, 255))  # '@' character, white

        assert graphic.char == 64
        assert graphic.color == (255, 255, 255)
        assert graphic.entity is None

    def test_graphic_with_entity(self):
        """Test graphic component with entity."""
        entity = Entity("Test")
        graphic = Graphic(64, (255, 0, 0), entity)  # '@' character, red

        assert graphic.char == 64
        assert graphic.color == (255, 0, 0)
        assert graphic.entity is entity

    def test_graphic_different_colors(self):
        """Test graphic component with different colors."""
        graphic1 = Graphic(64, (255, 255, 255))
        graphic2 = Graphic(64, (0, 255, 0))
        graphic3 = Graphic(64, (0, 0, 255))

        assert graphic1.color == (255, 255, 255)
        assert graphic2.color == (0, 255, 0)
        assert graphic3.color == (0, 0, 255)

    def test_graphic_different_chars(self):
        """Test graphic component with different characters."""
        graphic1 = Graphic(64, (255, 255, 255))  # '@'
        graphic2 = Graphic(111, (255, 255, 255))  # 'o'
        graphic3 = Graphic(84, (255, 255, 255))  # 'T'

        assert graphic1.char == 64
        assert graphic2.char == 111
        assert graphic3.char == 84


class TestAIComponent:
    """Test cases for AI component."""

    def test_ai_creation(self):
        """Test AI component creation."""
        ai = AI()

        assert ai.entity is None

    def test_ai_with_entity(self):
        """Test AI component with entity."""
        entity = Entity("Test")
        ai = AI(entity)

        assert ai.entity is entity

    def test_ai_perform_base(self):
        """Test base AI perform method (should do nothing)."""
        ai = AI()
        game_map = Mock()
        entities = []

        # Should not raise an error
        ai.perform(game_map, entities)


class TestBasicMonsterAI:
    """Test cases for BasicMonsterAI component."""

    def test_basic_monster_ai_creation(self):
        """Test BasicMonsterAI creation."""
        ai = BasicMonsterAI()

        assert isinstance(ai, AI)
        assert ai.entity is None

    def test_basic_monster_ai_no_entity(self):
        """Test BasicMonsterAI with no entity."""
        ai = BasicMonsterAI()
        game_map = Mock()
        entities = []

        # Should not raise an error
        ai.perform(game_map, entities)

    def test_basic_monster_ai_no_position(self):
        """Test BasicMonsterAI with entity without position."""
        entity = Entity("Monster")
        ai = BasicMonsterAI(entity)
        game_map = Mock()
        entities = []

        # Should not raise an error
        ai.perform(game_map, entities)

    def test_basic_monster_ai_no_player(self):
        """Test BasicMonsterAI with no player in entities."""
        entity = Entity("Monster")
        entity.add_component(Position(5, 5))
        ai = BasicMonsterAI(entity)

        game_map = Mock()
        game_map.visible = {(5, 5): True}
        entities = [entity]

        # Should not raise an error
        ai.perform(game_map, entities)

    def test_basic_monster_ai_player_no_position(self):
        """Test BasicMonsterAI with player without position."""
        monster = Entity("Monster")
        monster.add_component(Position(5, 5))
        ai = BasicMonsterAI(monster)

        player = Entity("Player", is_player=True)
        # No position component

        game_map = Mock()
        game_map.visible = {(5, 5): True}
        entities = [monster, player]

        # Should not raise an error
        ai.perform(game_map, entities)

    def test_basic_monster_ai_not_visible(self):
        """Test BasicMonsterAI when monster is not visible."""
        monster = Entity("Monster")
        monster.add_component(Position(5, 5))
        ai = BasicMonsterAI(monster)

        player = Entity("Player", is_player=True)
        player.add_component(Position(10, 10))

        game_map = Mock()
        game_map.visible = {(5, 5): False}  # Monster not visible
        entities = [monster, player]

        # Should not move
        ai.perform(game_map, entities)

        assert monster.position.x == 5
        assert monster.position.y == 5


class TestDamageComponent:
    """Test cases for Damage component."""

    def test_damage_creation(self):
        """Test damage component creation."""
        damage = Damage(10)

        assert damage.amount == 10
        assert damage.entity is None

    def test_damage_with_entity(self):
        """Test damage component with entity."""
        entity = Entity("Test")
        damage = Damage(15, entity)

        assert damage.amount == 15
        assert damage.entity is entity

    def test_damage_different_amounts(self):
        """Test damage component with different amounts."""
        damage1 = Damage(5)
        damage2 = Damage(10)
        damage3 = Damage(20)

        assert damage1.amount == 5
        assert damage2.amount == 10
        assert damage3.amount == 20

    def test_damage_zero(self):
        """Test damage component with zero damage."""
        damage = Damage(0)

        assert damage.amount == 0
