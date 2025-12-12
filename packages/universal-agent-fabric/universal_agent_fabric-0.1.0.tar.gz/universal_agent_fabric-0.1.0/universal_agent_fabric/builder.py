"""
universal_agent_fabric.builder

Compiler logic that merges Roles, Domains, and Policies into a kernel-compatible
manifest structure.
"""

from typing import Any, Dict, List, Optional

from .schemas import Domain, FabricSpec, GovernanceRule, Role

# Kernel manifest representation (dict form for YAML serialization)
KernelManifest = Dict[str, Any]


class FabricBuilder:
    def __init__(self, spec: FabricSpec):
        self.spec = spec
        self._manifest: KernelManifest = {
            "name": spec.name,
            "version": "1.0.0",
            "graphs": [],
            "routers": [],
            "tools": [],
            "policies": [],
            "metadata": {
                "tags": ["fabric-generated"],
                "extra": {
                    "generated_by": "universal_agent_fabric",
                    "role": spec.role.name,
                    "domains": [d.name for d in spec.domains],
                },
            },
        }

    def build(self) -> KernelManifest:
        """Execute the compilation pipeline."""
        self._compile_policies()
        self._compile_tools()
        self._compile_routers()
        self._compile_graph()
        return self._manifest

    def _compile_tools(self) -> None:
        """Aggregate capabilities from domains into tools."""
        capabilities = []
        for domain in self.spec.domains:
            capabilities.extend(domain.capabilities)

        for cap in capabilities:
            tool_spec = {
                "name": cap.name,
                "description": cap.description,
                "protocol": cap.protocol,
                "config": cap.config_template,
            }

            policy_ref = self._find_matching_policy(cap.name)
            if policy_ref:
                tool_spec["policy"] = {"name": policy_ref}

            self._manifest["tools"].append(tool_spec)

    def _compile_policies(self) -> None:
        """Convert governance rules into kernel policies."""
        if not self.spec.governance:
            return

        policy_spec = {"name": "fabric-governance", "rules": []}
        for rule in self.spec.governance:
            policy_spec["rules"].append(
                {
                    "description": rule.name,
                    "target": [rule.target_pattern],
                    "action": rule.action,
                    "conditions": rule.conditions,
                }
            )

        self._manifest["policies"].append(policy_spec)

    def _compile_routers(self) -> None:
        """Build router spec, mixing in domain prompts."""
        domain_prompts = "\n".join([d.system_prompt_mixin for d in self.spec.domains])
        final_prompt = f"{self.spec.role.system_prompt_template}\n\nDOMAIN KNOWLEDGE:\n{domain_prompts}"

        router_spec = {
            "name": "primary-router",
            "strategy": "llm",
            "system_message": final_prompt,
            "model_candidates": ["gpt-4o"],
        }

        if self._manifest["policies"]:
            router_spec["policy"] = "fabric-governance"

        self._manifest["routers"].append(router_spec)

    def _compile_graph(self) -> None:
        """
        Instantiate the requested graph template (e.g. 'planning_loop').
        In a full implementation, this would load from manifests/graphs/.
        Here we generate a minimal ReAct-style loop.
        """
        template = self.spec.role.base_template
        # Basic template selection hook for future expansion
        graph_name = template or "default_loop"

        graph_spec = {
            "name": "main",
            "version": "1.0.0",
            "entry_node": "start",
            "nodes": [
                {"id": "start", "kind": "router", "router": {"name": "primary-router"}},
                {
                    "id": "tool_exec",
                    "kind": "tool",
                    # In a real graph the tool would be chosen dynamically; keep placeholder.
                    "tool": {"name": "dynamic_placeholder"},
                },
            ],
            "edges": [],
            "metadata": {
                "tags": [],
                "extra": {"template": graph_name},
            },
        }
        self._manifest["graphs"].append(graph_spec)

    def _find_matching_policy(self, target_name: str) -> Optional[str]:
        """Check if any governance rule targets this capability name."""
        for rule in self.spec.governance:
            if rule.target_pattern == "*" or rule.target_pattern in target_name:
                return "fabric-governance"
        return None

