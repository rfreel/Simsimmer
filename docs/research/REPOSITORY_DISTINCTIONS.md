# Repository Distinction Contract

This taxonomy is normative vocabulary for repository design. Machine enforcement is used where semantics are decidable; schemas constrain structured records; the remainder stays explicit prose rather than pretending automation can prove it.

## 1 Purpose
repository/project; problem/solution; goal/method; mission/milestone; scope/objective; in-scope/out-of-scope; requirement/preference; constraint/convention; success criterion/activity; deliverable/intermediate artifact; definition of done/stopping rule; known solution/research problem; current objective/future objective.

## 2 Authority
canonical/derived; authoritative/advisory; source of truth/cache; specification/implementation; policy/procedure; rule/heuristic; invariant/default; required/optional; human-authoritative/agent-authoritative; repository/task-local instruction; global/directory-local rule; current/superseded rule; machine-enforced/prose-only rule.

## 3 State
current/desired; observed/inferred; verified/unverified; complete/partial; implemented/proposed; working/passing; passing/correct; correct/production-ready; active/dormant; open/closed; blocked/unfinished; deprecated/deleted; superseded/invalid; historical/live.

## 4 Evidence
claim/evidence; evidence/interpretation; test result/conclusion; receipt/assertion; reproduction/demonstration; example/proof; synthetic/empirical; benchmark/acceptance test; training/holdout; independent/self verification; positive evidence/absence of failure; artifact existence/correctness; source provenance/transformed output.

## 5 Knowledge
fact/hypothesis; decision/rationale; assumption/established fact; question/residual; discovery/interpretation; learning/implementation; reusable/task-specific; stable/time-sensitive; external/repository-native; human note/machine-consumable; raw trace/compressed lesson; novel finding/rediscovery; positive/negative result.

## 6 Work
task/issue; issue/bug; bug/missing feature; feature/experiment; experiment/research question; research/implementation; implementation/integration; refactor/behavioral change; maintenance/capability expansion; one-shot/recurring; independent/dependency; parallel/sequential; reversible/irreversible; cheap probe/expensive commitment; local optimization/system improvement.

## 7 Planning
backlog/active queue; TODO/committed work; priority/dependency order; urgency/importance; expected value/confidence; opportunity/obligation; candidate/selected approach; plan/execution record; next/eventual action; blocked/optional dependency; finite task/open search; completion/saturation target.

## 8 Code and architecture
interface/implementation; public/internal API; core/adapter; library/application; runtime/tooling; domain/infrastructure; mechanism/policy; configuration/code; static data/runtime state; persistent/ephemeral; pure/side effect; deterministic/stochastic; local/external dependency; primitive/composition; reusable abstraction/incidental duplication.

## 9 Files and artifacts
source/generated; editable/generated-only; input/output; raw/normalized; canonical/working dataset; fixture/production data; code/data; configuration/secret; documentation/executable specification; temporary/persistent; human/machine-readable; version-controlled/ignored; repository/external artifact; release/development artifact.

## 10 Dependencies
direct/transitive; runtime/development; required/optional; pinned/floating; vendored/external; trusted/untrusted; internal/third-party; build/runtime; dependency/integration; availability/correctness.

## 11 Testing
unit/integration; integration/e2e; regression/acceptance; property/example; deterministic/probabilistic; fixture/oracle; oracle/implementation-under-test; happy/adversarial; expected/unexpected failure; flaky/regression; source/packaged artifact; smoke/exhaustive; test coverage/behavioral coverage; passing/requirement satisfied.

## 12 Evaluation and research
search space/candidate; generator/evaluator; evaluator/verifier; training/validation/holdout; inner/outer objective; metric/target; proxy/terminal criterion; baseline/challenger; exploration/exploitation; mutation/promotion; discovery/confirmation; improvement/noise; local/transferable gain; reusable capability/benchmark overfit; search progress/permanent learning.

