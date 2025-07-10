# AI System Architecture Design

## Overview

This document outlines the design for a comprehensive, extensible AI system for Yendoria that supports dynamic factions, emergent world events, and deep NPC behavior. The system is built around modularity, event-driven communication, and data-driven configuration to maximize extensibility and modding support.

## Core Design Principles

### 1. **Event-Driven Architecture**
- All AI systems communicate through the existing EventBus
- Loose coupling between systems
- Easy to add new systems without modifying existing ones

### 2. **Component-Based Design**
- Each AI capability is a separate component
- Components can be mixed and matched
- Clear separation of concerns

### 3. **Data-Driven Configuration**
- AI behaviors defined in external configuration files
- Hot-reloadable configurations for rapid iteration
- Version-controlled AI definitions

### 4. **Plugin Architecture**
- Clear interfaces for extending AI systems
- Dependency injection for system composition
- Runtime registration of new AI components

## System Dependencies

### Required Foundation Systems (Implement First)

1. **Enhanced Entity-Component System**
   - Ability to attach AI components to entities
   - Component lifecycle management
   - Query system for finding entities with specific AI components

2. **Configuration Management System**
   - Loading and validation of AI configuration files
   - Hot-reloading support
   - Schema validation for AI definitions

3. **Persistence System**
   - Save/load AI state and memories
   - World state persistence
   - Incremental saves for large world states

4. **Turn/Time Management System**
   - AI tick scheduling
   - Variable time scales (real-time vs turn-based)
   - Priority-based AI processing

5. **Spatial Indexing System**
   - Efficient queries for "entities near X"
   - Line-of-sight calculations
   - Territory/zone management

## Core AI Architecture

### AI Manager Hub

The central coordinator that manages all AI systems and provides the plugin interface.

```python
class AIManager:
    """Central hub for all AI systems"""

    def __init__(self, event_bus: EventBus, config_manager: ConfigManager):
        self.event_bus = event_bus
        self.config_manager = config_manager
        self.ai_systems: Dict[str, AISystem] = {}
        self.ai_components: Dict[str, Type[AIComponent]] = {}
        self.tick_scheduler = AITickScheduler()

    def register_system(self, system: AISystem) -> None:
        """Register an AI system for management"""

    def register_component(self, component_type: Type[AIComponent]) -> None:
        """Register an AI component type for entities"""

    def tick(self, delta_time: float) -> None:
        """Process AI systems based on priority and scheduling"""

    def reload_configurations(self) -> None:
        """Hot-reload all AI configurations"""
```

### Base Interfaces

```python
class AISystem(ABC):
    """Base interface for all AI systems"""

    @property
    @abstractmethod
    def name(self) -> str:
        """System identifier"""

    @property
    @abstractmethod
    def dependencies(self) -> List[str]:
        """Other systems this depends on"""

    @abstractmethod
    def initialize(self, context: AIContext) -> None:
        """Initialize the system"""

    @abstractmethod
    def tick(self, delta_time: float) -> None:
        """Process system logic"""

    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup resources"""

class AIComponent(ABC):
    """Base interface for AI components attached to entities"""

    @abstractmethod
    def process(self, entity: Entity, context: AIContext) -> None:
        """Process AI behavior for this entity"""

    @abstractmethod
    def can_attach_to(self, entity: Entity) -> bool:
        """Check if this component can be attached to entity"""
```

## Individual AI Systems

### 1. Faction AI System

Manages faction-level politics, goals, and relationships.

**Configuration Schema:**
```json
{
  "factions": {
    "cult_of_flame": {
      "name": "Cult of the Hollow Flame",
      "personality": {
        "aggression": 0.8,
        "cunning": 0.9,
        "loyalty": 0.7,
        "expansionism": 0.6
      },
      "goals": [
        {
          "type": "control_territory",
          "target": "shrine_zones",
          "priority": 0.9
        },
        {
          "type": "eliminate_faction",
          "target": "silver_wardens",
          "priority": 0.6
        }
      ],
      "relationships": {
        "silver_wardens": -0.8,
        "ratkin_tribes": 0.2
      },
      "resources": {
        "military_strength": 75,
        "economic_power": 60,
        "magical_influence": 90
      }
    }
  }
}
```

