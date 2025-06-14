Modding Quick Start
===================

This guide will get you creating mods for Yendoria in just a few minutes. If you're new to modding or want a comprehensive tutorial, see the :doc:`modding_tutorial`.

Installation & Setup
---------------------

1. **Ensure Yendoria is Working**::

    poetry install
    poetry run python -m yendoria

2. **Create Your Mod Directory**::

    mkdir my_mods
    cd my_mods

3. **Test the Event System**::

    poetry run python examples/mods/event_system_demo.py

Your First Mod in 5 Minutes
----------------------------

Let's create a simple mod that adds flavor text to the game.

**Step 1: Create the Mod File**

Create ``atmosphere_mod.py``:

.. code-block:: python

   from yendoria.modding import EventBus, EventType, GameEvent
   import random

   class AtmosphereMod:
       """Adds atmospheric flavor text to the game."""

       def __init__(self, event_bus: EventBus):
           self.event_bus = event_bus
           self.event_bus.subscribe(EventType.LEVEL_GENERATE, self.on_level_generate)
           self.event_bus.subscribe(EventType.COMBAT_START, self.on_combat_start)
           self.event_bus.subscribe(EventType.ENTITY_DEATH, self.on_entity_death)

       def on_level_generate(self, event: GameEvent) -> None:
           """Add atmospheric descriptions to new levels."""
           atmospheres = [
               "🌫️  A damp mist clings to the dungeon walls...",
               "🔥 The air shimmers with heat from unknown sources.",
               "❄️  A bone-chilling cold permeates this level.",
               "🌟 Strange lights flicker in the darkness.",
               "💀 The stench of death hangs heavy here."
           ]
           print(random.choice(atmospheres))

       def on_combat_start(self, event: GameEvent) -> None:
           """Add dramatic combat descriptions."""
           combat_lines = [
               "⚔️  Steel rings against claw!",
               "🛡️  Battle is joined in the depths!",
               "⚡ Lightning-quick strikes fill the air!",
               "🔥 The fury of combat erupts!"
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
                   f"🌪️  {entity.name} is vanquished in a swirl of dust."
               ]
               print(random.choice(death_lines))

**Step 2: Test Your Mod**

.. code-block:: python

   # test_atmosphere.py
   if __name__ == "__main__":
       from yendoria.modding import EventBus, EventType
       from atmosphere_mod import AtmosphereMod

       # Create event bus and mod
       event_bus = EventBus()
       mod = AtmosphereMod(event_bus)

       # Test level generation
       print("🧪 Testing level generation...")
       event_bus.emit_simple(EventType.LEVEL_GENERATE, {"rooms": []})

       # Test combat
       print("\\n🧪 Testing combat...")
       event_bus.emit_simple(EventType.COMBAT_START, {
           "attacker": type('Player', (), {})(),
           "defender": type('Orc', (), {})()
       })

       # Test death
       print("\\n🧪 Testing death...")
       event_bus.emit_simple(EventType.ENTITY_DEATH, {
           "entity": type('Orc', (), {"name": "Fierce Orc"})()
       })

       print("\\n✅ Atmosphere mod test complete!")

Run your test::

    python test_atmosphere.py

**Step 3: Integrate Into Game**

To use your mod in the actual game, you would need to integrate it into the game engine. This is currently a manual process (automatic mod loading is planned for Phase 2):

.. code-block:: python

   # In the game's main initialization code:
   from atmosphere_mod import AtmosphereMod

   # After creating the engine:
   atmosphere_mod = AtmosphereMod(engine.event_bus)

Common Mod Patterns
-------------------

Statistics Tracking
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class StatsTracker:
       def __init__(self, event_bus: EventBus):
           self.kills = 0
           self.steps = 0
           event_bus.subscribe(EventType.ENTITY_DEATH, self.count_kills)
           event_bus.subscribe(EventType.ENTITY_MOVE, self.count_steps)

       def count_kills(self, event: GameEvent) -> None:
           killer = event.data.get("killer")
           if hasattr(killer, "is_player") and killer.is_player:
               self.kills += 1

       def count_steps(self, event: GameEvent) -> None:
           if event.data.get("is_player", False):
               self.steps += 1

Gameplay Modification
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class LuckSystem:
       def __init__(self, event_bus: EventBus):
           self.luck = 0
           event_bus.subscribe(EventType.COMBAT_START, self.apply_luck)

       def apply_luck(self, event: GameEvent) -> None:
           attacker = event.data.get("attacker")
           if hasattr(attacker, "is_player") and attacker.is_player:
               if self.luck < -50:
                   # Very unlucky - sometimes avoid combat
                   if random.random() < 0.1:
                       event.cancel()
                       print("🍀 You stumble and avoid the fight!")

Event Cancellation
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def peaceful_mode(event: GameEvent) -> None:
       """Cancel all combat events for peaceful gameplay."""
       event.cancel()
       print("☮️  Combat avoided - peaceful mode active!")

   # Register the handler
   event_bus.subscribe(EventType.COMBAT_START, peaceful_mode)

Available Events Reference
--------------------------

**Entity Events:**
- ``ENTITY_SPAWN`` - When entities are created
- ``ENTITY_MOVE`` - When entities move
- ``ENTITY_DEATH`` - When entities die

**Combat Events:**
- ``COMBAT_START`` - Combat begins (cancellable)
- ``COMBAT_HIT`` - Successful attacks

**Game Flow Events:**
- ``TURN_START`` - Beginning of each turn
- ``TURN_END`` - End of each turn

**World Events:**
- ``LEVEL_GENERATE`` - New level created

For complete event details, see :doc:`modding`.

Next Steps
----------

* **Learn More**: Read the :doc:`modding_tutorial` for comprehensive examples
* **Advanced Features**: Check the :doc:`modding_roadmap` for upcoming capabilities
* **Technical Details**: See :doc:`modding` for complete API documentation
* **Examples**: Study ``examples/mods/event_system_demo.py`` for practical patterns

Troubleshooting
---------------

**Mod not responding to events?**
   - Check that you're subscribing to the correct event type
   - Verify the event is actually being emitted during gameplay
   - Ensure your handler function signature is correct: ``(self, event: GameEvent) -> None``

**Type errors?**
   - Remember event data is ``dict[str, Any]`` - always validate types
   - Use ``event.data.get("key")`` instead of ``event.data["key"]``
   - Check the event documentation for expected data fields

**Need help?**
   - Review the comprehensive examples in the tutorial
   - Check the modding architecture documentation
   - Examine the core event system implementation
