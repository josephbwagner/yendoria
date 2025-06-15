"""
AI-specific components for the Entity Component System.

This module provides components specifically designed for AI systems,
including faction membership, personality traits, memory, and behavior trees.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from .component import Component


@dataclass
class FactionConfig:
    """Configuration for faction-specific attributes."""

    name: str | None = None
    description: str | None = None
    relations: dict[str, float] = field(default_factory=dict)
    territory: list[str] = field(default_factory=list)


class AIState(Enum):
    """AI behavior states."""

    IDLE = "idle"
    PATROL = "patrol"
    PURSUE = "pursue"
    FLEE = "flee"
    INVESTIGATE = "investigate"
    COMBAT = "combat"
    RITUAL = "ritual"
    SOCIAL = "social"


@dataclass
class Memory:
    """A single memory stored by an AI agent."""

    content: str
    timestamp: float
    importance: float  # 0.0 to 1.0
    reliability: float  # 0.0 to 1.0 (how accurate the memory is)
    associated_entity: str | None = None
    location: tuple[int, int] | None = None
    fade_rate: float = 0.01  # How quickly this memory fades

    # For behavior system compatibility
    episodic_memories: dict[str, list[dict[str, Any]]] = None  # type: ignore[assignment]

    def __post_init__(self):
        if self.episodic_memories is None:
            self.episodic_memories = {}


class FactionComponent(Component):
    """
    Component that marks an entity as belonging to a specific faction.

    This is used by the Faction AI Manager to coordinate group behavior.
    """

    def __init__(
        self,
        faction_id: str,
        rank: str = "member",
        loyalty: float = 1.0,
        config: FactionConfig | None = None,
    ):
        """
        Initialize faction membership.

        Args:
            faction_id: ID of the faction this entity belongs to
            rank: Rank within the faction (member, leader, etc.)
            loyalty: Loyalty to the faction (0.0 to 1.0)
            config: Optional faction configuration with extended attributes
        """
        super().__init__()
        self.faction_id = faction_id
        self.rank = rank
        self.loyalty = loyalty
        self.reputation: dict[str, float] = {}  # Reputation with other factions

        # Apply configuration or use defaults
        faction_config = config or FactionConfig()
        self.name = faction_config.name or faction_id
        self.description = faction_config.description or f"Faction {faction_id}"
        self.relations: dict[str, float] = faction_config.relations.copy()
        self.territory: list[str] = faction_config.territory.copy()


class PersonalityComponent(Component):
    """
    Component that defines an AI entity's personality traits.

    These traits influence decision-making in behavior trees and utility AI.
    """

    def __init__(self, traits: dict[str, float] | None = None):
        """
        Initialize personality traits.

        Args:
            traits: Dictionary of personality trait values (0.0 to 1.0)
        """
        super().__init__()

        # Default personality traits
        default_traits = {
            "aggression": 0.5,
            "caution": 0.5,
            "curiosity": 0.5,
            "loyalty": 0.5,
            "intelligence": 0.5,
            "greed": 0.5,
            "empathy": 0.5,
            "ambition": 0.5,
            "restlessness": 0.5,  # For behavior system compatibility
            "charisma": 0.5,  # For behavior system compatibility
        }

        self.traits = default_traits.copy()
        if traits:
            self.traits.update(traits)

    def get_trait(self, trait_name: str, default: float = 0.5) -> float:
        """Get a personality trait value."""
        return self.traits.get(trait_name, default)

    def set_trait(self, trait_name: str, value: float) -> None:
        """Set a personality trait value (clamped to 0.0-1.0)."""
        self.traits[trait_name] = max(0.0, min(1.0, value))

    def modify_trait(self, trait_name: str, delta: float) -> None:
        """Modify a personality trait by a delta amount."""
        current = self.get_trait(trait_name)
        self.set_trait(trait_name, current + delta)


class MemoryComponent(Component):
    """
    Component that stores an AI entity's memories and knowledge.

    Used by the Memory & Knowledge System for learning and rumor propagation.
    """

    def __init__(self, max_memories: int = 100):
        """
        Initialize memory storage.

        Args:
            max_memories: Maximum number of memories to store
        """
        super().__init__()
        self.memories: list[Memory] = []
        self.knowledge: dict[str, Any] = {}
        self.max_memories = max_memories

        # Social knowledge
        self.known_entities: dict[str, dict[str, Any]] = {}
        self.relationships: dict[str, float] = {}  # Entity ID -> relationship strength

    def add_memory(self, memory: Memory) -> None:
        """Add a new memory, removing oldest if at capacity."""
        self.memories.append(memory)

        # Remove oldest memories if over capacity
        if len(self.memories) > self.max_memories:
            # Sort by importance and age, keep the most important/recent
            self.memories.sort(key=lambda m: (m.importance, -m.timestamp))
            self.memories = self.memories[-self.max_memories :]

    def get_memories_about(self, entity_id: str) -> list[Memory]:
        """Get all memories related to a specific entity."""
        return [m for m in self.memories if m.associated_entity == entity_id]

    def get_memories_at_location(self, location: tuple[int, int]) -> list[Memory]:
        """Get all memories from a specific location."""
        return [m for m in self.memories if m.location == location]

    def forget_old_memories(self, current_time: float) -> None:
        """Remove memories that have faded below relevance threshold."""
        threshold = 0.1
        self.memories = [
            m
            for m in self.memories
            if m.importance - (m.fade_rate * (current_time - m.timestamp)) > threshold
        ]

    def set_relationship(self, entity_id: str, strength: float) -> None:
        """Set relationship strength with another entity (-1.0 to 1.0)."""
        self.relationships[entity_id] = max(-1.0, min(1.0, strength))

    def get_relationship(self, entity_id: str) -> float:
        """Get relationship strength with another entity."""
        return self.relationships.get(entity_id, 0.0)


class BehaviorTreeComponent(Component):
    """
    Component that holds an AI entity's behavior tree configuration.

    Used by the Agent Behavior System for decision-making.
    """

    def __init__(
        self,
        tree_config: str | dict | None = None,
        *,
        tree_data: dict | None = None,
    ):
        """
        Initialize behavior tree.

        Args:
            tree_config: Either a tree config ID (string) or a tree definition (dict)
            tree_data: Alternative parameter name for tree definition
                (for compatibility)
        """
        super().__init__()

        # Type annotations for attributes
        self.tree_config_id: str | None
        self.tree_definition: dict | None

        # Handle tree_data parameter for compatibility
        if tree_data is not None:
            tree_config = tree_data

        if isinstance(tree_config, str):
            self.tree_config_id = tree_config
            self.tree_definition = None  # Will be loaded by behavior system
        elif isinstance(tree_config, dict):
            self.tree_config_id = None
            self.tree_definition = tree_config
        else:
            self.tree_config_id = None
            self.tree_definition = None

        self.current_state = AIState.IDLE
        self.blackboard: dict[str, Any] = {}  # Working memory for behavior tree
        self.last_update_time = 0.0

        # For behavior system compatibility
        self.tree_data = self.tree_definition  # Alias for compatibility
        self.current_action: str | None = None  # For behavior system compatibility

    def set_blackboard_value(self, key: str, value: Any) -> None:
        """Set a value in the behavior tree's blackboard."""
        self.blackboard[key] = value

    def get_blackboard_value(self, key: str, default: Any = None) -> Any:
        """Get a value from the behavior tree's blackboard."""
        return self.blackboard.get(key, default)

    def clear_blackboard(self) -> None:
        """Clear all blackboard values."""
        self.blackboard.clear()


