# Simsimmer TODO

Scout root: `cdc74975f620853d76991c84f862aa90833c28a1`  
Scout task: `SCOUT-20260822-01`

This backlog is dependency-ordered. The current repository has a comparatively strong control plane, but the live flywheel, executable benchmark layer, retained-learning compiler, and reusable implementation substrate are not yet demonstrated end to end. Do not expand breadth ahead of those proofs.

## P0 — Prove the system actually compounds

### 1. Prove scheduled autoresearch against current `main`

Current observation: `autoresearch/ratchet` is **41 commits behind `main` and 0 commits ahead**. That is safe, but it means the current hardened/protected repository has not yet demonstrated a persisted state delta through the scheduled lane.

- [ ] Trigger one manual `scheduled-autoresearch` run from current `main`.
- [ ] Verify pre-run ratchet validation accepts only `state/**` divergence.
- [ ] Verify reviewed `main` merges into the ratchet without history rewriting.
- [ ] Verify all simulator tests pass before research.
- [ ] Verify explore/exploit/transfer/compress execute against the locked evaluator.
- [ ] Verify all simulator tests pass after research.
- [ ] Verify no path outside `state/**` changes.
- [ ] Verify the ratchet push succeeds without force.
- [ ] Compare `main...autoresearch/ratchet`: any ahead paths must be only `state/**`.
- [ ] Preserve run ID, root SHA, resulting ratchet SHA, changed state paths, and rollback point as a receipt.

Acceptance gate: one hosted run completes successfully and leaves either (a) a valid state-only ratchet commit or (b) an explicit no-delta receipt. No infrastructure or verifier failure may be reclassified as a candidate rejection.

### 2. Observe one natural scheduled run

- [ ] After the manual proof, allow one cron execution at the configured twice-daily cadence.
- [ ] Verify concurrency serialization prevents overlapping ratchet writers.
- [ ] Verify the scheduled run uses the current `main` workflow definition.
- [ ] Compare its receipt with the manual run for semantic equivalence.

Acceptance gate: manual and cron paths produce the same containment guarantees.

### 3. Close the live GitHub settings residual — issue #10

`main` is now protected by the imported ruleset, but issue #10 tracks the remaining administrative target.

- [ ] Re-read live Actions policy rather than assuming the desired configuration is active.
- [ ] Confirm GitHub-owned actions allowed and broad third-party allowance denied.
- [ ] Confirm full-SHA action policy where GitHub exposes it.
- [ ] Confirm default workflow token is read-only.
- [ ] Confirm Actions cannot create/approve PRs by default.
- [ ] Confirm fork workflows receive neither secrets nor write tokens.
- [ ] Confirm external-contributor approval policy.
- [ ] Confirm 30-day Actions log retention.
- [ ] Confirm `main` ruleset requires PR + strict `test` + resolved threads and blocks force/delete.
- [ ] Confirm merge settings target: merge + squash yes, rebase no, auto-merge/update-branch/delete-head yes.
- [ ] Confirm secret scanning, push protection, Dependabot alerts, and security updates.
- [ ] Update/close issue #10 only from live evidence.

Acceptance gate: live settings match `control/github-settings.target.json`, with every mismatch retained as a residual.

### 4. Bind the real decomposition subject and unblock PR #3

PR #3 deliberately leaves `RG-P0-01` subject root unbound and Agent Mail rollout R1 unrun.

- [ ] Resolve the real subject root for `RG-P0-01` from repository state, not chat inference.
- [ ] Bind the subject/path classification in the bead representation.
- [ ] Re-run the v3 compatibility verifier after binding.
- [ ] Recompute ready set, DAG, critical path, and acceptance-authority classifications.
- [ ] Preserve any semantic relation reclassifications as explicit deltas.

Acceptance gate: `RG-P0-01` has an evidenced subject binding and the graph remains valid under the same deterministic checks.

### 5. Run Agent Mail rollout R1 only after P0-4

