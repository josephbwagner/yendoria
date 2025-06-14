Modding Tutorial
================

This tutorial will guide you through creating your first mod for Yendoria, from basic event handling to advanced gameplay modifications. By the end, you'll understand how to hook into the game's event system and create meaningful extensions.

Prerequisites
-------------

Before starting this tutorial, you should:

* Have basic Python programming knowledge
* Be familiar with object-oriented programming concepts
* Have Yendoria installed and running
* Understand the basics of the game mechanics

Setting Up Your Development Environment
---------------------------------------

1. **Clone or Download Yendoria**::

    git clone https://github.com/josephbwagner/yendoria.git
    cd yendoria

2. **Install Dependencies**::

    poetry install

3. **Run the Game** to ensure everything works::

    poetry run python -m yendoria

4. **Create a Workspace** for your mod development::

    mkdir my_mods
    cd my_mods

Tutorial 1: Your First Event Handler
-------------------------------------

Let's start with a simple mod that tracks player statistics.

**Step 1: Understanding Events**

Yendoria's modding system is built around events. Every major action in the game (movement, combat, level generation) triggers events that mods can listen to.

**Step 2: Create Your First Mod**

Create a file called ``stats_tracker.py``:

.. code-block:: python

   """
   Simple stats tracking mod for Yendoria.
   Demonstrates basic event handling and data collection.
   """

   from yendoria.modding import EventBus, EventType, GameEvent


   class StatsTracker:
       """Tracks basic player statistics throughout the game."""

       def __init__(self, event_bus: EventBus):
           """Initialize the stats tracker and subscribe to events."""
           self.event_bus = event_bus

           # Initialize counters
           self.steps_taken = 0
           self.combats_fought = 0
           self.monsters_killed = 0
           self.current_turn = 0

           # Subscribe to relevant events
           self.event_bus.subscribe(EventType.ENTITY_MOVE, self.on_entity_move)
           self.event_bus.subscribe(EventType.COMBAT_START, self.on_combat_start)
           self.event_bus.subscribe(EventType.ENTITY_DEATH, self.on_entity_death)
           self.event_bus.subscribe(EventType.TURN_END, self.on_turn_end)

       def on_entity_move(self, event: GameEvent) -> None:
           """Handle entity movement events."""
           # Only count player movement
           if event.data.get("is_player", False):
               self.steps_taken += 1

       def on_combat_start(self, event: GameEvent) -> None:
           """Handle combat start events."""
           attacker = event.data.get("attacker")
           # Only count combats where player is the attacker
           if hasattr(attacker, "is_player") and attacker.is_player:
               self.combats_fought += 1

       def on_entity_death(self, event: GameEvent) -> None:
           """Handle entity death events."""
           killer = event.data.get("killer")
           entity = event.data.get("entity")

           # Count monsters killed by player
           if (hasattr(killer, "is_player") and killer.is_player and
               not hasattr(entity, "is_player")):
               self.monsters_killed += 1

       def on_turn_end(self, event: GameEvent) -> None:
           """Handle turn end events."""
           self.current_turn = event.data.get("turn_count", 0)

           # Show stats every 50 turns
           if self.current_turn > 0 and self.current_turn % 50 == 0:
               self.show_stats()

       def show_stats(self) -> None:
           """Display current statistics."""
           print(f"\\n📊 STATS (Turn {self.current_turn}):")
           print(f"   🚶 Steps taken: {self.steps_taken}")
           print(f"   ⚔️  Combats fought: {self.combats_fought}")
           print(f"   💀 Monsters killed: {self.monsters_killed}")

           # Calculate derived stats
           if self.combats_fought > 0:
               kill_ratio = self.monsters_killed / self.combats_fought * 100
               print(f"   🎯 Kill ratio: {kill_ratio:.1f}%")

           if self.current_turn > 0:
               steps_per_turn = self.steps_taken / self.current_turn
               print(f"   📈 Steps per turn: {steps_per_turn:.1f}")

       def get_stats(self) -> dict:
           """Return current statistics as a dictionary."""
           return {
               "steps_taken": self.steps_taken,
               "combats_fought": self.combats_fought,
               "monsters_killed": self.monsters_killed,
               "current_turn": self.current_turn,
           }

