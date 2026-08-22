from __future__ import annotations

import argparse
import hashlib
import json
import math
from functools import reduce
from operator import mul
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHI_CONJUGATE = (math.sqrt(5.0) - 1.0) / 2.0
CLASSIFICATIONS = ("DERIVED", "NEW_WITNESS", "NEW_COMPOSITION", "CANDIDATE_PRIMITIVE", "REDUNDANT", "RESIDUAL")
AXES = {
    "abstraction_level": ["primitive", "mechanism", "operator", "workflow", "policy", "telos"],
    "whole_part_level": ["local", "part", "component", "subsystem", "system", "global"],
    "epistemic_state": ["observed", "derived", "assumed", "estimated", "predicted", "unknown", "contested", "falsified"],
    "temporal_regime": ["static", "transition", "recurring", "deadline", "lifecycle"],
    "coupling": ["independent", "weakly_coupled", "strongly_coupled"],
    "reversibility": ["reversible", "costly_to_reverse", "irreversible"],
    "verification_regime": ["example", "property", "oracle", "acceptance", "negative", "holdout", "adversarial"],
    "resource_contention": ["none", "bounded", "scarce", "contended"],
    "objective_form": ["constraint", "scalar", "lexicographic", "pareto", "saturation"],
    "representation": ["text", "table", "graph", "state_machine", "logic", "executable"],
}
DEFAULT_DOMAINS = ["generic", "software", "protocol", "data", "operations", "science", "hardware"]


def load_basis(path: Path) -> dict:
    data = json.loads(path.read_text())
    if data.get("schema") != "simsimmer/spec-distinction-basis-v1":
        raise ValueError("unexpected distinction basis schema")
    return data


def distinction_labels(basis: dict) -> list[str]:
    return [f"{axis}::{term}" for axis, terms in basis["distinctions"].items() for term in terms]


def decode(index: int, dimensions: list[tuple[str, list[str]]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, values in reversed(dimensions):
        index, digit = divmod(index, len(values))
        result[key] = values[digit]
    return {key: result[key] for key, _ in dimensions}


def golden_indices(total: int, limit: int, seed: float):
    limit = min(max(0, limit), total)
    seen: set[int] = set()
    k = 0
    while len(seen) < limit:
        idx = int(((seed + k * PHI_CONJUGATE) % 1.0) * total)
        k += 1
        if idx not in seen:
            seen.add(idx)
            yield idx


def schedule(basis: dict, limit: int, seed: float, domains: list[str]) -> tuple[int, list[dict]]:
    dimensions = [("spec_distinction", distinction_labels(basis))]
    dimensions.extend((key, list(values)) for key, values in AXES.items())
    dimensions.append(("domain_specialization", domains))
    total = reduce(mul, (len(v) for _, v in dimensions), 1)
    probes = []
    for ordinal, idx in enumerate(golden_indices(total, limit, seed)):
        coordinate = decode(idx, dimensions)
        canonical = json.dumps(coordinate, sort_keys=True, separators=(",", ":"))
        probes.append({
            "probe_id": hashlib.sha256(canonical.encode()).hexdigest()[:16],
            "ordinal": ordinal,
            "coordinate": coordinate,
            "classification": "RESIDUAL",
            "evidence": [],
            "reason": "scheduled; semantic evaluation pending",
        })
    return total, probes


def ablation_plan(basis: dict) -> list[dict]:
    return [{
        "ablation_id": hashlib.sha256(f"{axis}::{term}".encode()).hexdigest()[:16],
        "remove": f"{axis}::{term}",
        "retain_only_if": "concrete decision/verification/execution/authority/provenance loss is witnessed",
        "status": "RESIDUAL",
    } for axis, terms in basis["distinctions"].items() for term in terms]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--basis", type=Path, default=HERE / "data" / "distinctions.json")
    ap.add_argument("--limit", type=int, default=128)
    ap.add_argument("--seed", type=float, default=0.0)
    ap.add_argument("--domains", default=",".join(DEFAULT_DOMAINS))
    ap.add_argument("--include-ablation-plan", action="store_true")
    args = ap.parse_args()
    domains = [x.strip() for x in args.domains.split(",") if x.strip()]
    if not domains:
        raise SystemExit("at least one domain specialization is required")
    basis = load_basis(args.basis)
    total, probes = schedule(basis, args.limit, args.seed, domains)
    result = {
        "schema": "simsimmer/spec-basis-simulation-v1",
        "method": "golden-angle low-discrepancy traversal over the declared finite product space",
        "bounded_saturation": True,
        "space_size": total,
        "requested_limit": args.limit,
        "seed": args.seed,
        "domains": domains,
        "allowed_classifications": list(CLASSIFICATIONS),
        "probes": probes,
    }
    if args.include_ablation_plan:
        result["ablation_plan"] = ablation_plan(basis)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
