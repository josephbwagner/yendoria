"""
Simple Gameplay Mods for Yendoria

This file contains several simple, well-documented mods that demonstrate
common modding patterns and can be used as templates for your own mods.
"""

import random

from yendoria.modding import EventBus, EventType, GameEvent

# Configuration constants for AtmosphereMod
ATMOSPHERIC_MESSAGE_TURN_THRESHOLD = 10
ATMOSPHERIC_MESSAGE_CHANCE = 0.01

# Configuration constants for LuckSystem
LUCK_EVENT_CHANCE = 0.03
LUCK_MESSAGE_COOLDOWN = 15
LUCK_MESSAGE_INTERVAL = 30
LUCK_COMBAT_AVOIDANCE_THRESHOLD = -80
LUCK_COMBAT_AVOIDANCE_CHANCE = 0.15
LUCK_HIGH_THRESHOLD = 60
LUCK_LOW_THRESHOLD = -60
LUCK_COMBAT_BOOST_THRESHOLD = 7
LUCK_LEVEL_HIGH_THRESHOLD = 70
LUCK_LEVEL_LOW_THRESHOLD = -70
LUCK_LEVEL_ROOM_COUNT = 8
LUCK_DECAY = 8
LUCK_EVENT_GOOD_CHANCE = 0.5
LUCK_DISPLAY_VERY_HIGH = 80
LUCK_DISPLAY_HIGH = 50
LUCK_DISPLAY_MEDIUM = 20
LUCK_DISPLAY_VERY_LOW = -80
LUCK_DISPLAY_LOW = -50
LUCK_DISPLAY_POOR = -20


class AtmosphereMod:
    """Adds atmospheric flavor text to enhance game immersion."""

    def __init__(self, event_bus: EventBus):
        """Initialize and register atmospheric event handlers."""
        self.event_bus = event_bus
        self.event_bus.subscribe(EventType.LEVEL_GENERATE, self.on_level_generate)
        self.event_bus.subscribe(EventType.COMBAT_START, self.on_combat_start)
        self.event_bus.subscribe(EventType.ENTITY_DEATH, self.on_entity_death)
        self.event_bus.subscribe(EventType.TURN_START, self.on_turn_start)

    def on_level_generate(self, event: GameEvent) -> None:
        """Add atmospheric descriptions to new levels."""
        atmospheres = [
            "🌫️  A damp mist clings to the dungeon walls...",
            "🔥 The air shimmers with heat from unknown sources.",
            "❄️  A bone-chilling cold permeates this level.",
            "🌟 Strange lights flicker in the darkness.",
            "💀 The stench of death hangs heavy here.",
            "🌿 Ancient roots have broken through the stone.",
            "⚡ The air crackles with magical energy.",
        ]
        print(random.choice(atmospheres))

    def on_combat_start(self, event: GameEvent) -> None:
        """Add dramatic combat descriptions."""
        combat_lines = [
            "⚔️  Steel rings against claw!",
            "🛡️  Battle is joined in the depths!",
            "⚡ Lightning-quick strikes fill the air!",
            "🔥 The fury of combat erupts!",
            "🌪️  A whirlwind of violence begins!",
            "💥 Weapons clash in deadly dance!",
        ]
        print(random.choice(combat_lines))

    def on_entity_death(self, event: GameEvent) -> None:
        """Add dramatic death descriptions."""
        entity = event.data.get("entity")
        if entity and not hasattr(entity, "is_player"):
            death_lines = [
                f"💀 {entity.name} falls with a final, echoing cry.",
                f"⚰️  {entity.name} collapses into the shadows.",
                f"👻 {entity.name}'s spirit departs this realm.",
                f"🌪️  {entity.name} is vanquished in a swirl of dust.",
                f"💫 {entity.name} fades into nothingness.",
                f"🗿 {entity.name} crumbles to stone.",
            ]
            print(random.choice(death_lines))

    def on_turn_start(self, event: GameEvent) -> None:
        """Occasional atmospheric turn messages."""
        turn_count = event.data.get("turn_count", 0)

        # Very rare atmospheric messages (1% chance)
        if (
            turn_count > ATMOSPHERIC_MESSAGE_TURN_THRESHOLD
            and random.random() < ATMOSPHERIC_MESSAGE_CHANCE
        ):
            ambient_sounds = [
                "🔔 Distant bells echo through the corridors...",
                "🐺 A wolf howls somewhere in the darkness.",
                "💧 Water drips steadily from unseen heights.",
                "🦇 Bats flutter overhead in the shadows.",
                "🌬️  A cold breeze carries whispers of the past.",
            ]
            print(random.choice(ambient_sounds))


