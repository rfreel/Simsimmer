from __future__ import annotations

import argparse
import hashlib
import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Tuple

from tools.statecharts.research import ResearchLifecycle

from sim.simulator import BASELINE_POLICY, PARAM_BOUNDS, aggregate, metrics_dict, normalize_policy

ROOT = Path(__file__).resolve().parent
LOCK = ROOT / "evaluator.lock.json"
SIM = ROOT / "sim" / "simulator.py"
STATE_DIR = ROOT / "state"
RESULTS = STATE_DIR / "results.jsonl"
RESEARCH_SEEDS = [101, 211, 307, 401]
HOLDOUT_SEEDS = [1009, 1103, 1201, 1301]
CANONICAL_SEEDS = [2003, 2011, 2027, 2039]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_lock() -> None:
    lock = json.loads(LOCK.read_text())
    got = sha256(SIM)
    if got != lock["simulator_sha256"]:
        raise SystemExit(f"evaluator lock mismatch: expected {lock['simulator_sha256']} got {got}")
    if lock.get("research_seeds") != RESEARCH_SEEDS or lock.get("holdout_seeds") != HOLDOUT_SEEDS or lock.get("canonical_seeds") != CANONICAL_SEEDS:
        raise SystemExit("evaluator seed lock mismatch")


def load_variant(name: str) -> dict:
    return json.loads((ROOT / "variants" / f"{name}.json").read_text())


def state_path(name: str) -> Path:
    return STATE_DIR / f"{name}.json"


def load_policy(name: str) -> Dict[str, float]:
    # Every variant starts from the shared ratchet. Variant state is a receipt, not a private lineage.
    champion = STATE_DIR / "champion.json"
    if champion.exists():
        return normalize_policy(json.loads(champion.read_text())["policy"])
    return normalize_policy(BASELINE_POLICY)


def objective(metrics, variant: dict) -> float:
    score = metrics.fitness
    w = variant.get("objective_weights", {})
    score += w.get("solved_rate", 0.0) * metrics.solved_rate
    score += w.get("transfer_rate", 0.0) * metrics.transfer_rate
    score += w.get("rediscovery_rate", 0.0) * metrics.rediscovery_rate
    score -= w.get("compute_per_task", 0.0) * metrics.compute_per_task
    score -= w.get("active_basis", 0.0) * metrics.active_basis
    return score


def mutate(policy: Dict[str, float], variant: dict, rng: random.Random) -> Tuple[Dict[str, float], str]:
    allowed = variant.get("parameters", list(PARAM_BOUNDS))
    key = rng.choice(allowed)
    steps = variant.get("steps", {}).get(key, [-0.1, 0.1])
    delta = rng.choice(steps)
    candidate = dict(policy)
    candidate[key] = candidate[key] + delta
    candidate = normalize_policy(candidate)
    return candidate, f"{key}{delta:+g}"


def evaluate(policy: Dict[str, float], variant: dict):
    train = aggregate(policy, RESEARCH_SEEDS, n_tasks=variant.get("n_tasks", 256), shift=0.0)
    holdout = aggregate(policy, HOLDOUT_SEEDS, n_tasks=variant.get("n_tasks", 256), shift=variant.get("holdout_shift", 0.25))
    return train, holdout


def canonical_evaluate(policy: Dict[str, float]):
    return aggregate(policy, CANONICAL_SEEDS, n_tasks=384, shift=0.35)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=["explore", "exploit", "transfer", "compress"], required=True)
    ap.add_argument("--iterations", type=int, default=24)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    return run(args)


def run(args, lifecycle: ResearchLifecycle | None = None) -> int:
    """Execute one run; an injected lifecycle exposes evidence to controller tests."""
    lifecycle = lifecycle or ResearchLifecycle()
    try:
        return _run(args, lifecycle)
    except (Exception, SystemExit):
        lifecycle.fail()
        raise


