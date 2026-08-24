# Agent Mail coordination protocol

Status: **PINNED / READY FOR BOOTSTRAP, NOT YET INITIALIZED**

Agent Mail is the coordination layer for parallel bead execution. It is deliberately not the task ledger, evaluator, verifier, or promotion authority.

## Pin

Canonical pin: `coordination/agent-mail.lock.json`

- upstream: `Dicklesworthstone/mcp_agent_mail_rust`
- release: `v0.3.29`
- release commit: `ae1183b2489aa03f8852cc4d50221d4940981778`

Install only with the release-commit-pinned installer:

```bash
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/mcp_agent_mail_rust/ae1183b2489aa03f8852cc4d50221d4940981778/install.sh \
  | bash -s -- --version v0.3.29 --verify --no-service --yes
```

Or run:

```bash
bash coordination/install-agent-mail.sh
```

Then verify:

```bash
am --version
```

Do not silently follow `main` or auto-upgrade inside a research run.

## Boundary model

```text
BEAD GRAPH                canonical work truth
    |
    | selects legal runnable bead
    v
AGENT MAIL                coordination truth
    |- identity
    |- thread
    |- acknowledgements
    `- advisory file reservations
    |
    v
EXECUTION
    |
    v
ORACLE / REVIEW           evidence truth
    |
    v
