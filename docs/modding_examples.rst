Modding Examples
================

This section provides comprehensive, practical examples of Yendoria mods that demonstrate different modding patterns and capabilities. All examples are fully functional and can be used as templates for your own mods.

.. note::
   All example files are located in the ``examples/mods/`` directory and can be run independently for testing.

Basic Modding Patterns
-----------------------

Event Subscription and Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The foundation of all Yendoria mods is subscribing to and handling game events. Here's the basic pattern:

.. code-block:: python

   from yendoria.modding import EventBus, EventType, GameEvent

   class BasicMod:
       def __init__(self, event_bus: EventBus):
           self.event_bus = event_bus
           # Subscribe to events you want to handle
           self.event_bus.subscribe(EventType.ENTITY_MOVE, self.on_entity_move)
           self.event_bus.subscribe(EventType.COMBAT_START, self.on_combat_start)

       def on_entity_move(self, event: GameEvent) -> None:
           """Handle entity movement events."""
           entity = event.data.get("entity")
           is_player = event.data.get("is_player", False)
           if is_player:
               print(f"Player moved to {event.data.get('new_position')}")

       def on_combat_start(self, event: GameEvent) -> None:
           """Handle combat start events."""
           attacker = event.data.get("attacker")
           defender = event.data.get("defender")
           print(f"{attacker.name} attacks {defender.name}!")

Example Mod Collection
----------------------

All modding examples are located in the ``examples/mods/`` directory for easy discovery and organization. Each example demonstrates different aspects of the modding system and can be used as templates for your own mods.

Atmosphere Mod
~~~~~~~~~~~~~~

**File**: ``examples/mods/simple_gameplay_mods.py``

Adds immersive flavor text throughout the game to enhance the player experience.

**Features:**
* Level generation atmosphere descriptions
* Dynamic combat narration
* Dramatic death messages
* Occasional ambient sounds during exploration

**Key Events Used:**
* ``LEVEL_GENERATE`` - Atmospheric level descriptions
* ``COMBAT_START`` - Combat flavor text
* ``ENTITY_DEATH`` - Death narration
* ``TURN_START`` - Ambient sounds (rare)

**Example Usage:**

.. code-block:: python

   from examples.mods.simple_gameplay_mods import AtmosphereMod

   # Initialize the mod
   atmosphere_mod = AtmosphereMod(engine.event_bus)

   # The mod will automatically add flavor text during gameplay:
   # "🌫️ A damp mist clings to the dungeon walls..."
   # "⚔️ Steel rings against claw!"
   # "💀 The orc falls with a final, echoing cry."

Dynamic Luck System
~~~~~~~~~~~~~~~~~~~

**File**: ``examples/mods/simple_gameplay_mods.py``

Implements a luck mechanic that dynamically affects gameplay through chance events and combat outcomes.

**Features:**
* Luck value that changes based on player actions
* Random luck events (finding coins, breaking mirrors)
* Combat avoidance for very unlucky players
* Luck-based level generation feedback
* Periodic luck status messages

**Key Mechanics:**
* Luck ranges from -100 to +100
* Gradually tends toward neutral over time
* Victory increases luck, defeats decrease it
* Very low luck can prevent combat entirely

**Example Integration:**

.. code-block:: python

   from examples.mods.simple_gameplay_mods import LuckSystem

   luck_system = LuckSystem(engine.event_bus)

   # During gameplay:
   # "🍀 You found a lucky coin! (+12 luck)"
   # "💨 You slip and fall, avoiding the fight!" (very unlucky)
   # "✨ You feel confident and ready for battle!" (high luck)

   # Check current luck
   current_luck = luck_system.get_luck()
   print(f"Current luck: {current_luck}")

Statistics Tracking
~~~~~~~~~~~~~~~~~~~

**File**: ``examples/mods/simple_gameplay_mods.py``

Tracks comprehensive gameplay statistics for analysis and achievements.

**Basic Stats Tracker Features:**
* Steps taken
* Combats fought
* Monsters killed
* Kill ratio calculation
* Periodic stats display

**Advanced Stats Tracker Features:**
* Combat history with full context
* Movement pattern analysis
* Performance metrics (turn duration)
* Damage tracking by turn
* Exportable data to JSON

**Usage Example:**