class LuckSystem:
    """Implements a dynamic luck mechanic that affects gameplay."""

    def __init__(self, event_bus: EventBus):
        """Initialize the luck system."""
        self.event_bus = event_bus
        self.luck = 0  # Luck ranges from -100 to +100
        self.last_luck_message_turn = -10

        # Subscribe to events
        self.event_bus.subscribe(EventType.TURN_START, self.on_turn_start)
        self.event_bus.subscribe(EventType.COMBAT_START, self.on_combat_start)
        self.event_bus.subscribe(EventType.ENTITY_DEATH, self.on_entity_death)
        self.event_bus.subscribe(EventType.LEVEL_GENERATE, self.on_level_generate)

    def on_turn_start(self, event: GameEvent) -> None:
        """Handle turn start - update luck gradually."""
        turn_count = event.data.get("turn_count", 0)

        # Luck tends toward neutral over time
        if self.luck > 0:
            self.luck = max(0, self.luck - 1)
        elif self.luck < 0:
            self.luck = min(0, self.luck + 1)

        # Random luck events (3% chance per turn)
        if random.random() < LUCK_EVENT_CHANCE:
            self._trigger_luck_event()

        # Show luck status occasionally
        if (
            turn_count > 0
            and turn_count % LUCK_MESSAGE_INTERVAL == 0
            and turn_count - self.last_luck_message_turn >= LUCK_MESSAGE_COOLDOWN
        ):
            self._show_luck_status()
            self.last_luck_message_turn = turn_count

    def on_combat_start(self, event: GameEvent) -> None:
        """Handle combat start - apply luck effects."""
        attacker = event.data.get("attacker")

        # Only affect player-initiated combat
        if not (attacker and hasattr(attacker, "is_player") and attacker.is_player):
            return

        # Very unlucky players might avoid combat entirely
        if (
            self.luck <= LUCK_COMBAT_AVOIDANCE_THRESHOLD
            and random.random() < LUCK_COMBAT_AVOIDANCE_CHANCE
        ):
            event.cancel()
            print("💨 You slip and fall, avoiding the fight!")
            self.luck += 5  # Avoiding combat improves luck slightly
            return

        # Apply luck-based combat messages
        if self.luck >= LUCK_HIGH_THRESHOLD:
            print("✨ You feel confident and ready for battle!")
        elif self.luck <= LUCK_LOW_THRESHOLD:
            print("😰 You approach the fight with dread...")

    def on_entity_death(self, event: GameEvent) -> None:
        """Handle entity death - adjust luck based on outcome."""
        killer = event.data.get("killer")
        entity = event.data.get("entity")

        # Player killed a monster
        if (
            killer
            and hasattr(killer, "is_player")
            and killer.is_player
            and entity
            and not hasattr(entity, "is_player")
        ):
            # Increase luck for victories
            luck_gain = random.randint(3, 8)
            self.luck = min(100, self.luck + luck_gain)

            if luck_gain >= LUCK_COMBAT_BOOST_THRESHOLD:
                print(f"🌟 That was a lucky strike! (+{luck_gain} luck)")

    def on_level_generate(self, event: GameEvent) -> None:
        """Handle level generation - luck affects level quality."""
        rooms = event.data.get("rooms", [])

        # Lucky players get better level generation messages
        if (
            self.luck >= LUCK_LEVEL_HIGH_THRESHOLD
            and len(rooms) >= LUCK_LEVEL_ROOM_COUNT
        ):
            print("🏰 This level looks particularly well-designed!")
            self.luck -= LUCK_DECAY  # Using up some luck
        elif self.luck <= LUCK_LEVEL_LOW_THRESHOLD:
            print("😱 This level feels ominous and foreboding...")

    def _trigger_luck_event(self) -> None:
        """Trigger a random luck event."""
        if random.random() < LUCK_EVENT_GOOD_CHANCE:
            # Good luck event
            luck_change = random.randint(5, 15)
            self.luck = min(100, self.luck + luck_change)
            good_events = [
                f"🍀 You found a lucky coin! (+{luck_change} luck)",
                f"🌈 A rainbow appears! (+{luck_change} luck)",
                f"🐝 A friendly bee brings good fortune! (+{luck_change} luck)",
            ]
            print(random.choice(good_events))
        else:
            # Bad luck event
            luck_change = random.randint(5, 15)
            self.luck = max(-100, self.luck - luck_change)
            bad_events = [
                f"🪞 You break a mirror... (-{luck_change} luck)",
                f"🐈‍⬛ A black cat crosses your path. (-{luck_change} luck)",
                f"🧂 You spill some salt. (-{luck_change} luck)",
            ]
            print(random.choice(bad_events))

    def _show_luck_status(self) -> None:
        """Display current luck status."""
        if self.luck >= LUCK_DISPLAY_VERY_HIGH:
            print("🌟 You feel incredibly lucky!")
        elif self.luck >= LUCK_DISPLAY_HIGH:
            print("😊 Fortune seems to favor you.")
        elif self.luck >= LUCK_DISPLAY_MEDIUM:
            print("🙂 You feel pretty lucky today.")
        elif self.luck <= LUCK_DISPLAY_VERY_LOW:
            print("💀 You feel cursed by misfortune!")
        elif self.luck <= LUCK_DISPLAY_LOW:
            print("😰 Bad luck seems to follow you.")
        elif self.luck <= LUCK_DISPLAY_POOR:
            print("😕 You feel a bit unlucky.")
        else:
            print("😐 Your luck feels average.")

    def get_luck(self) -> int:
        """Get current luck value."""
        return self.luck


