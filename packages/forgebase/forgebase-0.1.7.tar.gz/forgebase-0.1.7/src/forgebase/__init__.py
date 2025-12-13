"""
ForgeBase - Cognitive Architecture Framework.

ForgeBase is the technical core of the Forge Framework, a cognitive infrastructure
where ForgeProcess reasoning transforms into observable, reflexive, and modular code.

This framework implements Clean Architecture + Hexagonal Architecture with
native observability, allowing code not just to execute, but also to understand,
measure, and explain its own functioning.

Fundamental Principles:
    - **Reflexivity**: Code that understands and explains its own functioning
    - **Autonomy**: Independent modules with well-defined contracts
    - **Cognitive Coherence**: Consistent patterns throughout the architecture

Main Modules:
    - domain: Entities, value objects, domain validators
    - application: Use cases, ports, DTOs, orchestration
    - adapters: External interfaces (CLI, HTTP, AI/LLM)
    - infrastructure: Concrete implementations (repository, logging, config)
    - observability: Native metrics and tracing system
    - testing: Cognitive testing infrastructure

Example::

    from forgebase.domain import EntityBase
    from forgebase.application import UseCaseBase

    class User(EntityBase):
        def __init__(self, id, name):
            super().__init__(id)
            self.name = name

        def validate(self):
            if not self.name:
                raise ValueError("Name is required")

Note::

    ForgeBase follows modular import patterns. Always import from the specific
    module, not from the root package:

    Correct: `from forgebase.domain import EntityBase`
    Incorrect: `from forgebase import EntityBase`

Author: Jorge, The Forge
Created: 2025-11-03
Version: 0.0.1
"""

__version__ = "0.0.1"
__author__ = "Jorge, The Forge"
__all__ = []  # Import from specific modules
