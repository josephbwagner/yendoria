# Code Quality Setup

This document describes the linting, formatting, and type checking setup for Yendoria.

## Tools Used

### Ruff
- **Purpose**: Fast linter and formatter for Python
- **Features**:
  - Linting (replaces flake8, pylint)
  - Code formatting (replaces black)
  - Import sorting (replaces isort)
  - Supports modern Python features

### MyPy
- **Purpose**: Static type checking
- **Features**:
  - Catches type-related errors
  - Improves code documentation
  - Helps with IDE support

### Pre-commit
- **Purpose**: Git hooks for automated checks
- **Features**:
  - Runs checks before each commit
  - Automatically fixes issues when possible
  - Ensures consistent code quality

## Configuration

All tool configurations are stored in `pyproject.toml`:

- **Ruff**: Configured for 88-character line length, Python 3.10+ features
- **MyPy**: Moderate strictness settings, ignores missing imports for external libraries

## Usage

### Manual Commands

```bash
# Linting
poetry run ruff check .

# Auto-fix linting issues
poetry run ruff check --fix .

# Format code
poetry run ruff format .

# Type checking
poetry run mypy src

# Check formatting without changing files
poetry run ruff format --check .
```

### VS Code Integration

The setup includes:

- **Settings**: `.vscode/settings.json` with format-on-save enabled
- **Tasks**: `.vscode/tasks.json` with linting and formatting tasks
- **Extensions**: `.vscode/extensions.json` with recommended extensions

#### Recommended Extensions:
- `charliermarsh.ruff` - Ruff linter and formatter
- `ms-python.mypy-type-checker` - MyPy type checking
- `ms-python.python` - Python language support
- `ms-python.vscode-pylance` - Enhanced Python language server

### Pre-commit Hooks

Hooks are automatically installed and run before each commit:

```bash
# Install hooks (already done)
poetry run pre-commit install

# Run hooks manually on all files
poetry run pre-commit run --all-files

# Skip hooks for a commit (use sparingly)
git commit --no-verify
```

### VS Code Tasks

You can run tasks from VS Code:
1. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Tasks: Run Task"
3. Select from:
   - **Lint with Ruff**
   - **Format with Ruff**
   - **Type Check with MyPy**
   - **Run All Checks**

## Automation Levels

1. **Editor Level**: Real-time feedback in VS Code
2. **Save Level**: Auto-formatting on save
3. **Commit Level**: Pre-commit hooks ensure quality
4. **Manual Level**: Run commands when needed

## Configuration Details

### Ruff Rules Enabled:
- `E`, `F`: Standard pycodestyle and Pyflakes
- `UP`: pyupgrade (modernize Python code)
- `I`: isort (import sorting)
- `PL`: pylint (additional linting)
- `B`: flake8-bugbear (find likely bugs)
- `SIM`: flake8-simplify (simplify code)
- `C4`: flake8-comprehensions (improve comprehensions)

### MyPy Settings:
- Checks untyped definitions
- Warns about redundant casts and unused ignores
- Strict optional checking enabled
- Moderate strictness (can be increased later)

## Customization

To modify tool behavior, edit the relevant sections in `pyproject.toml`:

- `[tool.ruff]` and `[tool.ruff.lint]` for Ruff settings
- `[tool.mypy]` for MyPy settings

## Troubleshooting

### Common Issues:

1. **Line too long**: Ruff enforces 88-character lines. Break long lines or use parentheses for expressions.

2. **Import organization**: Ruff automatically sorts imports. Don't organize them manually.

3. **Type errors**: Add type hints gradually. Use `# type: ignore` comments sparingly for external library issues.

4. **Pre-commit failures**: Fix the issues and commit again, or run `poetry run pre-commit run --all-files` to see all issues.

### Disabling Rules:

For specific lines:
```python
result = some_long_function_call()  # noqa: E501
```

For entire files, add to `pyproject.toml`:
```toml
[tool.ruff.lint.per-file-ignores]
"path/to/file.py" = ["E501", "F401"]
```
