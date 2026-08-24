# GitHub settings target

Task: `SETTINGS-20260822-01`  
Machine-readable target: `control/github-settings.target.json`

This document separates repository-controlled configuration from GitHub administrative settings. Do not infer that a target setting is active unless it has been independently observed after application.

## Observed state before this task

- Repository is public.
- Default branch is `main`.
- `main` had no branch protection and no required status checks.
- Merge commits, squash merges, and rebase merges were enabled.
- Auto-merge, update-branch, and delete-after-merge were disabled.
- CI and scheduled autoresearch used `ubuntu-latest`.

## Applied in repository code

- CI runner is pinned to `ubuntu-24.04`.
- Scheduled autoresearch runner is pinned to `ubuntu-24.04`.
- External actions remain pinned to full commit SHAs.
- CI remains `contents: read` and does not persist Git credentials.
- Scheduled autoresearch remains the only workflow with `contents: write` and can persist only `state/**` to `autoresearch/ratchet` after pre/post containment checks.
- CI cancels stale runs; scheduled research serializes instead of canceling in-flight state mutation.

## Administrative target

In **Settings → Actions → General**:

- Enable Actions.
- Choose **Allow selected actions and reusable workflows**.
- Allow actions created by GitHub.
- Do not broadly allow verified-creator or arbitrary third-party actions unless a later dependency task admits them.
- Require actions to be pinned to a full-length commit SHA where GitHub exposes that policy.
- Set default workflow permissions to read-only.
- Keep **Allow GitHub Actions to create and approve pull requests** off.
- For fork pull requests, require approval for all external contributors; do not send write tokens or secrets to forks.
- Set Actions log retention to 30 days.

For `main`, create a ruleset that:

- requires a pull request before merge;
- requires status check `test` and requires the branch to be current with `main`;
- requires conversation resolution;
- requires zero human approvals by default;
- blocks force pushes and deletion;
- does not require signed commits or linear history;
- leaves only an administrator emergency bypass.

In **Settings → General → Pull Requests**:

- keep merge commits enabled;
- keep squash merging enabled;
- disable rebase merging;
- enable auto-merge;
- enable update branch / always suggest updating pull-request branches where available;
- enable automatic deletion of head branches after merge.

In **Settings → Code security**:

- enable secret scanning;
- enable push protection;
- enable Dependabot alerts;
- enable Dependabot security updates;
- leave CodeQL default setup for a separately scoped security task so its runtime/noise can be evaluated independently.

## Why this is the selected path

The repository has one canonical reviewed branch and one scheduled state-only ratchet. The robust configuration therefore minimizes ambient authority: ordinary CI reads, the ratchet alone writes, external Actions are immutable-pinned, `main` is promotion-gated by the actual CI job, and no human approval is required merely to preserve autonomous throughput. Forks remain untrusted by default.

The explicit Ubuntu image reduces evaluator-environment drift relative to `ubuntu-latest`. Rebase merging is unnecessary because linear history is not an invariant here; merge commits preserve promotion provenance, while squash remains available for small branches.

## Residual

The connected GitHub tool can inspect repository metadata and edit repository files, but it does not expose mutation endpoints for Actions policy, branch rulesets/protection, merge preferences, retention, or code-security settings. Those administrative settings are therefore **target state, not claimed applied state** until verified separately.
