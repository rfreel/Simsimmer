# Bead simulation diff submission

Status: **PROPOSED_DIFF — not promoted to any external repository**

The immutable simulator stressed all 106 beads from the same root and compared seven graph policies. `validated_atomic_v2` ranked first in all five scoring regimes.

## Measured structural delta

| Metric | v1 | proposed v2 |
|---|---:|---:|
| Beads | 106 | 106 |
| Direct dependency edges | 187 | 159 |
| Transitively redundant edges | 39 | 0 |
| Unit critical path | 57 | 35 |
| Max runnable frontier | 8 | 10 |
| Per-bead gate links | 1,060 | 323 |
| Lifecycle-boundary collisions | 1 | 0 |

## Dependency changes

- Removed direct edges: **32**
  - transitively redundant in v1: **20**
  - explicit phase barriers relaxed: **12**
- Added direct edges: **4** to preserve pruned-basis dependencies after contract parallelization.

Phase-barrier relaxations are limited to contract/test work that does not consume the removed stage output. Canonical resaturation still cannot pass `RG-P3-15` before `RG-P2-15`; graph population still cannot pass the pruned-basis gate.

## Textual repairs

- `RG-P1-03`: removed negative-fixture execution from a state-machine definition bead.
- `RG-P4-11`: changed post-hoc “annotate” mutation into a verification bead.
- `RG-P8-09`: collapsed two apparent outcomes into one bounded-saturation receipt contract.

## Gate repair

The v1 graph attached all 10 global principles to all 106 beads. v2 keeps the principles global but records only decision-relevant `applicable_gates` per bead. The deterministic mapping reduced 1,060 links to 323; this is a planning classification, not empirical proof of irrelevance.

## Verification

- Immutable Runtime core tests: **7/7 PASS**.
- v2 IDs unique: **PASS**.
- All dependency references resolve: **PASS**.
- DAG acyclic: **PASS**.
- Direct transitive redundancy: **0**.
- Hard authority/order anchors: **PASS**.
- Unique bead receipt paths: **PASS**.

## Residual warnings

- The text heuristic flagged 30 acceptance clauses as not *obviously* machine-checkable. Manual inspection shows many are schema/contract assertions, so these were not auto-rewritten.
- Critical path uses unit bead weights; actual wall-clock critical path remains unknown.
- The 12 semantic phase-barrier relaxations are explicit planning judgments and should remain reviewable in the diff.
