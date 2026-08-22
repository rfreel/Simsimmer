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

The existing deterministic autoresearch harness remains the current executable evaluator. It hash-locks its simulator and seed sets, evaluates research/shifted holdout/canonical seeds, and persists accepted research state separately from the trusted evaluator.

## Contained autoresearch
Scheduled autoresearch runs on `autoresearch/ratchet`, syncs reviewed code from `main`, and fails if the job changes anything outside `state/**`. `main` is the promotion surface, not the scheduled worker's scratch branch.

## Architecture search
`tools/simulate_flywheel_architecture.py` exhaustively enumerates the declared 10-role × 4-mode architecture space (1,048,576 configurations). Its result is synthetic design evidence, not empirical proof. Under the current bootstrap complexity cap it selects hybrid task graph, routing, coordination, memory, QA, specification-basis, and trace-compiler roles while deferring lifecycle management, security adapters, and remote execution; the long-term frontier selects hybrid adapters across all ten roles. Repository-native canonical state remains authoritative in every stateful hybrid role.

## External structural reference
The Doodlestein flywheel is pinned as an advisory reference at `Dicklesworthstone/agentic_coding_flywheel_setup@6c9e68a918375e4717d452fc643480c3110a232d`. Simsimmer borrows manifest-driven setup, planning-first work, task graphs, routing, coordination, memory, and QA feedback while retaining its own simulation/promotion authority.

## Run
```bash
python scripts/doctor.py
python -m unittest discover -s tests -v
python autoresearch.py --variant explore --iterations 24 --seed 1
python tools/simulate_flywheel_architecture.py
python decompose-task-space/spec/simulate_spec_basis.py --limit 128
```

A passing command is evidence, not a claim of global correctness. See the repository distinction contract for status and authority semantics.
