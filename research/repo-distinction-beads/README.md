# Repository / distinction graph bead plan

Status: **PROPOSED RESEARCH PLAN**. This package does not modify the fixed simulator, tests, evaluator lock, or active champion.

The immutable simulator stressed 106 dependency-atomic beads against the same root. `validated_atomic_v2` ranked first in all five scoring regimes.

## Current structure

- 106 work beads
- 159 direct dependency edges
- 0 transitively redundant direct edges
- acyclic DAG
- unit-weight critical path: 35 beads
- maximum runnable frontier: 10
- initial runnable bead: `RG-P0-01`
- 11 hard ordering/authority anchors preserved

Machine-readable beads are split by phase in `beads/P0.jsonl` through `beads/P8.jsonl`.

## Phases

| Phase | Purpose | Beads |
|---|---|---:|
| P0 | truth surface | 10 |
| P1 | canonical graph kernel v2 | 14 |
| P2 | verifier / replay / CI | 15 |
| P3 | materiality adjudication | 15 |
| P4 | relation-instance graph | 15 |
| P5 | requirement compiler | 7 |
| P6 | query / impact runtime | 11 |
| P7 | mutation / promotion lifecycle | 10 |
| P8 | unseen holdout / resaturation | 9 |

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

## Closure rule

A bead closes only when its single named outcome exists, its acceptance check passes, and its bead-specific receipt is attributable to that outcome. Discovery/decision, mutation, verification, and promotion remain separate when crossing an authority or rollback boundary.

## Evidence

- `DIFF_SUMMARY.md` — v1 → proposed v2 structural changes.
- `BEAD_STRESS_SIM_RECEIPT.json` — same-root policy comparison and limitations.
- `BEADS_RECEIPT.json` — proposed v2 DAG verification receipt.

Fresh evidence recorded by the local planning run: immutable Runtime core tests 7/7 PASS; IDs unique; dependency references resolve; DAG acyclic; direct transitive redundancy zero; hard order anchors preserved; close receipt paths unique.

The stress heuristics still flag 30 acceptance clauses as not obviously machine-checkable. They remain open review targets rather than being rewritten automatically.
