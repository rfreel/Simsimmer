# Integration plan v3 — typed beads + derived routing

Status: proposed execution plan derived from the Doodlestein `br`/`bv` review and the existing repository/distinction bead graph.

## Objective

Preserve the 106-bead dependency-atomic plan while adding the missing semantic boundaries required for safe execution:

1. typed blocking vs descriptive relations,
2. explicit subject binding,
3. separate work/evidence/promotion state,
4. closure authority via oracle or review witness,
5. claim/lease coordination,
6. derived graph routing over the legal ready set,
7. graph-hash and metric-status provenance,
8. historical/retry evidence retention.

The immutable Simsimmer evaluator remains out of scope.

## Execution order

### A. Strengthen the canonical bead contract

1. Add explicit `subject_root` binding.
2. Replace untyped `depends_on` semantics with typed `relations` while retaining `depends_on` as a derived compatibility view during migration.
3. Define blocking relation types: `BLOCKS`, `WAITS_FOR`, `CONDITIONAL_BLOCKS`.
4. Define nonblocking relation types: `PARENT_OF`, `RELATED_TO`, `DISCOVERED_FROM`, `CAUSED_BY`, `DUPLICATES`, `SUPERSEDES`.
5. Add separate `work_state`, `evidence_state`, and `promotion_state`.
6. Add `acceptance_authority` and oracle/review-witness references.
7. Add actor/claim/lease metadata and stale-claim semantics.
8. Add source-requirement and proposed-mechanism fields without making proposals normative.

Gate A: a bead can answer what it is about, what blocks it, who may close it, and what evidence/promoter state exists without consulting prose conventions.

### B. Preserve migration compatibility

1. Translate every current `depends_on` edge to `BLOCKS` initially; do not infer weaker relation types automatically.
2. Reclassify edges only with explicit evidence.
3. Keep legacy `depends_on` generated from current blocking relations until all consumers use typed relations.
4. Verify ready-set equivalence before and after migration.

Gate B: migration changes representation, not the current legal execution set.

### C. Split ledger from router

Canonical layer owns bead facts only. Derived router owns graph analysis and recommendations.

Router pipeline:

`canonical graph -> blocking projection -> ready set -> graph metrics -> routing vector -> next/parallel tracks`

Hard rules:

- blocked work cannot be promoted into the ready set by score;
- phase is metadata unless represented by a blocking relation;
- centrality never becomes materiality evidence;
- scheduler output never mutates canonical bead state;
- every routing result includes graph hash and metric status.

### D. Compute a vector before choosing a scalar policy

For ready beads compute independently:

- declared priority,
- critical-path contribution,
- downstream unblock count,
- PageRank,
- betweenness,
- HITS/eigenvector where useful,
- degree,
- evidence-value estimate,
- uncertainty,
- estimated/observed cost,
- retry risk,
- mutable-surface contention,
- claim availability.

Expose `next` and `parallel_tracks`; preserve the vector in receipts even if a routing policy later compiles it into a score.

### E. Strengthen closure and retries

1. Work execution moves work state only.
2. Oracle/review witness moves evidence state.
3. Promotion authority moves promotion state.
4. Failed attempts remain append-only evidence.
5. Retry creates a new attempt linked to the prior attempt.
6. Close reason is explanatory metadata, not proof.

### F. Calibrate with real execution

1. Execute subject binding and path classification first.
2. Measure actual cost, retries, ambiguity, oracle cost, and downstream unlocks.
3. Replace synthetic scheduler priors only where observations support the change.
4. Re-run routing rivals on unseen DAG fixtures before promoting a default policy.

## Existing bead absorption map

Do not expand bead count by default.

- P0 absorbs explicit subject binding and graph/root hash semantics.
- P1 absorbs typed relation schema, state separation, lifecycle, and migration compatibility.
- P2 absorbs ready-set equivalence, schema/oracle/security tests, and graph-hash verification.
- P4 absorbs canonical relation-instance storage and asserted/derived separation.
- P6 absorbs ready filtering, graph metrics, `next`, parallel tracks, and historical queries.
- P7 absorbs claims/leases, attempt lineage, closure authority, and promotion separation.
- P8 absorbs unseen graph-shape holdouts and scheduler calibration.

Create a new bead only if the work cannot be closed independently inside those existing outcomes without mixing authorities.

## Verification matrix

| Requirement | Evidence |
|---|---|
| blocking and descriptive relations differ | typed-relation fixtures + ready-set tests |
| hierarchy is not silently blocking | parent-only fixture remains ready |
| migration preserves readiness | old/new ready-set equality receipt |
| router cannot legalize blocked work | adversarial high-score blocked fixture |
| work close != verification | lifecycle transition tests |
| verification != promotion | promotion-gate tests |
| router state is derived | idempotent recomputation with unchanged canonical hash |
| metrics are evidence-scoped | graph hash + metric status in every routing receipt |
| retries preserve history | append-only attempt lineage fixture |
| claims do not become ownership | lease expiry/stale-claim fixture |
| rich context is non-normative by default | proposed mechanism can change without requirement failure |

## Stopping rule

This integration is complete when:

- every canonical relation instance has a type;
- blocking projection exactly determines readiness;
- the current 106-bead ready set is preserved through migration unless an explicitly reviewed reclassification changes it;
- work/evidence/promotion states are independently representable;
- every bead has an explicit closure-authority class;
- router outputs are reproducible from a content-addressed canonical graph;
- `next` and parallel tracks are produced without canonical mutation;
- all adversarial boundary fixtures pass;
- at least two real bead receipts have calibrated the synthetic scheduler priors.
