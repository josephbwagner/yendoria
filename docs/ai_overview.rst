AI System Overview
==================

Yendoria features a sophisticated AI system built on a modular, extensible architecture. The AI system provides intelligent behavior for NPCs, monsters, and other entities in the game world.

Architecture
------------

The AI system is built on several key principles:

**Modular Design**
    Different AI systems can be swapped in and out based on requirements. Basic AI for simple creatures, advanced AI for complex NPCs.

**ECS Integration**
    Seamless integration with the Entity Component System, allowing AI to work with any entity that has the required components.

**Event-Driven**
    AI systems respond to events and can generate events for other systems to handle.

**Performance Scalable**
    From lightweight basic AI to complex advanced AI, choose the right system for your performance needs.

Core Components
---------------

AI Manager
~~~~~~~~~~

The :class:`~yendoria.systems.ai_manager.AIManager` serves as the central hub for all AI operations:

* **Entity Lifecycle Management**: Registers and unregisters AI entities
* **System Coordination**: Manages multiple AI behavior systems
* **Event Distribution**: Routes AI events between systems
* **Configuration Loading**: Handles AI archetypes and faction configurations

AI Behavior Systems
~~~~~~~~~~~~~~~~~~~

AI behavior is implemented through modular systems that implement the :class:`~yendoria.systems.ai_behavior_interface.AIBehaviorSystemInterface`:

**Basic AI System** (:class:`~yendoria.systems.ai_behavior_basic.BasicAIBehaviorSystem`)
    * Lightweight implementation for simple entities
    * Timer-based action selection
    * Minimal component requirements
    * Ideal for background NPCs and ambient life

**Advanced AI System** (:class:`~yendoria.systems.ai_behavior_advanced.AdvancedAIBehaviorSystem`)
    * Sophisticated behavior using personality, memory, and motivations
    * Dynamic reputation system
    * Complex decision-making processes
    * Suitable for important NPCs and complex creatures

AI Components
~~~~~~~~~~~~~

The AI system uses specialized ECS components:

**Core Components**
    * :class:`~yendoria.components.ai_components.BehaviorTreeComponent` - Basic behavior state and timing
    * :class:`~yendoria.components.ai_components.FactionComponent` - Group membership and relations
    * :class:`~yendoria.components.ai_components.PersonalityComponent` - Character traits and preferences

**Advanced Components**
    * :class:`~yendoria.components.ai_components.MemoryComponent` - Long-term memory system
    * :class:`~yendoria.components.ai_components.MotivationComponent` - Goals and drives
    * :class:`~yendoria.components.ai_components.ReputationComponent` - Social standing system

Configuration System
~~~~~~~~~~~~~~~~~~~~~

AI behavior is highly configurable through JSON files:

**Archetypes** (``config/ai/archetypes.json``)
    Pre-defined AI personality and behavior templates for different creature types.

**Factions** (``config/ai/factions.json``)
    Group definitions with relationships, territories, and characteristics.

Event System
~~~~~~~~~~~~

The AI system uses a comprehensive event system (:class:`~yendoria.components.ai_events.AIEvent`) for communication:

* **Behavior Events**: State changes, action completion
* **Social Events**: Reputation changes, faction interactions
* **Combat Events**: Damage, death, threat detection
* **Memory Events**: Information storage and retrieval

Error Handling & Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Robust error handling with the :mod:`~yendoria.systems.ai_error_handling` module:

* **Graceful Degradation**: AI continues functioning even with errors
* **Performance Monitoring**: Tracks AI system performance metrics
* **Debugging Support**: Comprehensive logging and error reporting

Usage Patterns
---------------

Basic AI Setup
~~~~~~~~~~~~~~

For simple entities that need minimal AI:

.. code-block:: python

    # Create entity with basic AI components
    entity = component_manager.create_entity()

    # Add required components
    behavior_component = BehaviorTreeComponent(
        current_state=AIState.IDLE,
        archetype="basic_monster"
    )
    component_manager.add_component(entity.id, behavior_component)

    # Register with AI manager
    ai_manager.register_entity(entity.id, "basic")

Advanced AI Setup
~~~~~~~~~~~~~~~~~

For complex NPCs with full AI capabilities:

.. code-block:: python

    # Create entity with advanced AI components
    entity = component_manager.create_entity()

    # Add comprehensive AI components
    behavior_component = BehaviorTreeComponent(
        current_state=AIState.IDLE,
        archetype="intelligent_npc"
    )
    personality_component = PersonalityComponent(
        traits={"aggression": 0.3, "curiosity": 0.8}
    )
    memory_component = MemoryComponent()
    faction_component = FactionComponent(faction_id="town_guard")

    component_manager.add_component(entity.id, behavior_component)
    component_manager.add_component(entity.id, personality_component)
    component_manager.add_component(entity.id, memory_component)
    component_manager.add_component(entity.id, faction_component)

    # Register with AI manager
    ai_manager.register_entity(entity.id, "advanced")

Configuration Examples
~~~~~~~~~~~~~~~~~~~~~~

**Archetype Definition**:

.. code-block:: json

    {
        "guard": {
            "personality": {
                "aggression": 0.6,
                "alertness": 0.9,
                "loyalty": 0.8
            },
            "behavior_tree": "guard_patrol",
            "default_state": "patrol",
            "faction": "town_guard"
        }
    }

**Faction Definition**:

.. code-block:: json

    {
        "town_guard": {
            "name": "Town Guard",
            "description": "Protectors of the town",
            "relations": {
                "merchants": 0.8,
                "bandits": -0.9
            },
            "territory": ["town_square", "main_gate"]
        }
    }

Performance Considerations
--------------------------

The AI system is designed with performance in mind:

**Choosing the Right System**
    * Use Basic AI for background entities and simple creatures
    * Reserve Advanced AI for important NPCs and complex interactions

**Update Frequency**
    * AI systems can be updated at different frequencies
    * Critical entities get more frequent updates

**Component Optimization**
    * Only add components that are actually needed
    * Memory and reputation components have the highest overhead

**Configuration Caching**
    * Archetypes and faction data are cached for fast access
    * Configuration changes require restart for optimal performance

Integration with Game Systems
-----------------------------

The AI system integrates seamlessly with other game systems:

**Combat System**
    AI entities can participate in combat, making tactical decisions based on their personality and faction

**Dialogue System**
    Advanced AI entities can engage in dynamic conversations based on their memory and reputation

**Quest System**
    AI entities can serve as quest givers, providing tasks based on faction relationships and current game state

**Economic System**
    Merchant AI can adjust prices based on reputation and faction standing

See Also
--------

* :doc:`ai_api` - Complete API documentation for all AI classes and modules
* :doc:`ai_examples` - Practical examples and use cases
* :doc:`modding_api` - Information on extending the AI system through mods
