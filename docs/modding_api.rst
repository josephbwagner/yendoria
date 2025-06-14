Modding API Reference
=====================

This document provides a complete technical reference for Yendoria's modding API, including all classes, methods, events, and data structures available to mod developers.

Core API Classes
----------------

EventBus
~~~~~~~~

.. autoclass:: yendoria.modding.EventBus
   :members:
   :undoc-members:
   :no-index:

The central event system that coordinates all mod communication with the game engine.

**Constructor:**

.. code-block:: python

   def __init__(self) -> None:
       """Initialize a new event bus."""

**Methods:**

``subscribe(event_type: EventType, handler: Callable[[GameEvent], None]) -> None``
   Register a handler function for a specific event type.

   :param event_type: The type of event to listen for
   :param handler: Function that takes a GameEvent and returns None

   **Example:**

   .. code-block:: python

      event_bus.subscribe(EventType.ENTITY_MOVE, self.on_entity_move)

``unsubscribe(event_type: EventType, handler: Callable) -> None``
   Remove a handler for a specific event type.

   :param event_type: The event type to stop listening for
   :param handler: The handler function to remove

``emit(event: GameEvent) -> GameEvent``
   Fire an event to all registered handlers.

   :param event: The event to emit
   :returns: The event (possibly modified by handlers)

   **Example:**

   .. code-block:: python

      event = GameEvent(EventType.ENTITY_SPAWN, {"entity": player})
      event_bus.emit(event)

``emit_simple(event_type: EventType, data: dict[str, Any] | None = None, cancellable: bool = False) -> GameEvent``
   Convenience method to emit an event with minimal setup.

   :param event_type: The type of event
   :param data: Event data (optional)
   :param cancellable: Whether the event can be cancelled
   :returns: The emitted event

   **Example:**

   .. code-block:: python

      event_bus.emit_simple(
          EventType.COMBAT_START,
          {"attacker": player, "defender": orc},
          cancellable=True
      )

``get_event_history(event_type: EventType | None = None) -> list[GameEvent]``
   Get recent event history, optionally filtered by type.

   :param event_type: Filter by this event type (optional)
   :returns: List of recent events

``clear_handlers() -> None``
   Clear all event handlers (useful for testing/cleanup).

GameEvent
~~~~~~~~~

.. autoclass:: yendoria.modding.GameEvent
   :members:
   :undoc-members:
   :no-index:

Represents a game event that can be observed and potentially modified by mods.

**Constructor:**

.. code-block:: python

   def __init__(
       self,
       event_type: EventType,
       data: dict[str, Any],
       cancellable: bool = False,
       source: str = "core"
   ) -> None:

**Attributes:**

``type: EventType``
   The type of event (from the EventType enum).

``data: dict[str, Any]``
   Event-specific data dictionary containing context information.

``cancellable: bool``
   Whether mods can cancel this event.

``cancelled: bool``
   Whether the event has been cancelled by a mod.

``source: str``
   What triggered this event (for debugging).

**Methods:**

``cancel() -> None``
   Cancel this event if it's cancellable.

   **Example:**

   .. code-block:: python

      def on_combat_start(self, event: GameEvent) -> None:
          if should_prevent_combat():
              event.cancel()
              print("Combat prevented!")

EventType
~~~~~~~~~

.. autoclass:: yendoria.modding.EventType
   :members:
   :undoc-members:
   :no-index:

Enumeration of all available game events that mods can subscribe to.

**Entity Events:**

``ENTITY_SPAWN``
   Emitted when any entity is created in the game world.

``ENTITY_MOVE``
   Emitted when any entity moves from one position to another.

``ENTITY_DEATH``
   Emitted when any entity dies or is destroyed.

**Combat Events:**

``COMBAT_START``
   Emitted when combat begins between two entities. **Cancellable**.

``COMBAT_HIT``
   Emitted when an attack successfully hits and deals damage.

