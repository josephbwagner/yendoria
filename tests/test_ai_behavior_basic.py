#!/usr/bin/env python3
"""Tests for the basic AI behavior system."""

from unittest.mock import Mock, patch

import pytest

from yendoria.components.ai_components import BehaviorTreeComponent
from yendoria.components.ai_events import AIEvent, AIEventType
from yendoria.components.component_manager import ComponentManager
from yendoria.entities.entity import Entity
from yendoria.systems.ai_behavior_basic import BasicAIBehaviorSystem


class TestBasicAIBehaviorSystem:
    """Test suite for BasicAIBehaviorSystem."""

    @pytest.fixture
    def component_manager(self):
        """Create a mock component manager."""
        return Mock(spec=ComponentManager)

    @pytest.fixture
    def ai_system(self, component_manager):
        """Create a BasicAIBehaviorSystem instance."""
        return BasicAIBehaviorSystem(component_manager)

    @pytest.fixture
    def entity(self):
        """Create a test entity."""
        entity = Entity("basic_entity")
        entity.id = "basic_entity_id"  # Set the id property
        return entity

    @pytest.fixture
    def behavior_tree_component(self):
        """Create a test behavior tree component."""
        return BehaviorTreeComponent(tree_config={"root": "wander"})

    def test_initialization(self, component_manager):
        """Test system initialization."""
        ai_system = BasicAIBehaviorSystem(component_manager)
        assert ai_system.component_manager == component_manager
        assert ai_system.entity_timers == {}

    def test_name_property(self, ai_system):
        """Test the name property."""
        assert ai_system.name == "Basic AI Behavior System"

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

        # Should not raise any exceptions due to error handler
        ai_system.update(0.1)

    def test_update_with_valid_entity(
        self, ai_system, component_manager, entity, behavior_tree_component
    ):
        """Test update with a valid entity."""
        # Set up entity list
        component_manager.get_entities_with_component.return_value = [entity]

        # Mock component retrieval
        component_manager.get_component.return_value = behavior_tree_component

        # Mock the _update_entity_behavior method
        with patch.object(ai_system, "_update_entity_behavior") as mock_update:
            ai_system.update(0.1)

            # Should have called _update_entity_behavior for the entity
            mock_update.assert_called_once_with(entity.id, 0.1)

    def test_update_entity_behavior_no_component(
        self, ai_system, component_manager, entity
    ):
        """Test entity behavior update when entity has no behavior component."""
        component_manager.get_component.return_value = None

        # Should return early without processing
        ai_system._update_entity_behavior(entity.id, 0.1)

        # Should have tried to get the behavior tree component
        component_manager.get_component.assert_called_once_with(
            entity.id, BehaviorTreeComponent
        )

    def test_update_entity_behavior_with_component(
        self, ai_system, component_manager, entity, behavior_tree_component
    ):
        """Test entity behavior update with valid component."""
        component_manager.get_component.return_value = behavior_tree_component

        # Set initial timer to trigger action selection
        ai_system.entity_timers[entity.id] = 1.5  # Greater than 1.0 to trigger action

        with patch.object(
            ai_system, "_choose_action", return_value="wander"
        ) as mock_choose:
            ai_system._update_entity_behavior(entity.id, 0.1)

            # Should have called _choose_action
            mock_choose.assert_called_once_with(entity.id)
            # Should have set the action on the behavior tree
            assert behavior_tree_component.current_action == "wander"
            # Should have updated entity timer
            assert entity.id in ai_system.entity_timers

    def test_entity_timer_initialization(
        self, ai_system, component_manager, entity, behavior_tree_component
    ):
        """Test that entity timers are properly initialized."""
        component_manager.get_component.return_value = behavior_tree_component

        # Entity should not have timer initially
        assert entity.id not in ai_system.entity_timers

        # After update, timer should be initialized
        ai_system._update_entity_behavior(entity.id, 0.1)
        assert entity.id in ai_system.entity_timers
        assert ai_system.entity_timers[entity.id] == 0.1

    def test_choose_action_returns_valid_action(self, ai_system):
        """Test that _choose_action returns a valid action."""
        entity_id = "test_entity"
        action = ai_system._choose_action(entity_id)

        # Should return one of the predefined actions
        valid_actions = ["wander", "patrol", "rest", "seek_food", "guard"]
        assert action in valid_actions

    def test_update_with_entity_no_id(self, ai_system, component_manager):
        """Test update with entity that has no ID."""
        entity_no_id = Entity("no_id_entity")
        entity_no_id.id = None

        component_manager.get_entities_with_component.return_value = [entity_no_id]

        # Should not raise any exceptions
        ai_system.update(0.1)

    def test_handle_event_reputation_changed(self, ai_system):
        """Test handling reputation change events."""
        event = AIEvent(
            event_type=AIEventType.REPUTATION_CHANGED,
            data={"entity_id": "test_entity", "faction": "guards", "change": 10},
        )

        # Should not raise any exceptions
        ai_system.handle_event(event)

    def test_handle_event_conflict_started(self, ai_system):
        """Test handling conflict start events."""
        event = AIEvent(
            event_type=AIEventType.CONFLICT_STARTED,
            data={
                "entity_id": "test_entity",
                "target": "player",
                "reason": "aggression",
            },
        )

        # Should not raise any exceptions
        ai_system.handle_event(event)

    def test_handle_event_faction_relationship_changed(self, ai_system):
        """Test handling faction relationship change events."""
        event = AIEvent(
            event_type=AIEventType.FACTION_RELATIONSHIP_CHANGED,
            data={
                "entity_id": "test_entity",
                "faction1": "guards",
                "faction2": "thieves",
                "new_status": "hostile",
            },
        )

        # Should not raise any exceptions
        ai_system.handle_event(event)

    def test_get_performance_stats(self, ai_system):
        """Test getting performance statistics."""
        # Add some entities to timers
        ai_system.entity_timers["entity1"] = 1.0
        ai_system.entity_timers["entity2"] = 2.0

        stats = ai_system.get_performance_stats()

        assert stats["entities_tracked"] == 2
        assert stats["system_type"] == "basic"
        assert "timer_based_updates" in stats["features"]

    def test_update_metrics_recording(self, ai_system, component_manager, entity):
        """Test that metrics are properly recorded during updates."""
        component_manager.get_entities_with_component.return_value = [entity]
        component_manager.get_component.return_value = None

        with patch("yendoria.systems.ai_behavior_basic.get_ai_metrics") as mock_metrics:
            mock_timer = Mock()
            mock_timer.__enter__ = Mock(return_value=mock_timer)
            mock_timer.__exit__ = Mock(return_value=False)
            mock_metrics.return_value.operation_timer.return_value = mock_timer

            ai_system.update(0.1)

            # Should have used the operation timer
            mock_metrics.return_value.operation_timer.assert_called_once_with(
                "simple_behavior_update"
            )

    def test_shutdown(self, ai_system):
        """Test system shutdown."""
        # Add some timers
        ai_system.entity_timers["entity1"] = 1.0
        ai_system.entity_timers["entity2"] = 2.0

        ai_system.shutdown()

        # Timers should be cleared
        assert len(ai_system.entity_timers) == 0
