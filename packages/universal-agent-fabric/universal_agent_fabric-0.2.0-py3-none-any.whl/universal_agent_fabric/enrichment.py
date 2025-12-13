"""
Enrichment Strategy Interface for Fabric.

Enables customizable fragment merging strategies for the NexusEnricher.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class EnrichmentStrategy(ABC):
    """
    Strategy for merging Fabric fragments.

    Enables:
    - Custom merge logic
    - Fragment composition strategies
    - Conflict resolution
    """

    @abstractmethod
    def merge(
        self,
        baseline: Dict[str, Any],
        role: Optional[Dict],
        domains: List[Dict],
        policies: List[Dict],
        mixins: List[Dict],
    ) -> Dict[str, Any]:
        """
        Merge fragments with strategy-specific logic.

        Args:
            baseline: UAA manifest from Nexus
            role: Role fragment
            domains: List of domain fragments
            policies: List of policy fragments
            mixins: List of mixin fragments

        Returns:
            Enriched manifest
        """
        pass


class DefaultEnrichmentStrategy(EnrichmentStrategy):
    """Default (current) enrichment strategy."""

    def __init__(self):
        """Initialize default strategy with merge helper."""
        self._merge_system_prompt = self._create_merge_helper()

    def _create_merge_helper(self):
        """Create system prompt merge helper function."""
        def merge_system_prompt(base: str, addition: str) -> str:
            """Merge system prompt fragments."""
            if not base:
                return addition
            if not addition:
                return base
            return f"{base}\n\n{addition}".strip()
        return merge_system_prompt

    def merge(
        self,
        baseline: Dict[str, Any],
        role: Optional[Dict],
        domains: List[Dict],
        policies: List[Dict],
        mixins: List[Dict],
    ) -> Dict[str, Any]:
        """
        Merge fragments using default (current) logic.

        This is the original implementation from NexusEnricher._merge_fragments().
        """
        enriched = baseline.copy()

        # Ensure lists exist
        if "routers" not in enriched:
            enriched["routers"] = []
        if "tools" not in enriched:
            enriched["tools"] = []
        if "policies" not in enriched:
            enriched["policies"] = []

        # Apply role (update system prompts in routers)
        if role:
            system_prompt = role.get(
                "system_prompt_template", role.get("system_prompt", "")
            )
            if system_prompt and enriched.get("routers"):
                for router in enriched["routers"]:
                    router["system_message"] = self._merge_system_prompt(
                        router.get("system_message", ""), system_prompt
                    )

            # If no routers exist but role has prompt, create primary router
            if system_prompt and not enriched["routers"]:
                enriched["routers"].append(
                    {
                        "name": "primary-router",
                        "strategy": "llm",
                        "system_message": system_prompt,
                        "model_candidates": role.get(
                            "model_candidates", ["gpt-4o-mini"]
                        ),
                        "default_model": role.get("default_model", "gpt-4o-mini"),
                    }
                )

        # Apply domains (add tools/capabilities, merge prompts)
        for domain in domains:
            if not domain:
                continue

            # Add capabilities as tools
            capabilities = domain.get("capabilities", [])
            for cap in capabilities:
                tool_spec = {
                    "name": cap.get("name"),
                    "description": cap.get("description"),
                    "protocol": cap.get("protocol", "mcp"),
                    "config": cap.get("config_template", cap.get("config", {})),
                }
                enriched["tools"].append(tool_spec)

            # Merge domain system prompt mixins into routers
            domain_prompt = domain.get("system_prompt_mixin", "")
            if domain_prompt and enriched.get("routers"):
                for router in enriched["routers"]:
                    router["system_message"] = self._merge_system_prompt(
                        router.get("system_message", ""), domain_prompt
                    )

        # Apply policies (add governance rules)
        for policy_set in policies:
            if not policy_set:
                continue

            # Handle both list of rules and dict with 'rules' key
            rules = []
            if isinstance(policy_set, list):
                rules = policy_set
            elif isinstance(policy_set, dict):
                rules = policy_set.get("rules", [policy_set])

            for rule in rules:
                enriched["policies"].append(rule)

        # Apply mixins (observability, safety)
        for mixin in mixins:
            if not mixin:
                continue

            if "observability" in mixin:
                enriched["observability"] = mixin["observability"]
            if "safety" in mixin:
                enriched["safety"] = mixin["safety"]
            if "logging" in mixin:
                enriched["logging"] = mixin["logging"]

        return enriched


class EnrichmentHandler(ABC):
    """Single responsibility handler in enrichment pipeline."""

    @abstractmethod
    def handle(
        self,
        manifest: Dict[str, Any],
        role: Optional[Dict],
        domains: List[Dict],
        policies: List[Dict],
        mixins: List[Dict],
    ) -> Dict[str, Any]:
        """
        Process manifest.

        Args:
            manifest: Current manifest state
            role: Role fragment
            domains: List of domain fragments
            policies: List of policy fragments
            mixins: List of mixin fragments

        Returns:
            Updated manifest
        """
        pass


class ComposableEnrichmentStrategy(EnrichmentStrategy):
    """
    Composable strategy for fine-grained control.

    Usage:
        strategy = ComposableEnrichmentStrategy()
        strategy.add_handler(RoleHandler())
        strategy.add_handler(DomainHandler())
        enricher = NexusEnricher(strategy=strategy)
    """

    def __init__(self):
        """Initialize composable strategy with empty handler list."""
        self._handlers: List[EnrichmentHandler] = []

    def add_handler(
        self, handler: EnrichmentHandler
    ) -> "ComposableEnrichmentStrategy":
        """
        Add handler to pipeline.

        Args:
            handler: Handler to add to pipeline

        Returns:
            Self for method chaining
        """
        self._handlers.append(handler)
        return self

    def merge(
        self,
        baseline: Dict[str, Any],
        role: Optional[Dict],
        domains: List[Dict],
        policies: List[Dict],
        mixins: List[Dict],
    ) -> Dict[str, Any]:
        """
        Merge fragments by running handlers in sequence.

        Args:
            baseline: UAA manifest from Nexus
            role: Role fragment
            domains: List of domain fragments
            policies: List of policy fragments
            mixins: List of mixin fragments

        Returns:
            Enriched manifest
        """
        result = baseline.copy()
        for handler in self._handlers:
            result = handler.handle(result, role, domains, policies, mixins)
        return result


class RoleEnrichmentHandler(EnrichmentHandler):
    """Handle role-specific enrichment."""

    def __init__(self):
        """Initialize role handler with merge helper."""
        self._merge_system_prompt = self._create_merge_helper()

    def _create_merge_helper(self):
        """Create system prompt merge helper function."""
        def merge_system_prompt(base: str, addition: str) -> str:
            """Merge system prompt fragments."""
            if not base:
                return addition
            if not addition:
                return base
            return f"{base}\n\n{addition}".strip()
        return merge_system_prompt

    def handle(
        self,
        manifest: Dict[str, Any],
        role: Optional[Dict],
        domains: List[Dict],
        policies: List[Dict],
        mixins: List[Dict],
    ) -> Dict[str, Any]:
        """
        Apply role-specific enrichment.

        Args:
            manifest: Current manifest state
            role: Role fragment
            domains: List of domain fragments (unused)
            policies: List of policy fragments (unused)
            mixins: List of mixin fragments (unused)

        Returns:
            Updated manifest
        """
        if not role:
            return manifest

        # Ensure routers list exists
        if "routers" not in manifest:
            manifest["routers"] = []

        system_prompt = role.get(
            "system_prompt_template", role.get("system_prompt", "")
        )
        if system_prompt and manifest.get("routers"):
            for router in manifest["routers"]:
                router["system_message"] = self._merge_system_prompt(
                    router.get("system_message", ""), system_prompt
                )

        # If no routers exist but role has prompt, create primary router
        if system_prompt and not manifest["routers"]:
            manifest["routers"].append(
                {
                    "name": "primary-router",
                    "strategy": "llm",
                    "system_message": system_prompt,
                    "model_candidates": role.get(
                        "model_candidates", ["gpt-4o-mini"]
                    ),
                    "default_model": role.get("default_model", "gpt-4o-mini"),
                }
            )

        return manifest


class DomainEnrichmentHandler(EnrichmentHandler):
    """Handle domain-specific enrichment."""

    def __init__(self):
        """Initialize domain handler with merge helper."""
        self._merge_system_prompt = self._create_merge_helper()

    def _create_merge_helper(self):
        """Create system prompt merge helper function."""
        def merge_system_prompt(base: str, addition: str) -> str:
            """Merge system prompt fragments."""
            if not base:
                return addition
            if not addition:
                return base
            return f"{base}\n\n{addition}".strip()
        return merge_system_prompt

    def handle(
        self,
        manifest: Dict[str, Any],
        role: Optional[Dict],
        domains: List[Dict],
        policies: List[Dict],
        mixins: List[Dict],
    ) -> Dict[str, Any]:
        """
        Apply domain-specific enrichment.

        Args:
            manifest: Current manifest state
            role: Role fragment (unused)
            domains: List of domain fragments
            policies: List of policy fragments (unused)
            mixins: List of mixin fragments (unused)

        Returns:
            Updated manifest
        """
        # Ensure lists exist
        if "tools" not in manifest:
            manifest["tools"] = []
        if "routers" not in manifest:
            manifest["routers"] = []

        for domain in domains:
            if not domain:
                continue

            # Add capabilities as tools
            capabilities = domain.get("capabilities", [])
            for cap in capabilities:
                tool_spec = {
                    "name": cap.get("name"),
                    "description": cap.get("description"),
                    "protocol": cap.get("protocol", "mcp"),
                    "config": cap.get("config_template", cap.get("config", {})),
                }
                manifest["tools"].append(tool_spec)

            # Merge domain system prompt mixins into routers
            domain_prompt = domain.get("system_prompt_mixin", "")
            if domain_prompt and manifest.get("routers"):
                for router in manifest["routers"]:
                    router["system_message"] = self._merge_system_prompt(
                        router.get("system_message", ""), domain_prompt
                    )

        return manifest


class PolicyEnrichmentHandler(EnrichmentHandler):
    """Handle policy-specific enrichment."""

    def handle(
        self,
        manifest: Dict[str, Any],
        role: Optional[Dict],
        domains: List[Dict],
        policies: List[Dict],
        mixins: List[Dict],
    ) -> Dict[str, Any]:
        """
        Apply policy-specific enrichment.

        Args:
            manifest: Current manifest state
            role: Role fragment (unused)
            domains: List of domain fragments (unused)
            policies: List of policy fragments
            mixins: List of mixin fragments (unused)

        Returns:
            Updated manifest
        """
        # Ensure policies list exists
        if "policies" not in manifest:
            manifest["policies"] = []

        for policy_set in policies:
            if not policy_set:
                continue

            # Handle both list of rules and dict with 'rules' key
            rules = []
            if isinstance(policy_set, list):
                rules = policy_set
            elif isinstance(policy_set, dict):
                rules = policy_set.get("rules", [policy_set])

            for rule in rules:
                manifest["policies"].append(rule)

        return manifest


class MixinEnrichmentHandler(EnrichmentHandler):
    """Handle mixin-specific enrichment."""

    def handle(
        self,
        manifest: Dict[str, Any],
        role: Optional[Dict],
        domains: List[Dict],
        policies: List[Dict],
        mixins: List[Dict],
    ) -> Dict[str, Any]:
        """
        Apply mixin-specific enrichment.

        Args:
            manifest: Current manifest state
            role: Role fragment (unused)
            domains: List of domain fragments (unused)
            policies: List of policy fragments (unused)
            mixins: List of mixin fragments

        Returns:
            Updated manifest
        """
        for mixin in mixins:
            if not mixin:
                continue

            if "observability" in mixin:
                manifest["observability"] = mixin["observability"]
            if "safety" in mixin:
                manifest["safety"] = mixin["safety"]
            if "logging" in mixin:
                manifest["logging"] = mixin["logging"]

        return manifest

