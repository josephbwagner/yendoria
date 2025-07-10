# Shared Components Analysis

This document analyzes components that could reasonably belong to either the engine or commercial game, requiring strategic decisions.

## Components Requiring Strategic Decision

### 1. Basic Examples (`examples/basic_game.py`, `examples/simple_dungeon.py`)

**Considerations:**
- **Engine**: Helps developers understand basic game structure
- **Commercial**: Contains specific game mechanics and content

**Recommendation**: **Engine** - Educational value outweighs IP concerns for basic examples

### 2. Core Documentation (`README.md`, base documentation)

**Considerations:**
- **Engine**: Attracts developers with project overview
- **Commercial**: Contains game-specific information and branding

**Recommendation**: **Split** - Create separate READMEs for each repository with appropriate focus

### 3. Build Infrastructure (`.github/workflows/`, basic CI/CD)

**Considerations:**
- **Engine**: Community benefits from seeing professional CI/CD setup
- **Commercial**: May contain proprietary deployment information

**Recommendation**: **Engine** - Basic CI/CD workflows help community contributions

### 4. Development Tools (`scripts/`, basic utilities)

**Considerations:**
- **Engine**: Development tools valuable for mod developers
- **Commercial**: Some tools may be game-specific

**Recommendation**: **Split** - Generic development tools → Engine, game-specific tools → Commercial

### 5. Basic Configuration System (`config/basic_settings.yml`)

**Considerations:**
- **Engine**: Modders need to understand configuration structure
- **Commercial**: Game configuration may reveal business logic

**Recommendation**: **Engine** - Basic configuration structure only, specific game configs → Commercial

### 6. Licensing Files (`LICENSE`, `CONTRIBUTING.md`)

**Considerations:**
- **Engine**: MIT license and contribution guidelines for open source
- **Commercial**: Proprietary license and internal contribution rules

**Recommendation**: **Split** - Different licenses and contribution guidelines for each

## Final Shared Component Classifications

### Move to Engine (Open Source)
- `examples/basic_game.py` - Basic educational example
- `.github/workflows/ci.yml` - Basic CI workflow (if exists)
- `scripts/development_tools.py` - Generic development utilities (if exists)
- Basic configuration templates
- `CONTRIBUTING.md` - Modified for open source contributions

### Move to Commercial (Proprietary)
- Game-specific examples with unique mechanics
- Deployment and release scripts
- Game-specific configuration files
- Internal development documentation

### Create New for Each Repository
- `README.md` - Separate READMEs with different focus
- `LICENSE` - MIT for engine, Proprietary for commercial
- Repository-specific documentation

## Implementation Notes

1. **No True "Shared" Components**: Every file should have a clear home
2. **Duplication When Needed**: Better to duplicate than create dependencies
3. **Clear Separation**: Each repository should be independently functional
4. **Educational Focus**: Engine should help developers learn, not compete with commercial game

## Updated Migration Strategy

The migration script should:
1. Make strategic decisions for each shared component
2. Create appropriate content for each repository
3. Ensure no component is truly "shared" between repositories
4. Focus engine on educational and development value
5. Protect commercial game's unique value propositions