class SimpleStatsTracker:
    """Basic statistics tracking for gameplay analysis."""

    def __init__(self, event_bus: EventBus):
        """Initialize stats tracker."""
        self.event_bus = event_bus
        self.reset_stats()

        # Subscribe to events
        self.event_bus.subscribe(EventType.ENTITY_MOVE, self.on_entity_move)
        self.event_bus.subscribe(EventType.COMBAT_START, self.on_combat_start)
        self.event_bus.subscribe(EventType.ENTITY_DEATH, self.on_entity_death)
        self.event_bus.subscribe(EventType.TURN_START, self.on_turn_start)

    def reset_stats(self) -> None:
        """Reset all tracked statistics."""
        self.steps_taken = 0
        self.combats_fought = 0
        self.monsters_killed = 0
        self.current_turn = 0
        self.total_damage_dealt = 0

    def on_entity_move(self, event: GameEvent) -> None:
        """Track player movement."""
        if event.data.get("is_player", False):
            self.steps_taken += 1

    def on_combat_start(self, event: GameEvent) -> None:
        """Track combat initiation."""
        attacker = event.data.get("attacker")
        if attacker and hasattr(attacker, "is_player") and attacker.is_player:
            self.combats_fought += 1

    def on_entity_death(self, event: GameEvent) -> None:
        """Track monster kills."""
        killer = event.data.get("killer")
        entity = event.data.get("entity")

        if (
            killer
            and hasattr(killer, "is_player")
            and killer.is_player
            and entity
            and not hasattr(entity, "is_player")
        ):
            self.monsters_killed += 1

    def on_turn_start(self, event: GameEvent) -> None:
        """Track turns and show periodic stats."""
        self.current_turn = event.data.get("turn_count", 0)

        # Show stats every 100 turns
        if self.current_turn > 0 and self.current_turn % 100 == 0:
            self.show_stats()

    def show_stats(self) -> None:
        """Display current statistics."""
        print(f"\\n📊 STATS (Turn {self.current_turn}):")
        print(f"   🚶 Steps taken: {self.steps_taken}")
        print(f"   ⚔️  Combats fought: {self.combats_fought}")
        print(f"   💀 Monsters killed: {self.monsters_killed}")

        # Calculate derived stats
        if self.combats_fought > 0:
            kill_ratio = (self.monsters_killed / self.combats_fought) * 100
            print(f"   🎯 Kill ratio: {kill_ratio:.1f}%")

        if self.current_turn > 0:
            steps_per_turn = self.steps_taken / self.current_turn
            print(f"   📈 Steps per turn: {steps_per_turn:.1f}")

    def get_stats(self) -> dict[str, int]:
        """Get current statistics as a dictionary."""
        return {
            "steps_taken": self.steps_taken,
            "combats_fought": self.combats_fought,
            "monsters_killed": self.monsters_killed,
            "current_turn": self.current_turn,
        }


