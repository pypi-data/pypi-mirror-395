"""
Universal Agent Fabric package.

This package compiles high-level agent definitions into kernel-ready manifests.

Pipeline:
    Nexus (translate) → Fabric (enrich) → Agent (execute)

Usage:
    # Build from scratch
    from universal_agent_fabric import FabricBuilder, FabricSpec

    # Enrich baseline from Nexus
    from universal_agent_fabric import NexusEnricher, enrich_manifest
"""

from .builder import FabricBuilder
from .enricher import NexusEnricher, enrich_manifest
from .enrichment import (
    ComposableEnrichmentStrategy,
    DefaultEnrichmentStrategy,
    DomainEnrichmentHandler,
    EnrichmentHandler,
    EnrichmentStrategy,
    MixinEnrichmentHandler,
    PolicyEnrichmentHandler,
    RoleEnrichmentHandler,
)
from .schemas import (
    Capability,
    Domain,
    FabricSpec,
    GovernanceRule,
    Role,
)

__all__ = [
    # Builder (original)
    "FabricBuilder",
    "FabricSpec",
    # Enricher (Nexus integration)
    "NexusEnricher",
    "enrich_manifest",
    # Enrichment strategies
    "EnrichmentStrategy",
    "DefaultEnrichmentStrategy",
    "ComposableEnrichmentStrategy",
    "EnrichmentHandler",
    "RoleEnrichmentHandler",
    "DomainEnrichmentHandler",
    "PolicyEnrichmentHandler",
    "MixinEnrichmentHandler",
    # Schemas
    "Role",
    "Domain",
    "Capability",
    "GovernanceRule",
]
__version__ = "0.2.0"
