"""
Tests for enrichment strategy interface.
"""

import pytest

from universal_agent_fabric.enrichment import (
    ComposableEnrichmentStrategy,
    DefaultEnrichmentStrategy,
    DomainEnrichmentHandler,
    EnrichmentHandler,
    MixinEnrichmentHandler,
    PolicyEnrichmentHandler,
    RoleEnrichmentHandler,
)
from universal_agent_fabric.enricher import NexusEnricher


class TestDefaultEnrichmentStrategy:
    """Test default enrichment strategy (preserves current behavior)."""

    def test_default_strategy_merges_role(self):
        """Default strategy applies role system prompt."""
        strategy = DefaultEnrichmentStrategy()
        baseline = {
            "name": "test-agent",
            "routers": [{"name": "router1", "system_message": "Base prompt"}],
        }
        role = {"system_prompt": "Role prompt"}

        result = strategy.merge(baseline, role, [], [], [])

        assert "Role prompt" in result["routers"][0]["system_message"]
        assert "Base prompt" in result["routers"][0]["system_message"]

    def test_default_strategy_creates_router_when_none_exists(self):
        """Default strategy creates router if role has prompt but no routers."""
        strategy = DefaultEnrichmentStrategy()
        baseline = {"name": "test-agent"}
        role = {
            "system_prompt": "Role prompt",
            "default_model": "gpt-4",
            "model_candidates": ["gpt-4", "gpt-3.5"],
        }

        result = strategy.merge(baseline, role, [], [], [])

        assert len(result["routers"]) == 1
        assert result["routers"][0]["name"] == "primary-router"
        assert result["routers"][0]["system_message"] == "Role prompt"
        assert result["routers"][0]["default_model"] == "gpt-4"

    def test_default_strategy_adds_domain_tools(self):
        """Default strategy adds domain capabilities as tools."""
        strategy = DefaultEnrichmentStrategy()
        baseline = {"name": "test-agent", "tools": []}
        domain = {
            "capabilities": [
                {
                    "name": "test_tool",
                    "description": "A test tool",
                    "protocol": "mcp",
                    "config_template": {"key": "value"},
                }
            ]
        }

        result = strategy.merge(baseline, None, [domain], [], [])

        assert len(result["tools"]) == 1
        assert result["tools"][0]["name"] == "test_tool"
        assert result["tools"][0]["protocol"] == "mcp"

    def test_default_strategy_merges_domain_prompts(self):
        """Default strategy merges domain system prompt mixins."""
        strategy = DefaultEnrichmentStrategy()
        baseline = {
            "name": "test-agent",
            "routers": [{"name": "router1", "system_message": "Base"}],
        }
        domain = {"system_prompt_mixin": "Domain context"}

        result = strategy.merge(baseline, None, [domain], [], [])

        assert "Domain context" in result["routers"][0]["system_message"]
        assert "Base" in result["routers"][0]["system_message"]

    def test_default_strategy_adds_policies(self):
        """Default strategy adds policy rules."""
        strategy = DefaultEnrichmentStrategy()
        baseline = {"name": "test-agent", "policies": []}
        policy = [{"name": "rule1", "action": "deny"}]

        result = strategy.merge(baseline, None, [], [policy], [])

        assert len(result["policies"]) == 1
        assert result["policies"][0]["name"] == "rule1"

    def test_default_strategy_applies_mixins(self):
        """Default strategy applies mixin configurations."""
        strategy = DefaultEnrichmentStrategy()
        baseline = {"name": "test-agent"}
        mixin = {
            "observability": {"enabled": True},
            "safety": {"level": "high"},
            "logging": {"level": "debug"},
        }

        result = strategy.merge(baseline, None, [], [], [mixin])

        assert result["observability"]["enabled"] is True
        assert result["safety"]["level"] == "high"
        assert result["logging"]["level"] == "debug"


