"""
universal_agent_fabric.schemas

High-level definitions for the Agent Universe.
These compile down to the low-level Universal Agent Kernel specifications.
"""

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class Capability(BaseModel):
    """Abstract definition of a skill (e.g., 'WebSearch'). Maps to kernel tools."""

    name: str
    description: str
    protocol: str = "mcp"
    config_template: Dict[str, Any] = Field(default_factory=dict)


class Domain(BaseModel):
    """
    A knowledge domain (e.g., 'Finance', 'DevOps').
    Provides vocabularies, tools, and memory stores.
    """

    name: str
    description: str
    capabilities: List[Capability] = Field(default_factory=list)
    system_prompt_mixin: str = ""  # Injected into routers


class Role(BaseModel):
    """
    An Agent archetype (e.g., 'SeniorResearcher').
    Defines the base behavior loop (Graph) and decision style (Router).
    """

    name: str
    base_template: str  # e.g. "planning_loop", "react_loop"
    system_prompt_template: str
    default_capabilities: List[str] = Field(default_factory=list)


class GovernanceRule(BaseModel):
    """A specific policy rule (e.g., 'No Delete')."""

    name: str
    target_pattern: str  # Regex or glob
    action: str  # "deny", "require_approval"
    conditions: Dict[str, Any] = Field(default_factory=dict)


class FabricSpec(BaseModel):
    """A composite definition used to build a specific agent."""

    role: Role
    domains: List[Domain]
    governance: List[GovernanceRule]
    name: str


__all__ = [
    "Capability",
    "Domain",
    "Role",
    "GovernanceRule",
    "FabricSpec",
]