**Extension Points:**
- Custom faction goal types
- New personality traits
- Custom relationship modifiers
- Faction-specific events

### 2. World State System

Tracks and manages world changes, territory control, and environmental effects.

**Configuration Schema:**
```json
{
  "world_zones": {
    "obsidian_catacombs": {
      "controller": "cult_of_flame",
      "corruption_level": 0.7,
      "environmental_effects": ["dark_magic_surge"],
      "strategic_value": 0.8,
      "connections": ["ember_shrine", "shadow_depths"]
    }
  },
  "global_events": {
    "blood_moon": {
      "frequency": "every_100_turns",
      "effects": [
        {"type": "boost_undead", "magnitude": 0.5},
        {"type": "reduce_visibility", "magnitude": 0.3}
      ]
    }
  }
}
```

**Extension Points:**
- Custom zone types and effects
- New environmental systems
- Custom global events
- Territory control mechanics

### 3. Agent Behavior System

Individual entity AI using personality-driven behavior trees.

**Configuration Schema:**
```json
{
  "agent_archetypes": {
    "cult_zealot": {
      "base_personality": {
        "aggression": 0.9,
        "caution": 0.2,
        "curiosity": 0.3,
        "loyalty": 0.95
      },
      "behavior_tree": "zealot_combat",
      "faction_allegiance": "cult_of_flame",
      "special_abilities": ["dark_blessing", "fanatical_charge"],
      "loot_preferences": ["artifacts", "magical_items"]
    }
  },
  "behavior_trees": {
    "zealot_combat": {
      "root": {
        "type": "selector",
        "children": [
          {
            "type": "sequence",
            "name": "protect_allies",
            "condition": "allies_in_danger",
            "actions": ["move_to_ally", "defensive_stance"]
          },
          {
            "type": "sequence",
            "name": "aggressive_attack",
            "condition": "enemy_visible",
            "actions": ["cast_buff", "charge_enemy", "melee_attack"]
          },
          {
            "type": "action",
            "name": "patrol",
            "action": "patrol_territory"
          }
        ]
      }
    }
  }
}
```

**Extension Points:**
- Custom behavior tree nodes
- New personality traits
- Custom conditions and actions
- Agent-specific abilities

### 4. Memory and Knowledge System

Manages what entities know and how information spreads.

**Configuration Schema:**
```json
{
  "knowledge_types": {
    "enemy_sighting": {
      "decay_rate": 0.1,
      "reliability_base": 0.9,
      "spread_chance": 0.7,
      "importance": 0.8
    },
    "player_reputation": {
      "decay_rate": 0.05,
      "reliability_base": 1.0,
      "spread_chance": 0.9,
      "importance": 0.9
    }
  },
  "gossip_networks": {
    "cult_of_flame": {
      "internal_spread_rate": 0.9,
      "external_spread_rate": 0.2,
      "bias_modifier": 0.8
    }
  }
}
```

### 5. Quest Generation System

Creates dynamic quests based on world state and faction needs.

**Configuration Schema:**
```json
{
  "quest_templates": {
    "faction_war_sabotage": {
      "triggers": [
        {
          "type": "faction_conflict",
          "participants": ["any", "any"],
          "conflict_type": "territorial_war"
        }
      ],
      "requirements": {
        "player_reputation": {"min": -50, "with_faction": "any_participant"},
        "world_state": {"active_conflicts": {"min": 1}}
      },
      "grammar": {
        "description": "Sabotage the {enemy_faction}'s {target_type} to aid the {ally_faction}",
        "objectives": [
          {
            "type": "destroy",
            "target": "{enemy_faction}.{strategic_asset}",
            "stealth_required": true
          }
        ]
      },
      "rewards": {
        "reputation": {"ally_faction": 15, "enemy_faction": -20},
        "world_effects": ["weaken_enemy_position"]
      }
    }
  }
}
```

