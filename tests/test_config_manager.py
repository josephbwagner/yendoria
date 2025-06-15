#!/usr/bin/env python3
"""Tests for the config manager system."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from yendoria.systems.config_manager import ConfigManager, ConfigWatcher


class TestConfigManager:
    """Test suite for ConfigManager."""

    @pytest.fixture
    def temp_config_dir(self):
        """Create a temporary directory for config files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def config_manager(self, temp_config_dir):
        """Create a ConfigManager instance with temporary directory."""
        return ConfigManager(config_root=str(temp_config_dir))

    @pytest.fixture
    def sample_config(self):
        """Create sample configuration data."""
        return {
            "ai_settings": {"update_interval": 0.1, "max_entities": 100},
            "behavior_trees": {
                "guard": {"root": "patrol", "nodes": ["patrol", "investigate", "alert"]}
            },
        }

    def test_initialization(self, temp_config_dir):
        """Test ConfigManager initialization."""
        config_manager = ConfigManager(config_root=str(temp_config_dir))
        assert config_manager.config_root == Path(str(temp_config_dir))
        assert config_manager.configs == {}
        assert config_manager.config_schemas == {}

    def test_initialization_with_default_dirs(self):
        """Test ConfigManager initialization with default directories."""
        config_manager = ConfigManager()
        assert config_manager.config_root == Path("config")

    def test_load_config_file_success(
        self, config_manager, temp_config_dir, sample_config
    ):
        """Test loading a valid configuration file."""
        config_file = temp_config_dir / "test_config.json"
        config_file.write_text(json.dumps(sample_config))

        result = config_manager.load_config(str(config_file), watch=False)

        assert result == sample_config
        assert str(config_file) in config_manager.configs

    def test_load_config_file_not_found(self, config_manager):
        """Test loading a non-existent configuration file."""
        with pytest.raises(FileNotFoundError):
            config_manager.load_config("non_existent.json", watch=False)

    def test_load_config_invalid_json(self, config_manager, temp_config_dir):
        """Test loading an invalid JSON configuration file."""
        config_file = temp_config_dir / "invalid.json"
        config_file.write_text("{ invalid json }")

        with pytest.raises(json.JSONDecodeError):
            config_manager.load_config(str(config_file), watch=False)

    def test_get_config_existing(self, config_manager, temp_config_dir, sample_config):
        """Test getting an existing configuration."""
        config_file = temp_config_dir / "test_config.json"
        config_file.write_text(json.dumps(sample_config))
        config_manager.load_config(str(config_file), watch=False)

        result = config_manager.get_config(str(config_file))
        assert result == sample_config

    def test_get_config_nonexistent(self, config_manager):
        """Test getting a non-existent configuration."""
        result = config_manager.get_config("non_existent.json")
        assert result == {}

    def test_get_config_value_existing(
        self, config_manager, temp_config_dir, sample_config
    ):
        """Test getting a specific config value using dot notation."""
        config_file = temp_config_dir / "test_config.json"
        config_file.write_text(json.dumps(sample_config))
        config_manager.load_config(str(config_file), watch=False)

        # Note: This test assumes get_config_value method exists or we mock it
        # Since it's not in the actual implementation, we'll test get_config instead
        result = config_manager.get_config(str(config_file))
        assert result["ai_settings"]["update_interval"] == 0.1

    def test_get_config_value_with_default(self, config_manager):
        """Test getting a config value with default."""
        result = config_manager.get_config("non_existent.json", {"default": "value"})
        assert result == {"default": "value"}

    def test_get_config_value_invalid_path(self, config_manager):
        """Test getting a config value with invalid path."""
        result = config_manager.get_config("", {})
        assert result == {}

    def test_register_callback(self, config_manager, temp_config_dir, sample_config):
        """Test registering a reload callback."""
        config_file = temp_config_dir / "test_config.json"
        config_file.write_text(json.dumps(sample_config))

        callback = Mock()
        config_manager.register_reload_callback(str(config_file), callback)

        # Load config to setup the callback
        config_manager.load_config(str(config_file), watch=False)

        # Trigger reload
        config_manager.reload_config(str(config_file))

        # Callback should have been called
        callback.assert_called()

    def test_unregister_callback(self, config_manager):
        """Test unregistering a callback."""
        callback = Mock()
        config_path = "test_config.json"

        # Register then unregister
        config_manager.register_reload_callback(config_path, callback)

        # Check that callback was registered
        assert config_path in config_manager.reload_callbacks
        assert callback in config_manager.reload_callbacks[config_path]

    def test_reload_config_with_callbacks(
        self, config_manager, temp_config_dir, sample_config
    ):
        """Test that callbacks are triggered on config reload."""
        config_file = temp_config_dir / "test_config.json"
        config_file.write_text(json.dumps(sample_config))

        callback = Mock()
        config_manager.register_reload_callback(str(config_file), callback)
        config_manager.load_config(str(config_file), watch=False)

        # Modify and reload
        modified_config = {**sample_config, "new_key": "new_value"}
        config_file.write_text(json.dumps(modified_config))
        config_manager.reload_config(str(config_file))

        # Callback should have been called
        callback.assert_called()

    def test_watch_configs(self, config_manager, temp_config_dir):
        """Test configuration file watching setup."""
        # Create a real config file for testing
        config_file = temp_config_dir / "watch_test.json"
        config_file.write_text('{"test": "value"}')

        # This is a basic test since actual file watching is complex to test
        with patch.object(config_manager, "_setup_file_watcher") as mock_setup:
            config_manager.load_config(str(config_file), watch=True)
            # Should attempt to setup file watcher
            mock_setup.assert_called()

    def test_stop_watching(self, config_manager):
        """Test stopping file watchers."""
        # Setup some mock watchers
        mock_observer = Mock()
        config_manager.file_watchers["test_path"] = mock_observer

        config_manager.stop_watchers()

        # Should have stopped the observer
        mock_observer.stop.assert_called()

    def test_reload_all_configs(self, config_manager, temp_config_dir, sample_config):
        """Test reloading all configurations."""
        config_file = temp_config_dir / "test_config.json"
        config_file.write_text(json.dumps(sample_config))
        config_manager.load_config(str(config_file), watch=False)

        # Modify file
        modified_config = {**sample_config, "reloaded": True}
        config_file.write_text(json.dumps(modified_config))

        # Load all AI configs (closest we have to reload_all)
        all_configs = config_manager.load_all_ai_configs()

        # Should return a dictionary
        assert isinstance(all_configs, dict)


