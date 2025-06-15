"""
Configuration management system for AI components.

This module provides hot-reloadable configuration management for AI systems,
allowing behavior to be modified without code changes and supporting modding.
"""

import json
import logging
import os
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

logger = logging.getLogger(__name__)

# Constants
DEBOUNCE_TIME = 0.5


class ConfigWatcher(FileSystemEventHandler):
    """Watches configuration files for changes and triggers reloads."""

    def __init__(self, config_manager: "ConfigManager") -> None:
        self.config_manager = config_manager
        self.last_modified: dict[str, float] = {}

    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events."""
        if event.is_directory:
            return

        file_path = event.src_path
        if not file_path.endswith((".json", ".yaml", ".yml")):
            return

        # Debounce rapid file changes
        current_time = time.time()
        if (
            file_path in self.last_modified
            and current_time - self.last_modified[file_path] < DEBOUNCE_TIME
        ):
            return

        self.last_modified[file_path] = current_time

        logger.info(f"Configuration file changed: {file_path}")
        self.config_manager.reload_config(file_path)


class ConfigManager:
    """
    Manages AI configuration files with hot reloading support.

    Provides centralized access to configuration data for AI systems
    with automatic reloading when files change.
    """

    def __init__(self, config_root: str = "config"):
        """
        Initialize the configuration manager.

        Args:
            config_root: Root directory for configuration files
        """
        self.config_root = Path(config_root)
        self.configs: dict[str, dict[str, Any]] = {}
        self.config_schemas: dict[str, dict[str, Any]] = {}
        # Observer type not available for annotation
        self.file_watchers: dict[str, Any] = {}
        self.reload_callbacks: dict[str, list[Any]] = {}

        # Ensure config directories exist
        self._ensure_config_directories()

    def _ensure_config_directories(self) -> None:
        """Create necessary configuration directories."""
        directories = [
            self.config_root,
            self.config_root / "ai",
            self.config_root / "ai" / "factions",
            self.config_root / "ai" / "archetypes",
            self.config_root / "ai" / "behaviors",
            self.config_root / "ai" / "quests",
            self.config_root / "ai" / "schemas",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def load_config(
        self, config_path: str, schema_path: str | None = None, watch: bool = True
    ) -> dict[str, Any]:
        """
        Load a configuration file.

        Args:
            config_path: Path to the configuration file
            schema_path: Optional path to schema for validation
            watch: Whether to watch the file for changes

        Returns:
            The loaded configuration data

        Raises:
            FileNotFoundError: If the config file doesn't exist
            json.JSONDecodeError: If the config file is invalid JSON
        """
        full_path = self.config_root / config_path

        if not full_path.exists():
            logger.error(f"Configuration file not found: {full_path}")
            raise FileNotFoundError(f"Configuration file not found: {full_path}")

        try:
            with open(full_path, encoding="utf-8") as f:
                if full_path.suffix.lower() == ".json":
                    config_data = json.load(f)
                else:
                    # For YAML support (would need PyYAML dependency)
                    raise ValueError(f"Unsupported config format: {full_path.suffix}")

            # Validate against schema if provided
            if schema_path:
                self._validate_config(config_data, schema_path)

            # Store the config
            self.configs[config_path] = config_data

            # Set up file watching if requested
            if watch:
                self._setup_file_watcher(str(full_path))

            logger.info(f"Loaded configuration: {config_path}")
            return dict(config_data)  # Ensure proper type

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file {full_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading config file {full_path}: {e}")
            raise

    def get_config(
        self, config_path: str, default: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Get a previously loaded configuration.

        Args:
            config_path: Path to the configuration file
            default: Default value to return if config not found

        Returns:
            The configuration data or the default value
        """
        if default is None:
            default = {}
        return self.configs.get(config_path, default)

    def reload_config(self, file_path: str) -> None:
        """
        Reload a configuration file and notify callbacks.

        Args:
            file_path: Full path to the file that changed
        """
        # Find the config key for this file path
        config_key = None
        for key in self.configs:
            if str(self.config_root / key) == file_path:
                config_key = key
                break

        if not config_key:
            logger.warning(f"No config key found for changed file: {file_path}")
            return

        try:
            # Reload the configuration
            old_config = self.configs.get(config_key, {}).copy()
            new_config = self.load_config(config_key, watch=False)

            # Notify callbacks about the change
            callbacks = self.reload_callbacks.get(config_key, [])
            for callback in callbacks:
                try:
                    callback(config_key, old_config, new_config)
                except Exception as e:
                    logger.error(f"Error in config reload callback: {e}")

            logger.info(f"Reloaded configuration: {config_key}")

        except Exception as e:
            logger.error(f"Failed to reload configuration {config_key}: {e}")

    def register_reload_callback(
        self,
        config_path: str,
        callback: Callable[[str, dict[str, Any], dict[str, Any]], None],
    ) -> None:
        """
        Register a callback to be called when a config file changes.

        Args:
            config_path: Path to the configuration file
            callback: Function to call with (config_path, old_config, new_config)
        """
        if config_path not in self.reload_callbacks:
            self.reload_callbacks[config_path] = []
        self.reload_callbacks[config_path].append(callback)

    def _setup_file_watcher(self, file_path: str) -> None:
        """Set up file watching for a configuration file."""
        if file_path in self.file_watchers:
            return  # Already watching

        observer = Observer()
        event_handler = ConfigWatcher(self)

        # Watch the directory containing the file
        watch_dir = os.path.dirname(file_path)
        observer.schedule(event_handler, watch_dir, recursive=False)
        observer.start()

        self.file_watchers[file_path] = observer
        logger.debug(f"Started watching config file: {file_path}")

    def _validate_config(self, config_data: dict, schema_path: str) -> None:
        """
        Validate configuration data against a schema.

        Args:
            config_data: The configuration data to validate
            schema_path: Path to the JSON schema file
        """
        # This would use jsonschema library if available
        # For now, just log that validation would happen
        logger.debug(f"Would validate config against schema: {schema_path}")

    def stop_watchers(self) -> None:
        """Stop all file watchers."""
        for observer in self.file_watchers.values():
            observer.stop()
            observer.join()
        self.file_watchers.clear()
        logger.info("Stopped all configuration file watchers")

    def get_ai_config(self, config_name: str) -> dict[str, Any] | None:
        """
        Get an AI-specific configuration by name.

        Args:
            config_name: Name of the AI config (e.g., 'factions', 'archetypes')

        Returns:
            The configuration data or None if not found
        """
        ai_config_path = f"ai/{config_name}.json"
        return self.get_config(ai_config_path)

    def load_all_ai_configs(self) -> dict[str, dict[str, Any]]:
        """
        Load all standard AI configuration files.

        Returns:
            Dictionary mapping config names to their data
        """
        ai_configs = {}
        config_files = ["factions", "archetypes", "behavior_trees", "quest_templates"]

        for config_name in config_files:
            try:
                config_path = f"ai/{config_name}.json"
                config_data = self.load_config(config_path)
                ai_configs[config_name] = config_data
                logger.info(f"Loaded AI config: {config_name}")
            except Exception as e:
                logger.warning(f"Failed to load AI config {config_name}: {e}")
                ai_configs[config_name] = {}

        return ai_configs

    def validate_ai_config(self, config_name: str) -> bool:
        """
        Validate an AI configuration against its schema.

        Args:
            config_name: Name of the AI config to validate

        Returns:
            True if valid, False otherwise
        """
        config_data = self.get_ai_config(config_name)
        if not config_data:
            logger.error(f"No config data found for {config_name}")
            return False

        schema_path = f"ai/schemas/{config_name}_schema.json"
        try:
            self._validate_config(config_data, schema_path)
            return True
        except Exception as e:
            logger.error(f"Validation failed for {config_name}: {e}")
            return False

    def __del__(self):
        """Cleanup when the config manager is destroyed."""
        self.stop_watchers()


