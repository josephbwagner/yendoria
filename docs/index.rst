Yendoria Documentation
======================

Welcome to Yendoria! This project is a traditional tile-based roguelike game built with Python and libtcod.

Features
--------

* **Entity Component System (ECS)**: Flexible architecture for game entities
* **Procedural Generation**: Randomly generated dungeons with rooms and corridors
* **Field of View**: Dynamic lighting and exploration system
* **Modern Python**: Built with Python 3.10+ using Poetry for dependency management
* **Comprehensive Testing**: Full test suite with 25+ unit tests

Quick Start
-----------

1. Install dependencies::

    poetry install

2. Run the game::

    poetry run python -m yendoria

3. Use arrow keys, WASD, vim keys, or numpad to move around and explore!

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api

Game Controls
-------------

* **Movement**: Arrow keys, WASD, vim keys (hjkl), or numpad (including diagonals)
* **Exploration**: Move to reveal new areas within your 8-tile field of view
* **Quit**: Press Escape or close the window

Architecture Overview
---------------------

The game uses an Entity Component System (ECS) architecture:

* **Entities**: Containers for components (Player, Orc, Troll)
* **Components**: Data containers (Position, Health, Graphic, AI, Damage)
* **Systems**: Logic processors (Rendering, Input handling, Game engine)

Key modules:

* ``engine.py``: Main game loop and coordination
* ``game_map/``: Map generation and tile management
* ``entities/``: Entity creation and management
* ``components/``: ECS component definitions
* ``systems/``: Game systems (rendering, etc.)
* ``input_handlers/``: Input processing
* ``utils/constants.py``: Game configuration and constants

Development
-----------

Run tests::

    poetry run pytest

Build documentation::

    cd docs
    poetry run sphinx-build -b html . _build/html

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
