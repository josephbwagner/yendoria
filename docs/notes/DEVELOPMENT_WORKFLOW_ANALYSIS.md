# Development Workflow Analysis: Dual Repository Setup

## Overview
This document analyzes the development workflow implications of the dual repository approach and clarifies when you'd work in each repository.

## Primary Development Workflow

### 🎮 **Commercial Game Repository (Your Main Workspace)**
**95% of your development time will be here**

#### What You'll Do Daily:
- Game feature development (combat, progression, UI)
- World generation implementation
- AI system development
- Content creation (quests, items, creatures)
- Bug fixes and gameplay improvements
- Performance optimization
- Asset integration
- Testing and debugging

#### Dependencies Setup:
```toml
# yendoria-game/pyproject.toml
[tool.poetry.dependencies]
yendoria-engine = "^1.0.0"  # Or path for local development
tcod = "^19.0.0"
numpy = "^2.0.0"
# ... all your game dependencies
```

#### For Local Engine Development:
```toml
# When you need to modify engine simultaneously
[tool.poetry.dependencies]
yendoria-engine = {path = "../yendoria-engine", develop = true}
```

## 🔧 **Engine Repository (Occasional Modifications)**

### When You'd Work in the Engine Repository:

#### 1. **Adding New Event Types** (Monthly/Quarterly)
```python
# yendoria-engine/src/yendoria/modding/event_system.py
class EventType(Enum):
    # Existing events
    GAME_START = "game_start"
    ENTITY_CREATED = "entity_created"

    # New events you need for your game
    COMBAT_STARTED = "combat_started"      # ← Add when implementing combat
    QUEST_COMPLETED = "quest_completed"    # ← Add when implementing quests
    BIOME_GENERATED = "biome_generated"    # ← Add when implementing world gen
```

#### 2. **Exposing New Modding Hooks** (As Needed)
When you implement a new game system and want it to be moddable:
```python
# yendoria-engine: Add new modding capability
class ModdingAPI:
    def register_combat_modifier(self, modifier_func):
        """Allow mods to modify combat calculations"""
        pass
```

#### 3. **Engine Bug Fixes** (Rare)
If you discover bugs in the basic event system or architecture.

#### 4. **Documentation Updates** (Occasional)
When you add new modding capabilities that need documentation.

## Development Workflow Patterns

### **Pattern 1: Game-Only Development (90% of time)**
```bash
cd yendoria-game/
# Normal game development
poetry run python -m yendoria_game
poetry run pytest
git commit -m "feat: add new combat system"
```

### **Pattern 2: Engine + Game Development (10% of time)**
When you need to add modding support for a new feature:

```bash
# 1. Add modding hooks to engine
cd ../yendoria-engine/
# Edit event system, add new event types
git commit -m "feat: add combat events for modding"
poetry build  # Build new version

# 2. Update game to use new engine features
cd ../yendoria-game/
poetry update yendoria-engine  # Get latest engine
# Implement game feature using new modding hooks
git commit -m "feat: implement combat with modding support"
```

### **Pattern 3: Local Linked Development**
For simultaneous engine + game development:

```bash
cd yendoria-game/
# Link to local engine for development
poetry add ../yendoria-engine/ --editable

# Now changes to engine are immediately available in game
# No need to rebuild/republish engine during development
```

## Repository Responsibilities

### **Engine Repository (Foundation)**
```
Responsibility: Provide modding infrastructure
Size: Small, focused codebase
Change Frequency: Low (quarterly releases)
Testing Focus: Modding APIs, event system
Release Cycle: Stable releases to PyPI
```

### **Game Repository (Your Main Project)**
```
Responsibility: Complete game implementation
Size: Large, comprehensive codebase
Change Frequency: High (daily development)
Testing Focus: Game functionality, integration
Release Cycle: Game versions, private releases
```

## Practical Development Examples

### **Example 1: Adding Magic System**
```bash
# Most development in game repo
cd yendoria-game/
# 1. Implement magic system (spells, mana, casting)
# 2. Add magic-related entities and components
# 3. Create spell effects and animations
# 4. Test magic system

# Only if you want magic to be moddable:
cd ../yendoria-engine/
# 5. Add SPELL_CAST, MANA_CHANGED events
# 6. Add spell registration API for mods
```

### **Example 2: Performance Optimization**
```bash
# Pure game development
cd yendoria-game/
# 1. Profile performance bottlenecks
# 2. Optimize rendering, AI, or world generation
# 3. No engine changes needed
```

