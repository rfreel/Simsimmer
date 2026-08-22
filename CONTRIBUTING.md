# Contributing

Read `AGENTS.md`, `PROJECT_INTENT.md`, `control/repository.manifest.json`, and `docs/OWNERSHIP.md` before mutating the repository.

Every change must declare a task or experiment ID, root commit, scope, files owned, success criterion, verification commands, and rollback point. Use `agent/<task>` or `exp/<experiment-id>` branches. `main` is canonical promoted state, not a scratch branch.

A plan is not authorization to modify unrelated surfaces. A passing test is evidence, not proof of correctness. Generated output is never silently promoted to source. Infrastructure failure is not candidate failure. Failed experiments that reveal reusable information should be retained under `knowledge/failures/` or `state/residuals/`.

Prefer additive, reversible changes. Breaking or destructive changes require an explicit migration and rollback plan. External tools may advise or execute through adapters, but canonical state must remain reconstructable from repository-native records and pinned provenance.