- [ ] Install the pinned Agent Mail dependency from its recorded commit/release.
- [ ] Let Agent Mail create/discover its own project identity; do not invent one.
- [ ] Run a single-agent smoke using exact bead ID `RG-P0-01` as the thread ID.
- [ ] Verify coordination state cannot alter bead readiness, verification, closure, promotion, or evaluator state.
- [ ] Record bootstrap commands, project UID, thread receipt, and uninstall/rollback path.

Acceptance gate: one live single-agent coordination round succeeds without changing canonical work-state authority.

## P1 — Build the missing compounding substrate

### 6. Turn experiment contracts into executable validation

The manifest defines required experiment fields, but admission is still largely convention-driven.

- [ ] Define one machine-readable experiment schema covering all fields in `control/repository.manifest.json`.
- [ ] Add deterministic validation for experiment/task records.
- [ ] Validate root SHA existence and branch/write-zone compatibility.
- [ ] Validate frozen evaluator/verifier references where applicable.
- [ ] Validate stopping rule and budget are non-empty and typed.
- [ ] Validate status transitions cannot skip required evidence states.
- [ ] Add negative fixtures for stale roots, missing fields, illegal write zones, and verifier/evaluator co-mutation.
- [ ] Run validator in CI before simulator tests.

Acceptance gate: malformed experiment records fail CI for the intended reason; existing valid records remain accepted or are migrated explicitly.

### 7. Build a receipt ledger with stable schemas

- [ ] Define receipt types for simulation, execution, verification, promotion, failure, residual, rollback, and infrastructure incident.
- [ ] Give every receipt stable IDs, root SHA, producer, timestamp, evidence pointers, status, and supersession links.
- [ ] Separate OBSERVED / DERIVED / ASSUMED / NOT-VERIFIED fields structurally, not only in prose.
- [ ] Add append-only ledger validation and duplicate detection.
- [ ] Provide deterministic query tools: by task, root, verifier, failure class, operator, and promoted abstraction.

Acceptance gate: a fresh agent can reconstruct why a promoted result exists without reading chat history.

### 8. Make retained learning real

Current `knowledge/{findings,failures,patterns,abstractions}` is mostly scaffolding.

- [ ] Define schemas for finding, failure boundary, pattern, abstraction, and archived/superseded record.
- [ ] Backfill the GitHub Actions zero-step incident as a failure-boundary exemplar.
- [ ] Backfill the bad evaluator-lock incident as a provenance/integrity exemplar.
- [ ] Backfill ratchet-containment design as a reusable workflow/operator exemplar.
- [ ] Add provenance links from knowledge records to source receipts/commits/runs.
- [ ] Add exact-dedup and semantic-near-duplicate review queue.
- [ ] Add supersession rather than destructive overwrite.

Acceptance gate: at least three real historical episodes compile into reusable knowledge and can be retrieved deterministically.

### 9. Implement the trace → relation → abstraction compiler

The mission requires `RELATE → GENERALIZE → COMPILE → REDISCOVER → ABLATE → RE-DERIVE → COMPRESS`; today most of that is conceptual.

- [ ] Define canonical trace/event schema.
- [ ] Define typed relations among traces, failures, hypotheses, verifiers, tasks, and abstractions.
- [ ] Implement repeated-substructure detection with deterministic witnesses.
- [ ] Compile candidate abstractions only from explicit supporting traces.
- [ ] Re-derive historical cases using candidate abstraction.
- [ ] Add rediscovery test using held-out equivalent cases.
- [ ] Ablate abstraction and measure added future work.
- [ ] Retain only abstractions that reduce work without losing required capability.

Acceptance gate: one abstraction is discovered from multiple traces, independently re-derived/rediscovered, ablated, and retained or rejected with receipts.

### 10. Create executable benchmarks for the actual project success criterion

`benchmarks/` currently states benchmark discipline but has no executable baseline suite.

Measure the mission directly: increasing verified capability or decreasing expected future work per unit compute while preserving provenance and rollback.

