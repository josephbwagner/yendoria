Modding System
==============

Yendoria features a comprehensive modding system built on an event-driven architecture that allows you to extend and customize the game without modifying core game files. The modding system is designed around the principles of safety, performance, and ease of use.

.. note::
   The modding system is currently in **Phase 1** implementation. See the :doc:`modding_roadmap` for upcoming features.

Overview
--------

The Yendoria modding system provides:

* **Event-Driven Architecture**: Hook into any game action through a comprehensive event system
* **Type-Safe APIs**: Full type annotations for reliable mod development
* **Non-Invasive Design**: Mods don't require modifying core game files
* **Event Cancellation**: Prevent or modify game actions dynamically
* **Performance Monitoring**: Built-in tracking of mod performance impact

Architecture
------------

Core Components
~~~~~~~~~~~~~~~

The modding system consists of several key components:

1. **Event Bus**: Central communication system for game events
2. **Event Types**: Comprehensive enumeration of hookable game events
3. **Game Events**: Rich event objects containing action context
4. **Event Handlers**: Mod functions that respond to specific events

Event System
~~~~~~~~~~~~

The event system is the foundation of Yendoria's modding capabilities. It allows mods to:

* Subscribe to specific game events
* Receive detailed context about game actions
* Cancel preventable events (like combat)
* Track event history for debugging

.. note::
   For complete API reference with all methods and signatures, see :doc:`modding_api`.

Available Events
----------------

Entity Events
~~~~~~~~~~~~~

**ENTITY_SPAWN** = ``"entity_spawn"``

Emitted when any entity (player, monster, item) is created in the game world.

**Event Data:**

* ``entity``: The entity object that was spawned
* ``position``: Tuple of (x, y) coordinates where entity was placed
* ``entity_type``: String identifier for the type of entity ("player", "orc", "troll", etc.)
* ``room``: Room object where entity was spawned (for monsters only)

**ENTITY_MOVE** = ``"entity_move"``

Emitted when any entity moves from one position to another.

**Event Data:**

* ``entity``: The entity that moved
* ``old_position``: Tuple of (x, y) coordinates before movement
* ``new_position``: Tuple of (x, y) coordinates after movement
* ``is_player``: Boolean indicating if the moving entity is the player
* ``movement``: Tuple of (dx, dy) movement delta

**ENTITY_DEATH** = ``"entity_death"``

Emitted when any entity dies or is destroyed.

**Event Data:**

* ``entity``: The entity that died
* ``killer``: Entity responsible for the death (if applicable)
* ``position``: Tuple of (x, y) coordinates where death occurred
* ``cause``: String describing cause of death ("combat", "trap", etc.)

Combat Events
~~~~~~~~~~~~~

**COMBAT_START** = ``"combat_start"``

Emitted when combat begins between two entities. This event is **cancellable**.

**Event Data:**

* ``attacker``: Entity initiating the attack
* ``defender``: Entity being attacked
* ``position``: Tuple of (x, y) coordinates where combat occurs

**Cancellable**: Yes - prevents the combat from occurring

**COMBAT_HIT** = ``"combat_hit"``

Emitted when an attack successfully hits and deals damage.

**Event Data:**

* ``attacker``: Entity that dealt the damage
* ``defender``: Entity that received damage
* ``damage``: Amount of damage dealt
* ``original_hp``: Defender's HP before taking damage

Game Flow Events
~~~~~~~~~~~~~~~~

**TURN_START** = ``"turn_start"``

Emitted at the beginning of each game turn.

**Event Data:**

* ``player``: The player entity
* ``turn_count``: Current turn number (starting from 0)

**TURN_END** = ``"turn_end"``

   Emitted when the player completes a turn-consuming action.

   **Event Data:**

   * ``player``: The player entity
   * ``turn_count``: Turn number that just completed

World Events
~~~~~~~~~~~~

**LEVEL_GENERATE** = ``"level_generate"``