``COMBAT_MISS``
   Emitted when an attack misses its target.

**Game Flow Events:**

``TURN_START``
   Emitted at the beginning of each game turn.

``TURN_END``
   Emitted when the player completes a turn-consuming action.

**World Events:**

``LEVEL_GENERATE``
   Emitted when a new dungeon level is generated.

``LEVEL_ENTER``
   Emitted when the player enters a new level.

``ROOM_GENERATE``
   Emitted when individual rooms are generated.

**Player Events:**

``PLAYER_LEVEL_UP``
   Emitted when the player character gains a level.

``PLAYER_DEATH``
   Emitted when the player character dies.

**Item Events:**

``ITEM_PICKUP``
   Emitted when an item is picked up.

``ITEM_USE``
   Emitted when an item is used.

``ITEM_DROP``
   Emitted when an item is dropped.

Event Data Reference
--------------------

This section documents the data fields available in each event type.

Entity Events
~~~~~~~~~~~~~

ENTITY_SPAWN
^^^^^^^^^^^^

**Data Fields:**

* ``entity`` (Entity): The entity object that was spawned
* ``position`` (tuple[int, int]): Coordinates where entity was placed
* ``entity_type`` (str): Type identifier ("player", "orc", "troll", etc.)
* ``room`` (Room, optional): Room where entity was spawned

**Example:**

.. code-block:: python

   def on_entity_spawn(self, event: GameEvent) -> None:
       entity = event.data.get("entity")
       position = event.data.get("position")
       entity_type = event.data.get("entity_type")
       print(f"{entity_type} spawned at {position}")

ENTITY_MOVE
^^^^^^^^^^^

**Data Fields:**

* ``entity`` (Entity): The entity that moved
* ``old_position`` (tuple[int, int]): Coordinates before movement
* ``new_position`` (tuple[int, int]): Coordinates after movement
* ``is_player`` (bool): Whether the moving entity is the player
* ``movement`` (tuple[int, int]): Movement delta (dx, dy)

**Example:**

.. code-block:: python

   def on_entity_move(self, event: GameEvent) -> None:
       if event.data.get("is_player", False):
           old_pos = event.data.get("old_position")
           new_pos = event.data.get("new_position")
           print(f"Player moved from {old_pos} to {new_pos}")

ENTITY_DEATH
^^^^^^^^^^^^

**Data Fields:**

* ``entity`` (Entity): The entity that died
* ``killer`` (Entity, optional): Entity responsible for the death
* ``position`` (tuple[int, int]): Coordinates where death occurred
* ``cause`` (str): Cause of death ("combat", "trap", etc.)

Combat Events
~~~~~~~~~~~~~

COMBAT_START
^^^^^^^^^^^^

**Cancellable**: Yes

**Data Fields:**

* ``attacker`` (Entity): Entity initiating the attack
* ``defender`` (Entity): Entity being attacked
* ``position`` (tuple[int, int]): Coordinates where combat occurs

**Example:**

.. code-block:: python

   def on_combat_start(self, event: GameEvent) -> None:
       attacker = event.data.get("attacker")
       defender = event.data.get("defender")

       # Prevent player from attacking friendly NPCs
       if (hasattr(attacker, "is_player") and attacker.is_player and
           hasattr(defender, "is_friendly") and defender.is_friendly):
           event.cancel()
           print("You cannot attack friendly characters!")

COMBAT_HIT
^^^^^^^^^^

**Data Fields:**

* ``attacker`` (Entity): Entity that dealt the damage
* ``defender`` (Entity): Entity that received damage
* ``damage`` (int): Amount of damage dealt
* ``original_hp`` (int): Defender's HP before taking damage

Game Flow Events
~~~~~~~~~~~~~~~~

TURN_START
^^^^^^^^^^

**Data Fields:**

* ``player`` (Entity): The player entity
* ``turn_count`` (int): Current turn number (starting from 0)

TURN_END
^^^^^^^^

