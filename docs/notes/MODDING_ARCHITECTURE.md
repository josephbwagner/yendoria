# Modding Architecture Design for Yendoria

## Current Architecture Assessment ✅

Yendoria already has excellent foundations for modding:

### **Strengths:**
- **Entity Component System (ECS)**: Perfect for extensibility
- **Protocol-based Design**: Clean interfaces for mod integration
- **Separated Systems**: Input, rendering, game logic are decoupled
- **Externalized Constants**: Game parameters already configurable
- **Modern Python**: Type hints and clean module structure

### **Areas for Enhancement:**
- Data-driven content definition
- Plugin loading system
- Event/hook system for mod integration
- Asset pipeline for mod resources
- API boundaries and versioning

---

## Strategic Considerations 🎯

### **1. Modding Scope Definition**

#### **What Should Be Moddable:**
- **Content**: Monsters, items, spells, character classes
- **Mechanics**: Combat rules, progression systems
- **Procedural Generation**: Room layouts, dungeon themes
- **UI/UX**: Interface elements, information display
- **Assets**: Graphics, sounds, text

#### **What Should Stay Core:**
- Save/load system architecture
- Network protocols (if multiplayer added)
- Core engine performance loops
- Security and anti-cheat systems

### **2. Backwards Compatibility Strategy**
- **API Versioning**: Semantic versioning for mod APIs
- **Deprecation Warnings**: Graceful migration paths
- **Save Compatibility**: Mods shouldn't break existing saves
- **Fallback Systems**: Graceful degradation when mods are missing

### **3. Performance Considerations**
- **Lazy Loading**: Load mod content only when needed
- **Resource Limits**: Prevent mods from consuming excessive resources
- **Profiling Hooks**: Help mod developers optimize performance
- **Hot Reloading**: For development without full restarts

---

## Technical Architecture 🏗️

### **1. Event System (Core Foundation)**

```python
# Event system for mod hooks
class EventType(Enum):
    ENTITY_SPAWN = "entity_spawn"
    COMBAT_START = "combat_start"
    LEVEL_GENERATE = "level_generate"
    ITEM_USE = "item_use"
    PLAYER_LEVEL_UP = "player_level_up"

class GameEvent:
    def __init__(self, event_type: EventType, data: dict, cancellable: bool = False):
        self.type = event_type
        self.data = data
        self.cancellable = cancellable
        self.cancelled = False

class EventBus:
    def __init__(self):
        self.handlers: dict[EventType, list[callable]] = defaultdict(list)

    def subscribe(self, event_type: EventType, handler: callable):
        """Register a mod function to handle specific events."""
        self.handlers[event_type].append(handler)

    def emit(self, event: GameEvent) -> GameEvent:
        """Fire an event to all registered handlers."""
        for handler in self.handlers[event.type]:
            try:
                handler(event)
                if event.cancelled and event.cancellable:
                    break
            except Exception as e:
                logger.error(f"Mod event handler error: {e}")
        return event
```

### **2. Plugin System Architecture**

```python
# Plugin discovery and loading
class ModPlugin:
    def __init__(self, name: str, version: str, author: str):
        self.name = name
        self.version = version
        self.author = author
        self.enabled = True

    def initialize(self, game_api: 'GameAPI') -> None:
        """Called when mod is loaded."""
        pass

    def shutdown(self) -> None:
        """Called when mod is unloaded."""
        pass

class ModManager:
    def __init__(self, mods_dir: Path):
        self.mods_dir = mods_dir
        self.loaded_mods: dict[str, ModPlugin] = {}
        self.event_bus = EventBus()

    def discover_mods(self) -> list[Path]:
        """Find all mod directories/files."""
        return list(self.mods_dir.glob("*/mod.toml"))

    def load_mod(self, mod_path: Path) -> ModPlugin:
        """Safely load a mod with dependency checking."""
        # Parse mod.toml for metadata
        # Check dependencies
        # Import mod module with error handling
        # Register with event system
        pass
```

### **3. Data-Driven Content System**

```python
# Content registry for moddable game objects
class ContentRegistry:
    def __init__(self):
        self.monsters: dict[str, MonsterTemplate] = {}
        self.items: dict[str, ItemTemplate] = {}
        self.spells: dict[str, SpellTemplate] = {}

    def register_monster(self, id: str, template: MonsterTemplate):
        """Register a new monster type from mod."""
        self.monsters[id] = template

    def get_monster(self, id: str) -> MonsterTemplate:
        """Get monster template by ID."""
        return self.monsters.get(id)

# Example monster template from JSON/YAML
{
    "id": "goblin_shaman",
    "name": "Goblin Shaman",
    "symbol": "g",
    "color": [0, 255, 0],
    "stats": {
        "hp": 15,
        "attack": 6,
        "defense": 2
    },
    "ai": "spellcaster",
    "spells": ["heal", "magic_missile"],
    "spawn_weight": 3
}
```

### **4. Game API for Mods**

```python
class GameAPI:
    """Stable API interface for mods."""

    def __init__(self, game_engine):
        self.engine = game_engine
        self.content = ContentRegistry()
        self.events = EventBus()

    # Entity management
    def spawn_entity(self, template_id: str, x: int, y: int) -> Entity:
        """Spawn an entity at given coordinates."""
        pass

    def get_entities_at(self, x: int, y: int) -> list[Entity]:
        """Get all entities at coordinates."""
        pass

    # Map access
    def get_tile(self, x: int, y: int) -> Tile:
        """Get tile information."""
        pass

    def set_tile(self, x: int, y: int, tile_type: str):
        """Modify map tile (with restrictions)."""
        pass

    # Player interaction
    def get_player() -> Entity:
        """Get player entity."""
        pass

    def show_message(self, text: str, color: tuple = (255, 255, 255)):
        """Display message to player."""
        pass

    # Content registration
    def register_monster(self, data: dict):
        """Register new monster type."""
        pass

    def register_spell(self, data: dict):
        """Register new spell."""
        pass
```

---

## Implementation Roadmap 🛣️

### **Phase 1: Foundation (1-2 weeks)**
1. **Event System**: Basic event bus with core game events
2. **Content Registry**: Simple registry for monsters/items
3. **Data Files**: Convert hardcoded content to JSON/YAML
4. **Mod Discovery**: Basic mod directory scanning

### **Phase 2: Basic Modding (2-3 weeks)**
1. **Plugin Loading**: Safe module import with error handling
2. **Game API**: Core API methods for mod interaction
3. **Content Templates**: Monster/item definition system
4. **Example Mods**: Simple "hello world" and content mods

### **Phase 3: Advanced Features (1-2 months)**
1. **Asset Pipeline**: Graphics/sound loading for mods
2. **UI Modification**: Allow mods to extend interface
3. **Save Compatibility**: Handle mod changes in saves
4. **Development Tools**: Hot reloading, debugging support

### **Phase 4: Polish & Community (Ongoing)**
1. **Documentation**: Comprehensive modding guide
2. **Mod Distribution**: Workshop/marketplace integration
3. **Validation Tools**: Automated mod testing
4. **Performance Monitoring**: Mod impact analysis

---

## Practical Examples 🎮

### **1. Simple Monster Mod**

**File: `mods/goblin_variants/mod.toml`**
```toml
[mod]
name = "Goblin Variants"
version = "1.0.0"
author = "ModAuthor"
description = "Adds new goblin types"
yendoria_version = ">=0.1.0"

[dependencies]
# No dependencies
```

**File: `mods/goblin_variants/monsters.json`**
```json
{
    "goblin_archer": {
        "name": "Goblin Archer",
        "symbol": "g",
        "color": [0, 200, 0],
        "stats": {"hp": 12, "attack": 8, "defense": 1},
        "ai": "ranged_attacker",
        "spawn_weight": 2
    }
}
```

