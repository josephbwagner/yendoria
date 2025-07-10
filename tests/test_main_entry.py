"""
Tests for main entry points and initialization.
"""

from unittest.mock import Mock, patch

from src.yendoria import main


class TestMainEntry:
    """Test cases for main entry points."""

    @patch("src.yendoria.main.GameEngine")
    def test_main_function(self, mock_game_engine_class):
        """Test the main function initializes and runs the game engine."""
        # Setup mock
        mock_engine = Mock()
        mock_game_engine_class.return_value = mock_engine

        # Call main
        main.main()

        # Verify engine was created and run
        mock_game_engine_class.assert_called_once()
        mock_engine.run.assert_called_once()

    def test_main_function_docstring(self):
        """Test that main function has proper documentation."""
        assert main.main.__doc__ is not None
        assert "Main function" in main.main.__doc__
        assert "game engine" in main.main.__doc__

    def test_main_module_has_main_function(self):
        """Test that main module exports main function."""
        assert hasattr(main, "main")
        assert callable(main.main)

    def test_main_module_docstring(self):
        """Test that main module has proper documentation."""
        assert main.__doc__ is not None
        assert "Main entry point" in main.__doc__
