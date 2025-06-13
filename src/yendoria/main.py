"""
Main entry point for Yendoria.

This module contains the main function that initializes and starts
the game engine.
"""

from .engine import GameEngine


def main() -> None:
    """
    Main function to start Yendoria.

    Initializes the game engine and starts the main game loop.
    """
    # Create and run the game engine
    engine = GameEngine()
    engine.run()


if __name__ == "__main__":
    main()
