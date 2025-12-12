"""
Universal Agent Fabric package.

This package compiles high-level agent definitions into kernel-ready manifests.
"""

from .builder import FabricBuilder
from .schemas import (
    Capability,
    Domain,
    FabricSpec,
    GovernanceRule,
    Role,
)

__all__ = [
    "FabricBuilder",
    "FabricSpec",
    "Role",
    "Domain",
    "Capability",
    "GovernanceRule",
]
__version__ = "0.1.1"