**File: `mods/goblin_variants/__init__.py`**
```python
from yendoria.modding import ModPlugin, GameAPI

class GoblinVariantsMod(ModPlugin):
    def initialize(self, api: GameAPI):
        # Load monster definitions
        monsters = self.load_json("monsters.json")
        for monster_id, data in monsters.items():
            api.register_monster(monster_id, data)

        # Subscribe to events
        api.events.subscribe(EventType.LEVEL_GENERATE, self.on_level_generate)

    def on_level_generate(self, event):
        # Custom logic for spawning goblin variants
        pass
```

### **2. Spell System Mod**

```python
class FireballSpell:
    def __init__(self):
        self.name = "Fireball"
        self.mana_cost = 10
        self.damage = 25
        self.radius = 3

    def cast(self, api: GameAPI, caster: Entity, target_x: int, target_y: int):
        # Create explosion effect
        for entity in api.get_entities_in_radius(target_x, target_y, self.radius):
            if entity != caster:
                entity.take_damage(self.damage)

        # Visual effect
        api.show_explosion_effect(target_x, target_y, self.radius)
        api.show_message(f"{caster.name} casts {self.name}!")
```

### **3. Map Generator Mod**

```python
class CaveGeneratorMod(ModPlugin):
    def initialize(self, api: GameAPI):
        api.register_map_generator("caves", self.generate_cave_level)

    def generate_cave_level(self, api: GameAPI, width: int, height: int) -> GameMap:
        # Custom cave generation algorithm
        cave_map = self.cellular_automata_caves(width, height)

        # Convert to game map format
        game_map = api.create_map(width, height)
        for x in range(width):
            for y in range(height):
                if cave_map[x][y]:
                    game_map.set_tile(x, y, "floor")
                else:
                    game_map.set_tile(x, y, "wall")

        return game_map
```

---

## Security & Safety Considerations 🔒

### **1. Code Execution Safety**
- **Import Restrictions**: Limit which modules mods can import
- **Resource Limits**: CPU/memory usage monitoring
- **Sandboxing**: Consider using `RestrictedPython` for user scripts
- **Code Review**: Encourage community review of popular mods

### **2. Save Game Integrity**
- **Versioning**: Track which mods were active when save was created
- **Graceful Degradation**: Handle missing mods in save files
- **Validation**: Verify save data hasn't been corrupted by mods

### **3. Performance Monitoring**
```python
class ModPerformanceMonitor:
    def __init__(self):
        self.mod_timings: dict[str, float] = {}

    def track_mod_call(self, mod_name: str, duration: float):
        if duration > 0.016:  # > 16ms (60fps budget)
            logger.warning(f"Mod {mod_name} took {duration:.3f}s")
```

---

## Community & Distribution 🌟

### **1. Developer Experience**
- **Hot Reloading**: Reload mods without restarting game
- **Debug Console**: In-game console for mod testing
- **Error Reporting**: Clear error messages for mod issues
- **Documentation**: Complete API reference with examples

### **2. Mod Distribution**
- **Local Files**: Simple directory-based mod loading
- **Workshop Integration**: Steam Workshop or similar platform
- **Mod Manager**: GUI tool for installing/managing mods
- **Dependency Resolution**: Automatic handling of mod dependencies

### **3. Quality Assurance**
- **Automated Testing**: Test mods against different game versions
- **Compatibility Database**: Track mod compatibility
- **User Ratings**: Community feedback on mod quality
- **Curation**: Featured/recommended mods list

---

## Getting Started Today 🚀

**Immediate steps you can take:**

1. **Extract Constants**: Move more hardcoded values to configuration files
2. **Add Event Hooks**: Start emitting events in key game systems
3. **Create Content Templates**: Convert monster definitions to data files
4. **Design Mod Directory Structure**: Plan where mods will live

**Quick Win Example:**
```python
# In your monster creation code, add:
event = GameEvent(EventType.ENTITY_SPAWN, {
    'entity': new_monster,
    'location': (x, y),
    'monster_type': monster_type
})
game.event_bus.emit(event)
```

This foundational work will make full modding implementation much easier later!

---

*The key is starting simple and building incrementally. Your ECS architecture is already mod-friendly - you just need to expose the right hooks and APIs!*
