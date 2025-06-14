# Yendoria

A traditional tile-based roguelike game built with Python and libtcod, featuring ASCII graphics, turn-based gameplay, and procedural dungeon generation.

## Features

### Core Gameplay
- **Turn-based gameplay**: Player and monster actions alternate in turns
- **ASCII graphics**: Traditional roguelike visual style using character-based graphics
- **Field of view**: Dynamic lighting system with 8-tile radius revealing map as you explore
- **Exploration system**: Tiles become "explored" once seen and remain visible in darker colors
- **Combat system**: Melee combat with health and damage mechanics

### Map Generation
- **Procedural dungeons**: Randomly generated levels with rooms and corridors
- **Room-based design**: Connected rectangular rooms with L-shaped corridors
- **Collision detection**: Proper wall and entity collision handling
- **Configurable generation**: Max 30 rooms, sizes between 6x6 and 10x10

### Entity System
- **Component-based architecture**: Flexible ECS (Entity Component System) design
- **Player character**: Controllable '@' character with health and movement
- **Monster AI**: Basic AI for orcs and trolls with movement and targeting
- **Health system**: Hit points and damage mechanics with component-based architecture
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
# Preferred method (runs without warnings)
poetry run python -m yendoria

# Alternative method (also works)
poetry run python -m yendoria.main
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
- **Components**: Data containers (Position, Health, Graphic, AI, Damage)
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

### Code Quality & CI/CD Pipeline
This project uses **production-grade development practices** with:

#### 🔄 **Continuous Integration**
- **GitHub Actions CI**: Multi-platform testing (Ubuntu, macOS, Windows)
- **Multi-Python Support**: Tested on Python 3.10, 3.11, 3.12, 3.13
- **Automated Quality Gates**: All code must pass linting, formatting, type checking, and tests
- **Test Coverage Reporting**: Comprehensive coverage tracking with Codecov integration

#### 🔒 **Security & Dependencies**
- **Automated Security Scanning**: Bandit (code security) + Safety (dependency vulnerabilities)
- **Dependabot Integration**: Automated dependency updates with security patches
- **pip-audit**: Additional dependency vulnerability scanning
- **Weekly Security Audits**: Scheduled automated security reviews

#### 📊 **Quality Assurance**
- **Ruff**: Ultra-fast linting and formatting (replaces flake8, black, isort)
- **MyPy**: Static type checking with strict configuration
- **Pre-commit Hooks**: Automated checks before every commit
- **Test Coverage**: 55%+ coverage requirement with branch coverage tracking

#### 🛠️ **Developer Experience**
- **VS Code Integration**: Comprehensive tasks and settings
- **Professional Templates**: Issue and PR templates for structured collaboration
- **Automated Workflows**: One-command quality validation

#### Quick Commands:
```bash
# 🔍 Code Quality Checks
poetry run ruff check --fix .     # Lint and auto-fix
poetry run ruff format .          # Format code
poetry run mypy                   # Type checking

# 🧪 Testing & Coverage
poetry run pytest                 # Run tests
poetry run pytest --cov=src/yendoria --cov-report=html  # Test with coverage

# 🔒 Security Scanning
poetry run bandit -r src/         # Security linting
poetry run safety check           # Dependency vulnerabilities

# 🚀 Complete CI Check (runs all validations)
poetry run ruff check . && poetry run ruff format --check . && poetry run mypy && poetry run pytest --cov=src/yendoria --cov-fail-under=55

# ⚡ Pre-commit (automated on git commit)
poetry run pre-commit run --all-files
```

#### VS Code Tasks
Access via Command Palette (`Cmd+Shift+P`/`Ctrl+Shift+P`) → "Tasks: Run Task":
- **Run Yendoria** - Start the game
- **Lint with Ruff** - Check code quality
- **Format with Ruff** - Format code
- **Type Check with MyPy** - Static analysis
- **Run Tests with Coverage** - Full test suite with coverage
- **Security Scan with Bandit** - Code security check
- **Security Check with Safety** - Dependency vulnerabilities
- **Full CI Check** - Complete validation pipeline

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed setup and usage information.

