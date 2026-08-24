# Simsimmer agent contract

The simulator is the evaluator. Do not optimize by editing the evaluator, its frozen seeds, or evaluator lock during an ordinary experiment.

## Non-negotiable workflow

1. **Simulate before generating.** Freeze target, constraints, evidence, and success tests; run rival simulations before code generation.
2. **Same-root rivals.** Competing candidates must share the same immutable root unless the experiment explicitly changes the root.
3. **Execute after selection.** Generate only selected candidates, run real compilers/tests/benchmarks, and feed receipts back into the simulator.
4. **Fail closed.** A failing verifier, infrastructure error, stale root, or provenance mismatch is not an ordinary candidate rejection and must not be converted into success.
5. **Accrete carefully.** Promote only verified compatible deltas. Preserve failures, counterexamples, residuals, and rollback information.
6. **Compile learning.** Relate traces, generalize repeated substructure, transfer/rediscover, ablate, re-derive, and compress the active basis.

## Write zones

Read `docs/OWNERSHIP.md` before writing. The short form:

- `state/**`: scheduled autoresearch lane only. Canonical scheduled writer is branch `autoresearch/ratchet`.
- `sim/**`, `tests/**`, `evaluator.lock.json`: trusted evaluator surface. Change only in a separately scoped evaluator-change branch with explicit verification.
- `variants/**`, `autoresearch.py`: research-controller surface. Do not change in the same experiment that evaluates a candidate policy.
- `vendor/**`: immutable/pinned upstream source. Never opportunistically edit vendored code.
- `control/**`, `docs/**`, `scripts/**`, `tools/**`, `agents/**`, `experiments/**`: project operating layer. Use task-scoped branches and avoid overlapping write ownership.
- `generated/**`, `artifacts/**`, `traces/raw/**`: derived outputs. Do not treat as canonical source; large/raw outputs should normally stay out of Git.

## Branches

- `main`: reviewed/promoted canonical project state.
- `autoresearch/ratchet`: contained scheduled state evolution; may write only `state/**` after syncing reviewed code from `main`.
- `agent/<task>`: implementation/research branches for human or agent work.
- `exp/<experiment-id>`: optional isolated experiment branches when generated code needs a Git surface.

Never use `main` as a scratch branch. Never let two agents own the same write surface at the same time.

## Research loop

1. Read `state/champion.json` if present, otherwise `state/baseline.json`.
2. Pick exactly one hypothesis/mutation unless the experiment contract explicitly defines a population.
3. Run it through `autoresearch.py` against research seeds and the shifted frozen holdout.
4. KEEP only when the fixed gate accepts it; otherwise REJECT and preserve the champion.
5. Record receipts. Never make a failing evaluator pass by weakening tests, changing seeds, or editing the simulator.
6. Periodically run transfer, rediscovery, ablation, and compression so the active basis cannot grow without pressure.

## Agent coordination

Before changing files, declare a task ID and intended write zone in the task/experiment record. Prefer disjoint file ownership. If another live agent owns the same surface, switch to a different task or create an isolated branch/worktree; do not race edits.

Mutable research state: `state/*.json`, `state/results.jsonl`.
Fixed substrate unless a separately reviewed evaluator-change task explicitly says otherwise: `sim/`, `tests/`, `evaluator.lock.json`.

## Agent Mail coordination

When work becomes multi-agent or two agents could touch overlapping files, use the pinned Agent Mail integration in `coordination/`.

- Canonical pin: `coordination/agent-mail.lock.json`.
- Bootstrap: `bash coordination/install-agent-mail.sh`.
- Operating protocol: `coordination/AGENT_MAIL.md`.
- Do not silently use Agent Mail `main` or auto-upgrade during a research run.
- Agent Mail owns coordination state only: identities, threads, acknowledgements, and advisory file reservations.
- Agent Mail does **not** decide bead readiness, bead closure, verification, promotion, or evaluator state.
- Use the exact bead ID as the Agent Mail thread ID, e.g. `RG-P0-01`.
- Before mutating shared files, reserve the narrowest practical project-relative paths; default reservation TTL is 3600 seconds and reservations must be explicitly released on completion/handoff when possible.
- A reservation is a coordination lease, not ownership and not a dependency edge.
- A START/HANDOFF/ack message is coordination evidence, not acceptance evidence unless the bead's configured oracle/reviewer explicitly consumes it.
- Preserve failed/retried attempts and handoffs; do not erase coordination history to make a bead look clean.
- The Agent Mail project path is the active Simsimmer checkout. The bead `subject_root` is a separate semantic field and must not be inferred from the Agent Mail project path.

Initial rollout is intentionally narrow: bootstrap and smoke-test Agent Mail on `RG-P0-01` before broader parallel bead execution.
