# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Release automation with semantic versioning
- Conventional commit workflow
- Automated changelog generation

## [0.1.0] - 2025-06-13

### Added
- Initial release of Yendoria roguelike game
- Core gameplay mechanics:
  - Turn-based gameplay with player and monster entities
  - Procedural dungeon generation with rooms and corridors
  - Field of view system with 8-tile radius
  - ASCII graphics using tcod library
  - Multiple input schemes (arrow keys, WASD, vim keys, numpad)
  - Basic combat system with health and damage
- Component-based entity system architecture
- Production-grade development setup:
  - Multi-platform CI/CD pipeline (Ubuntu, macOS, Windows)
  - Multi-Python version support (3.10, 3.11, 3.12, 3.13)
  - Comprehensive quality gates (ruff, mypy, pytest)
  - Security scanning (bandit, safety, pip-audit)
  - Test coverage reporting with Codecov
  - Automated dependency updates with Dependabot
  - Pre-commit hooks for code quality
  - GitHub issue and PR templates
  - VS Code integration with tasks
- Documentation:
  - Sphinx documentation with Furo theme
  - Automated GitHub Pages deployment
  - API documentation with type hints
  - Development guides and setup instructions

### Technical Details
- Built with Python 3.10+ and Poetry for dependency management
- Uses tcod 19.0.0 for terminal graphics and input handling
- Implements Entity Component System (ECS) architecture
- Comprehensive test suite with 55%+ coverage
- Type-checked with MyPy for reliability
- Linted and formatted with Ruff for consistency

[Unreleased]: https://github.com/josephbwagner/yendoria/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/josephbwagner/yendoria/releases/tag/v0.1.0
