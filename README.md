# Yendoria

A traditional tile-based roguelike game built with Python and libtcod, featuring ASCII graphics, turn-based gameplay, procedural dungeon generation, and a sophisticated AI system.

[![CI](https://github.com/josephbwagner/yendoria/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/josephbwagner/yendoria/actions)
[![codecov](https://codecov.io/gh/josephbwagner/yendoria/graph/badge.svg?token=UPLKZ72669)](https://codecov.io/gh/josephbwagner/yendoria)
[![Documentation](https://img.shields.io/badge/docs-sphinx-blue.svg)](https://josephbwagner.github.io/yendoria/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

## 🎮 Quick Start

### Installation
```bash
git clone https://github.com/josephbwagner/yendoria.git
cd yendoria
poetry install
```

### Run the Game
```bash
poetry run python -m yendoria
```

**Controls:** Arrow keys, WASD, vim keys (hjkl), or numpad to move. Escape to quit.

## ✨ Features

### Core Gameplay
- **Turn-based Combat**: Strategic roguelike gameplay with health and damage mechanics
- **Procedural Dungeons**: Randomly generated levels with rooms and corridors
- **Field of View**: Dynamic 8-tile radius exploration system
- **Advanced AI System**: Intelligent NPCs with personality, memory, factions, and behavior trees
- **Multiple Input Schemes**: Flexible controls supporting various preferences

### Technical Excellence
- **Entity Component System (ECS)**: Flexible, modular architecture
- **Production-Grade CI/CD**: Multi-platform testing, automated quality gates, security scanning
- **Comprehensive Documentation**: Sphinx-generated docs with API reference and examples
- **Type Safety**: Full MyPy static type checking
- **Test Coverage**: 55%+ coverage with automated testing across Python 3.10-3.13

## 📚 Documentation

**📖 [Complete Documentation](https://josephbwagner.github.io/yendoria/)** - Comprehensive guides, API reference, and examples

**Key Documentation Sections:**
- **[AI System Guide](docs/ai_overview.rst)** - Advanced AI architecture and usage
- **[API Reference](docs/api.rst)** - Complete code documentation
- **[Development Guide](CONTRIBUTING.md)** - Contributing and development setup
- **[Modding System](docs/modding.rst)** - Extensibility and customization

## 🛠️ Development

### Quality Tools
```bash
# Code quality
poetry run ruff check --fix .     # Lint and auto-fix
poetry run ruff format .          # Format code
poetry run mypy                   # Type checking

# Testing
poetry run pytest --cov=src/yendoria --cov-report=html

# Security
poetry run bandit -r src/         # Security scan
poetry run safety check           # Dependency vulnerabilities

# All checks (CI validation)
poetry run ruff check . && poetry run ruff format --check . && poetry run mypy && poetry run pytest --cov=src/yendoria --cov-fail-under=55
```

### VS Code Integration
Use Command Palette (`Cmd+Shift+P`) → "Tasks: Run Task" for:
- **Run Yendoria** - Start the game
- **Run All Checks** - Complete CI validation
- **Run Tests with Coverage** - Full test suite

## 🏗️ Architecture

**Entity Component System (ECS):**
- **Entities**: Game objects (Player, Monsters, NPCs)
- **Components**: Data containers (Position, Health, AI, Personality)
- **Systems**: Logic processors (AI Manager, Rendering, Combat)

**Key Systems:**
- **AI System**: Modular behavior with basic/advanced implementations
- **Configuration System**: JSON-based archetypes and faction definitions
- **Event System**: Decoupled communication between systems
- **Error Handling**: Robust error recovery and performance monitoring

See the [complete architecture documentation](https://josephbwagner.github.io/yendoria/) for detailed information.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup and workflow
- Code quality standards (automated via pre-commit hooks)
- Testing requirements (55%+ coverage)
- Architecture guidelines

**Quality Standards (Automated):**
- ✅ Ruff linting and formatting
- ✅ MyPy type checking
- ✅ Pytest with coverage reporting
- ✅ Security scanning (Bandit, Safety)
- ✅ Multi-platform compatibility (Ubuntu, macOS, Windows)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [python-tcod](https://github.com/libtcod/python-tcod)
- Inspired by classic roguelikes: Rogue, NetHack, Angband
- Tutorial influence from [Roguelike Tutorial Revised](http://rogueliketutorials.com/)