class TestComposableEnrichmentStrategy:
    """Test composable enrichment strategy."""

    def test_composable_strategy_runs_handlers_in_order(self):
        """Composable strategy runs handlers in the order they were added."""
        strategy = ComposableEnrichmentStrategy()
        call_order = []

        class TrackingHandler(EnrichmentHandler):
            def __init__(self, name):
                self.name = name

            def handle(self, manifest, role, domains, policies, mixins):
                call_order.append(self.name)
                return manifest

        handler1 = TrackingHandler("first")
        handler2 = TrackingHandler("second")
        handler3 = TrackingHandler("third")

        strategy.add_handler(handler1).add_handler(handler2).add_handler(handler3)

        baseline = {"name": "test"}
        strategy.merge(baseline, None, [], [], [])

        assert call_order == ["first", "second", "third"]

    def test_composable_strategy_passes_manifest_through_handlers(self):
        """Composable strategy passes manifest through handler chain."""
        strategy = ComposableEnrichmentStrategy()

        class IncrementHandler(EnrichmentHandler):
            def handle(self, manifest, role, domains, policies, mixins):
                manifest["counter"] = manifest.get("counter", 0) + 1
                return manifest

        strategy.add_handler(IncrementHandler()).add_handler(IncrementHandler())

        baseline = {"name": "test"}
        result = strategy.merge(baseline, None, [], [], [])

        assert result["counter"] == 2

    def test_composable_strategy_supports_method_chaining(self):
        """Composable strategy supports method chaining."""
        strategy = ComposableEnrichmentStrategy()
        handler1 = RoleEnrichmentHandler()
        handler2 = DomainEnrichmentHandler()

        result = strategy.add_handler(handler1).add_handler(handler2)

        assert result is strategy
        assert len(strategy._handlers) == 2


class TestRoleEnrichmentHandler:
    """Test role enrichment handler."""

    def test_role_handler_applies_system_prompt(self):
        """Role handler applies role system prompt to existing routers."""
        handler = RoleEnrichmentHandler()
        manifest = {
            "routers": [{"name": "router1", "system_message": "Base"}],
        }
        role = {"system_prompt": "Role prompt"}

        result = handler.handle(manifest, role, [], [], [])

        assert "Role prompt" in result["routers"][0]["system_message"]
        assert "Base" in result["routers"][0]["system_message"]

    def test_role_handler_creates_router_when_none_exists(self):
        """Role handler creates router if role has prompt but no routers."""
        handler = RoleEnrichmentHandler()
        manifest = {"name": "test-agent"}
        role = {
            "system_prompt": "Role prompt",
            "default_model": "gpt-4",
        }

        result = handler.handle(manifest, role, [], [], [])

        assert len(result["routers"]) == 1
        assert result["routers"][0]["name"] == "primary-router"
        assert result["routers"][0]["system_message"] == "Role prompt"

    def test_role_handler_skips_when_no_role(self):
        """Role handler does nothing when role is None."""
        handler = RoleEnrichmentHandler()
        manifest = {"name": "test-agent"}

        result = handler.handle(manifest, None, [], [], [])

        assert result == manifest


class TestDomainEnrichmentHandler:
    """Test domain enrichment handler."""

    def test_domain_handler_adds_tools(self):
        """Domain handler adds domain capabilities as tools."""
        handler = DomainEnrichmentHandler()
        manifest = {"name": "test-agent", "tools": []}
        domain = {
            "capabilities": [
                {
                    "name": "test_tool",
                    "description": "A test tool",
                    "protocol": "mcp",
                }
            ]
        }

        result = handler.handle(manifest, None, [domain], [], [])

        assert len(result["tools"]) == 1
        assert result["tools"][0]["name"] == "test_tool"

    def test_domain_handler_merges_prompts(self):
        """Domain handler merges domain system prompt mixins."""
        handler = DomainEnrichmentHandler()
        manifest = {
            "routers": [{"name": "router1", "system_message": "Base"}],
        }
        domain = {"system_prompt_mixin": "Domain context"}

        result = handler.handle(manifest, None, [domain], [], [])

        assert "Domain context" in result["routers"][0]["system_message"]

    def test_domain_handler_handles_multiple_domains(self):
        """Domain handler processes multiple domains."""
        handler = DomainEnrichmentHandler()
        manifest = {"name": "test-agent", "tools": []}
        domain1 = {
            "capabilities": [{"name": "tool1", "protocol": "mcp"}],
        }
        domain2 = {
            "capabilities": [{"name": "tool2", "protocol": "http"}],
        }

        result = handler.handle(manifest, None, [domain1, domain2], [], [])

        assert len(result["tools"]) == 2
        tool_names = {t["name"] for t in result["tools"]}
        assert tool_names == {"tool1", "tool2"}


