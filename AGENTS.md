# Agent Guidelines for Yendoria

## Build/Test Commands
- Run tests: `poetry run pytest` (single test: `poetry run pytest tests/test_specific.py::test_function`)
- Lint/format: `poetry run ruff check --fix && poetry run ruff format`
- Type check: `poetry run mypy src`
- Security scan: `poetry run bandit -r src`
- Pre-commit hooks: `poetry run pre-commit run --all-files`
- Build package: `poetry build`

## Code Style
- **Formatting**: Use Ruff (Black-compatible): 88 char lines, double quotes, 4-space indent
- **Imports**: Use `from .module import Item` for relative imports, sort with isort rules
- **Types**: Add type hints for function parameters/returns, use `TYPE_CHECKING` for circular imports
- **Docstrings**: Google-style docstrings for all public functions/classes
- **Naming**: snake_case for functions/variables, PascalCase for classes, UPPER_CASE for constants
- **Error handling**: Use specific exceptions, prefer early returns over deep nesting

## Project Structure
- Source code: `src/yendoria/` (entities, components, systems, utils)
- Tests: `tests/` with coverage >55% required
- Config: Use `pyproject.toml` for all tool configuration
- Commits: Follow conventional commits (feat/fix/docs/etc.)