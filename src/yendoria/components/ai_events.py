"""
AI-specific events for the event system.

This module extends the core event system with events specifically
for AI systems, including faction events, behavior changes, and
memory/learning events.
"""

from enum import Enum
from typing import Any

from ..modding import EventType as CoreEventType
from ..modding import GameEvent


class AIEventType(Enum):
    """AI-specific events that can be emitted and handled."""

    # Agent behavior events
    AI_STATE_CHANGED = "ai_state_changed"
    BEHAVIOR_TREE_STARTED = "behavior_tree_started"
    BEHAVIOR_TREE_COMPLETED = "behavior_tree_completed"
    BEHAVIOR_NODE_FAILED = "behavior_node_failed"

    # Faction events
    FACTION_RELATIONSHIP_CHANGED = "faction_relationship_changed"
    FACTION_RELATION_CHANGED = "faction_relationship_changed"  # Alias for compatibility
    FACTION_ALLIANCE_FORMED = "faction_alliance_formed"
    FACTION_WAR_DECLARED = "faction_war_declared"
    FACTION_PEACE_DECLARED = "faction_peace_declared"
    FACTION_BETRAYAL = "faction_betrayal"
    FACTION_TERRITORY_GAINED = "faction_territory_gained"
    FACTION_TERRITORY_LOST = "faction_territory_lost"
    FACTION_LEADER_CHANGED = "faction_leader_changed"

    # Memory and knowledge events
    MEMORY_CREATED = "memory_created"
    MEMORY_FORGOTTEN = "memory_forgotten"
    RUMOR_SPREAD = "rumor_spread"
    KNOWLEDGE_UPDATED = "knowledge_updated"
    ENTITY_RECOGNIZED = "entity_recognized"

    # Reputation events
    REPUTATION_CHANGED = "reputation_changed"
    TITLE_GAINED = "title_gained"
    TITLE_LOST = "title_lost"

    # World state events
    ZONE_CONTROL_CHANGED = "zone_control_changed"
    CORRUPTION_SPREAD = "corruption_spread"
    RITUAL_PERFORMED = "ritual_performed"
    SHRINE_ACTIVATED = "shrine_activated"
    SHRINE_CORRUPTED = "shrine_corrupted"

    # Conflict events
    CONFLICT_STARTED = "conflict_started"
    CONFLICT_RESOLVED = "conflict_resolved"
    BATTLE_OUTCOME = "battle_outcome"
    SIEGE_STARTED = "siege_started"
    SIEGE_ENDED = "siege_ended"

    # Quest events
    DYNAMIC_QUEST_GENERATED = "dynamic_quest_generated"
    QUEST_OBJECTIVE_UPDATED = "quest_objective_updated"
    FACTION_QUEST_OFFERED = "faction_quest_offered"

    # Player interaction events
    PLAYER_FACTION_DISCOVERED = "player_faction_discovered"
    PLAYER_REPUTATION_THRESHOLD = "player_reputation_threshold"
    PLAYER_WITNESSED_CRIME = "player_witnessed_crime"
    PLAYER_HELPED_FACTION = "player_helped_faction"
    PLAYER_BETRAYED_FACTION = "player_betrayed_faction"

    # Additional AI event types for game integration
    ENTITY_SPAWNED = "entity_spawned"
    TURN_STARTED = "turn_started"


class AIEvent(GameEvent):
    """
    AI-specific event class with additional functionality.

    Extends the base GameEvent with AI-specific metadata and helpers.
    """

    def __init__(
        self,
        event_type: AIEventType,
        data: dict[str, Any],
        cancellable: bool = False,
        source: str = "ai_system",
        priority: int = 0,
    ):
        """
        Initialize an AI event.

        Args:
            event_type: The type of AI event
            data: Event-specific data
            cancellable: Whether mods can cancel this event
            source: What AI system triggered this event
            priority: Event priority (higher = more important)
        """
        # Convert AIEventType to string for compatibility with base class
        try:
            core_type = CoreEventType(event_type.value)
        except ValueError:
            core_type = event_type.value  # type: ignore
        super().__init__(core_type, data, cancellable, source)
        self.ai_event_type = event_type
        self.event_type: str | CoreEventType = event_type.value
        self.priority = priority

    def get_entity_id(self) -> str | None:
        """Get the entity ID from event data if present."""
        return self.data.get("entity_id")

    def get_faction_id(self) -> str | None:
        """Get the faction ID from event data if present."""
        return self.data.get("faction_id")

    def get_location(self) -> tuple[int, int] | None:
        """Get the location from event data if present."""
        location = self.data.get("location")
        LOCATION_SIZE = 2
        if isinstance(location, tuple | list) and len(location) == LOCATION_SIZE:
            return tuple(location)
        return None


# Event creation helper functions
def create_ai_state_changed_event(
    entity_id: str, old_state: str, new_state: str
) -> AIEvent:
    """Create an AI state changed event."""
    return AIEvent(
        AIEventType.AI_STATE_CHANGED,
        {
            "entity_id": entity_id,
            "old_state": old_state,
            "new_state": new_state,
        },
    )


def create_faction_relationship_changed_event(
    faction_a: str,
    faction_b: str,
    old_relationship: float,
    new_relationship: float,
    reason: str = "unknown",
) -> AIEvent:
    """Create a faction relationship changed event."""
    return AIEvent(
        AIEventType.FACTION_RELATIONSHIP_CHANGED,
        {
            "faction_a": faction_a,
            "faction_b": faction_b,
            "old_relationship": old_relationship,
            "new_relationship": new_relationship,
            "reason": reason,
        },
        priority=1,  # Relationship changes are important
    )


