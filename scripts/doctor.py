from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "PROJECT_INTENT.md", "AGENTS.md", "CONTRIBUTING.md",
    "control/repository.manifest.json", "control/authority.json", "control/taxonomy.json",
    "docs/OWNERSHIP.md", "docs/research/REPOSITORY_DISTINCTIONS.md",
    "docs/architecture/FLYWHEEL.md", "docs/specs/EXPERIMENT_CONTRACT.md",
    "decompose-task-space/spec/SPEC_DISTINCTION_BASIS.md",
    "decompose-task-space/spec/EXTENSION_PROTOCOL.md",
    ".github/workflows/ci.yml", ".github/workflows/autoresearch.yml",
    ".github/dependabot.yml",
]
FORBIDDEN_TRACKED_PREFIXES = ("traces/raw/", "generated/tmp/", "artifacts/tmp/")
FULL_COMMIT_SHA = re.compile(r"[0-9a-f]{40}")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def tracked() -> list[str]:
    try:
        out = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    except Exception as exc:
        fail(f"cannot enumerate tracked files: {exc}")
    return [x for x in out.splitlines() if x]


def external_action_refs(workflow: Path) -> list[str]:
    refs: list[str] = []
    for raw in workflow.read_text().splitlines():
        line = raw.split("#", 1)[0].strip()
        match = re.search(r"(?:^|\s)uses:\s*([^\s]+)", line)
        if not match:
            continue
        ref = match.group(1)
        if ref.startswith("./"):
            continue
        refs.append(ref)
    return refs


def require_pinned_actions(workflow: Path) -> None:
    for ref in external_action_refs(workflow):
        if "@" not in ref:
            fail(f"external action missing ref in {workflow.relative_to(ROOT)}: {ref}")
        _name, revision = ref.rsplit("@", 1)
        if not FULL_COMMIT_SHA.fullmatch(revision):
            fail(
                f"external action is not pinned to a full commit SHA in "
                f"{workflow.relative_to(ROOT)}: {ref}"
            )


def main() -> int:
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            fail(f"missing required repository contract: {rel}")

    manifest = json.loads((ROOT / "control/repository.manifest.json").read_text())
    if manifest.get("schema") != "simsimmer/repository-manifest-v1":
        fail("unexpected repository manifest schema")
    if manifest.get("project", {}).get("simulate_before_generate") is not True:
        fail("simulate-before-generate invariant disabled")

    authority = json.loads((ROOT / "control/authority.json").read_text())
    if "human_explicit_instruction" not in authority.get("precedence", []):
        fail("authority precedence missing human explicit instruction")

    files = tracked()
    for path in files:
        if path.startswith(FORBIDDEN_TRACKED_PREFIXES):
            fail(f"ephemeral/raw output tracked as canonical Git state: {path}")

    ci_path = ROOT / ".github/workflows/ci.yml"
    autoresearch_path = ROOT / ".github/workflows/autoresearch.yml"
    for workflow_path in (ci_path, autoresearch_path):
        require_pinned_actions(workflow_path)

    ci = ci_path.read_text()
    if "contents: read" not in ci:
        fail("CI must keep GITHUB_TOKEN contents permission read-only")
    if "persist-credentials: false" not in ci:
        fail("CI checkout must not persist Git credentials")

    autoresearch = autoresearch_path.read_text()
    for token in (
        "ref: autoresearch/ratchet",
        "ratchet lane contains non-state divergence",
        "SIMSIMMER_SYNC_SHA",
        "autoresearch escaped state/ write boundary",
        "ratchet persistence contains non-state path",
        "git push origin HEAD:autoresearch/ratchet",
    ):
        if token not in autoresearch:
            fail(f"autoresearch containment token missing: {token}")
    if "contents: write" not in autoresearch:
        fail("scheduled ratchet requires explicit contents: write permission")

    dependabot = (ROOT / ".github/dependabot.yml").read_text()
    if 'package-ecosystem: "github-actions"' not in dependabot:
        fail("Dependabot must track pinned GitHub Actions revisions")

    ext = json.loads((ROOT / "control/external_references.json").read_text())
    for ref in ext.get("references", []):
        if ref.get("kind") == "git-reference" and not ref.get("commit"):
            fail(f"floating git reference: {ref.get('id')}")
        if ref.get("kind") == "library-artifact" and not ref.get("sha256"):
            fail(f"unhashed library artifact: {ref.get('id')}")

    print("OK: repository contracts, Actions pins/containment, provenance pins, and canonical/derived boundary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
