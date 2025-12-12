"""
Unit tests for universal_agent_fabric.builder.
"""

import pytest

from universal_agent_fabric.builder import FabricBuilder
from universal_agent_fabric.schemas import FabricSpec


class TestFabricBuilder:
    """Tests for FabricBuilder compilation logic."""

    def test_build_returns_dict(self, sample_fabric_spec: FabricSpec):
        """Builder returns a dictionary manifest."""
        builder = FabricBuilder(sample_fabric_spec)
        manifest = builder.build()
        assert isinstance(manifest, dict)

    def test_manifest_has_required_keys(self, sample_fabric_spec: FabricSpec):
        """Manifest contains all required top-level keys."""
        builder = FabricBuilder(sample_fabric_spec)
        manifest = builder.build()

        required_keys = {"name", "version", "graphs", "routers", "tools", "policies", "metadata"}
        assert required_keys.issubset(manifest.keys())

    def test_manifest_name_matches_spec(self, sample_fabric_spec: FabricSpec):
        """Manifest name matches the FabricSpec name."""
        builder = FabricBuilder(sample_fabric_spec)
        manifest = builder.build()
        assert manifest["name"] == "test-agent"

    def test_tools_compiled_from_domain_capabilities(self, sample_fabric_spec: FabricSpec):
        """Tools are generated from domain capabilities."""
        builder = FabricBuilder(sample_fabric_spec)
        manifest = builder.build()

        assert len(manifest["tools"]) == 1
        tool = manifest["tools"][0]
        assert tool["name"] == "test_tool"
        assert tool["protocol"] == "mcp"

    def test_policies_compiled_from_governance(self, sample_fabric_spec: FabricSpec):
        """Policies are generated from governance rules."""
        builder = FabricBuilder(sample_fabric_spec)
        manifest = builder.build()

        assert len(manifest["policies"]) == 1
        policy = manifest["policies"][0]
        assert policy["name"] == "fabric-governance"
        assert len(policy["rules"]) == 1
        assert policy["rules"][0]["action"] == "deny"

    def test_router_system_message_merges_role_and_domain(self, sample_fabric_spec: FabricSpec):
        """Router system message combines role prompt and domain mixin."""
        builder = FabricBuilder(sample_fabric_spec)
        manifest = builder.build()

        assert len(manifest["routers"]) == 1
        router = manifest["routers"][0]
        system_msg = router["system_message"]

        # Role prompt
        assert "test researcher" in system_msg.lower()
        # Domain mixin
        assert "test tools" in system_msg.lower()

    def test_router_policy_attached_when_governance_present(self, sample_fabric_spec: FabricSpec):
        """Router references governance policy when rules exist."""
        builder = FabricBuilder(sample_fabric_spec)
        manifest = builder.build()

        router = manifest["routers"][0]
        assert router.get("policy") == "fabric-governance"

    def test_graph_compiled_with_template_name(self, sample_fabric_spec: FabricSpec):
        """Graph includes template name from role in metadata.extra."""
        builder = FabricBuilder(sample_fabric_spec)
        manifest = builder.build()

        assert len(manifest["graphs"]) == 1
        graph = manifest["graphs"][0]
        assert graph["metadata"]["extra"]["template"] == "planning_loop"
        assert graph["entry_node"] == "start"

    def test_metadata_includes_generator_tag(self, sample_fabric_spec: FabricSpec):
        """Metadata identifies the fabric as generator in extra field."""
        builder = FabricBuilder(sample_fabric_spec)
        manifest = builder.build()

        assert "fabric-generated" in manifest["metadata"]["tags"]
        assert manifest["metadata"]["extra"]["generated_by"] == "universal_agent_fabric"