.. code-block:: python

   from examples.mods.simple_gameplay_mods import SimpleStatsTracker

   stats = SimpleStatsTracker(engine.event_bus)

   # Get current stats
   current_stats = stats.get_stats()
   # {'steps_taken': 45, 'combats_fought': 8, 'monsters_killed': 6, 'current_turn': 23}

   # Manually display stats
   stats.show_stats()

Pacifist Mode
~~~~~~~~~~~~~

**File**: ``examples/mods/simple_gameplay_mods.py``

Prevents all combat for peaceful gameplay exploration.

**Features:**
* Cancels all combat events
* Tracks combats prevented
* Provides peaceful resolution messages
* Perfect for exploration-focused gameplay

**Usage:**

.. code-block:: python

   from examples.mods.simple_gameplay_mods import PacifistMod

   pacifist = PacifistMod(engine.event_bus)
   # "☮️ Pacifist mode activated - all combat will be prevented!"

   # During gameplay, all combat attempts result in:
   # "☮️ Peace prevails - the combatants walk away."
   # "🤝 Diplomacy succeeds where violence would fail."

Advanced Example: Comprehensive Event Demo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**File**: ``examples/mods/event_system_demo.py``

A sophisticated example that demonstrates advanced event handling patterns and mod capabilities.

**Features:**
* Multiple event type handling
* Event cancellation demonstration
* Statistical tracking
* Conditional logic based on game state
* Combat intervention mechanics

**Key Patterns Demonstrated:**

.. code-block:: python

   class ExampleEventListener:
       def on_combat_start(self, event: GameEvent) -> None:
           """Example of conditional event cancellation."""
           self.combat_count += 1

           # Cancel every 5th combat for demonstration
           if self.combat_count == 5:
               print("🛡️ Divine intervention prevents this combat!")
               event.cancel()  # This prevents the combat from occurring

       def on_entity_death(self, event: GameEvent) -> None:
           """Example of conditional logic based on event data."""
           entity = event.data.get("entity")
           killer = event.data.get("killer")

           # Award experience only for player kills
           if hasattr(killer, "is_player") and killer.is_player:
               print("🌟 Player gains experience for the kill!")

Testing Your Mods
------------------

All example mods include built-in testing functionality. You can run them independently to see how they work:

**Test Individual Mods:**

.. code-block:: bash

   # Test the simple gameplay mods
   cd examples/mods
   python simple_gameplay_mods.py

   # Test the comprehensive event system
   python event_system_demo.py

**Test Output Example:**

.. code-block:: text

   🧪 Simple Mods Demo
   ===================
   ✅ Mods initialized:
      🌫️ Atmosphere Mod - adds flavor text
      🍀 Luck System - dynamic luck mechanics
      📊 Stats Tracker - gameplay statistics

   🎮 Simulating gameplay...
   🌫️ A damp mist clings to the dungeon walls...
   ⚔️ Steel rings against claw!
   💀 The orc falls with a final, echoing cry.
   🍀 You found a lucky coin! (+8 luck)

   📋 Final Statistics:
      steps_taken: 20
      combats_fought: 4
      monsters_killed: 3
      current_turn: 20

Mod Development Best Practices
------------------------------

Code Organization
~~~~~~~~~~~~~~~~~

**File Structure:**
* One class per major mod feature
* Clear, descriptive class and method names
* Comprehensive docstrings
* Type hints for all parameters

**Example Structure:**

.. code-block:: python

   class WellStructuredMod:
       """
       Clear description of what this mod does.

       Features:
       * Feature 1 description
       * Feature 2 description
       """

       def __init__(self, event_bus: EventBus):
           """Initialize the mod with clear setup."""
           self.event_bus = event_bus
           self._register_handlers()

       def _register_handlers(self) -> None:
           """Private method to organize event registration."""
           self.event_bus.subscribe(EventType.ENTITY_MOVE, self.on_entity_move)
           # ... other subscriptions

       def on_entity_move(self, event: GameEvent) -> None:
           """Handle entity movement with clear documentation."""
           # Implementation with error checking
           entity = event.data.get("entity")
           if entity is None:
               return  # Graceful handling of missing data

Error Handling
~~~~~~~~~~~~~~

Always validate event data and handle edge cases:

.. code-block:: python

   def on_combat_start(self, event: GameEvent) -> None:
       """Robust event handler with error checking."""
       # Validate required data exists
       attacker = event.data.get("attacker")
       defender = event.data.get("defender")

       if attacker is None or defender is None:
           return  # Skip processing if data is missing

       # Check for expected attributes
       if not hasattr(attacker, "name"):
           return

       # Proceed with mod logic
       print(f"{attacker.name} attacks!")

Performance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Keep event handlers lightweight (< 1ms execution time)
* Use lazy evaluation for expensive operations
* Cache frequently accessed data
* Consider async operations for heavy processing

.. code-block:: python

   class PerformantMod:
       def __init__(self, event_bus: EventBus):
           self.event_bus = event_bus
           self._cached_data = {}  # Cache expensive calculations
           self.event_bus.subscribe(EventType.ENTITY_MOVE, self.on_entity_move)

       def on_entity_move(self, event: GameEvent) -> None:
           """Lightweight event handler."""
           # Quick validation
           if not event.data.get("is_player", False):
               return

           # Defer heavy processing
           self._schedule_heavy_processing(event.data)

       def _schedule_heavy_processing(self, data):
           """Separate heavy processing from event handling."""
           # Process in background or defer to next frame
           pass

Integration Patterns
--------------------

Multiple Mod Coordination
~~~~~~~~~~~~~~~~~~~~~~~~~

When using multiple mods together, consider interaction patterns:

.. code-block:: python

   def initialize_mod_suite(event_bus: EventBus):
       """Initialize a coordinated set of mods."""
       # Stats tracking (foundational)
       stats = AdvancedStatsTracker(event_bus)

       # Gameplay modifications
       luck = LuckSystem(event_bus)
       atmosphere = AtmosphereMod(event_bus)

       # Optional: peaceful mode
       # pacifist = PacifistMod(event_bus)  # Comment out for normal combat

       return {
           'stats': stats,
           'luck': luck,
           'atmosphere': atmosphere
       }

Mod Configuration
~~~~~~~~~~~~~~~~~

Support configuration for reusable mods:

.. code-block:: python

   class ConfigurableMod:
       def __init__(self, event_bus: EventBus, config: dict = None):
           self.config = config or {}
           self.message_frequency = self.config.get("message_frequency", 0.1)
           self.enable_combat_messages = self.config.get("combat_messages", True)

           # Configure based on settings
           if self.enable_combat_messages:
               event_bus.subscribe(EventType.COMBAT_START, self.on_combat_start)

Data Persistence
~~~~~~~~~~~~~~~~

For mods that need to save state:

.. code-block:: python

   import json
   from pathlib import Path

   class PersistentMod:
       def __init__(self, event_bus: EventBus, save_file: str = "mod_data.json"):
           self.event_bus = event_bus
           self.save_file = Path(save_file)
           self.data = self._load_data()

           # Register for game end events to save data
           event_bus.subscribe(EventType.PLAYER_DEATH, self.save_data)

       def _load_data(self) -> dict:
           """Load mod data from file."""
           if self.save_file.exists():
               return json.loads(self.save_file.read_text())
           return {"sessions": 0, "total_kills": 0}

       def save_data(self, event: GameEvent = None) -> None:
           """Save mod data to file."""
           self.save_file.write_text(json.dumps(self.data, indent=2))

Community Examples
------------------

The examples provided demonstrate patterns you can use to create:

**Gameplay Mods:**
* Difficulty modifiers
* New mechanics (hunger, thirst, sanity)
* Alternative win conditions
* Special abilities or spells

**Quality of Life Mods:**
* Enhanced UI information
* Gameplay statistics and analytics
* Automatic actions (auto-pickup, auto-explore)
* Accessibility features

**Atmospheric Mods:**
* Dynamic storytelling
* Procedural flavor text
* Ambient audio cues
* Seasonal or time-based changes

**Challenge Mods:**
* Permadeath variations
* Resource management
* Speed run timers
* Achievement systems

Next Steps
----------

1. **Study the Examples**: Review all example files to understand different patterns
2. **Start Simple**: Begin with a basic stats tracker or atmosphere mod
3. **Experiment**: Try modifying the example mods to suit your preferences
4. **Combine Features**: Create mods that use multiple event types together
5. **Share Your Mods**: Consider contributing your creations back to the community

For more advanced modding topics, see:
* :doc:`modding` - Complete API reference
* :doc:`modding_tutorial` - Step-by-step mod creation guide
* :doc:`modding_roadmap` - Upcoming modding features
