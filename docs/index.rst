Yendoria Documentation
======================

Welcome to Yendoria! This project is a traditional tile-based roguelike game built with Python and libtcod, featuring **production-grade development practices** and a comprehensive CI/CD pipeline.

Features
--------

### Core Gameplay
* **Entity Component System (ECS)**: Flexible architecture for game entities
* **Procedural Generation**: Randomly generated dungeons with rooms and corridors
* **Field of View**: Dynamic lighting and exploration system with 8-tile radius
* **Turn-based Combat**: Melee combat with health and damage mechanics
* **Multiple Input Schemes**: Arrow keys, WASD, vim keys, and numpad support

### Development Excellence
* **Production-Grade CI/CD**: GitHub Actions with multi-platform testing (Ubuntu, macOS, Windows)
* **Multi-Python Support**: Tested on Python 3.10, 3.11, 3.12, 3.13
* **Automated Quality Gates**: Comprehensive linting, formatting, type checking, and testing
* **Security Scanning**: Automated vulnerability detection with Bandit, Safety, and pip-audit
* **Test Coverage**: 55%+ coverage requirement with comprehensive reporting
* **Professional Workflows**: Pre-commit hooks, automated dependency updates, and structured templates

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

### Quality Assurance & CI/CD

This project follows **production-grade development practices**:

**Code Quality**::

    # Ultra-fast linting and formatting
    poetry run ruff check --fix .
    poetry run ruff format .

    # Static type checking
    poetry run mypy

**Testing & Coverage**::

    # Run full test suite
    poetry run pytest

    # With coverage reporting (55%+ required)
    poetry run pytest --cov=src/yendoria --cov-report=html

**Security Scanning**::

    # Code security analysis
    poetry run bandit -r src/

    # Dependency vulnerability scanning
    poetry run safety check

**Complete CI Validation**::

    # Run all quality checks (matches CI pipeline)
    poetry run ruff check . && poetry run ruff format --check . && poetry run mypy && poetry run pytest --cov=src/yendoria --cov-fail-under=55

**Automated Workflows**::

    # Pre-commit hooks (runs on every commit)
    poetry run pre-commit run --all-files

**GitHub Actions Pipeline**:

* **Multi-platform Testing**: Ubuntu, macOS, Windows
* **Multi-Python Testing**: Python 3.10, 3.11, 3.12, 3.13
* **Automated Quality Gates**: All code must pass linting, type checking, and tests
* **Security Scanning**: Weekly automated vulnerability scans
* **Dependency Updates**: Automated Dependabot integration
* **Test Coverage Reporting**: Codecov integration with coverage thresholds

### Documentation

Build documentation::

    cd docs
    poetry run sphinx-build -b html . _build/html

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
