"""
Domain layer - Business logic and entities.

This module contains the core domain logic of ForgeBase, including entities,
value objects, domain exceptions, and validators. The domain layer is kept
completely independent of infrastructure and external concerns, following
Clean Architecture principles.

Author: Jorge, The Forge
Created: 2025-11-03
"""

from forgebase.domain.entity_base import EntityBase

__all__ = ["EntityBase"]