**Step 3: Test Your Mod**

To test this mod, you would integrate it into the game by modifying the engine to create an instance of your ``StatsTracker``. For now, let's create a simple test:

.. code-block:: python

   # test_stats_tracker.py

   if __name__ == "__main__":
       from yendoria.modding import EventBus, EventType

       # Create event bus and stats tracker
       event_bus = EventBus()
       stats = StatsTracker(event_bus)

       # Simulate some events
       print("🧪 Testing stats tracker...")

       # Simulate player movement
       for i in range(5):
           event_bus.emit_simple(
               EventType.ENTITY_MOVE,
               {
                   "entity": type('Player', (), {'is_player': True})(),
                   "old_position": (i, 0),
                   "new_position": (i + 1, 0),
                   "is_player": True,
               }
           )

       # Simulate combat and kill
       event_bus.emit_simple(
           EventType.COMBAT_START,
           {
               "attacker": type('Player', (), {'is_player': True})(),
               "defender": type('Monster', (), {})(),
               "position": (5, 0),
           }
       )

       event_bus.emit_simple(
           EventType.ENTITY_DEATH,
           {
               "entity": type('Monster', (), {})(),
               "killer": type('Player', (), {'is_player': True})(),
               "cause": "combat",
           }
       )

       # Show final stats
       stats.show_stats()
       print("✅ Test completed!")

Tutorial 2: Interactive Gameplay Mod
-------------------------------------

Now let's create a more advanced mod that actually affects gameplay by implementing a "luck" system.

**Step 1: Design the Luck System**

Our luck system will:

* Track a "luck" value that changes over time
* Affect combat outcomes based on luck
* Provide lucky/unlucky events during gameplay
* Allow players to see their current luck

**Step 2: Implement the Luck System**

Create ``luck_system.py``:

.. code-block:: python

   """
   Luck system mod for Yendoria.
   Adds a dynamic luck mechanic that affects gameplay.
   """

   import random
   from yendoria.modding import EventBus, EventType, GameEvent


   class LuckSystem:
       """Implements a dynamic luck system that affects gameplay."""

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

           # Random luck events (5% chance per turn)
           if random.random() < 0.05:
               self._trigger_luck_event()

           # Show luck status every 20 turns (but not too often)
           if (turn_count > 0 and turn_count % 20 == 0 and
               turn_count - self.last_luck_message_turn >= 10):
               self._show_luck_status()
               self.last_luck_message_turn = turn_count

       def on_combat_start(self, event: GameEvent) -> None:
           """Handle combat start - apply luck effects."""
           attacker = event.data.get("attacker")

           # Only affect player-initiated combat
           if not (hasattr(attacker, "is_player") and attacker.is_player):
               return

           # Very unlucky players might avoid combat entirely
           if self.luck <= -80 and random.random() < 0.1:
               event.cancel()
               print("💨 You slip and fall, avoiding the fight!")
               self.luck += 5  # Avoiding combat improves luck slightly
               return

           # Apply luck-based combat messages
           if self.luck >= 50:
               print("✨ You feel confident and ready for battle!")
           elif self.luck <= -50:
               print("😰 You approach the fight with dread...")

       def on_entity_death(self, event: GameEvent) -> None:
           """Handle entity death - adjust luck based on outcome."""
           killer = event.data.get("killer")
           entity = event.data.get("entity")

           # Player killed a monster
           if (hasattr(killer, "is_player") and killer.is_player and
               not hasattr(entity, "is_player")):

               # Increase luck for victories
               luck_gain = random.randint(2, 8)
               self.luck = min(100, self.luck + luck_gain)

               if luck_gain >= 6:
                   print(f"🌟 That was a lucky strike! (+{luck_gain} luck)")

           # Player died (game over)
           elif hasattr(entity, "is_player") and entity.is_player:
               print(f"💀 Final luck: {self.luck}")

       def on_level_generate(self, event: GameEvent) -> None:
           """Handle level generation - luck affects level quality."""
           rooms = event.data.get("rooms", [])

           # Lucky players get better levels
           if self.luck >= 60 and len(rooms) >= 8:
               print("🏰 This level looks particularly well-designed!")
               self.luck -= 10  # Using up some luck

           # Unlucky players get warned about dangerous levels
           elif self.luck <= -60:
               print("⚠️  This place feels ominous and dangerous...")

       def _trigger_luck_event(self) -> None:
           """Trigger a random luck event."""
           event_type = random.choice(["good", "bad", "neutral"])

           if event_type == "good":
               luck_change = random.randint(5, 15)
               self.luck = min(100, self.luck + luck_change)
               messages = [
                   f"🍀 You find a lucky coin! (+{luck_change} luck)",
                   f"✨ A gentle breeze fills you with hope! (+{luck_change} luck)",
                   f"🌈 You see a good omen! (+{luck_change} luck)",
               ]
           elif event_type == "bad":
               luck_change = random.randint(5, 15)
               self.luck = max(-100, self.luck - luck_change)
               messages = [
                   f"💔 You step on a crack! (-{luck_change} luck)",
                   f"🕷️  A spider crosses your path! (-{luck_change} luck)",
                   f"🌩️  Dark clouds gather overhead! (-{luck_change} luck)",
               ]
           else:  # neutral
               messages = [
                   "🔮 The fates are watching...",
                   "⚖️  The cosmic balance shifts subtly...",
                   "🌙 You feel the weight of destiny...",
               ]

           print(random.choice(messages))

       def _show_luck_status(self) -> None:
           """Show current luck status to player."""
           if self.luck >= 75:
               status = "Extremely Lucky! 🌟🍀✨"
           elif self.luck >= 50:
               status = "Very Lucky! 🍀✨"
           elif self.luck >= 25:
               status = "Lucky! 🍀"
           elif self.luck >= -25:
               status = "Neutral ⚖️"
           elif self.luck >= -50:
               status = "Unlucky 😕"
           elif self.luck >= -75:
               status = "Very Unlucky! 😰💔"
           else:
               status = "Extremely Unlucky! 💀⚡🌩️"

           print(f"🔮 Your luck: {self.luck}/100 ({status})")

       def get_luck(self) -> int:
           """Get current luck value."""
           return self.luck

       def set_luck(self, value: int) -> None:
           """Set luck value (for testing/debugging)."""
           self.luck = max(-100, min(100, value))

Tutorial 3: Advanced Event Manipulation
----------------------------------------

Let's create a mod that demonstrates event cancellation and complex event interaction.

**Step 1: Design a "Divine Intervention" System**

This mod will:

* Track player performance and divine favor
* Occasionally prevent player death through divine intervention
* Cancel combat in specific circumstances
* Provide increasingly powerful interventions based on favor

**Step 2: Implement Divine Intervention**

Create ``divine_intervention.py``:

.. code-block:: python

   """
   Divine intervention system for Yendoria.
   Provides divine protection based on player actions.
   """

   import random
   from yendoria.modding import EventBus, EventType, GameEvent


   class DivineIntervention:
       """Implements divine intervention system with favor tracking."""

       # Constants for divine favor
       FAVOR_FOR_MERCY = 10
       FAVOR_FOR_EXPLORATION = 2
       FAVOR_COST_INTERVENTION = 50
       FAVOR_COST_COMBAT_BLOCK = 25

       def __init__(self, event_bus: EventBus):
           """Initialize the divine intervention system."""
           self.event_bus = event_bus
           self.divine_favor = 0
           self.interventions_used = 0
           self.rooms_explored = set()

           # Subscribe to events
           self.event_bus.subscribe(EventType.COMBAT_START, self.on_combat_start)
           self.event_bus.subscribe(EventType.ENTITY_DEATH, self.on_entity_death)
           self.event_bus.subscribe(EventType.ENTITY_MOVE, self.on_entity_move)
           self.event_bus.subscribe(EventType.TURN_START, self.on_turn_start)

       def on_combat_start(self, event: GameEvent) -> None:
           """Handle combat start - possibly intervene."""
           attacker = event.data.get("attacker")
           defender = event.data.get("defender")

           # Only intervene in player-initiated combat
           if not (hasattr(attacker, "is_player") and attacker.is_player):
               return

           # Check for mercy intervention (spare weak enemies)
           if self._should_show_mercy(defender):
               if self.divine_favor >= self.FAVOR_COST_COMBAT_BLOCK:
                   event.cancel()
                   self.divine_favor -= self.FAVOR_COST_COMBAT_BLOCK
                   self.divine_favor += self.FAVOR_FOR_MERCY
                   print("🕊️  Divine voice whispers: 'Show mercy to the weak.'")
                   print(f"✨ Divine favor: {self.divine_favor}")
                   return

           # Check for overwhelming odds intervention
           if self._facing_overwhelming_odds() and self.divine_favor >= self.FAVOR_COST_COMBAT_BLOCK:
               if random.random() < 0.3:  # 30% chance
                   event.cancel()
                   self.divine_favor -= self.FAVOR_COST_COMBAT_BLOCK
                   print("⚡ Divine lightning scares away your foes!")
                   print(f"✨ Divine favor: {self.divine_favor}")

       def on_entity_death(self, event: GameEvent) -> None:
           """Handle entity death - track divine favor."""
           entity = event.data.get("entity")
           killer = event.data.get("killer")

           # Player killed something
           if hasattr(killer, "is_player") and killer.is_player:
               # Lose favor for excessive killing
               if self.interventions_used == 0:  # First kill is free
                   pass
               else:
                   self.divine_favor = max(0, self.divine_favor - 1)

           # Player died - attempt intervention
           elif hasattr(entity, "is_player") and entity.is_player:
               if self._attempt_death_intervention():
                   # This is a theoretical intervention - actual implementation
                   # would require more complex interaction with the death system
                   print("💫 DIVINE INTERVENTION! You are spared from death!")
                   print("🌟 The gods have taken notice of your deeds.")
                   self.interventions_used += 1
                   # In a real implementation, this would prevent the death

       def on_entity_move(self, event: GameEvent) -> None:
           """Handle movement - track exploration for divine favor."""
           if not event.data.get("is_player", False):
               return

           position = event.data.get("new_position")
           if position:
               # Simplified room detection (in reality, would check actual rooms)
               room_id = f"{position[0]//10}_{position[1]//10}"
               if room_id not in self.rooms_explored:
                   self.rooms_explored.add(room_id)
                   self.divine_favor += self.FAVOR_FOR_EXPLORATION

       def on_turn_start(self, event: GameEvent) -> None:
           """Handle turn start - passive favor changes."""
           turn_count = event.data.get("turn_count", 0)

           # Slowly gain favor for survival
           if turn_count > 0 and turn_count % 25 == 0:
               self.divine_favor += 1

           # Show favor status occasionally
           if turn_count > 0 and turn_count % 100 == 0:
               self._show_divine_status()

       def _should_show_mercy(self, defender) -> bool:
           """Check if mercy should be shown to this defender."""
           # Simplified check - in reality would examine defender stats
           return random.random() < 0.2  # 20% of enemies are "weak"

       def _facing_overwhelming_odds(self) -> bool:
           """Check if player is facing overwhelming odds."""
           # Simplified check - would examine surrounding enemies
           return random.random() < 0.1  # 10% chance of overwhelming odds

       def _attempt_death_intervention(self) -> bool:
           """Attempt to intervene in player death."""
           if self.divine_favor >= self.FAVOR_COST_INTERVENTION:
               self.divine_favor -= self.FAVOR_COST_INTERVENTION
               return True
           return False

       def _show_divine_status(self) -> None:
           """Show current divine favor status."""
           if self.divine_favor >= 100:
               status = "Divine Champion! 👑✨"
           elif self.divine_favor >= 75:
               status = "Highly Favored! 🌟"
           elif self.divine_favor >= 50:
               status = "Blessed! ✨"
           elif self.divine_favor >= 25:
               status = "Noticed by the Gods 👁️"
           elif self.divine_favor >= 10:
               status = "Slight Favor 🕯️"
           else:
               status = "Unknown to the Gods 🌫️"

           print(f"🔮 Divine Favor: {self.divine_favor} ({status})")
           if self.interventions_used > 0:
               print(f"💫 Divine Interventions: {self.interventions_used}")

