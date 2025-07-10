# Release Automation Guide

Yendoria uses automated semantic versioning and release management to ensure consistent, predictable releases.

## 🔄 How It Works

### 1. Conventional Commits Drive Versioning

Every commit message determines the next version bump:

```bash
# Patch version bump (0.1.0 → 0.1.1)
git commit -m "fix(combat): correct damage calculation for critical hits"

# Minor version bump (0.1.0 → 0.2.0)
git commit -m "feat(inventory): add item pickup and storage system"

# Major version bump (0.1.0 → 1.0.0)
git commit -m "feat!: redesign combat system with breaking API changes"
```

### 2. Automated Release Process

When code is pushed to `master`:

1. **🧪 CI Tests Run**: Full test suite, linting, type checking, security scans
2. **📊 Commit Analysis**: `semantic-release` analyzes commit history since last release
3. **🔢 Version Calculation**: Determines next version based on conventional commits
4. **📝 Changelog Update**: Automatically updates `CHANGELOG.md` with categorized changes
5. **🏷️ Version Bumping**: Updates version in:
   - `pyproject.toml`
   - `src/yendoria/__init__.py`
   - `docs/conf.py`
6. **📦 Build & Release**: Creates distribution packages and GitHub release
7. **🎉 Artifacts**: Uploads wheel and source distributions

### 3. Version Strategy

Following [Semantic Versioning](https://semver.org/):

- **Major** (X.0.0): Breaking changes (`feat!:`, `BREAKING CHANGE:`)
- **Minor** (0.X.0): New features (`feat:`)
- **Patch** (0.0.X): Bug fixes (`fix:`, `perf:`)

## 🛠️ Developer Workflow

### Making a Conventional Commit

Use the VS Code task or command line:

```bash
# VS Code Task
Cmd/Ctrl + Shift + P → "Tasks: Run Task" → "Conventional Commit"

# Command Line
poetry run cz commit
```

This will guide you through creating a properly formatted commit message.

### Checking What's Coming Next

Preview the next version without making changes:

```bash
# VS Code Task
"Preview Next Version"

# Command Line
poetry run semantic-release version --print
```

### Manual Release Testing

Validate your release setup locally:

```bash
# VS Code Task
"Validate Release Setup"

# Command Line Commands
poetry version --short                    # Current version
poetry run cz version --dry-run          # Next version preview
poetry build                             # Test package building
```

## 📋 VS Code Tasks Available

| Task | Purpose |
|------|---------|
| **Conventional Commit** | Interactive commit message creation |
| **Check Current Version** | Display current project version |
| **Preview Next Version** | See what the next release version would be |
| **Generate Changelog** | Update changelog with commitizen |
| **Build Release Package** | Create distribution packages |
| **Validate Release Setup** | Test all release components |

## 🚀 Release Workflow Triggers

### Automatic Releases

- **Trigger**: Push to `master` branch
- **Condition**: Must have new commits since last release
- **Requirements**: All CI tests must pass

### Manual Releases

- **Trigger**: GitHub Actions → "Release" workflow → "Run workflow"
- **Options**: Can force release even without changes
- **Use Case**: Hotfixes, manual version bumps

## 📁 File Locations

| File | Purpose |
|------|---------|
| `CHANGELOG.md` | Auto-generated release notes |
| `pyproject.toml` | Version source and tool configuration |
| `src/yendoria/__init__.py` | Package version variable |
| `docs/conf.py` | Documentation version |
| `.github/workflows/release.yml` | Release automation workflow |
| `docs/CONVENTIONAL_COMMITS.md` | Commit message guide |

## 🎯 Best Practices

### 1. Descriptive Commit Messages

```bash
# Good
feat(gameplay): add inventory system with drag-and-drop UI

# Bad
feat: add stuff
```

### 2. Scope Usage

Use scopes to categorize changes:
- `feat(gameplay)`: Game mechanics
- `feat(ui)`: User interface
- `fix(rendering)`: Graphics/display
- `fix(audio)`: Sound system
- `docs(api)`: API documentation

### 3. Breaking Changes

When making breaking changes:

```bash
# Option 1: Exclamation mark
feat!: redesign save game format

# Option 2: Footer
feat: redesign save game format

BREAKING CHANGE: Save games from previous versions are incompatible
```

### 4. Multiple Changes

For commits with multiple types, use the most significant:

```bash
# If you fix bugs AND add features, prefer feat:
feat(combat): add new spell system and fix damage calculation
```

## 🔍 Troubleshooting

### No Release Generated

**Problem**: Pushed to master but no release was created
**Solutions**:
1. Check if commits follow conventional format
2. Verify CI tests passed
3. Look for existing release with same version
4. Use manual release with force option

### Version Not Updated

**Problem**: Version stayed the same after release
**Solutions**:
1. Ensure commits have version-affecting types (`feat`, `fix`, `perf`)
2. Check for conventional commit format compliance
3. Verify `semantic-release` configuration in `pyproject.toml`

### Build Failures

**Problem**: Release workflow fails during build
**Solutions**:
1. Run `poetry build` locally to test
2. Check dependencies are locked in `poetry.lock`
3. Verify all tests pass with `poetry run pytest`

## 📚 Further Reading

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Python Semantic Release](https://python-semantic-release.readthedocs.io/)
- [Commitizen](https://commitizen-tools.github.io/commitizen/)

---

*This automation ensures every release is properly versioned, documented, and tested before reaching users.*