### **Example 3: Bug Fix**
```bash
# Most bugs will be in game code
cd yendoria-game/
# Fix game logic, combat, UI bugs

# Only if bug is in event system:
cd ../yendoria-engine/
# Fix event dispatching, modding API bugs
```

## Release Workflow

### **Engine Releases (Infrequent)**
```bash
cd yendoria-engine/
poetry version patch  # 1.0.0 → 1.0.1
poetry build
poetry publish  # To PyPI
git tag v1.0.1
```

### **Game Development (Continuous)**
```bash
cd yendoria-game/
# Daily development, no releases to PyPI
# Private repository, internal versioning only
```

## Benefits of This Workflow

### **For You (Game Developer)**
✅ **Focused Development**: 95% of time in one repository
✅ **Simple Dependencies**: Engine is just another dependency
✅ **Flexible Coupling**: Can link locally when needed
✅ **Clear Separation**: Game code vs infrastructure code

### **For Future Modders**
✅ **Stable Foundation**: Engine doesn't change frequently
✅ **Clear APIs**: Well-defined modding interfaces
✅ **Independent Updates**: Can update game without breaking mods

## When to Work in Engine Repository

### **High Priority (Do These)**
- Adding events for new game systems you want to be moddable
- Fixing bugs in the event system
- Adding documentation for new modding capabilities

### **Low Priority (Consider)**
- Adding convenience APIs for modders
- Performance optimizations for modding framework
- Advanced modding features

### **Don't Do (Stay Focused)**
- Moving game logic to engine
- Adding game-specific features to engine
- Over-engineering modding APIs before you need them

## Recommendation

**Start Simple**:
1. Do all development in `yendoria-game/`
2. Only touch `yendoria-engine/` when you need new modding hooks
3. Keep engine minimal and focused
4. Let modding needs drive engine development, not the other way around

This keeps you productive on game development while building a solid modding foundation over time.

## Development Timeline: Repository Work Distribution

### **Phase 1: Early Development (Months 1-6) - Heavy Dual-Repo Work**
**Time Split: ~70% Game Repo / 30% Engine Repo**

As you implement core game systems, you'll frequently switch between repositories:

#### Example: Implementing Combat System
```bash
# Week 1: Build combat in game
cd yendoria-game/
# Implement basic combat mechanics, damage calculation, turn order
git commit -m "Add basic combat system"

# Week 2: Add modding support for combat
cd ../yendoria-engine/
# Add COMBAT_STARTED, DAMAGE_DEALT, COMBAT_ENDED events
# Add combat modifier APIs for mods
git commit -m "Add combat events and modding APIs"

# Week 3: Use new modding APIs in game
cd ../yendoria-game/
poetry update yendoria-engine  # Get latest engine
# Integrate combat with modding events
git commit -m "Integrate combat with modding system"
```

#### Example: Implementing Quest System
```bash
# Week 1-2: Build quest system in game
cd yendoria-game/
# Create quest classes, objectives, rewards
git commit -m "Add quest system"

# Week 3: Add quest modding support
cd ../yendoria-engine/
# Add QUEST_STARTED, QUEST_COMPLETED, OBJECTIVE_UPDATED events
# Add quest registration APIs for mods
git commit -m "Add quest modding framework"

# Week 4: Connect quest system to modding
cd ../yendoria-game/
# Use quest events, allow mod quests
git commit -m "Enable quest modding support"
```

### **Phase 2: Maturation (Months 6-12) - Decreasing Engine Work**
**Time Split: ~85% Game Repo / 15% Engine Repo**

Most core systems have modding support, so you focus on game content:

```bash
# Most weeks look like this:
cd yendoria-game/
# Add new areas, creatures, items, balance gameplay
# Engine work only when adding entirely new moddable systems
```

### **Phase 3: Polishing (Months 12+) - Minimal Engine Work**
**Time Split: ~95% Game Repo / 5% Engine Repo**

Engine is feature-complete for modding, you focus purely on game:

```bash
# Typical development:
cd yendoria-game/
# Polish gameplay, optimize performance, add content
# Engine work only for bug fixes or rare new modding features
```

## Engine Development Intensity by Game System

### **High Engine Work (New Modding APIs Needed)**
- **Combat System**: Events for damage, effects, turn order
- **Quest System**: Events for progress, completion, rewards
- **Magic/Spell System**: Events for casting, spell effects
- **Character Progression**: Events for leveling, skill gains
- **World Generation**: Hooks for terrain, structure placement
- **AI System**: Events for behavior changes, decision making