### Running Tests
Execute the test suite:
```bash
# Basic test run
poetry run pytest

# With coverage reporting
poetry run pytest --cov=src/yendoria

# Generate HTML coverage report
poetry run pytest --cov=src/yendoria --cov-report=html
# View report: open htmlcov/index.html

# With coverage threshold (CI requirement)
poetry run pytest --cov=src/yendoria --cov-fail-under=55
```

**Current Test Metrics:**
- ✅ **25/25 tests passing**
- ✅ **55.87% code coverage** (above 55% threshold)
- ✅ **Cross-platform compatibility** (Ubuntu, macOS, Windows)
- ✅ **Multi-Python version support** (3.10-3.13)

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

### Local Development Build
```bash
# Install in development mode
poetry install

# Build distribution packages
poetry build

# Install from built package
pip install dist/yendoria-0.1.0-py3-none-any.whl
```

### Production Deployment
The project includes **GitHub Actions workflows** for:
- ✅ **Automated builds** on every PR and push
- ✅ **Multi-platform testing** (Ubuntu, macOS, Windows)
- ✅ **Security scanning** and dependency updates
- ✅ **Release automation** (ready for semantic versioning)

**CI/CD Pipeline Status:**
- 🔄 **Continuous Integration**: Full quality gate validation
- 🔒 **Security**: Automated vulnerability scanning
- 📦 **Packaging**: Ready for PyPI publication
- 🏷️ **Releases**: Automated GitHub releases (when tagged)

## Project Status

### Current Implementation
✅ **Completed Features:**
- Complete ECS (Entity Component System) architecture
- Procedural dungeon generation with rooms and corridors
- Field of view calculation and exploration tracking
- Player movement with multiple input schemes
- Monster entities (orcs and trolls) with basic AI behavior
- Damage system with component-based combat mechanics
- Tile-based map system with proper graphics
- **Production-grade CI/CD pipeline** with GitHub Actions
- **Comprehensive test suite** (25 tests, 55%+ coverage)
- **Multi-platform compatibility** (Ubuntu, macOS, Windows, Python 3.10-3.13)
- **Automated security scanning** (Bandit, Safety, pip-audit)
- **Professional development workflows** (pre-commit, quality gates)
- Full documentation and development setup

🚧 **Planned Features:**
- Full combat system implementation (damage dealing/taking)
- Advanced monster AI with pathfinding
- UI improvements (health display, message log)
- Sound effects and enhanced graphics
- Save/load game functionality
- Multiple dungeon levels

## Documentation

📚 **Online Documentation**: https://your-username.github.io/roguelike-game/

The project documentation is automatically built and deployed to GitHub Pages using Sphinx. The documentation includes:

- **API Reference**: Complete code documentation with type hints
- **Getting Started Guide**: Installation and usage instructions
- **Development Guide**: Contributing guidelines and development setup
- **Architecture Overview**: Component system and game engine design

### Building Documentation Locally

Build documentation with Sphinx:
```bash
cd docs
poetry run sphinx-build -b html . _build/html
```

View the built documentation by opening `docs/_build/html/index.html` in your browser.

### Documentation Deployment

Documentation is automatically built and deployed via GitHub Actions:
- **Trigger**: Pushes to `main` branch and pull requests
- **Build**: Sphinx generates HTML documentation with the Furo theme
- **Deploy**: Automatically deployed to GitHub Pages on pushes to `main`
- **Manual**: Can be triggered manually from the Actions tab

## Dependencies

### Runtime Dependencies
- **tcod** (^16.0.0): The libtcod Python library for roguelike development
- **numpy** (^2.0.0): For efficient array operations (map tiles, FOV)

