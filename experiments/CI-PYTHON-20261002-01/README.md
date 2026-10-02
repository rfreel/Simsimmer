# Python minimum-version CI coverage

- id / experiment_id: CI-PYTHON-20261002-01
- owner: Codex coordinator
- branch: agent/ci-python-support-20261002
- root_sha: df9e145ea5f0c5282414bf869aaa88c43d91da01
- write_paths: .github/workflows/ci.yml; experiments/CI-PYTHON-20261002-01/**
- read_dependencies: pyproject.toml; AGENTS.md; docs/OWNERSHIP.md; existing CI commands; live main ruleset 21214975
- problem: package metadata promises Python >=3.11 but CI only exercises 3.12.
- objective: exercise the existing CI suite on the declared minimum and the existing runtime, retaining the required `test` check.
- scope: CI orchestration only; evaluator, controller, seeds, lock, research state and existing tests are immutable for this task.
- success_criteria: both Python versions run all existing checks; the required `test` check succeeds only if the entire version matrix succeeds, including fail-closed behavior for skipped/cancelled jobs.
- stopping_rule: stop after one selected implementation and local verification plus hosted CI observation, or preserve an explicit infrastructure residual.
- budget: two design rivals, one implementation, at most two corrective iterations; no paid services or deployment.
- candidate_space: raise metadata minimum to 3.12; retain metadata and add a 3.11/3.12 matrix with an aggregate `test` gate.
- generator: manual bounded CI design.
- evaluator: same-root deterministic contract simulation comparing minimum-version preservation, coverage, required-check identity and failure truth table; synthetic design evidence only.
- verifiers: repository doctor, existing unit/spec tests, smoke commands, YAML structure inspection, gate failure truth table, hosted checks.
- seed: none; deterministic checks.
- status: locally verified; hosted verification and promotion pending.

## Invariants

Retain all current checks, pinned actions, read-only contents permission, checkout credential isolation and the main ruleset's required `test` context. Do not change research state or weaken the evaluator to obtain passing results.

## Rollback

Discard this task branch before promotion; after promotion revert the scoped CI change. No research state migration is involved.

## Selection and verification receipt

The same-root contract simulation rejected raising the minimum because it removes declared 3.11 compatibility. It selected the matrix plus aggregate gate. Its 16 two-version success/failure/cancelled/skipped combinations accepted only two successful results. This is bounded synthetic design evidence.

Local execution on Python 3.11.16 and 3.12.14 passed every existing CI command: repository doctor; 3 simulator tests; 5 specification tests; exploit smoke (3 iterations, seed 42); specification scheduler (limit 16); the 1,048,576-configuration architecture replay; and the 106-bead verification. Architecture receipt hashes agreed across both runtimes (`212e8df4b2cc45bf54eaed35c5fc59b59362ed470624d9843efd94a8dc2cac1d`). Smoke and architecture outputs were written outside canonical state; autoresearch ran without `--write`.

YAML inspection confirmed every existing run command is preserved, versions are quoted strings, and the aggregate job remains `test`. Executing the aggregate shell check for success, failure, cancelled, skipped and empty results accepted only success. `git diff --check` passed. An independent read-only review found no CI diff defect; this is review evidence, not a hosted execution claim.

Live ruleset 21214975 requires `test`, strict up-to-date status and resolved review threads. The aggregate uses `always()` so upstream failure/skipping cannot silently remove the gate. Hosted matrix execution remains INCOMPLETE until checks run on the published change.