class PacifistMod:
    """Prevents all combat for peaceful gameplay."""

    def __init__(self, event_bus: EventBus):
        """Initialize pacifist mode."""
        self.event_bus = event_bus
        self.combats_prevented = 0
        self.event_bus.subscribe(EventType.COMBAT_START, self.prevent_combat)
        print("☮️  Pacifist mode activated - all combat will be prevented!")

    def prevent_combat(self, event: GameEvent) -> None:
        """Cancel all combat events."""
        self.combats_prevented += 1
        event.cancel()

        peaceful_messages = [
            "☮️  Peace prevails - the combatants walk away.",
            "🤝 Diplomacy succeeds where violence would fail.",
            "🕊️  A peaceful resolution is found.",
            "💝 Love conquers all - no blood is shed.",
            "🌸 The power of friendship stops the fight.",
        ]
        print(random.choice(peaceful_messages))

        # Show stats occasionally
        if self.combats_prevented % 10 == 0:
            print(f"📊 Prevented {self.combats_prevented} combats so far!")


def demo_simple_mods():
    """Demonstration of simple gameplay mods."""
    print("🧪 Simple Mods Demo")
    print("===================")

    # Create event bus and mods
    event_bus = EventBus()

    # Initialize mods
    AtmosphereMod(event_bus)
    luck = LuckSystem(event_bus)
    stats = SimpleStatsTracker(event_bus)

    print("✅ Mods initialized:")
    print("   🌫️  Atmosphere Mod - adds flavor text")
    print("   🍀 Luck System - dynamic luck mechanics")
    print("   📊 Stats Tracker - gameplay statistics")

    # Simulate some events
    print("\\n🎮 Simulating gameplay...")

    # Level generation
    event_bus.emit_simple(
        EventType.LEVEL_GENERATE,
        {"rooms": [f"room_{i}" for i in range(10)], "player_start": (5, 5)},
    )

    # Simulate several turns
    for turn in range(1, 21):
        # Turn start
        event_bus.emit_simple(
            EventType.TURN_START,
            {"turn_count": turn, "player": type("Player", (), {"name": "Hero"})()},
        )

        # Player movement
        event_bus.emit_simple(
            EventType.ENTITY_MOVE,
            {
                "entity": type("Player", (), {"name": "Hero"})(),
                "old_position": (turn, 5),
                "new_position": (turn + 1, 5),
                "is_player": True,
                "movement": (1, 0),
            },
        )

        # Occasional combat
        if turn % 5 == 0:
            enemy = random.choice(["Orc", "Goblin", "Troll"])

            # Combat (might be cancelled by luck)
            event_bus.emit_simple(
                EventType.COMBAT_START,
                {
                    "attacker": type(
                        "Player", (), {"name": "Hero", "is_player": True}
                    )(),
                    "defender": type("Enemy", (), {"name": enemy})(),
                    "position": (turn + 1, 5),
                },
            )

            # If combat wasn't cancelled, enemy dies
            if not event_bus.get_event_history(EventType.COMBAT_START)[-1].cancelled:
                event_bus.emit_simple(
                    EventType.ENTITY_DEATH,
                    {
                        "entity": type("Enemy", (), {"name": enemy})(),
                        "killer": type(
                            "Player", (), {"name": "Hero", "is_player": True}
                        )(),
                        "cause": "combat",
                    },
                )

    # Show final stats
    print("\\n📋 Final Statistics:")
    final_stats = stats.get_stats()
    for key, value in final_stats.items():
        print(f"   {key}: {value}")

    print(f"\\n🍀 Final luck: {luck.get_luck()}")
    print("\\n✅ Simple mods demo completed!")


if __name__ == "__main__":
    demo_simple_mods()
