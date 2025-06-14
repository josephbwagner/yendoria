"""
Advanced Statistics Mod for Yendoria

This mod demonstrates comprehensive game tracking and analysis,
including real-time statistics, performance metrics, and historical data.
Perfect for players who want detailed insights into their gameplay.
"""

import json
import time
from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from typing import Any

from yendoria.modding import EventBus, EventType, GameEvent


@dataclass
class CombatRecord:
    """Record of a single combat encounter."""

    turn: int
    attacker: str
    defender: str
    position: tuple[int, int]
    timestamp: float
    damage_dealt: int = 0
    was_fatal: bool = False


@dataclass
class MovementRecord:
    """Record of entity movement."""

    turn: int
    entity: str
    from_pos: tuple[int, int]
    to_pos: tuple[int, int]
    distance: float
    timestamp: float


class AdvancedStatsTracker:
    """
    Comprehensive statistics tracking mod.

    Features:
    - Real-time combat analysis
    - Movement pattern tracking
    - Performance metrics
    - Historical data storage
    - Exportable statistics
    """

    def __init__(self, event_bus: EventBus):
        """Initialize the advanced stats tracker."""
        self.event_bus = event_bus
        self.start_time = time.time()

        # Basic counters
        self.current_turn = 0
        self.total_steps = 0
        self.total_combats = 0
        self.total_kills = 0
        self.player_deaths = 0

        # Advanced tracking
        self.combat_history: list[CombatRecord] = []
        self.movement_history: deque = deque(maxlen=1000)  # Limit memory usage
        self.damage_by_turn: dict[int, int] = defaultdict(int)
        self.kills_by_entity_type: dict[str, int] = defaultdict(int)
        self.movement_patterns: dict[str, int] = defaultdict(int)

        # Performance metrics
        self.turn_durations: list[float] = []
        self.last_turn_start = time.time()

        # Subscribe to all relevant events
        self._register_event_handlers()

    def _register_event_handlers(self) -> None:
        """Register all event handlers for comprehensive tracking."""
        self.event_bus.subscribe(EventType.TURN_START, self.on_turn_start)
        self.event_bus.subscribe(EventType.TURN_END, self.on_turn_end)
        self.event_bus.subscribe(EventType.ENTITY_MOVE, self.on_entity_move)
        self.event_bus.subscribe(EventType.COMBAT_START, self.on_combat_start)
        self.event_bus.subscribe(EventType.COMBAT_HIT, self.on_combat_hit)
        self.event_bus.subscribe(EventType.ENTITY_DEATH, self.on_entity_death)
        self.event_bus.subscribe(EventType.PLAYER_DEATH, self.on_player_death)
        self.event_bus.subscribe(EventType.LEVEL_GENERATE, self.on_level_generate)

    def on_turn_start(self, event: GameEvent) -> None:
        """Track turn timing and display periodic statistics."""
        self.current_turn = event.data.get("turn_count", 0)
        current_time = time.time()

        # Record turn duration
        if hasattr(self, "last_turn_start"):
            duration = current_time - self.last_turn_start
            self.turn_durations.append(duration)

        self.last_turn_start = current_time

        # Show comprehensive stats every 100 turns
        if self.current_turn > 0 and self.current_turn % 100 == 0:
            self.display_comprehensive_stats()

    def on_turn_end(self, event: GameEvent) -> None:
        """Handle turn end events."""
        # Could track end-of-turn state here
        pass

    def on_entity_move(self, event: GameEvent) -> None:
        """Track detailed movement patterns."""
        entity = event.data.get("entity")
        old_pos = event.data.get("old_position", (0, 0))
        new_pos = event.data.get("new_position", (0, 0))
        is_player = event.data.get("is_player", False)

        if entity is None:
            return

        # Calculate movement distance
        dx = new_pos[0] - old_pos[0]
        dy = new_pos[1] - old_pos[1]
        distance = (dx * dx + dy * dy) ** 0.5

        # Record movement
        movement = MovementRecord(
            turn=self.current_turn,
            entity=getattr(entity, "name", "Unknown"),
            from_pos=old_pos,
            to_pos=new_pos,
            distance=distance,
            timestamp=time.time(),
        )
        self.movement_history.append(movement)

        # Track player movement specifically
        if is_player:
            self.total_steps += 1

            # Analyze movement patterns
            direction = self._get_movement_direction(dx, dy)
            self.movement_patterns[direction] += 1

    def on_combat_start(self, event: GameEvent) -> None:
        """Track combat initiation."""
        self.total_combats += 1

        attacker = event.data.get("attacker")
        defender = event.data.get("defender")
        position = event.data.get("position", (0, 0))

        # Record combat start
        combat = CombatRecord(
            turn=self.current_turn,
            attacker=getattr(attacker, "name", "Unknown"),
            defender=getattr(defender, "name", "Unknown"),
            position=position,
            timestamp=time.time(),
        )
        self.combat_history.append(combat)

    def on_combat_hit(self, event: GameEvent) -> None:
        """Track combat damage."""
        damage = event.data.get("damage", 0)

        # Add to current turn's damage total
        self.damage_by_turn[self.current_turn] += damage

        # Update the last combat record if available
        if self.combat_history:
            self.combat_history[-1].damage_dealt += damage

    def on_entity_death(self, event: GameEvent) -> None:
        """Track entity deaths and analyze kill patterns."""
        entity = event.data.get("entity")
        killer = event.data.get("killer")

        if entity is None:
            return

        # Track kills by player
        if killer and hasattr(killer, "is_player") and killer.is_player:
            self.total_kills += 1
            entity_type = getattr(entity, "name", "Unknown")
            self.kills_by_entity_type[entity_type] += 1

            # Mark last combat as fatal if applicable
            if self.combat_history and self.combat_history[-1].defender == getattr(
                entity, "name", "Unknown"
            ):
                self.combat_history[-1].was_fatal = True

    def on_player_death(self, event: GameEvent) -> None:
        """Track player deaths."""
        self.player_deaths += 1
        cause = event.data.get("cause", "unknown")

        print(f"💀 GAME OVER - Death #{self.player_deaths} (Cause: {cause})")
        self.display_final_stats()

    def on_level_generate(self, event: GameEvent) -> None:
        """Track level generation events."""
        rooms = event.data.get("rooms", [])
        player_start = event.data.get("player_start", (0, 0))

        print(f"🗺️  Level generated: {len(rooms)} rooms, starting at {player_start}")

    def _get_movement_direction(self, dx: int, dy: int) -> str:
        """Convert movement delta to direction name."""
        directions = {
            (0, 0): "none",
            (0, -1): "north",
            (0, 1): "south",
            (1, 0): "east",
            (-1, 0): "west",
            (1, -1): "northeast",
            (1, 1): "southeast",
            (-1, -1): "northwest",
            (-1, 1): "southwest",
        }
        return directions.get((dx, dy), "unknown")

    def display_comprehensive_stats(self) -> None:
        """Display detailed statistics summary."""
        runtime = time.time() - self.start_time

        print("\\n" + "=" * 60)
        print(f"📊 COMPREHENSIVE STATS (Turn {self.current_turn})")
        print("=" * 60)

        # Basic stats
        print("🎮 BASIC STATISTICS:")
        print(f"   Runtime: {runtime:.1f} seconds")
        print(f"   Total steps: {self.total_steps}")
        print(f"   Total combats: {self.total_combats}")
        print(f"   Total kills: {self.total_kills}")
        print(f"   Player deaths: {self.player_deaths}")

        # Efficiency metrics
        if self.current_turn > 0:
            steps_per_turn = self.total_steps / self.current_turn
            combats_per_turn = self.total_combats / self.current_turn
            print(f"   Steps per turn: {steps_per_turn:.2f}")
            print(f"   Combats per turn: {combats_per_turn:.2f}")

        # Combat effectiveness
        if self.total_combats > 0:
            kill_ratio = (self.total_kills / self.total_combats) * 100
            print(f"   Kill ratio: {kill_ratio:.1f}%")

        # Movement patterns
        if self.movement_patterns:
            print("\\n🧭 MOVEMENT PATTERNS:")
            for direction, count in sorted(
                self.movement_patterns.items(), key=lambda x: x[1], reverse=True
            )[:5]:
                percentage = (
                    (count / self.total_steps) * 100 if self.total_steps > 0 else 0
                )
                print(f"   {direction}: {count} ({percentage:.1f}%)")

        # Kill breakdown
        if self.kills_by_entity_type:
            print("\\n💀 KILLS BY TYPE:")
            for entity_type, count in sorted(
                self.kills_by_entity_type.items(), key=lambda x: x[1], reverse=True
            )[:5]:
                print(f"   {entity_type}: {count}")

        # Performance metrics
        if self.turn_durations:
            avg_turn_time = sum(self.turn_durations) / len(self.turn_durations)
            max_turn_time = max(self.turn_durations)
            print("\\n⚡ PERFORMANCE:")
            print(f"   Avg turn time: {avg_turn_time:.3f}s")
            print(f"   Max turn time: {max_turn_time:.3f}s")

        print("=" * 60)

    def display_final_stats(self) -> None:
        """Display final statistics at game end."""
        print("\\n" + "🏁 FINAL GAME STATISTICS " + "🏁")
        self.display_comprehensive_stats()

        # Additional final stats
        runtime = time.time() - self.start_time
        print(f"\\n🕒 Session lasted {runtime:.1f} seconds")
        if self.current_turn > 0:
            print(f"⏱️  Average time per turn: {runtime / self.current_turn:.2f}s")

    def export_stats(self, filename: str = "yendoria_stats.json") -> None:
        """Export statistics to JSON file."""
        stats_data = {
            "session_info": {
                "start_time": self.start_time,
                "end_time": time.time(),
                "total_turns": self.current_turn,
                "runtime_seconds": time.time() - self.start_time,
            },
            "basic_stats": {
                "total_steps": self.total_steps,
                "total_combats": self.total_combats,
                "total_kills": self.total_kills,
                "player_deaths": self.player_deaths,
            },
            "movement_patterns": dict(self.movement_patterns),
            "kills_by_type": dict(self.kills_by_entity_type),
            "damage_by_turn": dict(self.damage_by_turn),
            "combat_history": [
                asdict(combat) for combat in self.combat_history[-50:]
            ],  # Last 50 combats
            "performance": {
                "turn_durations": (
                    self.turn_durations[-100:] if self.turn_durations else []
                ),  # Last 100 turns
                "average_turn_time": (
                    sum(self.turn_durations) / len(self.turn_durations)
                    if self.turn_durations
                    else 0
                ),
            },
        }

        try:
            with open(filename, "w") as f:
                json.dump(stats_data, f, indent=2)
            print(f"📁 Statistics exported to {filename}")
        except Exception as e:
            print(f"❌ Failed to export stats: {e}")

    def get_quick_stats(self) -> dict[str, Any]:
        """Get current statistics as a dictionary."""
        return {
            "turn": self.current_turn,
            "steps": self.total_steps,
            "combats": self.total_combats,
            "kills": self.total_kills,
            "deaths": self.player_deaths,
            "runtime": time.time() - self.start_time,
        }