## Modding Interface

### Plugin Discovery

```python
class AIPlugin(ABC):
    """Base class for AI plugins"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin identifier"""

    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version"""

    @abstractmethod
    def register_systems(self, ai_manager: AIManager) -> None:
        """Register AI systems provided by this plugin"""

    @abstractmethod
    def register_components(self, ai_manager: AIManager) -> None:
        """Register AI components provided by this plugin"""
```

### Configuration Extension

Modders can extend configurations by providing additional files:

```
mods/
  advanced_factions/
    ai_config/
      factions/
        shadow_guild.json
        merchant_alliance.json
      archetypes/
        shadow_assassin.json
        merchant_trader.json
      quests/
        trade_war_templates.json
```

### Event Hooks for Modders

```python
# Modders can listen to AI events
@event_handler(EventType.FACTION_RELATIONSHIP_CHANGED)
def on_faction_relationship_changed(event: GameEvent):
    """Custom mod logic for relationship changes"""

@event_handler(EventType.AI_QUEST_GENERATED)
def on_quest_generated(event: GameEvent):
    """Modify or validate generated quests"""
```

## Implementation Roadmap

### Phase 1: Foundation (Required Dependencies)
1. **Enhanced Entity-Component System**
   - Component attachment/detachment
   - Component queries and filtering
   - Lifecycle management

2. **Configuration Management**
   - JSON/YAML configuration loading
   - Schema validation
   - Hot-reloading support

3. **Basic Persistence**
   - Save/load entity states
   - World state persistence
   - AI memory storage

### Phase 2: Core AI Systems
1. **AI Manager Hub**
   - System registration and management
   - Tick scheduling
   - Plugin interface

2. **Faction System**
   - Basic faction definition and goals
   - Simple relationship tracking
   - Territory control

3. **Agent Behavior System**
   - Basic behavior trees
   - Personality traits
   - Simple AI components

### Phase 3: Advanced Features
1. **World State System**
   - Environmental effects
   - Global events
   - Complex territory mechanics

2. **Memory and Knowledge System**
   - Information propagation
   - Gossip networks
   - Memory decay

3. **Quest Generation System**
   - Template-based generation
   - Dynamic quest creation
   - World-state integration

### Phase 4: Polish and Optimization
1. **Performance Optimization**
   - AI system profiling
   - Batch processing
   - Spatial optimizations

2. **Advanced Modding Support**
   - Visual AI editors
   - Runtime debugging tools
   - Performance monitoring

## Example Mod Implementation

Here's how a modder would add a new faction:

1. **Create faction definition** (`mods/seafaring_raiders/ai_config/factions/sea_raiders.json`):
```json
{
  "sea_raiders": {
    "name": "Seafaring Raiders",
    "personality": {
      "aggression": 0.7,
      "cunning": 0.8,
      "mobility": 0.9,
      "greed": 0.8
    },
    "goals": [
      {
        "type": "raid_settlements",
        "priority": 0.8
      }
    ],
    "special_mechanics": ["amphibious_movement", "ship_combat"]
  }
}
```

2. **Create custom goal type** (`mod_plugin.py`):
```python
class RaidSettlementsGoal(FactionGoal):
    def evaluate_targets(self, faction: Faction, world_state: WorldState) -> List[Target]:
        # Custom logic for finding raid targets
        settlements = world_state.find_settlements(
            exclude_faction=faction,
            min_wealth=100
        )
        return [Target(s, priority=s.wealth * 0.01) for s in settlements]

# Register the goal type
ai_manager.register_goal_type("raid_settlements", RaidSettlementsGoal)
```

This architecture provides a solid foundation for implementing the comprehensive AI system described in the design document while maintaining extensibility and modding support.
