Modding Roadmap
===============

This document outlines the planned development phases for Yendoria's modding system, including current capabilities, upcoming features, and long-term goals.

Current Status: Phase 1 ✅
---------------------------

**Completed Features:**

Event System Foundation
~~~~~~~~~~~~~~~~~~~~~~~

* ✅ **Comprehensive Event Bus**: Central event system for game-wide communication
* ✅ **Type-Safe Events**: Full type annotations for reliable mod development
* ✅ **Event Cancellation**: Ability to prevent certain game actions
* ✅ **Event History**: Debug-friendly event tracking and replay
* ✅ **Performance Monitoring**: Built-in tracking of event handler performance

Integrated Game Events
~~~~~~~~~~~~~~~~~~~~~~

* ✅ **Entity Lifecycle**: Spawn, movement, and death events for all entities
* ✅ **Combat System**: Start, hit, and resolution events with full context
* ✅ **Turn Management**: Turn start/end events with turn counting
* ✅ **World Generation**: Level generation events with map data
* ✅ **Player Actions**: Comprehensive tracking of player interactions

Development Support
~~~~~~~~~~~~~~~~~~~

* ✅ **Documentation**: Complete API documentation with examples
* ✅ **Type Safety**: Full mypy compatibility for mod development
* ✅ **Error Handling**: Graceful degradation when mods fail
* ✅ **Example Code**: Comprehensive examples demonstrating capabilities

**Current Capabilities:**

Mods can currently:

* Hook into any major game action through events
* Track detailed game statistics and player behavior
* Cancel certain actions (like combat) conditionally
* Implement custom game mechanics triggered by events
* Debug mod behavior through event history
* Access full context about game state changes

Phase 2: Content and Discovery 🚧
----------------------------------

**Target: Q3 2025**

Data-Driven Content System
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 📋 **Extract Hardcoded Data**: Move monster/item definitions to external JSON/YAML files
* 📋 **Content Templates**: Abstract template system for game objects
* 📋 **Data Validation**: JSON Schema validation for content files
* 📋 **Hot Reloading**: Development-time reloading of content without restart

Mod Discovery and Loading
~~~~~~~~~~~~~~~~~~~~~~~~~

* 📋 **Standard Mod Structure**: Define mod directory layouts and manifest files
* 📋 **Automatic Discovery**: Scan mod directories and load valid mods
* 📋 **Dependency Resolution**: Handle mod dependencies and load ordering
* 📋 **Safe Execution**: Sandboxed mod loading with error isolation

Registration APIs
~~~~~~~~~~~~~~~~~~

* 📋 **Decorator Patterns**: ``@register_monster``, ``@register_spell`` decorators
* 📋 **Content Registry**: Central registry for mod-added content
* 📋 **Override System**: Allow mods to modify existing content
* 📋 **Conflict Resolution**: Handle conflicts between mods gracefully

**Planned File Structure:**

.. code-block:: text

   mods/
   ├── awesome_monsters/
   │   ├── mod.yml                 # Mod metadata and dependencies
   │   ├── main.py                 # Mod entry point
   │   ├── data/
   │   │   ├── monsters.json       # Monster definitions
   │   │   ├── items.json          # Item definitions
   │   │   └── spells.json         # Spell definitions
   │   └── assets/
   │       ├── sprites/            # Custom graphics
   │       └── sounds/             # Audio files
   └── gameplay_tweaks/
       ├── mod.yml
       └── main.py

**Example Mod Definition:**

.. code-block:: yaml

   # mod.yml
   name: "Awesome Monsters"
   version: "1.2.0"
   author: "ModAuthor"
   description: "Adds dragons, elementals, and other fantastic creatures"
   api_version: "1.0.0"
   dependencies:
     - name: "base_game"
       version: ">=0.2.0"
   permissions:
     - "entity_creation"
     - "combat_modification"

.. code-block:: python

   # main.py
   from yendoria.modding import mod_api

   @mod_api.register_monster("fire_dragon")
   def create_fire_dragon():
       return MonsterTemplate(
           name="Fire Dragon",
           char="D",
           color=(255, 0, 0),
           stats=Stats(hp=150, attack=25, defense=15),
           special_abilities=["fire_breath", "flight"]
       )

Phase 3: Advanced Features 🔮
------------------------------

**Target: Q4 2025 - Q1 2026**

Asset Pipeline
~~~~~~~~~~~~~~

* 🔮 **Custom Graphics**: Support for mod-provided sprites and tilesets
* 🔮 **Audio Integration**: Custom sound effects and music
* 🔮 **Resource Management**: Efficient loading and caching of mod assets
* 🔮 **Format Support**: PNG, OGG, TTF file support with validation

UI Modification System
~~~~~~~~~~~~~~~~~~~~~~

* 🔮 **HUD Extensions**: Allow mods to add new UI elements
* 🔮 **Menu Modification**: Custom menus and interface screens
* 🔮 **Information Display**: Custom status indicators and overlays
* 🔮 **Input Handling**: Mod-defined keybindings and controls

Save Game Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~

* 🔮 **Mod Data Persistence**: Save mod state in game saves
* 🔮 **Version Migration**: Handle save files when mods are updated
* 🔮 **Graceful Degradation**: Load saves when mods are missing
* 🔮 **Conflict Resolution**: Handle save/load with mod changes

Advanced Event System
~~~~~~~~~~~~~~~~~~~~~~

* 🔮 **Async Events**: Support for non-blocking event handlers
* 🔮 **Event Priorities**: Control event handler execution order
* 🔮 **Event Chaining**: Events that trigger other events
* 🔮 **Custom Event Types**: Allow mods to define their own events

