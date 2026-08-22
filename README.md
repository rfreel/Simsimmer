# Simsimmer

A simulator-first autoresearch and software-engineering flywheel.

Canonical loop:

`SIMULATE → SELECT → GENERATE → EXECUTE → VERIFY → ACCRETE → RELATE → GENERALIZE → COMPILE/REUSE → TRANSFER → REDISCOVER → ABLATE → RE-DERIVE → COMPRESS → SEARCH FARTHER`

Start here:
1. `PROJECT_INTENT.md` — mission, scope, objective, authority.
2. `AGENTS.md` — agent operating contract and write boundaries.
3. `control/repository.manifest.json` — machine-readable source-of-truth topology.
4. `docs/OWNERSHIP.md` — multi-agent collision avoidance.
5. `docs/research/REPOSITORY_DISTINCTIONS.md` — repository distinction taxonomy.
6. `docs/architecture/FLYWHEEL.md` — compounding architecture.
7. `decompose-task-space/spec/` — domain-agnostic specification distinction basis and extension protocol.
8. `experiments/decomposition-policy/` — imported same-root decomposition-policy simulation and reproducible 106-bead candidate graph.

The existing deterministic autoresearch harness remains the current executable evaluator. It hash-locks its simulator and seed sets, evaluates research/shifted holdout/canonical seeds, and persists accepted research state separately from the trusted evaluator.

## Contained autoresearch
Scheduled autoresearch runs on `autoresearch/ratchet`, syncs reviewed code from `main`, and fails if the job changes anything outside `state/**`. `main` is the promotion surface, not the scheduled worker's scratch branch.

## Architecture search
`tools/simulate_flywheel_architecture.py` exhaustively enumerates the declared 10-role × 4-mode architecture space (1,048,576 configurations). Its result is synthetic design evidence, not empirical proof. The bootstrap frontier is limited to seven active roles and preserves repository-native state/authority; the long-term frontier favors repository-native canonical state plus replaceable hybrid adapters across all ten roles.

## Dependency-atomic work graph
A prior same-root `immutable-context-sim 1.1.0` run compared six decomposition policies. `dependency_atomic` ranked first in all five objective regimes. The imported candidate graph contains 106 beads, is acyclic, has a unit-weight critical path of 57, carries 10 global acceptance gates, and begins at `RG-P0-01`. It remains **backlog planning evidence** until explicitly promoted to active work.

The decomposition rule is: one decision, mutation boundary, or independently verifiable outcome per bead. Discovery → decision → implementation → verification → promotion are separated whenever authority, evidence, or rollback changes.

## External structural reference
The Doodlestein flywheel is pinned as an advisory reference at `Dicklesworthstone/agentic_coding_flywheel_setup@6c9e68a918375e4717d452fc643480c3110a232d`. Simsimmer borrows manifest-driven setup, planning-first work, task graphs, routing, coordination, memory, and QA feedback while retaining its own simulation/promotion authority.

## Run
```bash
python scripts/doctor.py
python -m unittest discover -s tests -v
python autoresearch.py --variant explore --iterations 24 --seed 1
python tools/simulate_flywheel_architecture.py
python decompose-task-space/spec/simulate_spec_basis.py --limit 128
python experiments/decomposition-policy/verify_decomposition_beads.py
```

A passing command is evidence, not a claim of global correctness. See the repository distinction contract for status and authority semantics.