class TestPolicyEnrichmentHandler:
    """Test policy enrichment handler."""

    def test_policy_handler_adds_rules_from_list(self):
        """Policy handler adds rules from list policy."""
        handler = PolicyEnrichmentHandler()
        manifest = {"name": "test-agent", "policies": []}
        policy = [{"name": "rule1"}, {"name": "rule2"}]

        result = handler.handle(manifest, None, [], [policy], [])

        assert len(result["policies"]) == 2
        assert result["policies"][0]["name"] == "rule1"
        assert result["policies"][1]["name"] == "rule2"

    def test_policy_handler_adds_rules_from_dict(self):
        """Policy handler adds rules from dict with 'rules' key."""
        handler = PolicyEnrichmentHandler()
        manifest = {"name": "test-agent", "policies": []}
        policy = {"rules": [{"name": "rule1"}]}

        result = handler.handle(manifest, None, [], [policy], [])

        assert len(result["policies"]) == 1
        assert result["policies"][0]["name"] == "rule1"

    def test_policy_handler_handles_single_rule_dict(self):
        """Policy handler handles single rule as dict."""
        handler = PolicyEnrichmentHandler()
        manifest = {"name": "test-agent", "policies": []}
        policy = {"name": "rule1", "action": "deny"}

        result = handler.handle(manifest, None, [], [policy], [])

        assert len(result["policies"]) == 1
        assert result["policies"][0]["name"] == "rule1"


class TestMixinEnrichmentHandler:
    """Test mixin enrichment handler."""

    def test_mixin_handler_applies_observability(self):
        """Mixin handler applies observability configuration."""
        handler = MixinEnrichmentHandler()
        manifest = {"name": "test-agent"}
        mixin = {"observability": {"enabled": True}}

        result = handler.handle(manifest, None, [], [], [mixin])

        assert result["observability"]["enabled"] is True

    def test_mixin_handler_applies_safety(self):
        """Mixin handler applies safety configuration."""
        handler = MixinEnrichmentHandler()
        manifest = {"name": "test-agent"}
        mixin = {"safety": {"level": "high"}}

        result = handler.handle(manifest, None, [], [], [mixin])

        assert result["safety"]["level"] == "high"

    def test_mixin_handler_applies_logging(self):
        """Mixin handler applies logging configuration."""
        handler = MixinEnrichmentHandler()
        manifest = {"name": "test-agent"}
        mixin = {"logging": {"level": "debug"}}

        result = handler.handle(manifest, None, [], [], [mixin])

        assert result["logging"]["level"] == "debug"

    def test_mixin_handler_applies_all_mixins(self):
        """Mixin handler applies all mixin types."""
        handler = MixinEnrichmentHandler()
        manifest = {"name": "test-agent"}
        mixin = {
            "observability": {"enabled": True},
            "safety": {"level": "high"},
            "logging": {"level": "debug"},
        }

        result = handler.handle(manifest, None, [], [], [mixin])

        assert "observability" in result
        assert "safety" in result
        assert "logging" in result


class TestNexusEnricherWithStrategy:
    """Test NexusEnricher with custom strategies."""

    def test_enricher_uses_default_strategy_by_default(self):
        """NexusEnricher uses DefaultEnrichmentStrategy when no strategy provided."""
        enricher = NexusEnricher()
        assert isinstance(enricher.strategy, DefaultEnrichmentStrategy)

    def test_enricher_uses_custom_strategy(self):
        """NexusEnricher uses provided custom strategy."""
        custom_strategy = ComposableEnrichmentStrategy()
        enricher = NexusEnricher(strategy=custom_strategy)
        assert enricher.strategy is custom_strategy

    def test_enricher_with_composable_strategy(self, tmp_path):
        """NexusEnricher works with composable strategy."""
        # Create test files
        baseline_file = tmp_path / "baseline.yaml"
        baseline_file.write_text("name: test-agent\nrouters: []\ntools: []\n")

        role_file = tmp_path / "role.yaml"
        role_file.write_text("name: Test Role\nsystem_prompt: Test prompt\n")

        output_file = tmp_path / "output.yaml"

        # Create composable strategy
        strategy = ComposableEnrichmentStrategy()
        strategy.add_handler(RoleEnrichmentHandler())
        strategy.add_handler(DomainEnrichmentHandler())
        strategy.add_handler(PolicyEnrichmentHandler())
        strategy.add_handler(MixinEnrichmentHandler())

        enricher = NexusEnricher(strategy=strategy)
        result_path = enricher.enrich(
            str(baseline_file),
            role_path=str(role_file),
            output_path=str(output_file),
        )

        assert result_path == str(output_file)
        assert output_file.exists()


class TestCustomHandler:
    """Test creating and using custom handlers."""

    def test_custom_handler_integration(self):
        """Custom handler can be integrated into composable strategy."""
        class CustomHandler(EnrichmentHandler):
            def handle(self, manifest, role, domains, policies, mixins):
                manifest["custom_field"] = "custom_value"
                return manifest

        strategy = ComposableEnrichmentStrategy()
        strategy.add_handler(RoleEnrichmentHandler())
        strategy.add_handler(CustomHandler())
        strategy.add_handler(DomainEnrichmentHandler())

        baseline = {"name": "test"}
        result = strategy.merge(baseline, None, [], [], [])

        assert result["custom_field"] == "custom_value"