- [ ] Define baseline task corpus with frozen versions/provenance.
- [ ] Include easy, adversarial, transfer, decomposition, coordination, and repository-maintenance tasks.
- [ ] Measure solve rate, verifier pass rate, compute/work proxy, wall time, retries, reused abstractions, rediscovery, rollback completeness, and residual count.
- [ ] Separate synthetic simulator metrics from empirical repository metrics.
- [ ] Add repeated runs and uncertainty intervals where stochasticity exists.
- [ ] Freeze an outer holdout not used for operator/search selection.
- [ ] Record environment, Python version, runner image, commit, seeds, and data version.

Acceptance gate: baseline benchmark can be rerun from a clean checkout and produces a content-addressed receipt.

### 11. Resolve Python support truth

`pyproject.toml` declares Python `>=3.11`, while CI currently proves only Python 3.12.

Choose one, explicitly:

- [ ] Option A: add Python 3.11 to CI and keep `>=3.11`; or
- [ ] Option B: change `requires-python` to the minimum version actually supported and tested.
- [ ] Test all public commands on the declared minimum.

Acceptance gate: package metadata and CI support claim are identical.

### 12. Turn `src/` into a real package boundary

Current `src/` contains only a README while executable logic sits mostly at repository root.

- [ ] Decide whether Simsimmer is a package, a repository harness, or both.
- [ ] If package: create importable `src/simsimmer/` modules and a stable CLI boundary.
- [ ] Move reusable logic without moving/fuzzing the trusted evaluator in the same change.
- [ ] Keep evaluator/controller separation explicit in package structure.
- [ ] Add clean-install and wheel/sdist smoke tests.
- [ ] Verify commands work outside repository-root import side effects.

Acceptance gate: a clean environment can install Simsimmer and run its supported CLI/API without relying on accidental checkout paths.

## P1 — Make execution and coordination trustworthy at scale

### 13. Finish Agent Mail rollout in gated stages

Only after R1 passes:

- [ ] R2 two-agent non-overlap pilot.
- [ ] R3 controlled reservation-conflict pilot.
- [ ] R4 router coordination features.
- [ ] R5 broader multi-agent execution.
- [ ] At each stage verify Agent Mail remains advisory to canonical work/evidence/promotion state.
- [ ] Add failure-injection: lost acknowledgement, stale lease, duplicate worker, conflicting reservation, worker crash, partial handoff.

Acceptance gate: each rollout stage has a distinct verifier and rollback criterion; no stage is promoted by narrative judgment alone.

### 14. Build a real task router/scheduler

- [ ] Consume canonical bead/task graph rather than duplicate task state.
- [ ] Compute runnable frontier from typed dependency relations.
- [ ] Account for write-zone conflicts and leases.
- [ ] Prefer work that reduces critical path or unlocks frontier width.
- [ ] Track resource/capability requirements and unavailable executors.
- [ ] Reject stale roots before dispatch.
- [ ] Preserve residuals when nothing is runnable.
- [ ] Add deterministic replay of routing decisions.

Acceptance gate: router schedules a multi-task fixture correctly, reproduces the same decisions from the same state, and fails closed on stale/conflicting state.

### 15. Add independent verification lane

- [ ] Separate implementation receipts from verifier receipts.
- [ ] For material changes, require a verifier that did not author the candidate delta when practical.
- [ ] Record verifier identity/version/tooling/root.
- [ ] Add adversarial negative tests for self-verification leakage.
- [ ] Ensure promotion checks evidence, not agent-reported success.

Acceptance gate: promotion can reject an implementation even when its author claims success.

## P2 — Security, resilience, and repository operations

### 16. Add CodeQL as a separately scoped security task

- [ ] Evaluate GitHub default setup for the current Python surface.
- [ ] Enable only after checking noise/cost against repository scale.
- [ ] Record baseline findings and suppressions with rationale, never blanket-ignore.

### 17. Add dependency and supply-chain receipts