class ReputationComponent(Component):
    """
    Component that tracks an entity's reputation with various factions and individuals.

    Used by the Reputation Engine and Faction AI Manager.
    """

    def __init__(self):
        """Initialize reputation tracking."""
        super().__init__()

        # Reputation with factions (-1.0 to 1.0)
        self.faction_reputation: dict[str, float] = {}

        # Reputation with individual entities (-1.0 to 1.0)
        self.individual_reputation: dict[str, float] = {}

        # Titles and standing
        self.titles: list[str] = []
        self.standing_modifiers: dict[str, float] = {}

        # For behavior system compatibility
        self.faction_standings = self.faction_reputation  # Alias for compatibility

    def get_faction_reputation(self, faction_id: str) -> float:
        """Get reputation with a specific faction."""
        return self.faction_reputation.get(faction_id, 0.0)

    def set_faction_reputation(self, faction_id: str, value: float) -> None:
        """Set reputation with a faction (-1.0 to 1.0)."""
        self.faction_reputation[faction_id] = max(-1.0, min(1.0, value))

    def modify_faction_reputation(self, faction_id: str, delta: float) -> None:
        """Modify reputation with a faction by a delta amount."""
        current = self.get_faction_reputation(faction_id)
        self.set_faction_reputation(faction_id, current + delta)

    def get_individual_reputation(self, entity_id: str) -> float:
        """Get reputation with a specific individual."""
        return self.individual_reputation.get(entity_id, 0.0)

    def set_individual_reputation(self, entity_id: str, value: float) -> None:
        """Set reputation with an individual (-1.0 to 1.0)."""
        self.individual_reputation[entity_id] = max(-1.0, min(1.0, value))

    def add_title(self, title: str) -> None:
        """Add a reputation title."""
        if title not in self.titles:
            self.titles.append(title)

    def remove_title(self, title: str) -> None:
        """Remove a reputation title."""
        if title in self.titles:
            self.titles.remove(title)


