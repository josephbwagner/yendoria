#!/usr/bin/env python3
"""Tests for the advanced AI behavior system."""

from unittest.mock import Mock, patch

import pytest

from yendoria.components.ai_components import (
    BehaviorTreeComponent,
    MemoryComponent,
    MotivationComponent,
    PersonalityComponent,
)
from yendoria.components.component_manager import ComponentManager
from yendoria.entities.entity import Entity
from yendoria.systems.ai_behavior_advanced import (
    AdvancedAIBehaviorSystem,
    BehaviorContext,
)


class TestAdvancedAIBehaviorSystem:
    """Test suite for AdvancedAIBehaviorSystem."""

    @pytest.fixture
    def component_manager(self):
        """Create a mock component manager."""
        return Mock(spec=ComponentManager)

    @pytest.fixture
    def ai_system(self, component_manager):
        """Create an AdvancedAIBehaviorSystem instance."""
        return AdvancedAIBehaviorSystem(component_manager)

    @pytest.fixture
    def entity(self):
        """Create a test entity."""
        entity = Entity("test_entity")
        entity.id = "test_entity_id"
        return entity

    @pytest.fixture
    def personality_component(self):
        """Create a test personality component."""
        return PersonalityComponent(
            traits={
                "aggression": 0.5,
                "caution": 0.6,
                "curiosity": 0.4,
                "loyalty": 0.7,
                "intelligence": 0.3,
            }
        )

    @pytest.fixture
    def motivation_component(self):
        """Create a test motivation component."""
        component = MotivationComponent()
        # Set some test values for compatibility
        component.survival_needs = {
            "hunger": 0.5,
            "safety": 0.8,
            "health": 0.9,
            "territory": 0.3,
        }
        component.social_needs = {"companionship": 0.3, "approval": 0.6, "status": 0.4}
        return component

    @pytest.fixture
    def memory_component(self):
        """Create a test memory component."""
        return MemoryComponent(max_memories=50)

    @pytest.fixture
    def behavior_tree_component(self):
        """Create a test behavior tree component."""
        return BehaviorTreeComponent(tree_config={"root": "wander"})

    @pytest.fixture
    def complete_components(
        self,
        behavior_tree_component,
        personality_component,
        motivation_component,
        memory_component,
    ):
        """Create a complete set of AI components."""
        return {
            "behavior_tree": behavior_tree_component,
            "personality": personality_component,
            "motivation": motivation_component,
            "memory": memory_component,
        }

    def test_initialization(self, component_manager):
        """Test system initialization."""
        ai_system = AdvancedAIBehaviorSystem(component_manager)
        assert ai_system.component_manager == component_manager
        assert ai_system.name == "Advanced AI Behavior System"
        assert ai_system.entity_goals == {}
        assert ai_system.entity_timers == {}

    def test_update_with_no_entities(self, ai_system, component_manager):
        """Test update when no entities have AI components."""
        component_manager.get_entities_with_component.return_value = []

        # Should not raise any exceptions
        ai_system.update(0.1)

        component_manager.get_entities_with_component.assert_called_once_with(
            BehaviorTreeComponent
        )

    def test_update_with_exception_in_get_entities(self, ai_system, component_manager):
        """Test update handles exceptions when getting entities."""
        component_manager.get_entities_with_component.side_effect = Exception(
            "Test error"
        )

        # Should not raise any exceptions
        ai_system.update(0.1)

    def test_update_entity_behavior_missing_components(
        self, ai_system, component_manager, entity
    ):
        """Test entity behavior update with missing components."""
        # Set up entity to have behavior tree but missing other components
        component_manager.get_component.side_effect = (
            lambda entity_id, component_type: {
                BehaviorTreeComponent: BehaviorTreeComponent(
                    tree_config={"root": "test"}
                ),
                PersonalityComponent: None,
                MotivationComponent: None,
                MemoryComponent: None,
            }.get(component_type)
        )

        # Should return early without processing
        ai_system._update_entity_behavior(entity.id, 0.1)

        # Should have tried to get the behavior tree component
        assert component_manager.get_component.call_count >= 1

    def test_update_entity_behavior_complete(
        self, ai_system, component_manager, entity, complete_components
    ):
        """Test complete entity behavior update."""

        # Mock all required components
        def mock_get_component(entity_id, component_type):
            if component_type == BehaviorTreeComponent:
                return complete_components["behavior_tree"]
            elif component_type == PersonalityComponent:
                return complete_components["personality"]
            elif component_type == MotivationComponent:
                return complete_components["motivation"]
            elif component_type == MemoryComponent:
                return complete_components["memory"]
            return None

        component_manager.get_component.side_effect = mock_get_component

        # Mock the process_behavior_tree method
        with patch.object(ai_system, "_process_behavior_tree") as mock_process:
            ai_system._update_entity_behavior(entity.id, 0.1)

            # Should have called process_behavior_tree
            mock_process.assert_called_once()

            # Check that timer was initialized
            assert entity.id in ai_system.entity_timers

    def test_behavior_context_creation(
        self, personality_component, motivation_component, memory_component
    ):
        """Test BehaviorContext creation."""
        context = BehaviorContext(
            entity_id="test_id",
            personality=personality_component,
            motivation=motivation_component,
            memory=memory_component,
            delta_time=0.1,
        )

        assert context.entity_id == "test_id"
        assert context.personality == personality_component
        assert context.motivation == motivation_component
        assert context.memory == memory_component
        assert context.delta_time == 0.1

    def test_update_with_entities(
        self, ai_system, component_manager, entity, complete_components
    ):
        """Test update with valid entities."""
        # Set up entity list
        component_manager.get_entities_with_component.return_value = [entity]

        # Mock component retrieval
        def mock_get_component(entity_id, component_type):
            if component_type == BehaviorTreeComponent:
                return complete_components["behavior_tree"]
            elif component_type == PersonalityComponent:
                return complete_components["personality"]
            elif component_type == MotivationComponent:
                return complete_components["motivation"]
            elif component_type == MemoryComponent:
                return complete_components["memory"]
            return None

        component_manager.get_component.side_effect = mock_get_component

        # Mock the process_behavior_tree method
        with patch.object(ai_system, "_process_behavior_tree"):
            ai_system.update(0.1)

            # Should have retrieved entities
            component_manager.get_entities_with_component.assert_called_once_with(
                BehaviorTreeComponent
            )

    def test_update_entity_behavior_with_exception(
        self, ai_system, component_manager, entity
    ):
        """Test entity behavior update handles exceptions gracefully."""
        # Make get_component raise an exception
        component_manager.get_component.side_effect = Exception("Component error")

        # The _update_entity_behavior method doesn't handle exceptions,
        # so we expect it to propagate
        with pytest.raises(Exception, match="Component error"):
            ai_system._update_entity_behavior(entity.id, 0.1)

    def test_update_with_entity_no_id(self, ai_system, component_manager):
        """Test update with entity that has no ID."""
        entity_no_id = Entity("no_id_entity")
        entity_no_id.id = None

        component_manager.get_entities_with_component.return_value = [entity_no_id]

        # Should handle gracefully
        ai_system.update(0.1)

    def test_entity_timers_initialization(
        self, ai_system, component_manager, entity, complete_components
    ):
        """Test that entity timers are properly initialized."""

        def mock_get_component(entity_id, component_type):
            if component_type == BehaviorTreeComponent:
                return complete_components["behavior_tree"]
            elif component_type == PersonalityComponent:
                return complete_components["personality"]
            elif component_type == MotivationComponent:
                return complete_components["motivation"]
            elif component_type == MemoryComponent:
                return complete_components["memory"]
            return None

        component_manager.get_component.side_effect = mock_get_component

        # Mock the process_behavior_tree method
        with patch.object(ai_system, "_process_behavior_tree"):
            # Entity should not be in timers initially
            assert entity.id not in ai_system.entity_timers

            # Update behavior
            ai_system._update_entity_behavior(entity.id, 0.1)

            # Entity should now be in timers
            assert entity.id in ai_system.entity_timers
            assert isinstance(ai_system.entity_timers[entity.id], dict)


class TestBehaviorContext:
    """Test suite for BehaviorContext dataclass."""

    def test_behavior_context_attributes(self):
        """Test BehaviorContext has all required attributes."""
        personality = Mock(spec=PersonalityComponent)
        motivation = Mock(spec=MotivationComponent)
        memory = Mock(spec=MemoryComponent)

        context = BehaviorContext(
            entity_id="test_id",
            personality=personality,
            motivation=motivation,
            memory=memory,
            delta_time=0.5,
        )

        assert hasattr(context, "entity_id")
        assert hasattr(context, "personality")
        assert hasattr(context, "motivation")
        assert hasattr(context, "memory")
        assert hasattr(context, "delta_time")

    def test_behavior_context_values(self):
        """Test BehaviorContext stores correct values."""
        personality = Mock(spec=PersonalityComponent)
        motivation = Mock(spec=MotivationComponent)
        memory = Mock(spec=MemoryComponent)

        context = BehaviorContext(
            entity_id="unique_id",
            personality=personality,
            motivation=motivation,
            memory=memory,
            delta_time=1.5,
        )

        assert context.entity_id == "unique_id"
        assert context.personality is personality
        assert context.motivation is motivation
        assert context.memory is memory
        assert context.delta_time == 1.5
