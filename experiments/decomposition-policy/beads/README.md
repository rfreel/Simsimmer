# Dependency-Atomic Bead Graph

This directory preserves the exact imported 106-bead graph as immutable phase shards.

Why phase shards instead of a second hand-edited monolith: `BEADS.jsonl` and `BEADS_TODO.md` are derived artifacts with existing content hashes. Keeping one source representation prevents the human-readable TODO and machine-readable graph from drifting apart.

Reconstruct and verify both original artifacts:

```bash
python experiments/decomposition-policy/build_decomposition_beads.py
python experiments/decomposition-policy/verify_decomposition_beads.py
```

Expected generated hashes:

- `BEADS.jsonl`: `326e4a72c98647cde55aaba877c8d654be96cdfe402b52c4718aea51f512aaed`
- `BEADS_TODO.md`: `f0e657253ed7ebe6ddbe9e370dd0085e6410696bb1157c6c6f91123832773222`

The imported records are planning evidence. `status: open` means unfinished in the source bead graph; it does **not** mean the bead is active or claimed in Simsimmer. Promotion to `state/active/` is a separate authority transition.

The selected decomposition invariant is:

> one decision, mutation boundary, or independently verifiable outcome per bead.

Discovery → decision → implementation → verification → promotion remain separate whenever authority, evidence, or rollback changes.
