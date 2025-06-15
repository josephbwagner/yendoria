"""
AI System Integration Example.

This module demonstrates how to integrate the AI Manager with
the existing game systems and shows example usage patterns.
"""

import logging
from typing import TYPE_CHECKING, Any

from yendoria.components.ai_events import (
    AIEventType,
    create_faction_relation_changed_event,
    create_reputation_changed_event,
)
from yendoria.components.component_manager import (
    ComponentManager,
    get_component_manager,
)
from yendoria.systems.ai_behavior_advanced import AdvancedAIBehaviorSystem
from yendoria.systems.ai_error_handling import ai_error_handler, get_ai_metrics
from yendoria.systems.ai_singleton_registry import (
    initialize_ai_manager,
    initialize_config_manager,
)

if TYPE_CHECKING:
    from yendoria.systems.ai_manager import AIManager
    from yendoria.systems.config_manager import ConfigManager

logger = logging.getLogger(__name__)


@ai_error_handler("initialize AI systems")
def initialize_ai_systems() -> tuple[ComponentManager, "ConfigManager", "AIManager"]:
    """
    Initialize all AI-related systems in the correct order.

    Returns:
        Tuple of (component_manager, config_manager, ai_manager)
    """
    logger.info("Initializing AI systems...")

    # Initialize core systems
    component_manager = get_component_manager()
    config_manager = initialize_config_manager()
    ai_manager = initialize_ai_manager(component_manager, config_manager)

    # Register AI subsystems
    behavior_system = AdvancedAIBehaviorSystem(component_manager)
    ai_manager.register_system(
        "behavior",
        behavior_system,
        priority=10,  # High priority for core behaviors
        event_types=[
            AIEventType.REPUTATION_CHANGED,
            AIEventType.CONFLICT_STARTED,
            AIEventType.FACTION_RELATION_CHANGED,
        ],
    )

    logger.info("AI systems initialized successfully")
    return component_manager, config_manager, ai_manager


@ai_error_handler("create example AI entities")
def create_example_ai_entities(ai_manager: "AIManager") -> list[str]:
    """
    Create some example AI entities for demonstration.

    Args:
        ai_manager: The AI manager instance

    Returns:
        List of created entity IDs
    """
    entity_ids = []

    # Create a guard entity
    guard_id = "guard_001"
    ai_manager.register_ai_entity(guard_id, archetype="guard", faction="town_guard")
    entity_ids.append(guard_id)
    logger.info(f"Created guard entity: {guard_id}")

    # Create a merchant entity
    merchant_id = "merchant_001"
    ai_manager.register_ai_entity(
        merchant_id, archetype="merchant", faction="merchants_guild"
    )
    entity_ids.append(merchant_id)
    logger.info(f"Created merchant entity: {merchant_id}")

    # Create a bandit entity
    bandit_id = "bandit_001"
    ai_manager.register_ai_entity(bandit_id, archetype="bandit", faction="raiders")
    entity_ids.append(bandit_id)
    logger.info(f"Created bandit entity: {bandit_id}")

    return entity_ids


@ai_error_handler("demonstrate AI events")
def demonstrate_ai_events(ai_manager: "AIManager") -> None:
    """
    Demonstrate AI event system functionality.

    Args:
        ai_manager: The AI manager instance
    """
    logger.info("Demonstrating AI events...")

    # Create a reputation change event
    reputation_event = create_reputation_changed_event(
        entity_id="guard_001",
        target_id="merchant_001",
        target_type="individual",
        old_reputation=0.5,
        new_reputation=0.8,
    )
    ai_manager.handle_ai_event(reputation_event)

    # Create a faction relation change event
    faction_event = create_faction_relation_changed_event(
        faction_a="town_guard",
        faction_b="raiders",
        old_relationship=-0.5,
        new_relationship=-0.8,
        reason="bandit_attack",
    )
    ai_manager.handle_ai_event(faction_event)

    logger.info("AI events demonstration completed")


@ai_error_handler("run AI simulation step")
def run_ai_simulation_step(ai_manager: "AIManager", delta_time: float = 1.0) -> None:
    """
    Run a single step of AI simulation.

    Args:
        ai_manager: The AI manager instance
        delta_time: Time step for the simulation
    """
    logger.info(f"Running AI simulation step (delta_time: {delta_time})")

    metrics = get_ai_metrics()
    with metrics.operation_timer("simulation_step"):
        ai_manager.update(delta_time)

    logger.info("AI simulation step completed")


@ai_error_handler("query AI system info")
def query_ai_system_info(ai_manager: "AIManager") -> dict[str, Any]:
    """
    Query information about the AI system state.

    Args:
        ai_manager: The AI manager instance

    Returns:
        Dictionary containing AI system information
    """
    logger.info("Querying AI system information...")

    system_info = {
        "registered_entities": list(ai_manager.get_ai_entities()),
        "performance_stats": ai_manager.get_performance_stats(),
        "registered_systems": len(ai_manager.systems),
        "faction_memberships": len(ai_manager.faction_memberships),
    }

    logger.info(f"AI system info: {system_info}")
    return system_info


def run_integration_example() -> None:
    """
    Run a complete integration example demonstrating AI system usage.
    """
    try:
        logger.info("Starting AI integration example...")

        # Initialize systems
        component_manager, config_manager, ai_manager = initialize_ai_systems()

        # Create example entities
        create_example_ai_entities(ai_manager)

        # Demonstrate event handling
        demonstrate_ai_events(ai_manager)

        # Run some simulation steps
        for step in range(3):
            logger.info(f"Simulation step {step + 1}")
            run_ai_simulation_step(ai_manager, delta_time=1.0)

        # Query system information
        system_info = query_ai_system_info(ai_manager)
        logger.info(f"Final system state: {system_info}")

        logger.info("AI integration example completed successfully")

    except Exception as e:
        logger.error(f"AI integration example failed: {e}")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_integration_example()
