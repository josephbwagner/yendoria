#!/usr/bin/env python3
"""Integration test for AI system with game loop."""

import sys
from pathlib import Path

from yendoria.components.component_manager import get_component_manager

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_game_engine_ai_integration():
    """Test AI system integration with the game engine."""
    print("Testing AI integration with game engine...")

    try:
        # Import game engine
        from yendoria.engine import GameEngine

        print("✅ GameEngine import successful")

        # Initialize game engine in headless mode (no graphics)
        engine = GameEngine(width=80, height=50, headless=True)
        print("✅ GameEngine initialized successfully")

        # Check that AI integration was initialized
        assert hasattr(engine, "ai_integration"), "AI integration not found"
        assert engine.ai_integration.initialized, "AI integration not initialized"
        print("✅ AI integration initialized in game engine")

        # Test AI stats
        stats = engine.ai_integration.get_ai_stats()
        print(f"✅ AI stats: {stats}")

        # Test that entities were registered with AI
        ai_entities = engine.ai_integration.ai_entities
        print(f"✅ AI entities registered: {len(ai_entities)}")

        # Simulate a few game update cycles
        for turn in range(3):
            print(f"  Simulating turn {turn + 1}...")

            # Simulate player action (this would normally come from input)
            player_acted = True

            if player_acted:
                # This is what happens in the main game loop
                engine.update_monsters()  # This now uses AI system

        print("✅ Game loop simulation completed")

        # Check updated stats
        final_stats = engine.ai_integration.get_ai_stats()
        print(f"✅ Final AI stats: {final_stats}")

        # Test cleanup
        engine.ai_integration.shutdown()
        print("✅ AI integration shutdown successfully")

        print("🎉 Game engine AI integration test completed successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        raise


def test_manual_entity_registration():
    """Test manual registration of entities with AI system."""
    print("\nTesting manual entity registration...")

    try:
        from yendoria.engine import GameEngine

        # Initialize engine
        engine = GameEngine(headless=True)

        # Create a custom entity
        component_manager = get_component_manager()
        guard_entity = component_manager.create_entity(
            name="Town Guard", is_player=False
        )

        # Register it manually with the AI system
        engine.ai_integration.register_entity_with_ai(
            guard_entity, entity_type="guard", archetype="guard", faction="town_guard"
        )

        # Verify it was registered
        assert hasattr(guard_entity, "_ai_entity_id"), "Entity not marked with AI ID"
        assert guard_entity._ai_entity_id in engine.ai_integration.ai_entities

        print("✅ Manual entity registration successful")

        # Test getting AI action for the entity
        action = engine.ai_integration.get_ai_action_for_entity(guard_entity)
        print(f"✅ AI action for guard: {action}")

        engine.ai_integration.shutdown()

    except Exception as e:
        print(f"❌ Error in manual registration test: {e}")
        import traceback

        traceback.print_exc()
        raise


if __name__ == "__main__":
    try:
        test_game_engine_ai_integration()
        test_manual_entity_registration()
        print("\n🎉 All AI integration tests passed!")
    except Exception:
        print("\n❌ Some tests failed")
        sys.exit(1)