**Data Fields:**

* ``player`` (Entity): The player entity
* ``turn_count`` (int): Turn number that just completed

World Events
~~~~~~~~~~~~

LEVEL_GENERATE
^^^^^^^^^^^^^^

**Data Fields:**

* ``map`` (GameMap): The GameMap object containing the generated level
* ``player_start`` (tuple[int, int]): Coordinates where player will start
* ``rooms`` (list[Room]): List of Room objects that were generated

**Example:**

.. code-block:: python

   def on_level_generate(self, event: GameEvent) -> None:
       rooms = event.data.get("rooms", [])
       player_start = event.data.get("player_start")
       print(f"Generated level with {len(rooms)} rooms")
       print(f"Player starts at {player_start}")

Player Events
~~~~~~~~~~~~~

PLAYER_DEATH
^^^^^^^^^^^^

**Data Fields:**

* ``entity`` (Entity): The player entity
* ``position`` (tuple[int, int]): Coordinates where death occurred
* ``cause`` (str): Cause of death

Common Patterns
---------------

Event Handler Patterns
~~~~~~~~~~~~~~~~~~~~~~~

**Basic Event Handler:**

.. code-block:: python

   def on_event(self, event: GameEvent) -> None:
       """Basic event handler pattern."""
       # Validate required data
       required_field = event.data.get("required_field")
       if required_field is None:
           return

       # Process the event
       self.handle_event_logic(required_field)

**Conditional Event Cancellation:**

.. code-block:: python

   def on_cancellable_event(self, event: GameEvent) -> None:
       """Pattern for conditional event cancellation."""
       if self.should_cancel_event(event.data):
           event.cancel()
           print("Event cancelled by mod!")

**Player-Specific Event Handling:**

.. code-block:: python

   def on_entity_event(self, event: GameEvent) -> None:
       """Pattern for handling player-specific events."""
       entity = event.data.get("entity")
       is_player = event.data.get("is_player", False)

       # Alternative check using entity attributes
       is_player_alt = hasattr(entity, "is_player") and entity.is_player

       if is_player or is_player_alt:
           self.handle_player_action(event.data)

Data Validation Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~

**Safe Data Access:**

.. code-block:: python

   def safe_event_handler(self, event: GameEvent) -> None:
       """Pattern for safe event data access."""
       # Use .get() with defaults
       entity = event.data.get("entity")
       position = event.data.get("position", (0, 0))
       damage = event.data.get("damage", 0)

       # Validate types
       if not isinstance(position, tuple) or len(position) != 2:
           return

       if not isinstance(damage, int) or damage < 0:
           return

       # Safe to use data
       self.process_validated_data(entity, position, damage)

**Entity Attribute Checking:**

.. code-block:: python

   def check_entity_attributes(self, event: GameEvent) -> None:
       """Pattern for safely checking entity attributes."""
       entity = event.data.get("entity")
       if entity is None:
           return

       # Check for expected attributes
       name = getattr(entity, "name", "Unknown")
       is_player = getattr(entity, "is_player", False)

       # Or use hasattr for boolean checks
       if hasattr(entity, "is_friendly") and entity.is_friendly:
           print(f"Friendly entity: {name}")

Statistics Tracking Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Simple Counter Tracking:**

.. code-block:: python

   class StatsMod:
       def __init__(self, event_bus: EventBus):
           self.counters = {
               "moves": 0,
               "combats": 0,
               "kills": 0
           }

           event_bus.subscribe(EventType.ENTITY_MOVE, self.count_moves)
           event_bus.subscribe(EventType.COMBAT_START, self.count_combats)
           event_bus.subscribe(EventType.ENTITY_DEATH, self.count_kills)

       def count_moves(self, event: GameEvent) -> None:
           if event.data.get("is_player", False):
               self.counters["moves"] += 1

       def count_combats(self, event: GameEvent) -> None:
           attacker = event.data.get("attacker")
           if hasattr(attacker, "is_player") and attacker.is_player:
               self.counters["combats"] += 1

