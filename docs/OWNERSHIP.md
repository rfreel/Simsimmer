# Ownership and Collision Avoidance

This file defines write ownership, not merely code review preference.

| Surface | Canonical role | Normal writer | Concurrent rule |
|---|---|---|---|
| `PROJECT_INTENT.md`, `control/**` | authority/control plane | coordinator | exclusive |
| `sim/**`, `tests/**`, `evaluator.lock.json` | trusted evaluator | evaluator-change task | exclusive + review |
| `autoresearch.py`, `variants/**` | search controller | research-controller task | exclusive per file |
| `state/**` | live research state | `autoresearch/ratchet` or explicit state task | single writer |
| `experiments/<id>/**` | noncanonical experiment | experiment owner | exclusive by experiment ID |
| `agents/**` | agent role contracts | coordination task | disjoint files |
| `scripts/**` | operational procedures | tooling task | disjoint files |
| `tools/**` | reusable mechanisms | tool owner | disjoint subtrees |
| `knowledge/**` | retained learning | compiler/reviewer | append/additive by record |
| `vendor/**` | pinned imported source | dependency-update task | immutable otherwise |
| `artifacts/**`, `generated/**`, `traces/raw/**` | derived output | automation | not canonical source |

## Claim protocol
Before writing, create or update a task/experiment record declaring:
- `id`
- `owner`
- `branch`
- `root_sha`
- `write_paths`
- `read_dependencies`
- `status`

Two live agents may read the same files. They may not concurrently own overlapping write paths unless the task explicitly defines a merge coordinator and isolated branches/worktrees.

## Canonical branches
- `main`: reviewed/promoted state.
- `autoresearch/ratchet`: scheduled research state only; may persist only `state/**`.
- `agent/<task>`: scoped implementation/research.
- `exp/<experiment-id>`: generated/experimental implementations.

## External coordination
Adapters such as Beads, `bv`, Agent Mail, NTM, CASS/CM, UBS, DCG, or RCH may mirror or operate on repository state. They do not become sole canonical authority. Every externally owned stateful object must have a repository-native ID, provenance pointer, or reconstructable receipt.
