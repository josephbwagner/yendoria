# Yendoria

A traditional tile-based roguelike game built with Python and libtcod, featuring ASCII graphics, turn-based gameplay, and procedural dungeon generation.

## Features

### Core Gameplay
- **Turn-based gameplay**: Player and monster actions alternate in turns
- **ASCII graphics**: Traditional roguelike visual style using character-based graphics
- **Field of view**: Dynamic lighting system with 8-tile radius revealing map as you explore
- **Exploration system**: Tiles become "explored" once seen and remain visible in darker colors
- **Combat system**: Melee combat with health and damage mechanics (planned feature)

### Map Generation
- **Procedural dungeons**: Randomly generated levels with rooms and corridors
- **Room-based design**: Connected rectangular rooms with L-shaped corridors
- **Collision detection**: Proper wall and entity collision handling
- **Configurable generation**: Max 30 rooms, sizes between 6x6 and 10x10

### Entity System
- **Component-based architecture**: Flexible ECS (Entity Component System) design
- **Player character**: Controllable '@' character with health and movement
- **Monster AI**: Basic AI for orcs and trolls (AI system ready for implementation)
- **Health system**: Hit points and damage mechanics (entities have health components)
- **Graphics system**: Customizable character representation and colors

### Input & Controls
- **Multiple input schemes**: Arrow keys, WASD, vim keys, and numpad support
- **Responsive controls**: Smooth movement and action handling
- **Escape to quit**: Standard exit mechanism

## Installation

### Requirements
- Python 3.10 or higher
- Poetry (for dependency management)

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd yendoria
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

## Usage

### Running the Game
Start the game with:
```bash
poetry run python -m yendoria
```

Or use the VS Code task:
- Open the Command Palette (`Cmd+Shift+P` on macOS, `Ctrl+Shift+P` on Windows/Linux)
- Type "Tasks: Run Task"
- Select "Run Yendoria"

### Controls
- **Movement**: Arrow keys, WASD, vim keys (hjkl), or numpad (including diagonals)
- **Exploration**: Move to reveal new areas within field of view
- **Quit**: Press Escape or close the window

### Gameplay
1. Use movement keys to explore the dungeon
2. The '@' symbol represents your character
3. 'o' represents orcs, 'T' represents trolls
4. Dark blue areas are unexplored walls, lighter areas are explored
5. Your field of view illuminates an 8-tile radius around you
6. Explore all rooms to map out the dungeon!

## Architecture

### Component System
The game uses an Entity Component System (ECS) architecture:

- **Entities**: Containers for components (Player, Orc, Troll)
- **Components**: Data containers (Position, Health, Graphic, AI)
- **Systems**: Logic processors (Rendering, Input handling)

### Key Modules
- `engine.py`: Main game loop and coordination
- `game_map/`: Map generation and tile management
- `entities/`: Entity creation and management
- `components/`: ECS component definitions
- `systems/`: Game systems (rendering, etc.)
- `input_handlers/`: Input processing
- `utils/constants.py`: Game configuration and constants

## Development

### Running Tests
Execute the test suite:
```bash
poetry run pytest
```

Run tests with coverage:
```bash
poetry run pytest --cov=yendoria
```

### Code Structure
```
src/yendoria/
├── main.py              # Entry point
├── engine.py            # Game engine
├── components/          # ECS components
│   └── component.py
├── entities/            # Entity factories
│   ├── entity.py
│   ├── player.py
│   └── monster.py
├── game_map/            # Map system
│   ├── game_map.py
│   ├── tile.py
│   └── room.py
├── input_handlers/      # Input processing
│   └── event_handler.py
├── systems/             # Game systems
│   └── rendering.py
└── utils/               # Utilities
    └── constants.py
```

### Adding New Features

#### New Monster Types
1. Add monster factory function in `entities/monster.py`
2. Define unique graphics and stats
3. Update spawn logic in `engine.py`

#### New Components
1. Create component class in `components/component.py`
2. Add to entity factory functions
3. Update relevant systems to handle the component

#### New Map Features
1. Extend `GameMap` class in `game_map/game_map.py`
2. Add new tile types in `game_map/tile.py`
3. Update rendering system if needed

## Building and Distribution

### Create Distribution Package
```bash
poetry build
```

### Install from Built Package
```bash
pip install dist/yendoria-0.1.0-py3-none-any.whl
```

## Project Status

### Current Implementation
✅ **Completed Features:**
- Complete ECS (Entity Component System) architecture
- Procedural dungeon generation with rooms and corridors
- Field of view calculation and exploration tracking
- Player movement with multiple input schemes
- Monster entities (orcs and trolls) with positioning
- Tile-based map system with proper graphics
- Comprehensive test suite (25 tests)
- Full documentation and development setup

🚧 **Planned Features:**
- Combat system implementation
- Monster AI activation and pathfinding
- UI improvements (health display, message log)
- Sound effects and enhanced graphics
- Save/load game functionality
- Multiple dungeon levels

## Documentation

Build documentation with Sphinx:
```bash
poetry run python -m sphinx -b html docs docs/_build/html
```

View the built documentation by opening `docs/_build/html/index.html` in your browser.

## Dependencies

### Runtime Dependencies
- **tcod** (^16.0.0): The libtcod Python library for roguelike development
- **numpy** (^2.0.0): For efficient array operations (map tiles, FOV)

### Development Dependencies
- **pytest** (^6.0): Testing framework
- **sphinx** (^7.0): Documentation generation (updated for Python 3.13 compatibility)
- **sphinx-autodoc-typehints**: Type hints in documentation

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`poetry run pytest`)
6. Commit your changes (`git commit -am 'Add new feature'`)
7. Push to the branch (`git push origin feature/new-feature`)
8. Create a Pull Request

### Coding Standards
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include docstrings for all classes and functions
- Write tests for new functionality
- Update documentation as needed

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Built with [python-tcod](https://github.com/libtcod/python-tcod)
- Inspired by classic roguelike games like Rogue, NetHack, and Angband
- Tutorial influence from [Roguelike Tutorial Revised](http://rogueliketutorials.com/)
