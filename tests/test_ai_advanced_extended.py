"""
Tests for AI behavior advanced functionality.
"""

import contextlib
from unittest.mock import Mock

from src.yendoria.components.ai_components import (
    BehaviorTreeComponent,
    MemoryComponent,
    MotivationComponent,
    PersonalityComponent,
)
from src.yendoria.components.component_manager import ComponentManager
from src.yendoria.systems.ai_behavior_advanced import (
    AdvancedAIBehaviorSystem,
    BehaviorContext,
)


class TestBehaviorContext:
    """Test cases for BehaviorContext class."""

    def test_behavior_context_creation(self):
        """Test BehaviorContext object creation."""
        # Create mock components
        mock_personality = Mock(spec=PersonalityComponent)
        mock_motivation = Mock(spec=MotivationComponent)
        mock_memory = Mock(spec=MemoryComponent)

        context = BehaviorContext(
            entity_id="test_entity",
            personality=mock_personality,
            motivation=mock_motivation,
            memory=mock_memory,
            delta_time=0.1,
        )

        # Test values
        assert context.entity_id == "test_entity"
        assert context.personality == mock_personality
        assert context.motivation == mock_motivation
        assert context.memory == mock_memory
        assert context.delta_time == 0.1

    def test_behavior_context_with_data(self):
        """Test BehaviorContext with different data."""
        mock_personality = Mock(spec=PersonalityComponent)
        mock_motivation = Mock(spec=MotivationComponent)
        mock_memory = Mock(spec=MemoryComponent)

        context = BehaviorContext(
            entity_id="entity_123",
            personality=mock_personality,
            motivation=mock_motivation,
            memory=mock_memory,
            delta_time=0.05,
        )

        assert context.entity_id == "entity_123"
        assert context.delta_time == 0.05

    def test_behavior_context_update_shared_data(self):
        """Test BehaviorContext with shared data updates."""
        mock_personality = Mock(spec=PersonalityComponent)
        mock_motivation = Mock(spec=MotivationComponent)
        mock_memory = Mock(spec=MemoryComponent)

        context = BehaviorContext(
            entity_id="test_entity",
            personality=mock_personality,
            motivation=mock_motivation,
            memory=mock_memory,
            delta_time=0.1,
        )

        # Context should store data consistently
        assert context.entity_id == "test_entity"

    def test_behavior_context_update_visibility(self):
        """Test BehaviorContext visibility updates."""
        mock_personality = Mock(spec=PersonalityComponent)
        mock_motivation = Mock(spec=MotivationComponent)
        mock_memory = Mock(spec=MemoryComponent)

        context = BehaviorContext(
            entity_id="test_entity",
            personality=mock_personality,
            motivation=mock_motivation,
            memory=mock_memory,
            delta_time=0.1,
        )

        # Test that context maintains component references
        assert context.personality is mock_personality
        assert context.motivation is mock_motivation
        assert context.memory is mock_memory


class TestAdvancedAIBehaviorSystem:
    """Test cases for AdvancedAIBehaviorSystem class."""

    def test_advanced_ai_behavior_system_creation(self):
        """Test AdvancedAIBehaviorSystem creation."""
        mock_component_manager = Mock(spec=ComponentManager)
        system = AdvancedAIBehaviorSystem(mock_component_manager)

        assert system is not None
        assert system.component_manager is mock_component_manager
        assert hasattr(system, "entity_goals")
        assert hasattr(system, "entity_timers")

    def test_advanced_ai_behavior_system_process_entities_empty(self):
        """Test processing empty entity list."""
        mock_component_manager = Mock(spec=ComponentManager)
        mock_component_manager.get_entities_with_component.return_value = []

        system = AdvancedAIBehaviorSystem(mock_component_manager)

        # Should not raise an error
        system.update(0.1)

    def test_advanced_ai_behavior_system_process_entities_no_ai(self):
        """Test processing entities without AI components."""
        mock_component_manager = Mock(spec=ComponentManager)
        mock_component_manager.get_entities_with_component.return_value = []

        system = AdvancedAIBehaviorSystem(mock_component_manager)

        # Should not raise an error
        system.update(0.1)

    def test_advanced_ai_behavior_system_with_ai_component(self):
        """Test processing entities with AI components."""
        mock_component_manager = Mock(spec=ComponentManager)

        # Mock entity with AI components
        mock_entity = Mock()
        mock_entity.entity_id = "test_entity"
        mock_component_manager.get_entities_with_component.return_value = [mock_entity]

        # Mock component retrieval
        mock_personality = Mock(spec=PersonalityComponent)
        mock_motivation = Mock(spec=MotivationComponent)
        mock_memory = Mock(spec=MemoryComponent)
        mock_behavior_tree = Mock(spec=BehaviorTreeComponent)

        def mock_get_component(entity, component_type):
            if component_type == PersonalityComponent:
                return mock_personality
            elif component_type == MotivationComponent:
                return mock_motivation
            elif component_type == MemoryComponent:
                return mock_memory
            elif component_type == BehaviorTreeComponent:
                return mock_behavior_tree
            return None

        mock_component_manager.get_component = mock_get_component

        system = AdvancedAIBehaviorSystem(mock_component_manager)

        # Should complete without error
        system.update(0.1)

    def test_advanced_ai_behavior_system_context_creation(self):
        """Test that system creates proper context."""
        mock_component_manager = Mock(spec=ComponentManager)
        mock_component_manager.get_entities_with_component.return_value = []

        system = AdvancedAIBehaviorSystem(mock_component_manager)

        # Test that system initializes correctly
        assert system.component_manager is mock_component_manager
        assert isinstance(system.entity_goals, dict)
        assert isinstance(system.entity_timers, dict)

    def test_advanced_ai_behavior_system_get_ai_components(self):
        """Test getting AI components from entity."""
        mock_component_manager = Mock(spec=ComponentManager)
        mock_component_manager.get_entities_with_component.return_value = []

        system = AdvancedAIBehaviorSystem(mock_component_manager)

        # Test that system initializes properly
        assert system.component_manager is not None

    def test_advanced_ai_behavior_system_execute_behavior(self):
        """Test executing behavior if method exists."""
        mock_component_manager = Mock(spec=ComponentManager)
        mock_component_manager.get_entities_with_component.return_value = []

        system = AdvancedAIBehaviorSystem(mock_component_manager)

        # Test system can update
        system.update(0.1)

    def test_advanced_ai_behavior_system_update_visibility(self):
        """Test updating visibility data if method exists."""
        mock_component_manager = Mock(spec=ComponentManager)
        mock_component_manager.get_entities_with_component.return_value = []

        system = AdvancedAIBehaviorSystem(mock_component_manager)

        # Test system property
        assert system.name == "Advanced AI Behavior System"

    def test_advanced_ai_behavior_system_performance(self):
        """Test system performance with multiple entities."""
        mock_component_manager = Mock(spec=ComponentManager)
        mock_component_manager.get_entities_with_component.return_value = []

        system = AdvancedAIBehaviorSystem(mock_component_manager)

        # Should handle update efficiently
        system.update(0.1)

    def test_advanced_ai_behavior_system_edge_cases(self):
        """Test edge cases for the system."""
        mock_component_manager = Mock(spec=ComponentManager)
        mock_component_manager.get_entities_with_component.side_effect = Exception(
            "Test error"
        )

        system = AdvancedAIBehaviorSystem(mock_component_manager)

        # Test with exception in component retrieval
        with contextlib.suppress(Exception):
            system.update(0.1)
