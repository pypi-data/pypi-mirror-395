"""
Fabric Enricher - Bridge between Nexus and Agent.

This module enriches baseline UAA manifests (from Nexus) with:
- Roles (personas, system prompts)
- Domains (tools, capabilities, context)
- Policies (governance rules, safety)
- Mixins (observability, safety hooks)

Pipeline:
    Nexus (translate) → Fabric (enrich) → Agent (execute)
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .enrichment import DefaultEnrichmentStrategy, EnrichmentStrategy


class NexusEnricher:
    """
    Enrich baseline UAA manifests from Nexus with Fabric composition.

    Usage:
        # Step 1: Translate with Nexus
        nexus translate langgraph_agent.py --output baseline.yaml

        # Step 2: Enrich with Fabric
        fabric enrich baseline.yaml \
          --role manifests/roles/researcher.yaml \
          --domain ontology/domains/finance.yaml \
          --policy policy/rules/safety.yaml \
          --out production_ready.yaml

        # Step 2 (with custom strategy):
        from universal_agent_fabric.enrichment import (
            ComposableEnrichmentStrategy,
            RoleEnrichmentHandler,
        )
        strategy = ComposableEnrichmentStrategy()
        strategy.add_handler(RoleEnrichmentHandler())
        enricher = NexusEnricher(strategy=strategy)
        enricher.enrich(...)
    """

    def __init__(self, strategy: Optional[EnrichmentStrategy] = None):
        """
        Initialize NexusEnricher with optional enrichment strategy.

        Args:
            strategy: Enrichment strategy to use. Defaults to DefaultEnrichmentStrategy
                which preserves current behavior.
        """
        self.strategy = strategy or DefaultEnrichmentStrategy()

    def enrich(
        self,
        baseline_manifest_path: str,
        role_path: Optional[str] = None,
        domain_paths: Optional[List[str]] = None,
        policy_paths: Optional[List[str]] = None,
        mixin_paths: Optional[List[str]] = None,
        output_path: str = "enriched_manifest.yaml",
    ) -> str:
        """
        Enrich baseline manifest with Fabric fragments.

        Args:
            baseline_manifest_path: UAA manifest from Nexus
            role_path: Role YAML (optional)
            domain_paths: Domain YAMLs (optional)
            policy_paths: Policy YAMLs (optional)
            mixin_paths: Mixin YAMLs - observability, safety (optional)
            output_path: Output path

        Returns:
            Path to enriched manifest
        """
        # Load baseline
        with open(baseline_manifest_path) as f:
            baseline = yaml.safe_load(f)

        # Load Fabric fragments
        role = self._load_yaml(role_path) if role_path else None
        domains = [self._load_yaml(p) for p in (domain_paths or [])]
        policies = [self._load_yaml(p) for p in (policy_paths or [])]
        mixins = [self._load_yaml(p) for p in (mixin_paths or [])]

        # Enrich baseline with fragments using strategy
        enriched = self.strategy.merge(baseline, role, domains, policies, mixins)

        # Add enrichment metadata
        if "metadata" not in enriched:
            enriched["metadata"] = {}
        enriched["metadata"]["enriched_by"] = "universal_agent_fabric"
        enriched["metadata"]["role"] = role.get("name") if role else None
        enriched["metadata"]["domains"] = [d.get("name") for d in domains if d]

        # Write output
        with open(output_path, "w") as f:
            yaml.dump(enriched, f, sort_keys=False, default_flow_style=False)

        return output_path

    def _load_yaml(self, path: str) -> Optional[Dict]:
        """Load YAML file, return None if not found."""
        try:
            with open(path) as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return None
        except Exception:
            return None


def enrich_manifest(
    baseline_path: str,
    role_path: Optional[str] = None,
    domain_paths: Optional[List[str]] = None,
    policy_paths: Optional[List[str]] = None,
    mixin_paths: Optional[List[str]] = None,
    output_path: str = "enriched_manifest.yaml",
) -> str:
    """
    Convenience function to enrich a manifest.

    Args:
        baseline_path: Path to baseline UAA manifest (from Nexus)
        role_path: Path to role YAML
        domain_paths: List of domain YAML paths
        policy_paths: List of policy YAML paths
        mixin_paths: List of mixin YAML paths
        output_path: Output path for enriched manifest

    Returns:
        Path to enriched manifest

    Example:
        enriched = enrich_manifest(
            "baseline.yaml",
            role_path="manifests/roles/researcher.yaml",
            domain_paths=["ontology/domains/finance.yaml"],
            policy_paths=["policy/rules/safety.yaml"],
            output_path="production_ready.yaml"
        )
    """
    enricher = NexusEnricher()
    return enricher.enrich(
        baseline_manifest_path=baseline_path,
        role_path=role_path,
        domain_paths=domain_paths,
        policy_paths=policy_paths,
        mixin_paths=mixin_paths,
        output_path=output_path,
    )