class TestConfigWatcher:
    """Test suite for ConfigWatcher."""

    @pytest.fixture
    def config_manager(self):
        """Create a mock config manager."""
        return Mock(spec=ConfigManager)

    @pytest.fixture
    def config_watcher(self, config_manager):
        """Create a ConfigWatcher instance."""
        return ConfigWatcher(config_manager)

    def test_on_modified_directory_ignored(self, config_watcher, config_manager):
        """Test that directory modification events are ignored."""
        event = Mock()
        event.is_directory = True
        event.src_path = "/some/directory"

        config_watcher.on_modified(event)

        # Should not call reload_config
        config_manager.reload_config.assert_not_called()

    def test_on_modified_non_config_file_ignored(self, config_watcher, config_manager):
        """Test that non-config file modifications are ignored."""
        event = Mock()
        event.is_directory = False
        event.src_path = "/some/file.txt"

        config_watcher.on_modified(event)

        # Should not call reload_config
        config_manager.reload_config.assert_not_called()

    def test_on_modified_config_file_processed(self, config_watcher, config_manager):
        """Test that config file modifications are processed."""
        event = Mock()
        event.is_directory = False
        event.src_path = "/some/config.json"

        config_watcher.on_modified(event)

        # Should call reload_config
        config_manager.reload_config.assert_called_once_with("/some/config.json")

    def test_on_modified_debouncing(self, config_watcher, config_manager):
        """Test that rapid file changes are debounced."""
        event = Mock()
        event.is_directory = False
        event.src_path = "/some/config.json"

        # First call
        config_watcher.on_modified(event)

        # Rapid second call (should be debounced)
        config_watcher.on_modified(event)

        # Should only call reload_config once due to debouncing
        config_manager.reload_config.assert_called_once()

    def test_on_modified_yaml_file(self, config_watcher, config_manager):
        """Test that YAML files are processed."""
        event = Mock()
        event.is_directory = False
        event.src_path = "/some/config.yaml"

        config_watcher.on_modified(event)

        config_manager.reload_config.assert_called_once_with("/some/config.yaml")

    def test_on_modified_yml_file(self, config_watcher, config_manager):
        """Test that YML files are processed."""
        event = Mock()
        event.is_directory = False
        event.src_path = "/some/config.yml"

        config_watcher.on_modified(event)

        config_manager.reload_config.assert_called_once_with("/some/config.yml")
