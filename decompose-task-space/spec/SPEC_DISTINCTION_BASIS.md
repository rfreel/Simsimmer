# Specification Distinction Basis

Status: candidate canonical basis under `decompose-task-space/`. Authority: subordinate to `PROJECT_INTENT.md`, `control/**`, `AGENTS.md`, and applicable repository specs/ADRs.

Purpose: a domain-agnostic specification ontology that preserves distinctions needed for decisions, verification, execution, provenance, and future reuse. It is not a single hierarchy. Means/ends, whole/part, task containment, execution dependency, frame, operator, witness/delta, time, epistemics, resources, agency, risk, constraints, evidence, and provenance remain orthogonal dimensions unless an explicit relation is evidenced.

## WHY
`telos`, `purpose`, `objective`, `success criterion`, `value/preference`, `authority`, `stakeholder`.

## WHAT
`problem`, `desired state`, `current state`, `scope`, `in-scope`, `out-of-scope`, `deliverable`, `requirement`, `non-requirement`, `assumption`, `unknown`, `decision`, `deferred decision`.

## SEMANTICS
`entity`, `type`, `identity`, `state`, `event`, `relation`, `distinction`, `invariant`, `constraint`, `policy`, `rule`, `exception`, `precedence`, `cardinality`, `quantifier`, `unit`, `boundary`.

## DECOMPOSITION
`whole/part`, `task containment`, `execution dependency`, `frame`, `operator`, `witness/delta`, `contains/depends_on/candidate realizes`, `primitive/compound`, `mandatory/optional`, `alternative/complementary`, `independent/coupled`, `local/global`, `static/dynamic`.

## BEHAVIOR
`input`, `output`, `precondition`, `postcondition`, `transition`, `trigger`, `action`, `side effect`, `failure`, `recovery`, `rollback`, `idempotence`, `ordering`, `concurrency`, `termination`.

## INTERFACE
`producer/consumer`, `provided/required`, `internal/external`, `sync/async`, `push/pull`, `request/event`, `schema`, `protocol`, `compatibility`, `version`, `ownership`.

## DATA / STATE
`source of truth`, `derived state`, `persistent/ephemeral`, `mutable/immutable`, `canonical/cached`, `identity/value`, `consistency`, `freshness`, `retention`, `migration`.

## TIME
`before/after`, `duration`, `deadline`, `latency`, `frequency`, `timeout`, `retry`, `lifecycle`, `temporal scope`.

## RESOURCES
`executor`, `capability`, `tool`, `compute`, `memory`, `storage`, `network`, `money`, `scarce resource`, `contention`, `capacity`.

## QUALITY
`correctness`, `precision`, `recall`, `latency`, `throughput`, `availability`, `reliability`, `durability`, `maintainability`, `usability`, `accessibility`, `portability`, `scalability`, `efficiency`.

## RISK
`hazard`, `failure mode`, `severity`, `likelihood`, `blast radius`, `reversibility`, `security boundary`, `privacy boundary`, `trust boundary`, `abuse case`.

## EPISTEMICS
`observed`, `derived`, `assumed`, `estimated`, `predicted`, `unknown`, `contested`, `falsified`, `confidence`, `provenance`, `freshness`.

## VERIFICATION
`claim`, `witness`, `oracle`, `test`, `acceptance criterion`, `negative test`, `counterexample`, `regression`, `holdout`, `coverage`, `stopping condition`.

## CHANGE
`baseline`, `delta`, `migration`, `compatibility`, `rollout`, `rollback`, `feature gate`, `deprecation`, `supersession`.

## EXECUTION
`task`, `dependency`, `owner`, `priority`, `resource`, `milestone`, `blocker`, `completion condition`, `handoff`.

## RESIDUALS
`ambiguity`, `missing evidence`, `unresolved rival`, `unmodeled state`, `unverified assumption`, `unavailable capability`, `open dependency`, `scope uncertainty`, `known limitation`.

## Acceptance / ablation rule
The basis is not accepted because it is large. Remove each distinction, regenerate representative specifications, and retain it only when removal causes a concrete decision, verification, execution, authority, or provenance loss that cannot be recovered by an existing composition. Record the minimal discriminating witness.

## Saturation rule
A run may claim saturation only relative to its declared distinction basis, abstraction levels, whole/part levels, epistemic states, temporal regimes, coupling, reversibility, verification regime, resource contention, objective form, representation set, domain-specialization set, seed policy, and budget. No bounded run establishes global completeness.
