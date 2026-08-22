# Agent Roles

Agents are fungible workers; authority is attached to repository contracts and evidence, not model identity.

Recommended roles:
- **coordinator** — owns task decomposition, write-zone assignment, integration order;
- **generator** — proposes candidates from a frozen experiment contract;
- **executor** — builds/runs candidates and emits receipts;
- **critic** — searches for counterexamples and missing distinctions;
- **reviewer** — independently checks candidate changes without relying on generator confidence;
- **historian/compiler** — relates traces, records negative knowledge, and proposes reusable abstractions;
- **release verifier** — checks promotion criteria against canonical evidence.

A worker and reviewer should be different lineages where practical. Agreement is not independent verification when prompts, evidence, model, or implementation lineage are shared.
