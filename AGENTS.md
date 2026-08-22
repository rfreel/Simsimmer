# Simsimmer agent contract

The simulator is the evaluator. Do not optimize by editing the evaluator, its frozen seeds, or evaluator lock during an experiment.

Research loop:
1. Read `state/champion.json` if present, otherwise `state/baseline.json`.
2. Pick exactly one hypothesis/mutation.
3. Run it through `autoresearch.py` against research seeds and the shifted frozen holdout.
4. KEEP only when the variant gate accepts it; otherwise REJECT and preserve the champion.
5. Record receipts. Never convert a failing evaluator into a passing one by weakening tests or changing the simulator.
6. Periodically run transfer, rediscovery, ablation, and compression variants so the active basis cannot grow without pressure.

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
