# Repository / distinction graph bead plan

Status: **PROPOSED RESEARCH PLAN — V3 PREWALK ACTIVE**. This package does not modify the fixed simulator, tests, evaluator lock, or active champion.

The immutable simulator stressed 106 dependency-atomic beads against the same root. `validated_atomic_v2` ranked first in all five scoring regimes. A later Doodlestein `br`/`bv` review exposed additional decision-relevant boundaries around typed dependencies, ready-vs-important routing, closure evidence, claims, and graph-derived scheduling.

## Current structure

- 106 work beads
- 159 direct dependency edges
- 0 transitively redundant direct edges
- acyclic DAG
- unit-weight critical path: 35 beads
- maximum runnable frontier: 10
- initial runnable bead: `RG-P0-01`
- 11 hard ordering/authority anchors preserved
- P0 represented under bead contract v3
- P1–P8 remain the validated v2 proposed graph pending explicit subject binding

Machine-readable beads are split by phase in `beads/P0.jsonl` through `beads/P8.jsonl`.

## V3 additions

- `DISTINCTIONS_V3.md` — 110 materially decision-relevant distinctions derived from the Beads/Flywheel review.
- `INTEGRATION_PLAN_V3.md` — dependency-ordered plan for typed relations, closure authority, router separation, claims, and calibration.
- `BEAD_CONTRACT_V3.schema.json` — proposed richer bead contract.
- `V3_MIGRATION_RECEIPT.json` — deterministic compatibility probe and bounded promotion receipt.

The full 106-bead v3 compatibility projection was generated locally but is **not canonical**. The probe preserved all 106 bead IDs, mapped all 159 legacy `depends_on` instances to directional `WAITS_FOR` relations, preserved the exact ready set `[RG-P0-01]`, remained acyclic, and preserved the unit critical path at 35. Only P0 is promoted to the richer representation before subject binding.

## Phases

| Phase | Purpose | Beads | Representation |
|---|---|---:|---|
| P0 | truth surface + explicit subject binding | 10 | v3 prewalk |
| P1 | canonical graph kernel | 14 | v2 pending subject bind |
| P2 | verifier / replay / CI | 15 | v2 pending subject bind |
| P3 | materiality adjudication | 15 | v2 pending subject bind |
| P4 | relation-instance graph | 15 | v2 pending subject bind |
| P5 | requirement compiler | 7 | v2 pending subject bind |
| P6 | query / impact / routing runtime | 11 | v2 pending subject bind |
| P7 | mutation / promotion lifecycle | 10 | v2 pending subject bind |
| P8 | unseen holdout / resaturation | 9 | v2 pending subject bind |

## Global acceptance gates

- **G1** — Catalog size is not evidence of graph quality.
- **G2** — Zero rejected candidates is a suspicious adjudicator signal, not success.
- **G3** — Relation-type coverage is not relation-instance coverage.
- **G4** — Schema-valid is not semantically valid.
- **G5** — Passing tests are evidence, not proof of total correctness.
- **G6** — Generated closure is not silently promoted to canonical truth.
- **G7** — Every material canonical claim has provenance.
- **G8** — Every destructive canonical change has rollback and lineage.
- **G9** — Every saturation claim names grammar, source basis, holdout, simulator, and stopping rule.
- **G10** — New enumeration is blocked while a higher-value structural residual remains open.
- **G11** — Host repository is not implicitly the subject repository. Every execution receipt names the immutable subject root.
- **G12** — A bead cannot auto-close without an executable acceptance oracle or an authorized review witness; otherwise it remains `NEEDS_REVIEW` or `UNRESOLVED`.

## Relation rule

Readiness and graph importance are different layers.

- `BLOCKS`, `WAITS_FOR`, and `CONDITIONAL_BLOCKS` may affect readiness.
- `PARENT_OF`, `RELATED_TO`, `DISCOVERED_FROM`, `CAUSED_BY`, `DUPLICATES`, and `SUPERSEDES` are descriptive unless another explicit blocking relation exists.
- Legacy `A.depends_on=[B]` projects to `A WAITS_FOR B` during migration.
- Hierarchy is not silently converted into a blocker.
- Routing consumes the legal ready set; a graph score cannot make blocked work runnable.

## State rule

Work state, evidence state, and promotion state are separate:

`work execution -> evidence evaluation -> promotion authorization`

Closing/executing a bead is therefore not equivalent to verification, and verification is not equivalent to promotion.

## Closure rule

A bead closes only when its single named outcome exists, its acceptance authority is satisfied, and its bead-specific receipt is attributable to that outcome. Discovery/decision, mutation, verification, and promotion remain separate when crossing an authority or rollback boundary.

Implementation sketches may be rich but remain advisory unless separately frozen by an authority-bearing decision.

## Routing rule

Canonical bead state and derived routing state remain separate. The eventual router operates as:

`canonical graph -> blocking projection -> ready set -> graph metrics -> routing vector -> next / parallel tracks`

Graph metrics such as critical path, downstream unblocks, PageRank, betweenness, HITS/eigenvector, and degree are scheduling evidence, not materiality evidence. Routing receipts must carry the source graph hash and per-metric status (`computed`, `approx`, `timeout`, or `skipped`).

## Evidence

- `DIFF_SUMMARY.md` — v1 → proposed v2 structural changes.
- `BEAD_STRESS_SIM_RECEIPT.json` — same-root policy comparison and limitations.
- `BEADS_RECEIPT.json` — proposed v2 DAG verification receipt.
- `V3_MIGRATION_RECEIPT.json` — v2 → v3 representation probe and P0 promotion boundary.

Fresh evidence recorded by the planning runs: immutable Runtime core tests 7/7 PASS; IDs unique; dependency references resolve; DAG acyclic; direct transitive redundancy zero; hard order anchors preserved; close receipt paths unique. The v3 compatibility probe additionally preserved the ready set and structural critical path.

The v3 probe classified acceptance authority conservatively as 44 candidate oracles, 30 review witnesses, 11 mixed, and 21 unresolved. These are provisional classifications, not implemented verifier claims. Oracle implementation and subject-specific execution remain open.
