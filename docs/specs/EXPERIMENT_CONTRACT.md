# Experiment Contract

Every Simsimmer experiment freezes its decision-relevant contract before candidate generation or mutation. This specification is subordinate to `PROJECT_INTENT.md`, `control/repository.manifest.json`, and `AGENTS.md`.

## Required fields

Each experiment record must declare:

- `experiment_id` — stable repository-native identifier.
- `root_sha` — immutable repository root used by all same-root rivals.
- `problem` — the residual or capability gap being investigated.
- `objective` — what the experiment is trying to improve or discriminate.
- `scope` — explicit in-scope and out-of-scope surfaces.
- `success_criteria` — observable acceptance conditions frozen before search.
- `stopping_rule` — budget, saturation criterion, failure boundary, or explicit termination condition.
- `budget` — bounded compute, iterations, time, candidates, or other scarce resources.
- `candidate_space` — admissible mutations, policies, implementations, or rival hypotheses.
- `generator` — mechanism that proposes candidates.
- `evaluator` — trusted mechanism that scores or judges candidates.
- `verifiers` — independent checks required beyond the evaluator.
- `seed` — deterministic seed or declared seed policy where stochasticity exists.
- `status` — current lifecycle state.

## Authority separation

The candidate generator may not mutate the frozen success criteria, holdout identity, evaluator identity, evaluator lock, hard resource limits, promotion gate, canonical provenance, or repository authority precedence during an ordinary experiment.

If one of those surfaces must change, end the current experiment and open a separately scoped evaluator/control-plane change with its own verification.

## Same-root rule

Rivals compared within one experiment must share `root_sha` unless changing the root is itself the declared independent variable. Results from different roots are not silently ranked as same-root evidence.

## Execution and receipts

A candidate selected by simulation remains advisory until executed through the declared implementation boundary and checked by the declared verifiers. Each run should preserve enough receipt data to reconstruct:

- experiment ID and root SHA;
- candidate identity or mutation;
- evaluator identity/hash;
- inputs/seeds;
- commands or execution mechanism;
- observed metrics/results;
- verifier results;
- keep/reject/error classification;
- residuals and counterexamples;
- rollback point.

## Result classes

Keep infrastructure and model outcomes distinct:

- `KEEP` — candidate satisfies the frozen promotion gate.
- `REJECT` — candidate executed normally but did not satisfy the gate.
- `ERROR` — execution/evaluator/verifier failed; not evidence that the candidate is worse.
- `INVALID` — candidate or experiment violates the frozen contract.
- `RESIDUAL` — unresolved distinction or missing evidence remains.

## Promotion

Promotion requires the frozen experiment gate plus proportionate repository verification. A simulator score alone is insufficient. Generated output, reports, or state do not become canonical source merely because an experiment succeeded.

## Change rule

If the objective, evaluator, holdout, success criteria, budget semantics, candidate grammar, or authority boundary changes materially, record a new experiment identity or explicit superseding contract rather than silently editing historical evidence.