# Convenience functions for AI configs
def get_faction_config() -> dict[str, Any]:
    """Get faction configurations."""
    from yendoria.systems.ai_singleton_registry import get_config_manager

    try:
        config_manager = get_config_manager()
        return config_manager.get_config("ai/factions.json", {})
    except RuntimeError:
        logger.warning("Config manager not initialized, returning empty faction config")
        return {}


def get_archetype_config() -> dict[str, Any]:
    """Get archetype configurations."""
    from yendoria.systems.ai_singleton_registry import get_config_manager

    try:
        config_manager = get_config_manager()
        return config_manager.get_config("ai/archetypes.json", {})
    except RuntimeError:
        logger.warning(
            "Config manager not initialized, returning empty archetype config"
        )
        return {}


def get_behavior_tree_config() -> dict[str, Any]:
    """Get behavior tree configurations."""
    from yendoria.systems.ai_singleton_registry import get_config_manager

    try:
        config_manager = get_config_manager()
        return config_manager.get_config("ai/behavior_trees.json", {})
    except RuntimeError:
        logger.warning(
            "Config manager not initialized, returning empty behavior tree config"
        )
        return {}


def get_quest_template_config() -> dict[str, Any]:
    """Get quest template configurations."""
    from yendoria.systems.ai_singleton_registry import get_config_manager

    try:
        config_manager = get_config_manager()
        return config_manager.get_config("ai/quest_templates.json", {})
    except RuntimeError:
        logger.warning(
            "Config manager not initialized, returning empty quest template config"
        )
        return {}


def initialize_config_manager(config_root: str = "config") -> ConfigManager:
    """
    Initialize the configuration manager singleton.

    Args:
        config_root: Root directory for configuration files

    Returns:
        The configuration manager instance
    """
    from yendoria.systems.ai_singleton_registry import set_config_manager

    config_manager = ConfigManager(config_root)
    return set_config_manager(config_manager)


# Deprecated functions - use get_*_config functions instead
def load_faction_config() -> dict[str, Any]:
    """Load the faction configuration. DEPRECATED: Use get_faction_config() instead."""
    return get_faction_config()


def load_archetype_config() -> dict[str, Any]:
    """
    Load the archetype configuration.
    DEPRECATED: Use get_archetype_config() instead.
    """
    return get_archetype_config()


def load_behavior_tree_config() -> dict[str, Any]:
    """
    Load the behavior tree configuration.
    DEPRECATED: Use get_behavior_tree_config() instead.
    """
    return get_behavior_tree_config()


def load_quest_template_config() -> dict[str, Any]:
    """
    Load the quest template configuration.
    DEPRECATED: Use get_quest_template_config() instead.
    """
    return get_quest_template_config()


# Example usage and testing
if __name__ == "__main__":
    # Example of how to use the config manager
    config_mgr = ConfigManager()

    def on_faction_config_changed(
        config_path: str, old_config: dict[str, Any], new_config: dict[str, Any]
    ) -> None:
        print(f"Faction config changed! Old keys: {list(old_config.keys())}")
        print(f"New keys: {list(new_config.keys())}")

    # Register a callback for faction config changes
    config_mgr.register_reload_callback("ai/factions.json", on_faction_config_changed)

    # Load all AI configs
    ai_configs = config_mgr.load_all_ai_configs()
    print(f"Loaded {len(ai_configs)} AI configuration files")

    # Keep the manager alive to test file watching
    # (In real usage, this would be managed by the main game loop)
    try:
        time.sleep(10)  # Wait for potential file changes
    except KeyboardInterrupt:
        pass
    finally:
        config_mgr.stop_watchers()
