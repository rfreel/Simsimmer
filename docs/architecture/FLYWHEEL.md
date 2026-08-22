# Simsimmer Flywheel Architecture

Simsimmer is a simulation-first research and software-engineering control loop. This document describes the repository-level architecture; it does not override `PROJECT_INTENT.md`, `control/repository.manifest.json`, or `AGENTS.md`.

## Canonical loop

`SIMULATE → SELECT → GENERATE → EXECUTE → VERIFY → ACCRETE → RELATE → GENERALIZE → COMPILE/REUSE → TRANSFER → REDISCOVER → ABLATE → RE-DERIVE → COMPRESS → SEARCH FARTHER`

## Architectural invariants

1. **Simulation precedes mutation.** Freeze the target, constraints, evidence, and success tests before generating candidate changes.
2. **Candidate and evaluator authority stay separate.** Ordinary research may mutate candidate policy/state, not the trusted simulator, frozen seeds, evaluator lock, or promotion gate.
3. **Execution produces receipts.** Selection is advisory until the selected candidate is executed and verified against repository-defined checks.
4. **Promotion is explicit.** `main` is reviewed canonical state. Scheduled autoresearch evolves only `state/**` on `autoresearch/ratchet` and may not silently promote code.
5. **Failures are retained as information.** Infrastructure failures, counterexamples, rejected candidates, residuals, and rollback points must not be collapsed into ordinary success/failure labels.
6. **Learning must reduce future work.** Repeated successful structure should be related, generalized, compiled into reusable operators or procedures, transferred, rediscovered, ablated, re-derived, and compressed.
7. **Canonical state remains reconstructable.** External tools and adapters may advise or execute, but repository-native contracts, provenance, and receipts remain sufficient to recover authority and state.

## Layers

- **Authority/control:** `PROJECT_INTENT.md`, `AGENTS.md`, `control/**`, `docs/specs/**`.
- **Trusted evaluator:** `sim/**`, `tests/**`, `evaluator.lock.json`.
- **Research controller:** `autoresearch.py`, `variants/**`.
- **Mutable research state:** `state/**`.
- **Experiments and receipts:** `experiments/**`, `knowledge/**`.
- **Operational mechanisms:** `scripts/**`, `tools/**`, `agents/**`.
- **Derived/noncanonical output:** `generated/**`, `artifacts/**`, `traces/raw/**`.

## Write lanes

- `main`: reviewed and promoted canonical state.
- `autoresearch/ratchet`: scheduled state evolution; persistence restricted to `state/**`.
- `agent/<task>`: task-scoped implementation or research.
- `exp/<experiment-id>`: experiment-scoped generated candidates.

## Verification boundary

A passing simulator score is not enough. Candidate promotion requires the checks specified by the task or experiment contract plus proportionate repository verification. Infrastructure failure is classified separately from candidate failure. A successful command is evidence only for the behavior it exercised.

## Compounding criterion

The flywheel is functioning only when repeated work leaves at least one durable improvement: verified capability, reusable operator/workflow, stronger verifier, explicit failure boundary, compressed active basis, or unresolved residual with provenance.