class MotivationComponent(Component):
    """
    Component that defines an AI entity's current motivations and goals.

    Used by Utility AI systems to evaluate and prioritize actions.
    """

    def __init__(self):
        """Initialize motivations."""
        super().__init__()

        # Current needs (0.0 to 1.0, higher = more urgent)
        self.needs = {
            "survival": 0.0,  # Health, safety
            "social": 0.0,  # Interaction, approval
            "achievement": 0.0,  # Goals, accomplishment
            "curiosity": 0.0,  # Exploration, knowledge
            "comfort": 0.0,  # Rest, resources
        }

        # For behavior system compatibility - separate dicts with survival needs
        self.survival_needs = {
            "hunger": 0.0,
            "safety": 1.0,  # Start with full safety
            "health": 1.0,
            "territory": 0.0,
        }

        self.social_needs = {
            "companionship": 0.0,
            "approval": 0.0,
            "status": 0.0,
        }

        # Current goals with priorities
        self.goals: list[dict[str, Any]] = []

        # Drives that influence behavior
        self.drives = {
            "hunger": 0.0,
            "fear": 0.0,
            "anger": 0.0,
            "fatigue": 0.0,
        }

    def set_need(self, need_name: str, value: float) -> None:
        """Set a need level (0.0 to 1.0)."""
        self.needs[need_name] = max(0.0, min(1.0, value))

    def get_need(self, need_name: str) -> float:
        """Get a need level."""
        return self.needs.get(need_name, 0.0)

    def add_goal(
        self, goal_type: str, target: Any, priority: float, **kwargs: Any
    ) -> None:
        """Add a new goal."""
        goal = {
            "type": goal_type,
            "target": target,
            "priority": priority,
            "created_time": datetime.now().timestamp(),
            **kwargs,
        }
        self.goals.append(goal)

        # Sort goals by priority
        self.goals.sort(key=lambda g: g["priority"], reverse=True)

    def remove_goal(self, goal_type: str, target: Any = None) -> None:
        """Remove goals of a specific type and optionally target."""
        self.goals = [
            g
            for g in self.goals
            if not (
                g["type"] == goal_type and (target is None or g["target"] == target)
            )
        ]

    def get_top_goal(self) -> dict[str, Any] | None:
        """Get the highest priority goal."""
        return self.goals[0] if self.goals else None


class KnowledgeComponent(Component):
    """
    Component that stores structured knowledge about the world.

    Used for faction intelligence, map knowledge, and strategic planning.
    """

    def __init__(self):
        """Initialize knowledge storage."""
        super().__init__()

        # Territorial knowledge
        self.known_zones: dict[str, dict[str, Any]] = {}
        self.zone_control: dict[str, str] = {}  # Zone ID -> Controlling faction

        # Entity knowledge
        self.known_entities: dict[str, dict[str, Any]] = {}

        # Faction intelligence
        self.faction_intel: dict[str, dict[str, Any]] = {}

        # Rumors and unverified information
        self.rumors: list[dict[str, Any]] = []

    def update_zone_knowledge(self, zone_id: str, **properties: Any) -> None:
        """Update knowledge about a zone."""
        if zone_id not in self.known_zones:
            self.known_zones[zone_id] = {}
        self.known_zones[zone_id].update(properties)

    def set_zone_control(self, zone_id: str, faction_id: str) -> None:
        """Update knowledge of zone control."""
        self.zone_control[zone_id] = faction_id

    def get_zone_controller(self, zone_id: str) -> str | None:
        """Get the known controller of a zone."""
        return self.zone_control.get(zone_id)

    def add_rumor(self, content: str, source: str, reliability: float) -> None:
        """Add a rumor to the knowledge base."""
        rumor = {
            "content": content,
            "source": source,
            "reliability": reliability,
            "timestamp": datetime.now().timestamp(),
        }
        self.rumors.append(rumor)

        # Keep only recent rumors
        MAX_RUMORS = 50
        if len(self.rumors) > MAX_RUMORS:
            self.rumors = self.rumors[-MAX_RUMORS:]
