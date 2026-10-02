# Bead-system distinctions v3

Status: proposed canonical research guidance for the repository/distinction bead plan.

## Representation boundaries

1. Plan space / bead space / code space / evidence space.
2. Host repository / subject repository / simulator root / evaluator root / output root.
3. Canonical bead state / derived scheduler state.
4. Work ledger / routing engine / verifier / promotion authority.
5. Declared priority / graph-derived leverage.
6. Ready / important.
7. Runnable / claimed / executed / verified / promotable / promoted.
8. Narrative acceptance criterion / executable oracle / authorized review witness.
9. Implementation proposal / required outcome.
10. Current state / historical state / replayed state.

## Relation semantics

11. Blocking relation / descriptive relation.
12. `BLOCKS` / `WAITS_FOR` / `CONDITIONAL_BLOCKS`.
13. Hierarchy (`PARENT_OF`) / execution dependency.
14. `RELATED_TO` / dependency.
15. `DISCOVERED_FROM` / causation.
16. `CAUSED_BY` / provenance.
17. `DUPLICATES` / semantic equivalence / alias.
18. `SUPERSEDES` / deletes / invalidates.
19. Direct dependency / transitive dependency.
20. Asserted relation / inferred relation.
21. Canonical relation / derived closure.
22. Edge type / edge instance.
23. Pairwise edge / hyperedge.
24. Directional relation / symmetric relation.
25. Blocking now / potentially blocking under condition.
26. Local-project relation / cross-project routed relation.

## Scheduling semantics

27. Legality filter / optimization score.
28. Topological readiness / phase membership.
29. Critical-path contribution / centrality.
30. PageRank / betweenness / HITS / eigenvector / degree.
31. Downstream unblock count / global influence.
32. Quick win / bottleneck / keystone / high-priority task.
33. Single-next recommendation / parallel execution tracks.
34. Static priority / dynamic routing recommendation.
35. Cost estimate / observed cost.
36. Expected duration / retry risk / review delay.
37. Worker availability / mutable-surface contention.
38. Parallelizable in graph / safe to execute concurrently.
39. Metric computed / approximate / timed out / skipped.
40. Scheduler recommendation / execution authority.

## Work-item semantics

41. Atomic execution boundary / tiny description.
42. Rich bead context / mixed responsibility.
43. Bead / epic / task / question / bug / feature / chore / docs.
44. Parent-child organization / hard prerequisite.
45. Open / in-progress / blocked / deferred / draft / closed / tombstoned / pinned.
46. Closed / verified.
47. Closed reason / verification receipt.
48. Assignee / owner / verifier / promoter.
49. Claim / lease / permanent ownership.
50. Claimed / actively progressing / stale claim.
51. Work estimate / scheduling priority.
52. Source requirement / derived task.
53. Bead-local notes / canonical specification.
54. Comment history / state transition evidence.
55. Retry / new attempt.
56. Failure history / current outcome.

## Evidence and closure

57. Evidence / assertion.
58. Machine-checkable oracle / review witness.
59. PASS / FAIL / NEEDS_REVIEW / UNRESOLVED.
60. Execution success / acceptance satisfaction.
61. Acceptance satisfaction / authorization to promote.
62. Verifier identity / worker identity.
63. Candidate-controlled code / evaluator-controlled code.
64. Oracle hash / subject-root hash.
65. Fresh evidence / stale evidence.
66. Evidence completeness / graph completeness.
67. Test passing / total correctness.
68. Close reason / causal explanation.
69. Verification receipt / promotion receipt.
70. Independent verifier / self-verification.

## State, sync, and history

71. Fast local working state / git-friendly canonical export.
72. SQLite state / JSONL export.
73. Auto-flush / git commit.
74. Export / import / reconcile / merge.
75. Local mutation / remote synchronization.
76. Base snapshot / left state / right state.
77. Delete / tombstone.
78. Conflict / deterministic merge.
79. Current graph hash / historical graph hash.
80. Data hash / metric cache key.
81. Point-in-time graph / present graph.
82. Semantic diff / byte diff.
83. Reopen / retry / supersede.
84. Stale record / invalid record.

## Multi-agent coordination

85. Bead identity / coordination-thread identity.
86. Claim / file reservation.
87. Graph readiness / coordination availability.
88. Runnable work / already claimed work.
89. Agent assignment / routing recommendation.
90. Shared workspace / isolated worktree.
91. Parallel graph tracks / parallel write safety.
92. Agent failure / bead failure.
93. Stale claim / blocked bead.
94. Coordination metadata / canonical work semantics.
95. Actor / session / attempt.
96. Fungible worker / authoritative reviewer.

## Materiality guards

97. Graph centrality / decision relevance.
98. High fan-out / high value.
99. High priority / unblocked.
100. Many dependencies / justified complexity.
101. Rich implementation sketch / binding design decision.
102. More beads / better decomposition.
103. More edges / better graph.
104. Dense graph / complete graph.
105. Plan coverage / decision coverage.
106. Bead closure / project completion.
107. Router confidence / truth confidence.
108. Simulation result / real execution evidence.
109. Synthetic cost prior / calibrated cost prior.
110. Scheduling gain / semantic correctness.

## Required consequences

- Only blocking relation types affect `ready`.
- Hierarchy is nonblocking unless a separate blocking relation exists.
- Routing consumes the ready set; it cannot make blocked work runnable.
- The router is derived state and may be recomputed without mutating the bead ledger.
- Every routing output carries a source graph hash and per-metric computation status.
- Closing a bead does not imply verification or promotion.
- Rich context is encouraged, but each bead keeps one independently closable outcome boundary.
- Implementation sketches are advisory unless explicitly frozen by an authority-bearing decision.
- One stable bead ID should connect task state, receipts, coordination threads, file reservations, and relevant commits.
- Historical failures and retries are retained rather than overwritten.
- Cross-project routing is explicit and must not weaken subject-root binding.