# Alias for compatibility
def create_faction_relation_changed_event(
    faction_a: str,
    faction_b: str,
    old_relationship: float,
    new_relationship: float,
    reason: str = "unknown",
) -> AIEvent:
    """Create a faction relationship changed event (compatibility alias)."""
    return create_faction_relationship_changed_event(
        faction_a, faction_b, old_relationship, new_relationship, reason
    )


def create_memory_created_event(
    entity_id: str,
    memory_content: str,
    importance: float,
    location: tuple[int, int] | None = None,
) -> AIEvent:
    """Create a memory created event."""
    data = {
        "entity_id": entity_id,
        "memory_content": memory_content,
        "importance": importance,
    }
    if location:
        data["location"] = location

    return AIEvent(AIEventType.MEMORY_CREATED, data)


def create_reputation_changed_event(
    entity_id: str,
    target_id: str,
    target_type: str,  # "faction" or "individual"
    old_reputation: float,
    new_reputation: float,
) -> AIEvent:
    """Create a reputation changed event."""
    return AIEvent(
        AIEventType.REPUTATION_CHANGED,
        {
            "entity_id": entity_id,
            "target_id": target_id,
            "target_type": target_type,
            "old_reputation": old_reputation,
            "new_reputation": new_reputation,
        },
    )


def create_zone_control_changed_event(
    zone_id: str,
    old_controller: str | None,
    new_controller: str | None,
    method: str = "conquest",
) -> AIEvent:
    """Create a zone control changed event."""
    return AIEvent(
        AIEventType.ZONE_CONTROL_CHANGED,
        {
            "zone_id": zone_id,
            "old_controller": old_controller,
            "new_controller": new_controller,
            "method": method,
        },
        priority=2,  # Territory changes are very important
    )


def create_conflict_started_event(
    faction_a: str,
    faction_b: str,
    conflict_type: str,
    cause: str,
    location: tuple[int, int] | None = None,
) -> AIEvent:
    """Create a conflict started event."""
    data: dict[str, str | tuple[int, int]] = {
        "faction_a": faction_a,
        "faction_b": faction_b,
        "conflict_type": conflict_type,
        "cause": cause,
    }
    if location:
        data["location"] = location

    return AIEvent(
        AIEventType.CONFLICT_STARTED,
        data,
        priority=2,  # Conflicts are very important
    )


def create_dynamic_quest_generated_event(
    quest_id: str,
    quest_type: str,
    faction_id: str | None,
    trigger_event: str,
    requirements: dict[str, Any],
) -> AIEvent:
    """Create a dynamic quest generated event."""
    return AIEvent(
        AIEventType.DYNAMIC_QUEST_GENERATED,
        {
            "quest_id": quest_id,
            "quest_type": quest_type,
            "faction_id": faction_id,
            "trigger_event": trigger_event,
            "requirements": requirements,
        },
    )


def create_player_reputation_threshold_event(
    faction_id: str, old_threshold: str, new_threshold: str, reputation_value: float
) -> AIEvent:
    """Create a player reputation threshold event."""
    return AIEvent(
        AIEventType.PLAYER_REPUTATION_THRESHOLD,
        {
            "faction_id": faction_id,
            "old_threshold": old_threshold,
            "new_threshold": new_threshold,
            "reputation_value": reputation_value,
        },
    )


def create_entity_spawned_event(
    entity_id: str, entity_type: str, location: tuple[int, int], faction_id: str
) -> AIEvent:
    """Create an entity spawned event."""
    return AIEvent(
        AIEventType.ENTITY_SPAWNED,
        {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "location": location,
            "faction_id": faction_id,
        },
    )


def create_turn_started_event(turn_number: int, active_entities: int) -> AIEvent:
    """Create a turn started event."""
    return AIEvent(
        AIEventType.TURN_STARTED,
        {
            "turn_number": turn_number,
            "active_entities": active_entities,
        },
    )


# Event handler examples for AI systems
def log_faction_events(event: AIEvent) -> None:
    """Example handler that logs faction-related events."""
    if event.ai_event_type in [
        AIEventType.FACTION_RELATIONSHIP_CHANGED,
        AIEventType.FACTION_ALLIANCE_FORMED,
        AIEventType.FACTION_WAR_DECLARED,
    ]:
        print(f"Faction Event: {event.ai_event_type.value} - {event.data}")


def track_reputation_changes(event: AIEvent) -> None:
    """Example handler that tracks reputation changes for analytics."""
    if event.ai_event_type == AIEventType.REPUTATION_CHANGED:
        entity_id = event.data.get("entity_id")
        target_id = event.data.get("target_id")
        new_rep = event.data.get("new_reputation", 0.0)
        old_rep = event.data.get("old_reputation", 0.0)
        change = float(new_rep) - float(old_rep)
        print(f"Reputation: {entity_id} -> {target_id}: {change:+.2f}")


def trigger_quests_on_conflict(event: AIEvent) -> None:
    """Example handler that generates quests when conflicts start."""
    if event.ai_event_type == AIEventType.CONFLICT_STARTED:
        faction_a = event.data.get("faction_a")
        faction_b = event.data.get("faction_b")
        print(
            f"Conflict started between {faction_a} and {faction_b} - generating quests!"
        )
        # This would trigger the quest generation system
