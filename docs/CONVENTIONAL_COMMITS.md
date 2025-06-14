# Conventional Commits Guide

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for standardized commit messages and automated versioning.

## Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

### Version Impact
- **feat**: A new feature (triggers **minor** version bump)
- **fix**: A bug fix (triggers **patch** version bump)
- **perf**: Performance improvement (triggers **patch** version bump)

### No Version Impact
- **docs**: Documentation only changes
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **refactor**: Code changes that neither fix bugs nor add features
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes to build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files

### Breaking Changes
Add `!` after the type (e.g., `feat!:`) or include `BREAKING CHANGE:` in the footer to trigger a **major** version bump.

## Examples

### Feature Addition
```
feat(gameplay): add inventory system

- Implement item pickup and storage
- Add inventory UI with keyboard shortcuts
- Support for consumable and equipment items

Closes #42
```

### Bug Fix
```
fix(rendering): correct field of view calculation

Fixed off-by-one error in FOV algorithm that caused
tiles at maximum range to not be properly revealed.

Fixes #38
```

### Breaking Change
```
feat!: change save file format for better performance

BREAKING CHANGE: Save files from versions prior to 2.0.0
are no longer compatible and will need to be recreated.
```

### Documentation
```
docs: update installation instructions

Add Poetry installation steps and troubleshooting section
for common setup issues on Windows.
```

### Performance Improvement
```
perf(map): optimize pathfinding algorithm

Replace naive A* implementation with optimized version
using binary heap, reducing pathfinding time by 60%.
```

## Using Commitizen

This project includes [Commitizen](https://commitizen-tools.github.io/commitizen/) to help create conventional commits:

```bash
# Interactive commit message creation
poetry run cz commit

# Or use the shorter alias
poetry run cz c
```

## Automated Versioning

The release workflow automatically:

1. **Analyzes commits** since the last release
2. **Determines version bump** based on commit types:
   - `feat`: Minor version bump (0.1.0 → 0.2.0)
   - `fix`, `perf`: Patch version bump (0.1.0 → 0.1.1)
   - Breaking changes: Major version bump (0.1.0 → 1.0.0)
3. **Updates version** in pyproject.toml, __init__.py, and docs
4. **Generates changelog** from commit messages
5. **Creates Git tag** and GitHub release
6. **Builds distribution packages**

## Best Practices

### Commit Message Tips
- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- Keep the description under 50 characters
- Capitalize the description
- Don't end the description with a period
- Use the body to explain what and why (not how)

### Scope Guidelines
- **gameplay**: Core game mechanics (combat, movement, etc.)
- **entities**: Player, monsters, items
- **map**: Map generation, tiles, rooms
- **ui**: User interface, menus, HUD
- **graphics**: Rendering, colors, animations
- **audio**: Sound effects, music
- **save**: Save/load functionality
- **config**: Configuration and settings
- **docs**: Documentation changes
- **tests**: Test-related changes
- **build**: Build system, dependencies
- **ci**: Continuous integration

### Example Workflow
1. Make your changes
2. Stage your files: `git add .`
3. Create conventional commit: `poetry run cz commit`
4. Push to branch: `git push origin feature-branch`
5. Create pull request
6. After merge to master, release workflow runs automatically