Best Practices for Mod Development
-----------------------------------

Performance Guidelines
~~~~~~~~~~~~~~~~~~~~~~

1. **Keep Event Handlers Fast**

   .. code-block:: python

      # Good: Fast event handler
      def on_entity_move(self, event: GameEvent) -> None:
          if event.data.get("is_player", False):
              self.step_count += 1

      # Bad: Slow event handler
      def on_entity_move(self, event: GameEvent) -> None:
          # Don't do expensive operations in event handlers
          for i in range(10000):
              complex_calculation()

2. **Cache Expensive Calculations**

   .. code-block:: python

      class OptimizedMod:
          def __init__(self, event_bus):
              self.cached_data = {}
              self.cache_valid = False

          def on_turn_start(self, event):
              # Invalidate cache each turn
              self.cache_valid = False

          def get_expensive_data(self):
              if not self.cache_valid:
                  self.cached_data = self._calculate_expensive_data()
                  self.cache_valid = True
              return self.cached_data

3. **Use Appropriate Data Structures**

   .. code-block:: python

      # Good: Use sets for membership testing
      explored_rooms = set()

      def check_room(room_id):
          return room_id in explored_rooms  # O(1) lookup

      # Bad: Use lists for membership testing
      explored_rooms = []

      def check_room(room_id):
          return room_id in explored_rooms  # O(n) lookup

Error Handling
~~~~~~~~~~~~~~

1. **Always Validate Event Data**

   .. code-block:: python

      def on_combat_start(self, event: GameEvent) -> None:
          # Good: Validate data exists
          attacker = event.data.get("attacker")
          defender = event.data.get("defender")

          if not attacker or not defender:
              return  # Gracefully handle missing data

          # Now safely use attacker and defender

2. **Handle Exceptions Gracefully**

   .. code-block:: python

      def on_entity_death(self, event: GameEvent) -> None:
          try:
              # Mod logic here
              self.process_death(event)
          except Exception as e:
              # Log error but don't crash the game
              print(f"Error in death handler: {e}")
              # Optionally: Reset mod state to safe defaults

3. **Provide Fallback Behavior**

   .. code-block:: python

      def get_entity_strength(self, entity) -> int:
          # Try to get strength from entity
          if hasattr(entity, "stats") and hasattr(entity.stats, "strength"):
              return entity.stats.strength

          # Fallback to reasonable default
          return 10

Code Organization
~~~~~~~~~~~~~~~~~

1. **Use Clear Class Structure**

   .. code-block:: python

      class WellOrganizedMod:
          """Clear docstring explaining what this mod does."""

          def __init__(self, event_bus: EventBus):
              """Initialize mod and register event handlers."""
              self._setup_state()
              self._register_events(event_bus)

          def _setup_state(self) -> None:
              """Initialize mod state variables."""
              self.counter = 0
              self.active = True

          def _register_events(self, event_bus: EventBus) -> None:
              """Register all event handlers."""
              event_bus.subscribe(EventType.ENTITY_MOVE, self.on_move)
              # ... other subscriptions

          # Event handlers
          def on_move(self, event: GameEvent) -> None:
              """Handle entity movement."""
              pass

          # Helper methods
          def _helper_method(self) -> None:
              """Private helper method."""
              pass

          # Public interface
          def get_status(self) -> dict:
              """Public method to get mod status."""
              return {"counter": self.counter, "active": self.active}

2. **Use Type Hints**

   .. code-block:: python

      from typing import Optional, List, Dict, Any
      from yendoria.modding import EventBus, GameEvent

      class TypedMod:
          def __init__(self, event_bus: EventBus) -> None:
              self.stats: Dict[str, int] = {}
              self.history: List[GameEvent] = []

          def process_entity(self, entity: Optional[Any]) -> bool:
              if entity is None:
                  return False
              # Process entity...
              return True

Testing Your Mods
~~~~~~~~~~~~~~~~~~

