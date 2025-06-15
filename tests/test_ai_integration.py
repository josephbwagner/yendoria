#!/usr/bin/env python3
"""Simple integration test for the AI system."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_ai_integration():
    """Test AI system integration."""
    print("Testing AI system integration...")

    # Test imports
    from yendoria.components.component_manager import get_component_manager

    print("✅ Component manager import successful")

    from yendoria.systems.config_manager import initialize_config_manager

    print("✅ Config manager import successful")

    from yendoria.systems.ai_manager import init_ai_manager

    print("✅ AI manager import successful")

    # Initialize systems
    component_manager = get_component_manager()
    config_manager = initialize_config_manager()
    ai_manager = init_ai_manager(component_manager, config_manager)
    print("✅ Systems initialized successfully")

    # Test basic functionality
    ai_manager.register_ai_entity("test_entity_001")
    entities = ai_manager.get_ai_entities()
    print(f"✅ AI entities registered: {len(entities)}")
    assert len(entities) >= 1, "Should have at least one registered entity"

    # Test performance stats
    stats = ai_manager.get_performance_stats()
    print(f"✅ Performance stats: {stats}")
    assert isinstance(stats, dict), "Stats should be a dictionary"

    # Test system registration
    from yendoria.systems.ai_behavior_advanced import AdvancedAIBehaviorSystem

    behavior_system = AdvancedAIBehaviorSystem(component_manager)
    ai_manager.register_system("behavior", behavior_system)
    print("✅ Behavior system registered")

    # Test update cycle
    ai_manager.update(1.0)
    print("✅ Update cycle completed")

    print("🎉 AI system integration test completed successfully!")


if __name__ == "__main__":
    success = test_ai_integration()
    sys.exit(0 if success else 1)
