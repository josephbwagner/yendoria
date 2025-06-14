"""
Example mod demonstrating the Yendoria event system integration.

This example shows how mods can hook into various game events
to extend functionality without modifying core game code.
"""

from yendoria.modding import EventBus, EventType, GameEvent

# Constants for the example
DIVINE_INTERVENTION_COMBAT = 5
LARGE_DUNGEON_THRESHOLD = 15


class ExampleEventListener:
    """Example event listener that demonstrates modding capabilities."""

    def __init__(self, event_bus: EventBus):
        """Initialize and register event handlers."""
        self.event_bus = event_bus
        self.combat_count = 0
        self.movement_count = 0

        # Register event handlers
        self.event_bus.subscribe(EventType.ENTITY_MOVE, self.on_entity_move)
        self.event_bus.subscribe(EventType.COMBAT_START, self.on_combat_start)
        self.event_bus.subscribe(EventType.ENTITY_DEATH, self.on_entity_death)
        self.event_bus.subscribe(EventType.TURN_START, self.on_turn_start)
        self.event_bus.subscribe(EventType.LEVEL_GENERATE, self.on_level_generate)

    def on_entity_move(self, event: GameEvent) -> None:
        """Handle entity movement events."""
        self.movement_count += 1
        old_pos = event.data.get("old_position")
        new_pos = event.data.get("new_position")
        is_player = event.data.get("is_player", False)

        if is_player:
            print(f"🚶 Player moved from {old_pos} to {new_pos}")
            if self.movement_count % 10 == 0:
                print(f"📊 Player has moved {self.movement_count} times!")

    def on_combat_start(self, event: GameEvent) -> None:
        """Handle combat start events."""
        self.combat_count += 1
        attacker = event.data.get("attacker")
        defender = event.data.get("defender")
        position = event.data.get("position")

        print(
            f"⚔️  Combat #{self.combat_count}: "
            f"{attacker.name if attacker else 'Unknown'} attacks "
            f"{defender.name if defender else 'Unknown'} at {position}"
        )

        # Example: Cancel combat if this is the 5th combat (for demonstration)
        if self.combat_count == DIVINE_INTERVENTION_COMBAT:
            print("🛡️  Divine intervention prevents this combat!")
            event.cancel()

    def on_entity_death(self, event: GameEvent) -> None:
        """Handle entity death events."""
        entity = event.data.get("entity")
        killer = event.data.get("killer")
        cause = event.data.get("cause", "unknown")

        print(
            f"💀 {entity.name if entity else 'Unknown'} has died "
            f"(killed by {killer.name if killer else 'Unknown'}, cause: {cause})"
        )

        # Example: Award experience or trigger special effects
        if killer and hasattr(killer, "is_player") and killer.is_player:
            print("🌟 Player gains experience for the kill!")

    def on_turn_start(self, event: GameEvent) -> None:
        """Handle turn start events."""
        turn_count = event.data.get("turn_count", 0)

        # Example: Every 20 turns, show a status message
        if turn_count > 0 and turn_count % 20 == 0:
            print(f"⏰ Turn {turn_count}: The dungeon grows colder...")

    def on_level_generate(self, event: GameEvent) -> None:
        """Handle level generation events."""
        player_start = event.data.get("player_start")
        rooms = event.data.get("rooms", [])

        print(
            f"🗺️  New level generated! {len(rooms)} rooms, "
            f"player starts at {player_start}"
        )

        # Example: Mod could add special rooms, modify generation, etc.
        if len(rooms) > LARGE_DUNGEON_THRESHOLD:
            print("🏰 This is a large dungeon level!")

    def get_stats(self) -> dict:
        """Get statistics tracked by this mod."""
        return {
            "combat_count": self.combat_count,
            "movement_count": self.movement_count,
        }


def example_usage():
    """Example of how to use the event system in a mod."""
    # This would typically be called when a mod is loaded
    from yendoria.engine import GameEngine

    # Create game engine (which includes event bus)
    engine = GameEngine(headless=True)  # Headless for testing

    # Create and register our example listener
    listener = ExampleEventListener(engine.event_bus)

    print("🎮 Event system integration example initialized!")
    print("📝 The following events will be tracked:")
    print("   - Entity movement (with player tracking)")
    print("   - Combat start/resolution")
    print("   - Entity deaths")
    print("   - Turn progression")
    print("   - Level generation")
    print()

    # In a real mod, the game would now run and events would be fired
    # For this example, we can simulate some events:

    # Simulate a level generation event
    engine.event_bus.emit_simple(
        EventType.LEVEL_GENERATE,
        {
            "map": None,  # Would be actual map
            "player_start": (5, 5),
            "rooms": [f"room_{i}" for i in range(12)],  # Mock rooms
        },
    )

    # Simulate player movement
    engine.event_bus.emit_simple(
        EventType.ENTITY_MOVE,
        {
            "entity": type("Player", (), {"name": "Player"})(),
            "old_position": (5, 5),
            "new_position": (6, 5),
            "is_player": True,
        },
    )

    # Show stats
    stats = listener.get_stats()
    print(f"📊 Final stats: {stats}")


if __name__ == "__main__":
    example_usage()