def _run(args, lifecycle: ResearchLifecycle) -> int:
    lifecycle.send("start")
    check_lock()
    lifecycle.send("lock_valid")
    variant = load_variant(args.variant)
    rng = random.Random(args.seed or int(datetime.now(timezone.utc).strftime("%Y%m%d")))
    current = load_policy(args.variant)
    train, holdout = evaluate(current, variant)
    current_score = objective(train, variant)
    current_holdout = objective(holdout, variant)
    baseline_holdout = current_holdout

    lifecycle.send("baseline_evaluated")
    rows = []
    keeps = 0
    for i in range(1, args.iterations + 1):
        lifecycle.send("candidate_started")
        cand, hypothesis = mutate(current, variant, rng)
        c_train, c_holdout = evaluate(cand, variant)
        c_score = objective(c_train, variant)
        c_holdout_score = objective(c_holdout, variant)

        train_gain = c_score - current_score
        holdout_delta = c_holdout_score - current_holdout
        floor = variant.get("holdout_regression_floor", -0.05)
        keep = train_gain > variant.get("min_gain", 1e-9) and holdout_delta >= floor

        if args.variant == "compress":
            smaller = c_holdout.active_basis < holdout.active_basis - 1e-9
            nonregress = c_holdout_score >= current_holdout - variant.get("compression_score_tolerance", 0.05)
            keep = keep or (smaller and nonregress)

        lifecycle.send("keep" if keep else "reject", **({"accepted": keep} if keep else {"rejected": not keep}))
        rows.append({
            "iteration": i,
            "hypothesis": hypothesis,
            "status": "KEEP" if keep else "REJECT",
            "train_score": round(c_score, 8),
            "holdout_score": round(c_holdout_score, 8),
            "train_gain": round(train_gain, 8),
            "holdout_delta": round(holdout_delta, 8),
        })
        if keep:
            current, train, holdout = cand, c_train, c_holdout
            current_score, current_holdout = c_score, c_holdout_score
            keeps += 1

    lifecycle.send("trials_finished")
    canonical = canonical_evaluate(current)
    lifecycle.send("canonical_evaluated")
    receipt = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "variant": args.variant,
        "iterations": args.iterations,
        "keeps": keeps,
        "evaluator_sha256": sha256(SIM),
        "policy": current,
        "train": metrics_dict(train),
        "holdout": metrics_dict(holdout),
        "objective_train": round(current_score, 8),
        "objective_holdout": round(current_holdout, 8),
        "initial_holdout_objective": round(baseline_holdout, 8),
        "canonical_holdout": metrics_dict(canonical),
        "canonical_holdout_fitness": round(canonical.fitness, 8),
        "trials": rows,
    }

    print(json.dumps(receipt, indent=2, sort_keys=True))

    if args.write:
        lifecycle.send("write_requested", write_enabled=args.write)
        STATE_DIR.mkdir(exist_ok=True)
        state_path(args.variant).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
        with RESULTS.open("a", encoding="utf-8") as f:
            f.write(json.dumps({k: receipt[k] for k in receipt if k != "trials"}, sort_keys=True) + "\n")

        lifecycle.send("receipts_written")
        champion_path = STATE_DIR / "champion.json"
        old_score = float("-inf")
        old_basis = float("inf")
        if champion_path.exists():
            old = json.loads(champion_path.read_text())
            old_score = old.get("canonical_holdout_fitness", old_score)
            old_basis = old.get("canonical_holdout", {}).get("active_basis", old_basis)
        better = canonical.fitness > old_score + 1e-9
        tie_but_smaller = abs(canonical.fitness - old_score) <= 1e-9 and canonical.active_basis < old_basis - 1e-9
        if better or tie_but_smaller:
            lifecycle.send("promote", promotable=better or tie_but_smaller)
            champion_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
            lifecycle.send("champion_written")
        else:
            lifecycle.send("retain", not_promotable=not (better or tie_but_smaller))
    else:
        lifecycle.send("dry_run", dry_run=not args.write)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
