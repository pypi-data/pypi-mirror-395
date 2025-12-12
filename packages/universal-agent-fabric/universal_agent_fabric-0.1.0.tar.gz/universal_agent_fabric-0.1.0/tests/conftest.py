"""
Pytest fixtures for universal_agent_fabric tests.
"""

from pathlib import Path

import pytest
import yaml

from universal_agent_fabric.schemas import (
    Capability,
    Domain,
    FabricSpec,
    GovernanceRule,
    Role,
)


@pytest.fixture
def sample_role() -> Role:
    """Minimal role for testing."""
    return Role(
        name="Test Researcher",
        base_template="planning_loop",
        system_prompt_template="You are a test researcher. Be thorough.",
        default_capabilities=["web_search"],
    )


@pytest.fixture
def sample_capability() -> Capability:
    """Minimal capability for testing."""
    return Capability(
        name="test_tool",
        description="A test tool for validation.",
        protocol="mcp",
        config_template={"command": "test-cmd"},
    )


@pytest.fixture
def sample_domain(sample_capability: Capability) -> Domain:
    """Minimal domain with one capability."""
    return Domain(
        name="Test Domain",
        description="A domain for testing.",
        capabilities=[sample_capability],
        system_prompt_mixin="You have access to test tools.",
    )


@pytest.fixture
def sample_governance_rule() -> GovernanceRule:
    """Minimal governance rule."""
    return GovernanceRule(
        name="no_delete",
        target_pattern="delete",
        action="deny",
        conditions={},
    )


@pytest.fixture
def sample_fabric_spec(
    sample_role: Role,
    sample_domain: Domain,
    sample_governance_rule: GovernanceRule,
) -> FabricSpec:
    """Complete FabricSpec for integration testing."""
    return FabricSpec(
        name="test-agent",
        role=sample_role,
        domains=[sample_domain],
        governance=[sample_governance_rule],
    )


@pytest.fixture
def project_root() -> Path:
    """Return project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def researcher_role_path(project_root: Path) -> Path:
    """Path to the sample researcher role YAML."""
    return project_root / "manifests" / "roles" / "researcher.yaml"


@pytest.fixture
def finance_domain_path(project_root: Path) -> Path:
    """Path to the sample finance domain YAML."""
    return project_root / "ontology" / "domains" / "finance.yaml"


@pytest.fixture
def safety_policy_path(project_root: Path) -> Path:
    """Path to the sample safety policy YAML."""
    return project_root / "policy" / "rules" / "safety.yaml"