1. **Create Unit Tests**

   .. code-block:: python

      # test_my_mod.py
      import unittest
      from yendoria.modding import EventBus, EventType
      from my_mod import MyMod

      class TestMyMod(unittest.TestCase):
          def setUp(self):
              self.event_bus = EventBus()
              self.mod = MyMod(self.event_bus)

          def test_movement_tracking(self):
              # Simulate player movement
              self.event_bus.emit_simple(
                  EventType.ENTITY_MOVE,
                  {"is_player": True, "new_position": (1, 1)}
              )

              # Check that mod tracked the movement
              self.assertEqual(self.mod.movement_count, 1)

          def test_combat_handling(self):
              # Test combat event handling
              pass

2. **Create Integration Tests**

   .. code-block:: python

      def test_mod_integration():
          """Test mod with realistic game simulation."""
          event_bus = EventBus()
          mod = MyMod(event_bus)

          # Simulate a complete game scenario
          simulate_level_generation(event_bus)
          simulate_player_movement(event_bus, steps=10)
          simulate_combat_encounter(event_bus)

          # Verify mod state
          assert mod.get_stats()["steps"] == 10
          assert mod.get_stats()["combats"] > 0

Common Patterns and Examples
----------------------------

State Machines
~~~~~~~~~~~~~~

For mods that need to track complex state changes:

.. code-block:: python

   from enum import Enum

   class QuestState(Enum):
       NOT_STARTED = "not_started"
       IN_PROGRESS = "in_progress"
       COMPLETED = "completed"

   class QuestMod:
       def __init__(self, event_bus):
           self.quest_state = QuestState.NOT_STARTED
           self.monsters_killed = 0
           event_bus.subscribe(EventType.ENTITY_DEATH, self.on_death)

       def on_death(self, event):
           if self.quest_state == QuestState.IN_PROGRESS:
               self.monsters_killed += 1
               if self.monsters_killed >= 5:
                   self.quest_state = QuestState.COMPLETED
                   print("🎉 Quest completed! You've slain 5 monsters!")

Resource Management
~~~~~~~~~~~~~~~~~~~

For mods that need to manage limited resources:

.. code-block:: python

   class ManaSystem:
       def __init__(self, event_bus):
           self.max_mana = 100
           self.current_mana = self.max_mana
           self.mana_regen_rate = 2

           event_bus.subscribe(EventType.TURN_START, self.on_turn_start)
           event_bus.subscribe(EventType.COMBAT_START, self.on_combat_start)

       def on_turn_start(self, event):
           # Regenerate mana each turn
           self.current_mana = min(self.max_mana,
                                 self.current_mana + self.mana_regen_rate)

       def on_combat_start(self, event):
           # Use mana for combat bonuses
           if self.current_mana >= 20:
               self.current_mana -= 20
               print("✨ You channel magical energy! (+damage)")

Data Persistence
~~~~~~~~~~~~~~~~

For mods that need to remember data between sessions:

.. code-block:: python

   import json
   import os

   class PersistentMod:
       def __init__(self, event_bus):
           self.data_file = "mod_data.json"
           self.load_data()
           event_bus.subscribe(EventType.PLAYER_DEATH, self.save_data)

       def load_data(self):
           if os.path.exists(self.data_file):
               with open(self.data_file, 'r') as f:
                   data = json.load(f)
                   self.total_games = data.get("total_games", 0)
                   self.best_score = data.get("best_score", 0)
           else:
               self.total_games = 0
               self.best_score = 0

       def save_data(self, event):
           self.total_games += 1
           data = {
               "total_games": self.total_games,
               "best_score": self.best_score
           }
           with open(self.data_file, 'w') as f:
               json.dump(data, f)

Next Steps
----------

After completing these tutorials, you should:

1. **Experiment** with different event combinations
2. **Read the API documentation** for complete event details
3. **Study the example mods** in the repository
4. **Join the community** to share your creations and get help
5. **Contribute** improvements to the modding system

Advanced Topics
~~~~~~~~~~~~~~~

Once you're comfortable with basic modding, explore:

* **Performance optimization** for complex mods
* **Multi-mod compatibility** and conflict resolution
* **Advanced event patterns** like event chaining
* **Contributing to the modding framework** itself

The modding system is designed to grow with your needs, so don't hesitate to suggest improvements or new features!
