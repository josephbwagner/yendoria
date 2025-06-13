# Contributing to Yendoria

This document describes the **production-grade development practices** for Yendoria, including our comprehensive CI/CD pipeline, quality assurance tools, and automated workflows.

## 🚀 Development Environment Setup

### Prerequisites
- Python 3.10+ (tested on 3.10, 3.11, 3.12, 3.13)
- Poetry for dependency management
- Git for version control

### Quick Setup
```bash
# Clone and setup
git clone <repository-url>
cd yendoria
poetry install

# Install automated quality hooks
poetry run pre-commit install

# Verify setup
poetry run pytest                    # Run tests
poetry run ruff check .             # Check code quality
poetry run mypy                     # Type checking
```

## 🏭 Production-Grade Tools

### Core Quality Stack

### Core Quality Stack

#### 🔧 Ruff - Ultra-Fast Python Tooling
- **Purpose**: All-in-one linting, formatting, and import sorting
- **Features**:
  - Replaces flake8, black, isort, and more
  - 10-100x faster than traditional tools
  - Auto-fixes most issues
  - Modern Python feature support

#### 🎯 MyPy - Static Type Analysis
- **Purpose**: Catch type-related errors before runtime
- **Features**:
  - Static type checking with gradual typing
  - IDE integration for better development experience
  - Configurable strictness levels
  - External library type stub support

#### 🪝 Pre-commit - Automated Quality Gates
- **Purpose**: Enforce quality standards on every commit
- **Features**:
  - Runs multiple tools automatically
  - Prevents bad code from entering repository
  - Auto-fixes issues when possible
  - Integrates with CI/CD pipeline

#### 🧪 Pytest - Comprehensive Testing
- **Purpose**: Test framework with coverage tracking
- **Features**:
  - 25+ unit tests covering core functionality
  - 55%+ code coverage requirement
  - HTML coverage reports
  - Parameterized and fixture-based testing

#### 🔒 Security Stack
- **Bandit**: Python security linting (checks for common vulnerabilities)
- **Safety**: Dependency vulnerability scanning
- **pip-audit**: Additional dependency security analysis

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

#### Main CI Pipeline (`.github/workflows/ci.yml`)
- **Triggers**: Every push and PR to main/develop branches
- **Matrix Testing**:
  - **OS**: Ubuntu, macOS, Windows
  - **Python**: 3.10, 3.11, 3.12, 3.13
- **Quality Gates**:
  1. Ruff linting and formatting validation
  2. MyPy static type checking
  3. Full test suite with coverage reporting
  4. Codecov integration for coverage tracking

#### Security Scanning (`.github/workflows/security.yml`)
- **Triggers**: Every push/PR + weekly scheduled scans
- **Scans**:
  1. Bandit security linting
  2. Safety dependency vulnerability check
  3. pip-audit additional security analysis
- **Reporting**: Security artifacts uploaded for review

#### Dependency Management
- **Dependabot**: Automated dependency updates
- **Schedule**: Weekly updates for Python packages and GitHub Actions
- **Security**: Automatic security patch updates

## ⚙️ Configuration

All tool configurations are centralized in `pyproject.toml`:

### Pytest & Coverage Configuration
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--cov=src/yendoria",
    "--cov-report=html:htmlcov",
    "--cov-report=xml:coverage.xml",
    "--cov-fail-under=55",
    "--cov-branch"
]
```

### Ruff Configuration
```toml
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "UP", "I", "PL", "B", "SIM", "C4"]
```

### MyPy Configuration
```toml
[tool.mypy]
python_version = "3.10"
check_untyped_defs = true
warn_redundant_casts = true
files = ["src/yendoria", "tests"]
```

### Security Configuration
```toml
[tool.bandit]
exclude_dirs = ["tests", "build", "dist"]
skips = ["B311"]  # Allow random for games
```

## 💻 Development Workflow

### Daily Development Commands

```bash
# 🔍 Code Quality
poetry run ruff check --fix .       # Lint with auto-fix
poetry run ruff format .            # Format code
poetry run mypy                     # Type checking

# 🧪 Testing & Coverage
poetry run pytest                   # Run tests
poetry run pytest --cov=src/yendoria --cov-report=html  # With coverage
open htmlcov/index.html             # View coverage report

# 🔒 Security Scanning
poetry run bandit -r src/           # Security linting
poetry run safety check             # Dependency vulnerabilities

# ⚡ Complete Validation (matches CI)
poetry run ruff check . && \
poetry run ruff format --check . && \
poetry run mypy && \
poetry run pytest --cov=src/yendoria --cov-fail-under=55

# 🪝 Pre-commit Testing
poetry run pre-commit run --all-files
```

### VS Code Integration (Recommended)

### VS Code Integration (Recommended)

**Automatic Setup**: The project includes complete VS Code configuration:

#### Extensions (`.vscode/extensions.json`)
- `charliermarsh.ruff` - Ruff linting and formatting
- `ms-python.mypy-type-checker` - MyPy integration
- `ms-python.python` - Python language support
- `ms-python.vscode-pylance` - Enhanced language server

#### Settings (`.vscode/settings.json`)
- **Format on Save**: Automatic code formatting
- **Lint on Save**: Real-time error detection
- **Type Checking**: Live MyPy integration

#### Tasks (`.vscode/tasks.json`)
Access via `Cmd+Shift+P` → "Tasks: Run Task":
- **Run Yendoria** - Start the game
- **Lint with Ruff** - Code quality check
- **Format with Ruff** - Code formatting
- **Type Check with MyPy** - Static analysis
- **Run Tests with Coverage** - Full test suite
- **Security Scan with Bandit** - Security check
- **Security Check with Safety** - Dependency scan
- **Full CI Check** - Complete validation pipeline

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
