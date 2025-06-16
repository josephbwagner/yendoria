AI System API Reference
========================

This section provides complete API documentation for all AI-related modules and classes in Yendoria.

AI Manager
----------

.. automodule:: yendoria.systems.ai_manager
   :members:
   :undoc-members:
   :show-inheritance:

AI Behavior Systems
-------------------

AI Behavior Interface
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: yendoria.systems.ai_behavior_interface
   :members:
   :undoc-members:
   :show-inheritance:

Basic AI Behavior System
~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: yendoria.systems.ai_behavior_basic
   :members:
   :undoc-members:
   :show-inheritance:

Advanced AI Behavior System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: yendoria.systems.ai_behavior_advanced
   :members:
   :undoc-members:
   :show-inheritance:

AI Components
-------------

.. automodule:: yendoria.components.ai_components
   :members:
   :undoc-members:
   :show-inheritance:

AI Events
---------

.. automodule:: yendoria.components.ai_events
   :members:
   :undoc-members:
   :show-inheritance:

AI Engine Integration
---------------------

.. automodule:: yendoria.systems.ai_engine_integration
   :members:
   :undoc-members:
   :show-inheritance:

Error Handling & Monitoring
----------------------------

.. automodule:: yendoria.systems.ai_error_handling
   :members:
   :undoc-members:
   :show-inheritance:

Configuration Management
-------------------------

.. automodule:: yendoria.systems.config_manager
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: ConfigManager

AI-Related Config Manager Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Config Manager provides specialized methods for handling AI configurations:

.. autoclass:: yendoria.systems.config_manager.ConfigManager
   :members: get_ai_config, load_all_ai_configs, validate_ai_config
   :show-inheritance:
