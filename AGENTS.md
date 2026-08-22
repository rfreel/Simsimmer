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