Emitted when a new dungeon level is generated.

**Event Data:**

* ``map``: The GameMap object containing the generated level
* ``player_start``: Tuple of (x, y) coordinates where player will start
* ``rooms``: List of Room objects that were generated

Player Events
~~~~~~~~~~~~~

**PLAYER_DEATH** = ``"player_death"``

Emitted when the player character dies (game over condition).

**Event Data:**

* ``entity``: The player entity
* ``position``: Tuple of (x, y) coordinates where death occurred
* ``cause``: String describing cause of death

Writing Your First Mod
-----------------------

Here's a simple example of a mod that tracks player movement and shows messages:

.. code-block:: python

   from yendoria.modding import EventBus, EventType, GameEvent

   class MovementTrackerMod:
       def __init__(self, event_bus: EventBus):
           self.event_bus = event_bus
           self.movement_count = 0

           # Subscribe to player movement events
           self.event_bus.subscribe(EventType.ENTITY_MOVE, self.on_player_move)

       def on_player_move(self, event: GameEvent) -> None:
           # Only track player movement
           if event.data.get("is_player", False):
               self.movement_count += 1

               # Show a message every 10 moves
               if self.movement_count % 10 == 0:
                   print(f"You have taken {self.movement_count} steps!")

Event Handler Best Practices
-----------------------------

Performance Guidelines
~~~~~~~~~~~~~~~~~~~~~~

* **Keep handlers lightweight**: Event handlers should execute quickly (< 1ms recommended)
* **Use async for heavy operations**: For computationally expensive tasks, consider async handlers
* **Cache frequently accessed data**: Don't recompute the same values in every event
* **Batch similar operations**: Group related changes together when possible

Error Handling
~~~~~~~~~~~~~~

* **Handle exceptions gracefully**: Uncaught exceptions in event handlers are logged but don't crash the game
* **Validate event data**: Always check that expected data fields exist before using them
* **Provide fallback behavior**: Design your mod to work even if some events are missing data

Type Safety
~~~~~~~~~~~

* **Use type hints**: All modding APIs provide full type annotations
* **Import from the public API**: Use ``from yendoria.modding import ...`` for stable interfaces
* **Check event data types**: Event data is typed as ``dict[str, Any]`` so validate types when needed

.. code-block:: python

   def on_entity_move(self, event: GameEvent) -> None:
       # Good: Type-safe event data access
       entity = event.data.get("entity")
       if entity is None:
           return

       position = event.data.get("new_position")
       if not isinstance(position, tuple) or len(position) != 2:
           return

       x, y = position
       # Now safely use x, y coordinates

Event Cancellation
-------------------

Some events can be cancelled to prevent the associated game action from occurring. Currently, the following events support cancellation:

* ``COMBAT_START``: Prevent combat from beginning

To cancel an event, call the ``cancel()`` method on the event object:

.. code-block:: python

   def on_combat_start(self, event: GameEvent) -> None:
       attacker = event.data.get("attacker")
       defender = event.data.get("defender")

       # Prevent combat if attacker has special "pacifist" status
       if hasattr(attacker, "is_pacifist") and attacker.is_pacifist:
           event.cancel()
           print("The pacifist refuses to fight!")

.. warning::
   Only attempt to cancel events that are marked as cancellable. Check the event documentation to see which events support cancellation.

Debugging and Development
-------------------------

Event History
~~~~~~~~~~~~~

The event bus maintains a history of recent events for debugging purposes:

.. code-block:: python

   # Get all recent events
   history = event_bus.get_event_history()

   # Get only movement events
   movement_history = event_bus.get_event_history(EventType.ENTITY_MOVE)

Event Source Tracking
~~~~~~~~~~~~~~~~~~~~~~

Events include a ``source`` field indicating what triggered them:

.. code-block:: python

   def debug_handler(self, event: GameEvent) -> None:
       print(f"Event {event.type} from {event.source}")