### **Medium Engine Work (Some Modding Hooks)**
- **Inventory System**: Events for item acquisition/use
- **Dialog System**: Hooks for custom conversations
- **Economy System**: Events for trading, pricing

### **Low Engine Work (Basic Events Sufficient)**
- **UI Improvements**: Use existing UI events
- **Graphics/Audio**: Mostly asset work, minimal modding
- **Performance Optimization**: Pure game-side work
- **Content Creation**: Uses existing content events

## The "Modding Completeness" Curve

```
Engine Work Intensity
     ↑
High │ ██████████
     │ █████████
     │ ████████
Med  │ ████
     │ ██
Low  │ █
     └──────────────────────────→
       0   6   12   18   24    Time (months)
```

### **Why This Happens:**

1. **Early**: Every new game system needs modding support → frequent engine work
2. **Middle**: Core systems complete, adding variations → occasional engine work
3. **Late**: Modding framework mature, focus on content → rare engine work

## Strategic Planning: When to Add Modding Support

### **Priority 1: Core Game Systems (Add Modding Early)**
These are fundamental systems that mods will want to extend:

```bash
# Plan your implementation order:
1. Combat System → Add modding hooks immediately
2. Character Progression → Add modding hooks immediately
3. Item/Equipment System → Add modding hooks immediately
4. Quest System → Add modding hooks immediately
```

**Why Early**: These systems form the foundation for most mods. Better to design modding support from the start than retrofit later.

### **Priority 2: Secondary Systems (Add Modding When Stable)**
```bash
# Implement game feature first, add modding later:
1. Build magic system, test it, balance it
2. THEN add spell modding APIs
3. Build dialog system, test conversation flow
4. THEN add dialog modding hooks
```

**Why Later**: These systems benefit from being solid before opening them to modification.

### **Priority 3: Polish Features (Minimal/No Modding)**
```bash
# Probably don't need modding support:
- Graphics optimization
- Audio mixing
- Save/load performance
- UI polish
- Analytics/telemetry
```

**Why Skip**: These are implementation details that mods shouldn't need to touch.

## Practical Development Strategy

### **Start Simple, Expand Gradually**
```python
# Phase 1: Basic events
class EventType(Enum):
    ENTITY_CREATED = "entity_created"
    ENTITY_DESTROYED = "entity_destroyed"

# Phase 2: Add combat events when you implement combat
class EventType(Enum):
    ENTITY_CREATED = "entity_created"
    ENTITY_DESTROYED = "entity_destroyed"
    COMBAT_STARTED = "combat_started"      # ← Added when implementing combat
    DAMAGE_DEALT = "damage_dealt"          # ← Added when implementing combat

# Phase 3: Add quest events when you implement quests
class EventType(Enum):
    # ... existing events ...
    QUEST_STARTED = "quest_started"        # ← Added when implementing quests
    QUEST_COMPLETED = "quest_completed"    # ← Added when implementing quests
```

### **The "Good Enough" Principle**
- **Don't over-engineer modding APIs** before you understand the game systems
- **Add basic events first**, expand to complex APIs later
- **Focus on game functionality** over perfect modding interfaces
- **Let real modding needs drive API complexity**, not theoretical possibilities

## Repository Work Estimation

### **For Your Current Development Phase:**
Based on your world generation roadmap, here's realistic time allocation:

**Months 1-3 (Foundation Systems):**
- 60% Game Repo: Basic ECS, rendering, input
- 40% Engine Repo: Core event system, basic modding hooks

**Months 4-9 (Core Gameplay):**
- 70% Game Repo: Combat, progression, quests
- 30% Engine Repo: Gameplay modding APIs

**Months 10-15 (World Generation):**
- 80% Game Repo: World gen algorithms, content
- 20% Engine Repo: World gen modding hooks

**Months 16+ (Polish & Content):**
- 90% Game Repo: Balance, content, polish
- 10% Engine Repo: Bug fixes, minor additions

### **The Sweet Spot:**
After ~12-18 months, you'll reach the "sweet spot" where:
- ✅ Engine has comprehensive modding APIs for core systems
- ✅ You can focus almost entirely on game development
- ✅ Modders have sufficient tools to create interesting modifications
- ✅ Dual-repo complexity becomes minimal day-to-day burden