## 13 Version control
working tree/commit; commit/branch; branch/release; local/remote; mainline/experiment; feature/integration branch; merge/rebase; history/current tree; tag/branch; version/commit identity; draft/merge-ready PR; merged/deployed; revert/corrective follow-up; repository/installed state.

## 14 Change management
additive/destructive; compatible/breaking; schema extension/mutation; migration/replacement; forward migration/rollback; behavioral/implementation-only; intended/collateral; scoped/scope creep; workaround/permanent fix; root-cause/symptom suppression.

## 15 Releases
development/release; release candidate/promoted release; source/built package; build/install/runtime/behavioral success; artifact/metadata; reproducible/successful build; immutable release/mutable development.

## 16 Provenance
original/transformed; imported/repository-created; primary/secondary; external claim/internally verified; human/agent-authored; generated/reviewed/approved; discovery/incorporation timestamp; source/content identity; hash/filename; lineage/current representation.

## 17 Agent work
instruction/context; permission/capability; capability/obligation; suggestion/command; plan/authorization; read/mutation; local/remote mutation; proposal/committed change; agent output/verified state; confidence/evidence; memory/repository evidence; delegated/independently checked; parallel/canonical result; simulation/execution; tool/task success.

## 18 Multi-agent
ownership/participation; exclusive/shared task; independent/duplicated search; parallel exploration/coordinated implementation; local/shared state; candidate/accepted; conflict/legitimate alternative; consensus/correctness; mergeable/incompatible assumptions; worker/reviewer; generator/critic; reviewer/final authority.

## 19 Automation
manual/automated; triggered/scheduled; one-shot/recurring; stateless/stateful; idempotent/non-idempotent; retry-safe/dangerous; visible/silent failure; fail-open/closed; notification/mutation; observation/action job; automation/downstream success; transient/structural failure.

## 20 Security
public/private; secret/configuration; authentication/authorization; identity/permission; read/write permission; repository/deployment permission; trusted/untrusted input; sandbox/host execution; least privilege/convenience; credential presence/validity; security boundary/organizational convention.

## 21 Data
schema/instance; identity/attributes; entity/relation; node/edge; record/event; snapshot/history; state/transition; null/absent; unknown/not-applicable; duplicate/independent corroboration; logical/byte identity; ordering/membership; append-only/mutable; lossless/lossy transform.

## 22 Documentation
README/specification; specification/ADR; ADR/implementation note; tutorial/reference/explanation; current/historical; example/normative command; user/contributor/agent docs; architecture description/contract.

## 23 Failure
error/failure; failure/defect; defect/limitation; limitation/missing capability; expected limitation/regression; recoverable/terminal; local/systemic; data/code/environment/implementation; resource exhaustion/logical impossibility; unknown/unresolved cause; failed/useless experiment.

## 24 Optimization
correctness/performance/efficiency; latency/throughput; compute/human cost; immediate/compounding gain; specialization/generality; compression/information loss; reuse/premature abstraction; breadth/depth; novelty/utility; capability/complexity; target/guardrail; measured/perceived improvement.

## 25 Accretive design
consumed/retained work; transient answer/reusable artifact; trace/pattern; pattern/compiled abstraction; abstraction/tool; tool/workflow; workflow/policy; candidate/promoted abstraction; promoted/dormant capability; new/recombined capability; independent rediscovery/copied knowledge; accumulation/compounding; more artifacts/smaller stronger basis; historical learning/active basis/archive; search output/search-policy improvement; task solved/future tasks cheaper; capability acquired/demonstrated.

Central test: did this work only solve the current problem, or reduce expected cost for a class of future problems?

## Highest-leverage reconstruction basis
canonical/derived; fact/inference; claim/evidence; specification/implementation; proposal/accepted; simulation/execution; passing/correct; current/superseded; source/generated; persistent/ephemeral; reversible/irreversible; generator/verifier; search/promotion; task result/reusable capability; accumulation/compounding; resolved/residual; authority/capability; identity/representation; local/shared state; current problem/future-work reduction.