Common Patterns
---------------

Stat Tracking
~~~~~~~~~~~~~

Track game statistics by listening to relevant events:

.. code-block:: python

   class StatTracker:
       def __init__(self, event_bus: EventBus):
           self.combat_count = 0
           self.steps_taken = 0
           self.monsters_killed = 0

           event_bus.subscribe(EventType.COMBAT_START, self.on_combat)
           event_bus.subscribe(EventType.ENTITY_MOVE, self.on_movement)
           event_bus.subscribe(EventType.ENTITY_DEATH, self.on_death)

       def on_combat(self, event: GameEvent) -> None:
           self.combat_count += 1

       def on_movement(self, event: GameEvent) -> None:
           if event.data.get("is_player", False):
               self.steps_taken += 1

       def on_death(self, event: GameEvent) -> None:
           killer = event.data.get("killer")
           if hasattr(killer, "is_player") and killer.is_player:
               self.monsters_killed += 1

Conditional Effects
~~~~~~~~~~~~~~~~~~~

Apply effects based on game state:

.. code-block:: python

   class LuckSystem:
       def __init__(self, event_bus: EventBus):
           self.lucky_turn = False
           event_bus.subscribe(EventType.TURN_START, self.check_luck)
           event_bus.subscribe(EventType.COMBAT_START, self.apply_luck)

       def check_luck(self, event: GameEvent) -> None:
           turn_count = event.data.get("turn_count", 0)
           # Every 13th turn is lucky
           self.lucky_turn = (turn_count % 13 == 0)

       def apply_luck(self, event: GameEvent) -> None:
           if self.lucky_turn:
               print("🍀 Lady Luck smiles upon you!")
               # Could modify combat parameters, cancel enemy attacks, etc.

Technical Reference
-------------------

.. autoclass:: yendoria.modding.EventBus
   :members:
   :undoc-members:

.. autoclass:: yendoria.modding.GameEvent
   :members:
   :undoc-members:

.. autoclass:: yendoria.modding.EventType
   :members:
   :undoc-members:

Current Limitations
-------------------

The modding system is in **Phase 1** and has some current limitations:

* **No mod discovery**: Mods must be manually integrated into the game
* **No data-driven content**: Monster/item definitions are still hardcoded
* **No asset pipeline**: Custom graphics/sounds not yet supported
* **No save compatibility**: Mod data is not persisted in save files
* **No UI modding**: Cannot yet modify game interface elements

See the :doc:`modding_roadmap` for planned features and implementation timeline.

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Event handlers not being called**
   * Verify you're subscribing to the correct event type
   * Check that the event is actually being emitted during gameplay
   * Ensure your handler function signature matches ``(self, event: GameEvent) -> None``

**Type errors with event data**
   * Remember that event data is ``dict[str, Any]`` - always validate types
   * Use ``event.data.get("key")`` instead of ``event.data["key"]`` to avoid KeyError
   * Check the event documentation for expected data fields

**Performance issues**
   * Profile your event handlers to identify slow operations
   * Move heavy computation outside of event handlers
   * Consider using event history instead of tracking state in handlers

**Events being cancelled unexpectedly**
   * Check if other mods are cancelling the same events
   * Verify that only cancellable events are being cancelled
   * Review the order of event handler execution

Getting Help
~~~~~~~~~~~~

* Review the examples in ``examples/mods/event_system_demo.py``
* Check the comprehensive architecture documentation in ``docs/MODDING_ARCHITECTURE.md``
* Examine the core event system implementation in ``src/yendoria/modding/__init__.py``

Future Features
---------------

The modding system will be expanded in future phases:

* **Phase 2**: Data-driven content, mod discovery, registration APIs
* **Phase 3**: Asset pipeline, UI modding, save compatibility
* **Phase 4**: Development tools, mod manager, community features

See :doc:`modding_roadmap` for detailed implementation plans.