### Development Dependencies
- **pytest** (^7.0): Testing framework with coverage support
- **pytest-cov**: Test coverage reporting and HTML generation
- **pytest-html**: Enhanced test reports with HTML output
- **mypy**: Static type checking and analysis
- **ruff**: Ultra-fast linting, formatting, and import sorting
- **bandit**: Security vulnerability scanning for code
- **safety**: Dependency vulnerability scanning
- **pre-commit**: Git hooks for automated quality checks
- **sphinx** (^7.0): Documentation generation (Python 3.13 compatible)
- **sphinx-autodoc-typehints**: Type hints in generated documentation

### CI/CD Dependencies
- **GitHub Actions**: Multi-platform testing and deployment
- **Codecov**: Test coverage reporting and tracking
- **Dependabot**: Automated dependency updates and security patches

## Contributing

We welcome contributions! This project follows **production-grade development practices**.

### Quick Start for Contributors
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. **Set up development environment:**
   ```bash
   poetry install
   poetry run pre-commit install  # Install quality hooks
   ```

### Development Workflow
4. Make your changes following our **automated quality standards**
5. **Quality checks** (automated via pre-commit):
   ```bash
   # These run automatically on commit, or manually:
   poetry run ruff check --fix .    # Auto-fix linting issues
   poetry run ruff format .         # Format code
   poetry run mypy                  # Type checking
   poetry run pytest               # Run tests
   ```
6. Add tests for new functionality (**55%+ coverage required**)
7. Ensure **all CI checks pass** (ruff, mypy, pytest, security scans)
8. Commit your changes (`git commit -am 'Add amazing feature'`)
9. Push to the branch (`git push origin feature/amazing-feature`)
10. Create a Pull Request using our **PR template**

### Quality Standards (Automated)
- ✅ **Code Style**: Ruff linting and formatting (enforced)
- ✅ **Type Safety**: MyPy static analysis (zero errors required)
- ✅ **Test Coverage**: 55%+ coverage with passing tests
- ✅ **Security**: Bandit security scanning (no high-risk issues)
- ✅ **Dependencies**: Safety vulnerability scanning
- ✅ **Multi-platform**: Must work on Ubuntu, macOS, Windows
- ✅ **Multi-Python**: Compatible with Python 3.10-3.13

### Professional Templates
- 🐛 **Bug Report Template**: Structured issue reporting
- ✨ **Feature Request Template**: Game design consideration guidelines
- 🔧 **Technical Issue Template**: Architecture and code quality improvements
- 📝 **Pull Request Template**: Comprehensive change documentation

### Coding Standards (Automated Enforcement)
- **PEP 8 Compliance**: Enforced via Ruff linting
- **Type Hints**: Required for all functions (MyPy validation)
- **Documentation**: Docstrings required for classes and public functions
- **Testing**: Write tests for new functionality (pytest framework)
- **Security**: No security vulnerabilities (Bandit + Safety scanning)
- **Import Organization**: Automated via Ruff import sorting
- **Code Formatting**: Consistent style via Ruff formatting (88-char lines)

### Automated Quality Checks
When you commit, **pre-commit hooks automatically**:
1. 🔧 **Fix linting issues** where possible
2. 🎨 **Format code** to consistent style
3. 🔍 **Check types** with MyPy
4. 🔒 **Scan for security** issues
5. ✅ **Validate file consistency**

**CI Pipeline** runs on every PR:
- 🏗️ **Multi-platform builds** (Ubuntu, macOS, Windows)
- 🐍 **Multi-Python testing** (3.10, 3.11, 3.12, 3.13)
- 📊 **Test coverage analysis** with Codecov reporting
- 🔐 **Security vulnerability scanning**

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Built with [python-tcod](https://github.com/libtcod/python-tcod)
- Inspired by classic roguelike games like Rogue, NetHack, and Angband
- Tutorial influence from [Roguelike Tutorial Revised](http://rogueliketutorials.com/)