**Historical Data Tracking:**

.. code-block:: python

   from collections import deque
   from dataclasses import dataclass
   import time

   @dataclass
   class EventRecord:
       timestamp: float
       event_type: str
       data: dict

   class HistoryMod:
       def __init__(self, event_bus: EventBus, max_history: int = 1000):
           self.history = deque(maxlen=max_history)

           # Subscribe to all events of interest
           for event_type in [EventType.ENTITY_MOVE, EventType.COMBAT_START]:
               event_bus.subscribe(event_type, self.record_event)

       def record_event(self, event: GameEvent) -> None:
           record = EventRecord(
               timestamp=time.time(),
               event_type=event.type.value,
               data=dict(event.data)  # Copy the data
           )
           self.history.append(record)

Mod Integration Patterns
~~~~~~~~~~~~~~~~~~~~~~~~

**Multi-Mod Coordination:**

.. code-block:: python

   class ModManager:
       def __init__(self, event_bus: EventBus):
           self.event_bus = event_bus
           self.mods = {}

       def register_mod(self, name: str, mod_instance):
           """Register a mod with the manager."""
           self.mods[name] = mod_instance

       def get_mod(self, name: str):
           """Get a registered mod by name."""
           return self.mods.get(name)

       def initialize_standard_mods(self):
           """Initialize a standard set of mods."""
           self.register_mod("stats", StatsTracker(self.event_bus))
           self.register_mod("atmosphere", AtmosphereMod(self.event_bus))

**Configurable Mods:**

.. code-block:: python

   class ConfigurableMod:
       def __init__(self, event_bus: EventBus, config: dict = None):
           self.config = config or self.get_default_config()
           self.event_bus = event_bus

           # Configure based on settings
           if self.config.get("track_movement", True):
               event_bus.subscribe(EventType.ENTITY_MOVE, self.on_move)

           if self.config.get("track_combat", True):
               event_bus.subscribe(EventType.COMBAT_START, self.on_combat)

       def get_default_config(self) -> dict:
           return {
               "track_movement": True,
               "track_combat": True,
               "message_frequency": 0.1,
               "debug_mode": False
           }

Error Handling Best Practices
------------------------------

Exception Safety
~~~~~~~~~~~~~~~~

.. code-block:: python

   def robust_event_handler(self, event: GameEvent) -> None:
       """Example of robust error handling in event handlers."""
       try:
           # Main mod logic
           self.process_event(event)
       except KeyError as e:
           print(f"Missing expected data in event: {e}")
       except AttributeError as e:
           print(f"Entity missing expected attribute: {e}")
       except Exception as e:
           print(f"Unexpected error in mod: {e}")
           # Log to file in production mods

Graceful Degradation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def degradation_example(self, event: GameEvent) -> None:
       """Example of graceful degradation when data is missing."""
       entity = event.data.get("entity")

       # Primary feature: use entity name
       if entity and hasattr(entity, "name"):
           message = f"Entity {entity.name} performed action"
       # Fallback: use entity type
       elif event.data.get("entity_type"):
           message = f"Entity of type {event.data['entity_type']} performed action"
       # Final fallback: generic message
       else:
           message = "An entity performed an action"

       print(message)

Type Safety
~~~~~~~~~~~

.. code-block:: python

   from typing import Optional, Union

   def type_safe_handler(self, event: GameEvent) -> None:
       """Example of type-safe event handling."""
       # Type annotations help catch errors early
       entity: Optional[object] = event.data.get("entity")
       position: tuple[int, int] = event.data.get("position", (0, 0))
       damage: int = event.data.get("damage", 0)

       # Runtime type validation
       if not isinstance(position, tuple) or len(position) != 2:
           return

       if not isinstance(damage, (int, float)) or damage < 0:
           return

       # Now safe to use typed data
       x, y = position
       self.process_validated_action(entity, x, y, damage)

