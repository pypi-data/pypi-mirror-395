"""
Integration tests validating Fabric output against Universal Agent Kernel schema.
"""

from pathlib import Path

import pytest
import yaml

from universal_agent.manifests.schema import (
    AgentManifest,
    GraphSpec,
    PolicySpec,
    RouterSpec,
    ToolSpec,
)

from universal_agent_fabric.builder import FabricBuilder
from universal_agent_fabric.schemas import (
    Capability,
    Domain,
    FabricSpec,
    GovernanceRule,
    Role,
)


class TestKernelSchemaCompatibility:
    """Validate that Fabric output is compatible with the kernel AgentManifest."""

    def test_manifest_validates_against_agent_manifest(self, sample_fabric_spec: FabricSpec):
        """Compiled manifest passes AgentManifest Pydantic validation."""
        builder = FabricBuilder(sample_fabric_spec)
        manifest = builder.build()

        # This will raise ValidationError if schema mismatch
        agent = AgentManifest(**manifest)
        assert agent.name == "test-agent"

    def test_tools_validate_against_tool_spec(self, sample_fabric_spec: FabricSpec):
        """Each compiled tool passes ToolSpec validation."""
        builder = FabricBuilder(sample_fabric_spec)
        manifest = builder.build()

        for tool_data in manifest["tools"]:
            tool = ToolSpec(**tool_data)
            assert tool.name
            assert tool.protocol in ("mcp", "http", "local", "subprocess")

    def test_routers_validate_against_router_spec(self, sample_fabric_spec: FabricSpec):
        """Each compiled router passes RouterSpec validation."""
        builder = FabricBuilder(sample_fabric_spec)
        manifest = builder.build()

        for router_data in manifest["routers"]:
            router = RouterSpec(**router_data)
            assert router.name == "primary-router"
            assert router.system_message

    def test_policies_validate_against_policy_spec(self, sample_fabric_spec: FabricSpec):
        """Each compiled policy passes PolicySpec validation."""
        builder = FabricBuilder(sample_fabric_spec)
        manifest = builder.build()

        for policy_data in manifest["policies"]:
            policy = PolicySpec(**policy_data)
            assert policy.name == "fabric-governance"
            assert len(policy.rules) > 0

    def test_graphs_validate_against_graph_spec(self, sample_fabric_spec: FabricSpec):
        """Each compiled graph passes GraphSpec validation."""
        builder = FabricBuilder(sample_fabric_spec)
        manifest = builder.build()

        for graph_data in manifest["graphs"]:
            # Remove 'template' key as it's Fabric-specific metadata
            graph_copy = dict(graph_data)
            template = graph_copy.pop("template", None)
            graph = GraphSpec(**graph_copy)
            assert graph.name == "main"
            assert graph.entry_node == "start"


class TestSampleContentIntegration:
    """Integration tests using the repository's sample YAML content."""

    def test_researcher_role_loads(self, researcher_role_path: Path):
        """Sample researcher role YAML loads into Role model."""
        data = yaml.safe_load(researcher_role_path.read_text())
        role = Role(**data)
        assert role.name == "Senior Researcher"
        assert role.base_template == "planning_loop"

    def test_finance_domain_loads(self, finance_domain_path: Path):
        """Sample finance domain YAML loads into Domain model."""
        data = yaml.safe_load(finance_domain_path.read_text())
        domain = Domain(**data)
        assert domain.name == "Finance Domain"
        assert len(domain.capabilities) == 2

    def test_safety_policy_loads(self, safety_policy_path: Path):
        """Sample safety policy YAML loads into GovernanceRule models."""
        data = yaml.safe_load(safety_policy_path.read_text())
        rules = [GovernanceRule(**r) for r in data]
        assert len(rules) == 2
        assert rules[0].name == "no_trading"
        assert rules[1].action == "deny"

    def test_full_sample_build_validates(
        self,
        researcher_role_path: Path,
        finance_domain_path: Path,
        safety_policy_path: Path,
    ):
        """Full build from sample content passes kernel schema validation."""
        role = Role(**yaml.safe_load(researcher_role_path.read_text()))
        domain = Domain(**yaml.safe_load(finance_domain_path.read_text()))
        policy_data = yaml.safe_load(safety_policy_path.read_text())
        governance = [GovernanceRule(**r) for r in policy_data]

        spec = FabricSpec(
            name="finance-researcher",
            role=role,
            domains=[domain],
            governance=governance,
        )

        builder = FabricBuilder(spec)
        manifest = builder.build()

        # Validate full manifest
        agent = AgentManifest(**manifest)
        assert agent.name == "finance-researcher"
        assert len(agent.tools) == 2
        assert len(agent.routers) == 1
        assert len(agent.policies) == 1
        assert agent.routers[0].system_message
        assert "Senior Researcher" in agent.routers[0].system_message
        assert "market data" in agent.routers[0].system_message.lower()


class TestEdgeCases:
    """Edge case and error handling tests."""

    def test_empty_governance_produces_no_policies(self, sample_role, sample_domain):
        """When no governance rules exist, policies list is empty."""
        spec = FabricSpec(
            name="no-policy-agent",
            role=sample_role,
            domains=[sample_domain],
            governance=[],
        )
        builder = FabricBuilder(spec)
        manifest = builder.build()

        assert manifest["policies"] == []
        # Router should not reference non-existent policy
        assert "policy" not in manifest["routers"][0]

    def test_empty_domains_produces_no_tools(self, sample_role):
        """When no domains exist, tools list is empty."""
        spec = FabricSpec(
            name="no-tools-agent",
            role=sample_role,
            domains=[],
            governance=[],
        )
        builder = FabricBuilder(spec)
        manifest = builder.build()

        assert manifest["tools"] == []

    def test_multiple_domains_aggregate_capabilities(self, sample_role, sample_capability):
        """Multiple domains combine their capabilities into tools."""
        domain1 = Domain(
            name="Domain A",
            description="First domain",
            capabilities=[sample_capability],
            system_prompt_mixin="Domain A context.",
        )
        cap2 = Capability(
            name="another_tool",
            description="Another test tool.",
            protocol="http",
            config_template={"url": "http://example.com"},
        )
        domain2 = Domain(
            name="Domain B",
            description="Second domain",
            capabilities=[cap2],
            system_prompt_mixin="Domain B context.",
        )

        spec = FabricSpec(
            name="multi-domain-agent",
            role=sample_role,
            domains=[domain1, domain2],
            governance=[],
        )
        builder = FabricBuilder(spec)
        manifest = builder.build()

        assert len(manifest["tools"]) == 2
        tool_names = {t["name"] for t in manifest["tools"]}
        assert tool_names == {"test_tool", "another_tool"}

        # Router prompt should contain both domain mixins
        router_msg = manifest["routers"][0]["system_message"]
        assert "Domain A context" in router_msg
        assert "Domain B context" in router_msg

