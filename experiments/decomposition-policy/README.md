# Dependency-Atomic Decomposition Experiment

Status: imported simulation evidence; candidate execution graph, not silently activated canonical work.

`immutable-context-sim 1.1.0` compared six decomposition policies from the same immutable root. `dependency_atomic` ranked first in all five objective regimes: balanced, correctness-first, low-coordination, low-rework, and parallel-agents.

## Result
- 106 executable beads
- 0 mixed mutation+verification beads
- 0 hidden-decision beads
- dependency DAG acyclic
- unit-weight critical path: 57 beads
- 10 global invariants represented as acceptance gates, not fake tasks
- initial runnable frontier: `RG-P0-01`

The selected decomposition rule is: **one decision, mutation boundary, or independently verifiable outcome per bead.** Discovery → decision → implementation → verification → promotion are separated whenever authority, evidence, or rollback changes.

## Phase counts
| Phase | Beads |
|---|---:|
| P0 Truth surface | 10 |
| P1 Graph kernel v2 | 14 |
| P2 Verifier/replay/CI | 15 |
| P3 Materiality adjudication | 15 |
| P4 Relation-instance graph | 15 |
| P5 Requirement compiler | 7 |
| P6 Query/impact runtime | 11 |
| P7 Mutation/promotion | 10 |
| P8 Holdout/resaturation | 9 |
| **Total** | **106** |

## First chain
`RG-P0-01` snapshot canonical inventory + root hash → `RG-P0-02` classify canonical/derived/historical/generated, opening `RG-P0-03` canonical count scanner and `RG-P0-04` canonical hash scanner. In parallel `RG-P0-01` opens `RG-P0-05` bounded saturation vocabulary → `RG-P0-06` status-claim checker. `P0-03 + P0-04 + P0-05` open `RG-P0-07` generated manifest; `P0-01` opens `RG-P0-08` archive stale state; `P0-07 + P0-08` open `RG-P0-09` current-state receipt; `P0-06 + P0-09` open `RG-P0-10` one truth-surface audit command, which unlocks P1.

## Artifact discipline
The original 106-record `BEADS.jsonl` and complete `BEADS_TODO.md` are represented by one immutable phase-sharded source under `beads/phases/`. `build_decomposition_beads.py` reconstructs both byte-for-byte and requires their original SHA-256 hashes. `verify_decomposition_beads.py` independently recomputes graph counts, dependency integrity, frontier, critical path, gate coverage, and the 5/5 policy win.

The Library simulation receipt is identified by its exact source hash. The repository keeps a normalized JSON copy for semantic verification and explicitly does not claim byte identity for that normalized copy.

Repository-side verification must pass before this graph is promoted from imported planning evidence to active work.