Performance Guidelines
----------------------

Handler Performance
~~~~~~~~~~~~~~~~~~~

* **Keep handlers lightweight**: Target < 1ms execution time
* **Avoid blocking operations**: No file I/O or network calls in handlers
* **Cache expensive calculations**: Store results rather than recalculating
* **Use lazy evaluation**: Defer heavy processing until actually needed

.. code-block:: python

   class PerformantMod:
       def __init__(self, event_bus: EventBus):
           self.cache = {}
           self.pending_calculations = []
           event_bus.subscribe(EventType.ENTITY_MOVE, self.fast_handler)

       def fast_handler(self, event: GameEvent) -> None:
           """Lightweight event handler."""
           # Quick validation and caching
           entity_id = id(event.data.get("entity"))
           if entity_id not in self.cache:
               # Defer expensive calculation
               self.pending_calculations.append(entity_id)

           # Quick response
           print("Entity moved")

Memory Management
~~~~~~~~~~~~~~~~~

* **Limit history size**: Use ``collections.deque`` with ``maxlen``
* **Clean up resources**: Unsubscribe handlers when done
* **Avoid circular references**: Be careful with entity references

.. code-block:: python

   class MemoryEfficientMod:
       def __init__(self, event_bus: EventBus):
           self.event_bus = event_bus
           self.recent_events = deque(maxlen=100)  # Limited size
           event_bus.subscribe(EventType.ENTITY_MOVE, self.on_move)

       def cleanup(self):
           """Clean up resources when mod is no longer needed."""
           self.event_bus.unsubscribe(EventType.ENTITY_MOVE, self.on_move)
           self.recent_events.clear()

Debugging and Development
-------------------------

Debug Utilities
~~~~~~~~~~~~~~~

.. code-block:: python

   class DebugMod:
       def __init__(self, event_bus: EventBus, debug: bool = False):
           self.debug = debug
           self.event_bus = event_bus

           if debug:
               # Subscribe to all events for debugging
               for event_type in EventType:
                   event_bus.subscribe(event_type, self.debug_handler)

       def debug_handler(self, event: GameEvent) -> None:
           """Debug handler that logs all events."""
           print(f"DEBUG: {event.type.value} - {event.data}")

           # Log to file for detailed analysis
           with open("mod_debug.log", "a") as f:
               f.write(f"{event.type.value}: {event.data}\\n")

Testing Patterns
~~~~~~~~~~~~~~~~

.. code-block:: python

   def test_mod_functionality():
       """Example of mod testing."""
       # Create isolated event bus for testing
       test_bus = EventBus()
       mod = MyMod(test_bus)

       # Emit test events
       test_event = GameEvent(
           EventType.ENTITY_MOVE,
           {"entity": MockEntity(), "is_player": True}
       )
       test_bus.emit(test_event)

       # Assert expected behavior
       assert mod.player_move_count == 1

Migration and Compatibility
---------------------------

When the modding API evolves, follow these patterns for compatibility:

Version Checking
~~~~~~~~~~~~~~~~

.. code-block:: python

   class CompatibleMod:
       def __init__(self, event_bus: EventBus):
           self.event_bus = event_bus
           self.api_version = getattr(event_bus, "api_version", "1.0.0")

           # Version-specific initialization
           if self.api_version >= "2.0.0":
               self.use_new_features()
           else:
               self.use_legacy_features()

Graceful Feature Detection
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def feature_detection_example(self, event: GameEvent) -> None:
       """Example of detecting available features."""
       # Check if new data fields are available
       if "new_field" in event.data:
           # Use new feature
           self.handle_new_feature(event.data["new_field"])
       else:
           # Fall back to old behavior
           self.handle_legacy_behavior(event.data)

This completes the comprehensive API reference for Yendoria's modding system. For practical examples and tutorials, see the other modding documentation sections.
