"""
universal_agent_fabric.cli

Command line interface to build and enrich agents.

Usage:
  # Build from scratch
  fabric build --role researcher.yaml --domain finance.yaml --out agent.yaml

  # Enrich baseline from Nexus
  fabric enrich baseline.yaml --role researcher.yaml --domain finance.yaml --out production.yaml
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
from .enricher import NexusEnricher
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


def cmd_build(args: argparse.Namespace) -> None:
    """Build agent from scratch using Fabric fragments."""
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

    print(f"🔨 Building Agent: {spec.name}...")
    print(f"  Role: {role.name}")
    print(f"  Domains: {[d.name for d in domains]}")

    builder = FabricBuilder(spec)
    manifest = builder.build()

    with open(args.out, "w", encoding="utf-8") as handle:
        yaml.safe_dump(manifest, handle, sort_keys=False)

    print(f"✅ Build Complete: {args.out}")


def cmd_enrich(args: argparse.Namespace) -> None:
    """
    Enrich baseline UAA manifest from Nexus with Fabric fragments.

    This is the SECOND step in the Nexus → Fabric → Agent pipeline.
    """
    if load_dotenv:
        load_dotenv()

    print(f"📥 Enriching baseline manifest: {args.baseline}")

    if args.role:
        print(f"  Role: {args.role}")
    if args.domain:
        print(f"  Domains: {args.domain}")
    if args.policy:
        print(f"  Policies: {args.policy}")
    if args.mixin:
        print(f"  Mixins: {args.mixin}")

    try:
        enricher = NexusEnricher()
        output = enricher.enrich(
            baseline_manifest_path=args.baseline,
            role_path=args.role,
            domain_paths=args.domain or [],
            policy_paths=args.policy or [],
            mixin_paths=args.mixin or [],
            output_path=args.out,
        )

        print(f"✅ Enriched manifest: {output}")
        print("")
        print("Next steps:")
        print(f"  Run with Agent:")
        print(f"    python -m universal_agent.runtime {output}")

    except Exception as exc:
        print(f"❌ Enrichment failed: {exc}")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Universal Agent Fabric - Composition & Governance Layer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build agent from scratch
  fabric build --role manifests/roles/researcher.yaml \\
               --domain ontology/domains/finance.yaml \\
               --policy policy/rules/safety.yaml \\
               --out agent.yaml

  # Enrich baseline from Nexus
  fabric enrich baseline.yaml \\
         --role manifests/roles/researcher.yaml \\
         --domain ontology/domains/finance.yaml \\
         --policy policy/rules/safety.yaml \\
         --out production_ready.yaml

Pipeline:
  Nexus (translate) → Fabric (enrich) → Agent (execute)
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # BUILD command (original functionality)
    build_parser = subparsers.add_parser(
        "build", help="Build agent from scratch using Fabric fragments"
    )
    build_parser.add_argument("--role", required=True, help="Path to Role YAML")
    build_parser.add_argument(
        "--domain", action="append", help="Path to Domain YAML (can repeat)"
    )
    build_parser.add_argument(
        "--policy", action="append", help="Path to Policy YAML (can repeat)"
    )
    build_parser.add_argument(
        "--name", default="generated-agent", help="Name of the resulting agent"
    )
    build_parser.add_argument("--out", default="manifest.yaml", help="Output path")
    build_parser.set_defaults(func=cmd_build)

    # ENRICH command (new - for Nexus integration)
    enrich_parser = subparsers.add_parser(
        "enrich", help="Enrich baseline UAA manifest from Nexus"
    )
    enrich_parser.add_argument("baseline", help="Path to baseline UAA manifest (from Nexus)")
    enrich_parser.add_argument("--role", help="Path to Role YAML")
    enrich_parser.add_argument(
        "--domain", action="append", help="Path to Domain YAML (can repeat)"
    )
    enrich_parser.add_argument(
        "--policy", action="append", help="Path to Policy YAML (can repeat)"
    )
    enrich_parser.add_argument(
        "--mixin", action="append", help="Path to Mixin YAML (observability, safety)"
    )
    enrich_parser.add_argument(
        "--out", default="enriched_manifest.yaml", help="Output path"
    )
    enrich_parser.set_defaults(func=cmd_enrich)

    args = parser.parse_args()

    # Handle no command (backward compatibility - default to build-like behavior)
    if not args.command:
        # Check if old-style arguments provided
        if hasattr(args, "role") and args.role:
            cmd_build(args)
        else:
            parser.print_help()
            sys.exit(1)
    else:
        args.func(args)


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    main()
