from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import dataclass, asdict
from typing import Dict, Iterable, List

PARAM_BOUNDS = {
    "search_breadth": (1.0, 10.0),
    "search_depth": (1.0, 10.0),
    "verify_rate": (0.0, 1.0),
    "trace_rate": (0.0, 1.0),
    "reuse_threshold": (1.0, 8.0),
    "generalize_strength": (0.0, 1.0),
    "transfer_weight": (0.0, 1.0),
    "rediscover_weight": (0.0, 1.0),
    "ablate_rate": (0.0, 1.0),
    "compression_rate": (0.0, 1.0),
    "active_basis_cap": (4.0, 64.0),
    "novelty_budget": (0.0, 1.0),
}

INTEGER_PARAMS = {"search_breadth", "search_depth", "reuse_threshold", "active_basis_cap"}

BASELINE_POLICY = {
    "search_breadth": 4,
    "search_depth": 4,
    "verify_rate": 0.55,
    "trace_rate": 0.55,
    "reuse_threshold": 3,
    "generalize_strength": 0.45,
    "transfer_weight": 0.35,
    "rediscover_weight": 0.25,
    "ablate_rate": 0.20,
    "compression_rate": 0.35,
    "active_basis_cap": 24,
    "novelty_budget": 0.35,
}

@dataclass(frozen=True)
class Task:
    difficulty: float
    branching: float
    depth: float
    reusable: float
    novelty: float
    noise: float

@dataclass
class Metrics:
    solved_rate: float
    compute_per_task: float
    compute_per_solve: float
    reusable_yield: float
    transfer_rate: float
    verification_precision: float
    active_basis: float
    rediscovery_rate: float
    fitness: float


def normalize_policy(policy: Dict[str, float]) -> Dict[str, float]:
    out: Dict[str, float] = {}
    for key, (lo, hi) in PARAM_BOUNDS.items():
        value = float(policy.get(key, BASELINE_POLICY[key]))
        value = min(hi, max(lo, value))
        if key in INTEGER_PARAMS:
            value = int(round(value))
        out[key] = value
    return out