PROMOTION GATE            canonical-state authority
```

Agent Mail messages and reservations may be cited as coordination evidence, but they do not close a bead and do not prove implementation correctness.

## Identity conventions

- Coordination project: the absolute path of the active Simsimmer checkout.
- Subject root: comes from the bead contract, especially `RG-P0-01`; it is not inferred from the Agent Mail project path.
- Agent identity: use the Agent Mail generated/registered identity. Do not encode permanent ownership into the agent name.
- Thread ID: **exact bead ID**, e.g. `RG-P0-01`.
- One bead may have many message attempts; do not create a new thread merely because an agent restarts.

## First-time bootstrap

From the active Simsimmer checkout:

1. Run `bash coordination/install-agent-mail.sh`.
2. Start Agent Mail explicitly; the pin uses `--no-service` so bootstrap does not silently install a background service.
3. Register/ensure the checkout as the Agent Mail project using its absolute path.
4. Register the active coding agent with its actual program/model metadata.
5. Let Agent Mail create its discovery metadata. If `.agent-mail.yaml` is produced, review it before committing; do not invent `project_uid` by hand.
6. Run one-agent smoke checks before any swarm execution:
   - project resolves;
   - agent registers;
   - self status/inbox is readable;
   - a short-lived reservation can be created and released;
   - a message can be written to and fetched from a bead-ID thread.
7. Record the Agent Mail version and project identity in the bead execution receipt.

MCP-equivalent primitives at the pinned release include:

```text
ensure_project(human_key=<absolute checkout path>)
register_agent(project_key=<absolute checkout path>, program=<actual>, model=<actual>)
file_reservation_paths(...)
send_message(..., thread_id=<bead ID>)
fetch_inbox(...)
```

## Per-bead operating loop

### 1. Select

Use canonical bead readiness first. Agent Mail does not decide what is runnable.

### 2. Claim coordination intent

For a selected bead:

- use `thread_id=<bead ID>`;
- send a short `START` message containing:
  - bead ID;
  - intended outcome;
  - files/surfaces expected to change;
  - current root/commit;
  - known risks or handoff boundaries.

A `START` message is not bead ownership and is not a promotion event.

### 3. Reserve write surfaces

Before editing shared files, reserve the narrowest practical project-relative paths.

Defaults for Simsimmer:

- exclusive reservation for files being mutated;
- shared/non-exclusive only for deliberately read-mostly coordination surfaces;
- default TTL: 3600 seconds;
- renew only while work is active;
- explicitly release on completion or handoff rather than relying on expiry.

Do not reserve `**/*`, the whole repository, or paths outside the active project merely for convenience.

### 4. Work and communicate deltas

Send messages only when they change another agent's decision:

- discovered dependency;
- changed interface/contract;
- blocked state;
- file-overlap conflict;
- test/evidence failure relevant to parallel work;
- handoff or reservation release.

Avoid broadcast-style chatter.

### 5. Handoff

Before releasing a bead to another agent, send a `HANDOFF` message in the same bead thread with:

- current commit/root;
- files changed;
- tests/evidence run;
- failing/unverified items;
- reservations being released;
- exact next unresolved action.

### 6. Close coordination, not truth

Agent Mail coordination is complete when:

- relevant handoff/status message is recorded;
- reservations are released or explicitly transferred;
- no outstanding acknowledgement blocks another agent.

The bead itself closes only through its configured acceptance authority.

## Reservation policy

Reservations are advisory leases, not locks or ownership.

Hard distinctions:

- reservation conflict != dependency block;
- expired reservation != permission to ignore current work evidence;
- claimed bead != verified bead;
- message acknowledgement != acceptance criterion;
- agent identity != authority role;
- file reservation != canonical scope grant.

When a reservation conflict appears:

1. inspect the conflicting agent and bead/thread;
2. coordinate in the relevant bead thread;
3. split paths if the work is actually independent;
4. otherwise serialize the writes;
5. record the resolution in the bead attempt receipt.

## Mapping into bead v3

Agent Mail should populate or reference these v3 fields without owning them:

```text
claim.agent_name        <- registered Agent Mail identity
claim.lease_expires_at  <- coordination lease/claim expiry if used
attempts[].actor        <- Agent Mail identity
attempts[].thread_id    <- exact bead ID
attempts[].reservation  <- reservation receipt/reference
attempts[].messages     <- selected message/thread references
```

Do not copy the full mailbox into bead records. Store stable references/receipts and preserve Agent Mail as its own append-only coordination substrate.

## Rollout plan

### R0 — Pin and contract

Complete when:

- exact upstream release/commit is pinned;
- AGENTS.md names Agent Mail's authority boundary;
- installation/bootstrap instructions exist.

### R1 — Single-agent smoke

Use `RG-P0-01` only.

Goal: prove project identity, bead-thread convention, reservations, and receipts without parallelism.

No P1-P8 execution yet.

### R2 — Two-agent non-overlap pilot

After `RG-P0-01` binds the subject and `RG-P0-02` classifies paths:

- choose two simultaneously runnable beads with disjoint write surfaces;
- use separate Agent Mail identities;
- use exact bead IDs as thread IDs;
- create narrow reservations;
- measure coordination overhead, stale-claim behavior, and handoff completeness.

### R3 — Deliberate conflict pilot

Create a controlled fixture where two agents would touch overlapping paths.

Pass if:

- reservation conflict is visible before conflicting writes;
- agents negotiate split/serialization;
- no bead dependency is invented merely from file contention;
- both attempts retain evidence.

### R4 — Router integration

Only after R1-R3:

- router excludes beads with unresolved write-surface conflicts when appropriate;
- claim availability and reservation contention become routing features, not legality overrides;
- routing receipts include Agent Mail coordination snapshot identity/time.

### R5 — Multi-agent execution

Enable broader parallel execution only when:

- subject root is bound;
- closure authority is explicit for active beads;
- Agent Mail bootstrap smoke passes at the pinned version;
- stale/expired reservations have a tested recovery path;
- every agent uses bead IDs for threads;
- handoff format is stable;
- router cannot convert coordination state into verification/promotion authority.

## Upgrade procedure

Agent Mail upgrades are explicit changes:

1. select candidate release/tag and commit;
2. inspect upstream release/changelog delta;
3. update `agent-mail.lock.json` on a dedicated diff;
4. repeat R1 smoke against the candidate;
5. run reservation-conflict and thread-continuity fixtures;
6. verify no change to Simsimmer evaluator/frozen seeds;
7. promote the new pin only with a receipt.

Never use an Agent Mail upgrade as an implicit side effect of starting a bead run.
