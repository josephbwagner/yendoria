AI System Examples
==================

This section provides practical examples of using the AI system in various scenarios.

Basic Examples
--------------

Creating a Simple Monster
~~~~~~~~~~~~~~~~~~~~~~~~~~

This example shows how to create a basic monster with simple AI behavior:

.. code-block:: python

    from yendoria.components.component_manager import ComponentManager
    from yendoria.components.ai_components import BehaviorTreeComponent, AIState
    from yendoria.systems.ai_manager import AIManager
    from yendoria.systems.config_manager import ConfigManager

    # Initialize managers
    component_manager = ComponentManager()
    config_manager = ConfigManager()
    ai_manager = AIManager(component_manager, config_manager)

    # Create a simple orc
    orc = component_manager.create_entity()

    # Add basic AI behavior
    behavior_component = BehaviorTreeComponent(
        current_state=AIState.PATROL,
        archetype="orc_warrior",
        behavior_tree="simple_aggressive"
    )
    component_manager.add_component(orc.id, behavior_component)

    # Register with AI manager (uses basic AI by default)
    ai_manager.register_entity(orc.id)

    # The orc will now exhibit basic patrol and combat behavior

Creating a Faction Member
~~~~~~~~~~~~~~~~~~~~~~~~~~

This example demonstrates creating an entity with faction relationships:

.. code-block:: python

    from yendoria.components.ai_components import FactionComponent

    # Create a town guard
    guard = component_manager.create_entity()

    # Add faction membership
    faction_component = FactionComponent(
        faction_id="town_guard",
        rank=2,
        loyalty=0.8
    )
    component_manager.add_component(guard.id, faction_component)

    # Add behavior component with guard archetype
    behavior_component = BehaviorTreeComponent(
        current_state=AIState.PATROL,
        archetype="town_guard",
        patrol_points=[(10, 10), (15, 10), (15, 15), (10, 15)]
    )
    component_manager.add_component(guard.id, behavior_component)

    ai_manager.register_entity(guard.id)

Advanced Examples
-----------------

Creating an Intelligent NPC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example shows how to create a complex NPC with memory, personality, and motivations:

.. code-block:: python

    from yendoria.components.ai_components import (
        PersonalityComponent, MemoryComponent, MotivationComponent,
        ReputationComponent
    )

    # Create a merchant NPC
    merchant = component_manager.create_entity()

    # Define personality traits
    personality_component = PersonalityComponent(
        traits={
            "greed": 0.7,
            "friendliness": 0.6,
            "honesty": 0.4,
            "curiosity": 0.3,
            "aggression": 0.1
        },
        preferences={
            "gold": 0.9,
            "information": 0.7,
            "safety": 0.8
        }
    )

    # Add memory system
    memory_component = MemoryComponent(
        max_memories=100,
        importance_threshold=0.3
    )

    # Define motivations
    motivation_component = MotivationComponent(
        goals={
            "profit": 0.8,
            "reputation": 0.6,
            "safety": 0.7
        },
        drives={
            "wealth": 0.9,
            "social_standing": 0.5
        }
    )

    # Add reputation tracking
    reputation_component = ReputationComponent()

    # Add all components
    components = [
        BehaviorTreeComponent(
            current_state=AIState.SOCIAL,
            archetype="merchant",
            behavior_tree="merchant_trading"
        ),
        FactionComponent(faction_id="merchants"),
        personality_component,
        memory_component,
        motivation_component,
        reputation_component
    ]

    for component in components:
        component_manager.add_component(merchant.id, component)

    # Register with advanced AI system
    ai_manager.register_entity(merchant.id, behavior_system="advanced")

Event Handling Examples
-----------------------

Responding to AI Events
~~~~~~~~~~~~~~~~~~~~~~~

This example shows how to handle AI events in your game systems:

.. code-block:: python

    from yendoria.components.ai_events import AIEvent, AIEventType

    def on_ai_event(event: AIEvent) -> None:
        """Handle AI events in the game."""
        if event.event_type == AIEventType.REPUTATION_CHANGED:
            entity_id = event.entity_id
            reputation_data = event.data

            print(f"Entity {entity_id} reputation changed:")
            print(f"  Faction: {reputation_data.get('faction')}")
            print(f"  New standing: {reputation_data.get('standing')}")

        elif event.event_type == AIEventType.MEMORY_STORED:
            entity_id = event.entity_id
            memory_data = event.data

            print(f"Entity {entity_id} stored new memory:")
            print(f"  Content: {memory_data.get('content')}")
            print(f"  Importance: {memory_data.get('importance')}")

    # Register event handler with AI manager
    ai_manager.register_event_handler(AIEventType.REPUTATION_CHANGED, on_ai_event)
    ai_manager.register_event_handler(AIEventType.MEMORY_STORED, on_ai_event)