Security and Sandboxing
~~~~~~~~~~~~~~~~~~~~~~~~

* 🔮 **RestrictedPython**: Secure execution of untrusted mod code
* 🔮 **Resource Limits**: CPU/memory usage monitoring per mod
* 🔮 **API Boundaries**: Strict separation between mod and core APIs
* 🔮 **Mod Validation**: Static analysis and runtime checks

Phase 4: Tools and Community 🌟
--------------------------------

**Target: Q2-Q3 2026**

Development Tools
~~~~~~~~~~~~~~~~~

* 🌟 **Mod CLI**: Command-line tools for creating, testing, and packaging mods
* 🌟 **Hot Reloading**: Live mod development without game restart
* 🌟 **Debug Console**: In-game console for mod testing and debugging
* 🌟 **Performance Profiler**: Tools to optimize mod performance

Testing Framework
~~~~~~~~~~~~~~~~~~

* 🌟 **Mod Unit Tests**: Framework for testing mod functionality
* 🌟 **Integration Tests**: Test mod compatibility with game versions
* 🌟 **Automated Testing**: CI/CD pipeline for mod validation
* 🌟 **Compatibility Matrix**: Track mod compatibility across versions

Documentation and Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 🌟 **Interactive Tutorials**: Step-by-step mod creation guides
* 🌟 **Comprehensive Examples**: Library of example mods for reference
* 🌟 **API Reference**: Complete documentation of all modding APIs
* 🌟 **Best Practices Guide**: Performance and design recommendations

Community Features
~~~~~~~~~~~~~~~~~~~

* 🌟 **Mod Repository**: Central hub for sharing and discovering mods
* 🌟 **Mod Manager**: In-game interface for installing/managing mods
* 🌟 **User Ratings**: Community feedback and mod recommendations
* 🌟 **Mod Collections**: Curated mod packs and compatibility sets

Long-term Vision 🚀
--------------------

**Ultimate Modding Goals:**

Complete Extensibility
~~~~~~~~~~~~~~~~~~~~~~~

* Every game system should be moddable
* Total conversions should be possible
* Core game mechanics should be replaceable
* Custom game modes and rulesets

Rich Development Ecosystem
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Visual mod development tools
* Asset creation pipelines
* Collaborative development features
* Professional mod distribution

Community-Driven Content
~~~~~~~~~~~~~~~~~~~~~~~~~

* User-generated content marketplace
* Mod contests and featured content
* Community governance of mod standards
* Integration with gaming platforms

Implementation Timeline
-----------------------

**2025 Q2-Q3**: Phase 2 Development
   * Data-driven content system
   * Mod discovery and loading
   * Basic registration APIs

**2025 Q4**: Phase 2 Completion
   * Content template system
   * Dependency management
   * Mod conflict resolution

**2026 Q1**: Phase 3 Start
   * Asset pipeline development
   * UI modification framework
   * Save compatibility system

**2026 Q2-Q3**: Phase 3 Completion
   * Advanced event features
   * Security improvements
   * Performance optimization

**2026 Q4+**: Phase 4 and Beyond
   * Development tools
   * Community features
   * Long-term vision implementation

Success Metrics
---------------

**Phase 2 Success Criteria:**
   * 5+ community-created content mods
   * Smooth mod installation process
   * Zero mod-related crashes

**Phase 3 Success Criteria:**
   * Custom graphics/audio mods working
   * UI modification examples
   * Save/load with mods stable

**Phase 4 Success Criteria:**
   * Active mod development community
   * 50+ published mods
   * Self-sustaining mod ecosystem

Technical Considerations
------------------------

Performance Impact
~~~~~~~~~~~~~~~~~~

* Event system overhead: < 1% of total game performance
* Mod loading time: < 500ms for typical mod collection
* Memory usage: < 50MB additional for average mod setup
* Asset loading: Lazy loading to minimize startup impact

Compatibility Strategy
~~~~~~~~~~~~~~~~~~~~~~

* **Semantic Versioning**: Clear API version compatibility guarantees
* **Deprecation Cycle**: 2 major versions before removing deprecated features
* **Migration Tools**: Automated mod updating for API changes
* **Backward Compatibility**: Support for older mod API versions

Community Guidelines
~~~~~~~~~~~~~~~~~~~~

* **Open Source**: Encourage open-source mod development
* **Documentation**: Require documentation for complex mods
* **Code Quality**: Promote best practices and code reviews
* **Inclusivity**: Foster welcoming and diverse mod community

Contributing to Modding Development
-----------------------------------

The modding system development is open to community contributions:

**How to Help:**

* **Test Early Features**: Try Phase 2 preview builds and report issues
* **Create Example Mods**: Develop mods that showcase system capabilities
* **Documentation**: Improve guides, tutorials, and API documentation
* **Feature Requests**: Propose new modding capabilities and use cases

**Priority Areas:**

1. **Performance Testing**: Help identify bottlenecks in event system
2. **Use Case Validation**: Ensure modding APIs meet real-world needs
3. **Security Review**: Help identify potential security vulnerabilities
4. **Cross-Platform Testing**: Verify mod system works on all platforms

Getting Involved
~~~~~~~~~~~~~~~~~

* Join discussions in GitHub Issues about modding features
* Contribute to modding documentation and examples
* Test preview releases and provide feedback
* Share ideas for mod capabilities and tools

The modding system represents a significant investment in Yendoria's future, and community input is essential for creating the best possible modding experience.