- [ ] Inventory all GitHub Actions, vendored sources, external tools, and future Python dependencies.
- [ ] Pin by immutable identifier where possible.
- [ ] Record upstream source, version, commit/hash, license, update policy, and verification method.
- [ ] Add automated stale-pin discovery without automatic promotion.

### 18. Test failure/recovery paths of the ratchet

- [ ] Main/state merge conflict.
- [ ] Illegal non-state ratchet divergence.
- [ ] Concurrent scheduled runs.
- [ ] Push race/non-fast-forward.
- [ ] Runner termination after state mutation but before commit.
- [ ] Runner termination after commit but before push.
- [ ] Corrupt state JSON.
- [ ] Stale evaluator lock.

Acceptance gate: every injected fault fails closed and leaves a deterministic recovery path.

### 19. Add repository disaster-recovery procedure

- [ ] Define canonical backup/reconstruction sources.
- [ ] Document recovery from deleted ratchet branch, accidental state commit, bad main merge, corrupted state, and unavailable external coordination tool.
- [ ] Verify recovery in a disposable clone/repository fixture.

### 20. Close branch/repository hygiene gaps

- [ ] Enable delete-head-branch-after-merge if not already active.
- [ ] Remove stale diagnostic/task branches only after confirming no unique commits/receipts.
- [ ] Preserve long-lived `autoresearch/ratchet` intentionally.
- [ ] Decide merge-commit vs squash semantics by artifact type and document the rule.
- [ ] Enable auto-merge/update-branch only after live settings verification.

## P2 — Measure whether the flywheel is actually improving

### 21. Add a learning-efficiency scorecard

Track over time, without collapsing everything into one hidden scalar:

- verified tasks completed;
- expected work/compute per verified task;
- reusable abstractions retained;
- abstraction reuse hits;
- independent rediscoveries;
- regressions caught before promotion;
- failure boundaries retained;
- residuals opened/closed;
- active-basis size;
- benchmark/holdout performance;
- provenance/rollback completeness;
- human interventions per task.

Acceptance gate: trends are reproducible from repository receipts, not hand-entered dashboard numbers.

### 22. Establish promotion criteria for “compounding”

Do not call the system compounding merely because state grows.

- [ ] Require evidence that retained learning reduces future work or expands verified capability.
- [ ] Require ablation evidence for promoted abstractions.
- [ ] Penalize basis growth that does not improve reachability/work.
- [ ] Preserve Pareto/residual structure instead of forcing a single score where objectives conflict.

Acceptance gate: at least one before/after benchmark demonstrates a reusable retained artifact improving a later unseen task under a frozen evaluation regime.

## P3 — Expansion only after the above works

- [ ] Add new domain simulators through separately reviewed evaluator-change tasks.
- [ ] Add multi-language execution adapters only when a real task requires them.
- [ ] Add richer search policies/populations only after baseline empirical benchmarks exist.
- [ ] Add self-improving router/operator search only behind outer holdout gating.
- [ ] Add remote/distributed executors only after local deterministic replay and recovery are proven.
- [ ] Add deployment capability only as a separately authorized trust boundary.

## Explicit non-goals for now

- Do not weaken or co-optimize the simulator/evaluator to make candidates pass.
- Do not turn `main` into a scratch or autonomous research branch.
- Do not let Agent Mail or any external coordination layer become canonical authority.
- Do not claim global saturation from bounded search.
- Do not add broad dependencies before a concrete missing capability justifies them.
- Do not scale agent count before collision, stale-root, handoff, and recovery behavior are verified.

## Current frontier summary

1. **Prove the ratchet on the current hardened repo.**
2. **Finish live settings verification.**
3. **Bind `RG-P0-01`; run Agent Mail R1.**
4. **Build executable experiment/receipt/knowledge contracts.**
5. **Create real empirical benchmarks.**
6. **Compile and ablate one genuinely reusable abstraction.**
7. **Only then scale routing, agents, operators, and domains.**

That sequence is the shortest path from “well-structured repository” to “demonstrably compounding system.”
