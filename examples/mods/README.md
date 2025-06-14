# Yendoria Modding Examples

This directory contains comprehensive examples demonstrating Yendoria's modding capabilities.

## Available Examples

### Simple Gameplay Mods (`simple_gameplay_mods.py`)

Collection of basic, well-documented mods that demonstrate common patterns:

- **AtmosphereMod**: Adds immersive flavor text throughout the game
- **LuckSystem**: Dynamic luck mechanic that affects gameplay
- **SimpleStatsTracker**: Basic statistics tracking for gameplay analysis
- **PacifistMod**: Prevents all combat for peaceful exploration

**Usage:**
```bash
cd examples/mods
PYTHONPATH=../../src python simple_gameplay_mods.py
```

### Advanced Statistics Mod (`advanced_stats_mod.py`)

Comprehensive statistics tracking with advanced features:

- Real-time combat analysis
- Movement pattern tracking
- Performance metrics
- Historical data storage
- Exportable statistics to JSON

**Note:** This file has some linting warnings due to magic numbers in demo code.

### Event System Demo (`event_system_demo.py`)

Comprehensive demonstration of the event system with advanced patterns:

- Multiple event type handling
- Event cancellation demonstration
- Statistical tracking
- Conditional logic based on game state
- Combat intervention mechanics
- Integration with game engine

**Usage:**
```bash
cd examples/mods
PYTHONPATH=../../src python event_system_demo.py
```

## Testing the Examples

All examples include built-in testing functionality:

1. **Simple Mods Demo:**
   ```bash
   PYTHONPATH=src poetry run python examples/mods/simple_gameplay_mods.py
   ```

2. **Event System Demo:**
   ```bash
   PYTHONPATH=../../src python event_system_demo.py
   ```

3. **Advanced Statistics Demo:**
   ```bash
   PYTHONPATH=../../src python advanced_stats_mod.py
   ```

## Using Examples as Templates

These examples are designed to be used as templates for your own mods:

1. Copy the example file you want to base your mod on
2. Rename it to reflect your mod's purpose
3. Modify the class names and functionality
4. Add your custom logic to the event handlers

## Integration with the Game

To integrate these mods into the actual game, you would add them to the game engine initialization:

```python
# In game initialization code
from examples.mods.simple_gameplay_mods import AtmosphereMod, LuckSystem

# After creating the engine
atmosphere_mod = AtmosphereMod(engine.event_bus)
luck_system = LuckSystem(engine.event_bus)
```

## Documentation

For comprehensive documentation about the modding system, see:

- `docs/modding_quickstart.rst` - Quick start guide
- `docs/modding.rst` - Complete modding documentation
- `docs/modding_api.rst` - Detailed API reference
- `docs/modding_tutorial.rst` - Step-by-step tutorials
- `docs/modding_examples.rst` - Documentation for these examples
- `docs/modding_roadmap.rst` - Future modding features

## Common Patterns Demonstrated

### Event Subscription
```python
self.event_bus.subscribe(EventType.ENTITY_MOVE, self.on_entity_move)
```

### Event Data Validation
```python
entity = event.data.get("entity")
if entity is None:
    return
```

### Event Cancellation
```python
if should_cancel_event():
    event.cancel()
    print("Event cancelled!")
```

### Statistics Tracking
```python
def on_entity_death(self, event: GameEvent) -> None:
    killer = event.data.get("killer")
    if hasattr(killer, "is_player") and killer.is_player:
        self.monsters_killed += 1
```

## Development Tips

1. **Start Simple**: Begin with basic event handlers and build complexity gradually
2. **Validate Data**: Always check that expected event data exists before using it
3. **Handle Errors**: Use try/catch blocks for robust mod behavior
4. **Performance**: Keep event handlers lightweight (< 1ms execution time)
5. **Documentation**: Document your mod's purpose and event usage clearly

## Contributing

If you create interesting mods based on these examples, consider contributing them back to the project!