def _policy_seed(policy: Dict[str, float], seed: int) -> int:
    payload = json.dumps(normalize_policy(policy), sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(f"{seed}:{payload}".encode()).digest()
    return int.from_bytes(digest[:8], "big")


def make_tasks(seed: int, n: int, shift: float = 0.0) -> List[Task]:
    rng = random.Random(seed)
    tasks: List[Task] = []
    for _ in range(n):
        difficulty = min(1.0, max(0.0, rng.betavariate(2.2 + shift, 2.4)))
        branching = min(1.0, max(0.0, rng.betavariate(2.0, 2.0 + 0.5 * shift)))
        depth = min(1.0, max(0.0, rng.betavariate(2.1 + 0.4 * shift, 2.2)))
        reusable = rng.betavariate(1.7, 2.2)
        novelty = min(1.0, max(0.0, rng.betavariate(1.8 + shift, 2.0)))
        noise = rng.betavariate(1.5, 4.0)
        tasks.append(Task(difficulty, branching, depth, reusable, novelty, noise))
    return tasks


def evaluate_policy(policy: Dict[str, float], *, seed: int, n_tasks: int = 256, shift: float = 0.0) -> Metrics:
    p = normalize_policy(policy)
    tasks = make_tasks(seed, n_tasks, shift)
    rng = random.Random(_policy_seed(p, seed))

    solved = 0
    total_compute = 0.0
    reusable_yield = 0.0
    transfer_hits = 0.0
    verified_good = 0.0
    verified_total = 0.0
    rediscovered = 0.0
    basis = 0.0

    breadth = p["search_breadth"] / 10.0
    depth = p["search_depth"] / 10.0

    for t in tasks:
        search_fit = 0.52 * breadth * (1.0 - 0.55 * t.branching) + 0.48 * depth * (1.0 - 0.50 * t.depth)
        novelty_fit = p["novelty_budget"] * t.novelty
        reuse_gain = min(1.0, basis / max(1.0, p["active_basis_cap"])) * (1.0 - t.novelty) * 0.30
        transfer_gain = p["transfer_weight"] * reusable_yield / max(1.0, len(tasks)) * 0.18
        raw = 1.75 * (search_fit + 0.35 * novelty_fit + reuse_gain + transfer_gain - 0.72 * t.difficulty)
        solve_prob = 1.0 / (1.0 + math.exp(-raw))
        solved_now = rng.random() < solve_prob

        compute = 1.0 + 1.9 * breadth + 1.7 * depth + 0.45 * p["verify_rate"] + 0.35 * p["trace_rate"]
        compute += 0.25 * p["novelty_budget"] + 0.12 * basis / max(1.0, p["active_basis_cap"])
        total_compute += compute

        if not solved_now:
            continue
        solved += 1

        truth = rng.random() > (0.06 + 0.24 * t.noise)
        if rng.random() < p["verify_rate"]:
            verified_total += 1
            detection = 0.70 + 0.28 * p["verify_rate"]
            verified_good += 1 if truth or rng.random() < detection else 0
        else:
            verified_good += 0.35 if truth else 0.0

        traced = rng.random() < p["trace_rate"]
        if traced:
            generalizable = t.reusable * p["generalize_strength"] * (1.0 - 0.45 * t.noise)
            if generalizable * 8.0 >= p["reuse_threshold"]:
                candidate = generalizable * (0.7 + 0.3 * p["rediscover_weight"])
                rediscovery_prob = min(1.0, p["rediscover_weight"] * (0.25 + 0.75 * t.reusable))
                if rng.random() < rediscovery_prob:
                    rediscovered += 1
                    candidate *= 1.15
                if rng.random() < p["ablate_rate"]:
                    candidate *= 0.75 + 0.25 * truth
                reusable_yield += candidate
                basis += candidate

        compression = p["compression_rate"] * (0.12 + 0.18 * p["ablate_rate"])
        basis *= max(0.0, 1.0 - compression / max(1.0, n_tasks / 32.0))
        basis = min(float(p["active_basis_cap"]), basis)
        transfer_hits += min(1.0, p["transfer_weight"] * t.reusable * (0.4 + reusable_yield / max(1.0, solved)))

    solved_rate = solved / n_tasks
    compute_per_task = total_compute / n_tasks
    compute_per_solve = total_compute / max(1, solved)
    transfer_rate = transfer_hits / max(1, solved)
    verification_precision = verified_good / max(1.0, verified_total + (solved - verified_total) * 0.35)
    rediscovery_rate = rediscovered / max(1, solved)

    fitness = (
        100.0 * solved_rate
        + 18.0 * transfer_rate
        + 10.0 * verification_precision
        + 6.0 * min(1.0, reusable_yield / max(1.0, solved))
        + 4.0 * rediscovery_rate
        - 5.5 * compute_per_task
        - 0.12 * basis
    )

    return Metrics(
        solved_rate=solved_rate,
        compute_per_task=compute_per_task,
        compute_per_solve=compute_per_solve,
        reusable_yield=reusable_yield,
        transfer_rate=transfer_rate,
        verification_precision=verification_precision,
        active_basis=basis,
        rediscovery_rate=rediscovery_rate,
        fitness=fitness,
    )


def aggregate(policy: Dict[str, float], seeds: Iterable[int], *, n_tasks: int = 256, shift: float = 0.0) -> Metrics:
    rows = [evaluate_policy(policy, seed=s, n_tasks=n_tasks, shift=shift) for s in seeds]
    keys = Metrics.__dataclass_fields__.keys()
    vals = {k: sum(getattr(r, k) for r in rows) / len(rows) for k in keys}
    return Metrics(**vals)


def metrics_dict(m: Metrics) -> Dict[str, float]:
    return {k: round(v, 8) for k, v in asdict(m).items()}