Triggering AI State Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example demonstrates how to trigger AI state changes from game events:

.. code-block:: python

    def on_combat_start(attacker_id: str, target_id: str) -> None:
        """Handle combat initiation."""
        # Trigger combat state for attacker
        combat_event = AIEvent(
            event_type=AIEventType.BEHAVIOR_STATE_CHANGED,
            entity_id=attacker_id,
            data={
                "old_state": "patrol",
                "new_state": "combat",
                "target": target_id
            },
            timestamp=time.time()
        )
        ai_manager.process_event(combat_event)

        # Nearby allies might join combat
        nearby_allies = get_nearby_faction_members(attacker_id, radius=5)
        for ally_id in nearby_allies:
            ally_event = AIEvent(
                event_type=AIEventType.ALLY_IN_COMBAT,
                entity_id=ally_id,
                data={
                    "ally": attacker_id,
                    "enemy": target_id
                },
                timestamp=time.time()
            )
            ai_manager.process_event(ally_event)

Configuration Examples
----------------------

Custom Archetypes
~~~~~~~~~~~~~~~~~

Example of defining custom AI archetypes in ``config/ai/archetypes.json``:

.. code-block:: json

    {
        "wise_elder": {
            "personality": {
                "wisdom": 0.9,
                "patience": 0.8,
                "aggression": 0.1,
                "curiosity": 0.7,
                "helpfulness": 0.8
            },
            "behavior_tree": "elder_advisor",
            "default_state": "social",
            "faction": "village_elders",
            "memory_capacity": 200,
            "motivations": {
                "knowledge_sharing": 0.9,
                "community_welfare": 0.8,
                "tradition_preservation": 0.7
            }
        },
        "sneaky_thief": {
            "personality": {
                "stealth": 0.9,
                "greed": 0.7,
                "cowardice": 0.6,
                "cunning": 0.8,
                "aggression": 0.3
            },
            "behavior_tree": "thief_opportunist",
            "default_state": "investigate",
            "faction": "thieves_guild",
            "preferred_actions": ["steal", "hide", "flee"],
            "avoid_combat": true
        }
    }

Complex Faction Relationships
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example of defining complex faction relationships in ``config/ai/factions.json``:

.. code-block:: json

    {
        "royal_guards": {
            "name": "Royal Guards",
            "description": "Elite protectors of the crown",
            "relations": {
                "nobility": 0.9,
                "merchants": 0.6,
                "thieves_guild": -0.8,
                "rebels": -0.9,
                "common_folk": 0.3
            },
            "territory": ["castle", "throne_room", "royal_quarters"],
            "hierarchy": {
                "captain": 5,
                "lieutenant": 3,
                "guard": 1
            },
            "shared_goals": ["protect_king", "maintain_order", "enforce_law"]
        },
        "merchants_guild": {
            "name": "Merchants Guild",
            "description": "Trade organization controlling commerce",
            "relations": {
                "royal_guards": 0.6,
                "nobility": 0.7,
                "thieves_guild": -0.4,
                "common_folk": 0.5,
                "bandits": -0.7
            },
            "territory": ["market_square", "trading_post", "warehouse_district"],
            "economic_power": 0.8,
            "shared_goals": ["increase_profits", "protect_trade_routes", "eliminate_competition"]
        }
    }

Integration Examples
--------------------

AI with Combat System
~~~~~~~~~~~~~~~~~~~~~~

This example shows how AI entities participate in combat:

.. code-block:: python

    def process_ai_combat_turn(entity_id: str, combat_system) -> None:
        """Process an AI entity's combat turn."""
        # Get AI components
        behavior = component_manager.get_component(entity_id, BehaviorTreeComponent)
        personality = component_manager.get_component(entity_id, PersonalityComponent)

        if not behavior:
            return

        # AI makes tactical decisions based on personality
        if personality and personality.traits.get("aggression", 0.5) > 0.7:
            # Aggressive AI prefers direct attacks
            action = combat_system.get_best_attack_action(entity_id)
        elif personality and personality.traits.get("cunning", 0.5) > 0.6:
            # Cunning AI looks for tactical advantages
            action = combat_system.get_tactical_action(entity_id)
        else:
            # Default to balanced approach
            action = combat_system.get_balanced_action(entity_id)

        # Execute the chosen action
        combat_system.execute_action(entity_id, action)

AI with Dialogue System
~~~~~~~~~~~~~~~~~~~~~~~

This example demonstrates AI entities in conversations:

.. code-block:: python

    def generate_ai_dialogue(speaker_id: str, listener_id: str, topic: str) -> str:
        """Generate contextual dialogue based on AI personality and memory."""
        # Get AI components
        personality = component_manager.get_component(speaker_id, PersonalityComponent)
        memory = component_manager.get_component(speaker_id, MemoryComponent)
        reputation = component_manager.get_component(speaker_id, ReputationComponent)

        # Check relationship with listener
        relationship = 0.5  # Default neutral
        if reputation:
            relationship = reputation.get_faction_standing(listener_id)

        # Adjust dialogue based on personality and relationship
        if personality:
            friendliness = personality.traits.get("friendliness", 0.5)
            if relationship > 0.7 and friendliness > 0.6:
                tone = "friendly"
            elif relationship < 0.3 or friendliness < 0.3:
                tone = "hostile"
            else:
                tone = "neutral"
        else:
            tone = "neutral"

        # Check relevant memories
        relevant_memories = []
        if memory:
            relevant_memories = memory.search_memories(topic, listener_id)

        # Generate dialogue based on context
        dialogue = dialogue_system.generate_response(
            speaker_id=speaker_id,
            topic=topic,
            tone=tone,
            memories=relevant_memories,
            relationship=relationship
        )

        return dialogue

Performance Optimization Examples
---------------------------------

Selective AI Updates
~~~~~~~~~~~~~~~~~~~~

This example shows how to optimize AI performance by updating different entities at different frequencies:

.. code-block:: python

    class OptimizedAIManager:
        def __init__(self):
            self.high_priority_entities = set()  # Important NPCs
            self.medium_priority_entities = set()  # Regular NPCs
            self.low_priority_entities = set()   # Background entities
            self.update_counter = 0

        def update(self, delta_time: float) -> None:
            """Update AI entities with different frequencies."""
            self.update_counter += 1

            # High priority: Update every frame
            for entity_id in self.high_priority_entities:
                self.update_entity_ai(entity_id, delta_time)

            # Medium priority: Update every 3 frames
            if self.update_counter % 3 == 0:
                for entity_id in self.medium_priority_entities:
                    self.update_entity_ai(entity_id, delta_time * 3)

            # Low priority: Update every 10 frames
            if self.update_counter % 10 == 0:
                for entity_id in self.low_priority_entities:
                    self.update_entity_ai(entity_id, delta_time * 10)

Component Optimization
~~~~~~~~~~~~~~~~~~~~~~

This example shows how to minimize component overhead:

.. code-block:: python

    def create_optimized_monster(monster_type: str):
        """Create a monster with minimal necessary components."""
        monster = component_manager.create_entity()

        if monster_type == "simple_guard":
            # Only basic components for simple behavior
            components = [
                BehaviorTreeComponent(
                    current_state=AIState.PATROL,
                    archetype="simple_guard"
                )
            ]
        elif monster_type == "elite_boss":
            # Full component set for complex behavior
            components = [
                BehaviorTreeComponent(archetype="boss_ai"),
                PersonalityComponent(traits={"aggression": 0.9}),
                MemoryComponent(max_memories=50),
                FactionComponent(faction_id="dungeon_lords"),
                ReputationComponent()
            ]
        else:
            # Balanced set for regular NPCs
            components = [
                BehaviorTreeComponent(archetype=monster_type),
                PersonalityComponent(),
                FactionComponent(faction_id="monsters")
            ]

        for component in components:
            component_manager.add_component(monster.id, component)

        return monster

See Also
--------

* :doc:`ai_overview` - High-level AI system architecture and concepts
* :doc:`ai_api` - Complete API documentation for all AI classes and modules
* :doc:`modding_api` - Information on extending the AI system through mods
