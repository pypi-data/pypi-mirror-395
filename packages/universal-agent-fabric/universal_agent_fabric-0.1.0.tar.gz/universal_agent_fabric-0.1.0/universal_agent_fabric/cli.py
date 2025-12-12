"""
universal_agent_fabric.cli

Command line interface to build agents.
Usage:
  python -m universal_agent_fabric.cli --role researcher.yaml --domain finance.yaml --out agent.yaml
"""

import argparse
import sys
from pathlib import Path
from typing import Any, List

import yaml

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None

from .builder import FabricBuilder
from .schemas import Domain, FabricSpec, GovernanceRule, Role


def load_yaml(path: str) -> Any:
    return yaml.safe_load(Path(path).read_text())


def _load_policies(policy_paths: List[str]) -> List[GovernanceRule]:
    governance: List[GovernanceRule] = []
    for p in policy_paths:
        rules = load_yaml(p)
        if isinstance(rules, dict):
            rules = rules.get("rules", [])
        for r in rules or []:
            governance.append(GovernanceRule(**r))
    return governance


def main() -> None:
    parser = argparse.ArgumentParser(description="Universal Agent Fabric Compiler")
    parser.add_argument("--role", required=True, help="Path to Role YAML")
    parser.add_argument(
        "--domain", action="append", help="Path to Domain YAML (can repeat)"
    )
    parser.add_argument(
        "--policy", action="append", help="Path to Policy YAML (can repeat)"
    )
    parser.add_argument(
        "--name", default="generated-agent", help="Name of the resulting agent"
    )
    parser.add_argument("--out", default="manifest.yaml", help="Output path")

    args = parser.parse_args()

    if load_dotenv:
        load_dotenv()

    try:
        role_data = load_yaml(args.role)
        role = Role(**role_data)

        domains = []
        for d in args.domain or []:
            domains.append(Domain(**load_yaml(d)))

        governance = _load_policies(args.policy or [])

    except Exception as exc:  # pragma: no cover - CLI convenience
        print(f"❌ Error loading components: {exc}")
        sys.exit(1)

    spec = FabricSpec(
        name=args.name,
        role=role,
        domains=domains,
        governance=governance,
    )

    print(f"Compiling Agent: {spec.name}...")
    print(f"  Role: {role.name}")
    print(f"  Domains: {[d.name for d in domains]}")

    builder = FabricBuilder(spec)
    manifest = builder.build()

    with open(args.out, "w", encoding="utf-8") as handle:
        yaml.safe_dump(manifest, handle, sort_keys=False)

    print(f"Build Complete: {args.out}")


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    main()

