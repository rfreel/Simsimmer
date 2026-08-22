# Simsimmer

A simulator-first Karpathy-style autoresearch harness for compounding search policies.

The fixed simulator models the loop:

`SEARCH → SOLVE → VERIFY → TRACE → GENERALIZE → COMPILE/REUSE → TRANSFER → REDISCOVER → ABLATE → COMPRESS → SEARCH FARTHER`

The candidate is a small policy vector. Each experiment mutates exactly one parameter, evaluates it on fixed research seeds plus a shifted holdout, keeps only accepted mutations, and records a receipt. The evaluator is hash-locked so ordinary research cannot silently change the target.

## Run

```bash
python -m unittest discover -s tests -v
python autoresearch.py --variant explore --iterations 24 --seed 1
python autoresearch.py --variant exploit --iterations 24 --seed 2 --write
python autoresearch.py --variant transfer --iterations 24 --seed 3 --write
python autoresearch.py --variant compress --iterations 24 --seed 4 --write
```

Variants are intentionally nonredundant:

- `explore`: search breadth, novelty, and new basins.
- `exploit`: local improvement around the champion.
- `transfer`: out-of-distribution transfer and rediscovery.
- `compress`: ablation and basis compression under a non-regression gate.

`state/champion.json` is the cross-variant ratchet. `state/results.jsonl` is the experiment ledger.

## Reuse for another domain

Keep the JSON policy/receipt contract and replace `sim/simulator.py` with the domain simulator in a separately reviewed evaluator change. Then regenerate `evaluator.lock.json`. Do not let the same autoresearch loop mutate both candidate and evaluator.