def demo_advanced_stats():
    """Demonstration of the advanced statistics tracker."""
    print("🧪 Advanced Statistics Tracker Demo")
    print("====================================")

    # Create event bus and stats tracker
    event_bus = EventBus()
    stats = AdvancedStatsTracker(event_bus)

    # Simulate a game session
    print("\\n🎮 Simulating game session...")

    # Level generation
    event_bus.emit_simple(
        EventType.LEVEL_GENERATE,
        {"rooms": [f"room_{i}" for i in range(8)], "player_start": (5, 5)},
    )

    # Constants
    LETHAL_DAMAGE_THRESHOLD = 10

    # Simulate 10 turns of gameplay
    for turn in range(1, 11):
        # Turn start
        event_bus.emit_simple(
            EventType.TURN_START,
            {"turn_count": turn, "player": type("Player", (), {"name": "Hero"})()},
        )

        # Player movement (random direction)
        import random

        directions = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
        ]
        dx, dy = random.choice(directions)
        old_pos = (5 + turn - 1, 5)
        new_pos = (5 + turn, 5 + dy)

        event_bus.emit_simple(
            EventType.ENTITY_MOVE,
            {
                "entity": type("Player", (), {"name": "Hero"})(),
                "old_position": old_pos,
                "new_position": new_pos,
                "is_player": True,
                "movement": (dx, dy),
            },
        )

        # Occasional combat
        if turn % 3 == 0:
            enemy_name = random.choice(["Orc", "Goblin", "Troll"])

            # Combat start
            event_bus.emit_simple(
                EventType.COMBAT_START,
                {
                    "attacker": type("Player", (), {"name": "Hero"})(),
                    "defender": type("Enemy", (), {"name": enemy_name})(),
                    "position": new_pos,
                },
            )

            # Combat hit
            damage = random.randint(5, 15)
            event_bus.emit_simple(
                EventType.COMBAT_HIT,
                {
                    "attacker": type("Player", (), {"name": "Hero"})(),
                    "defender": type("Enemy", (), {"name": enemy_name})(),
                    "damage": damage,
                    "original_hp": 20,
                },
            )

            # Enemy death (if enough damage)
            if damage >= LETHAL_DAMAGE_THRESHOLD:
                event_bus.emit_simple(
                    EventType.ENTITY_DEATH,
                    {
                        "entity": type("Enemy", (), {"name": enemy_name})(),
                        "killer": type(
                            "Player", (), {"name": "Hero", "is_player": True}
                        )(),
                        "cause": "combat",
                    },
                )

        # Turn end
        event_bus.emit_simple(
            EventType.TURN_END,
            {"turn_count": turn, "player": type("Player", (), {"name": "Hero"})()},
        )

        # Small delay to simulate turn time
        import time

        time.sleep(0.01)

    # Show final stats
    print("\\n📋 Final Statistics:")
    quick_stats = stats.get_quick_stats()
    for key, value in quick_stats.items():
        print(f"   {key}: {value}")

    # Export stats
    stats.export_stats("demo_stats.json")

    print("\\n✅ Advanced statistics demo completed!")
    print("📁 Check demo_stats.json for exported data")


if __name__ == "__main__":
    demo_advanced_stats()
