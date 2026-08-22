from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "PROJECT_INTENT.md", "AGENTS.md", "CONTRIBUTING.md",
    "control/repository.manifest.json", "control/authority.json", "control/taxonomy.json",
    "docs/OWNERSHIP.md", "docs/research/REPOSITORY_DISTINCTIONS.md",
    "docs/architecture/FLYWHEEL.md", "docs/specs/EXPERIMENT_CONTRACT.md",
    "decompose-task-space/spec/SPEC_DISTINCTION_BASIS.md",
    "decompose-task-space/spec/EXTENSION_PROTOCOL.md",
]
FORBIDDEN_TRACKED_PREFIXES = ("traces/raw/", "generated/tmp/", "artifacts/tmp/")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def tracked() -> list[str]:
    try:
        out = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    except Exception as exc:
        fail(f"cannot enumerate tracked files: {exc}")
    return [x for x in out.splitlines() if x]


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

    workflow = (ROOT / ".github/workflows/autoresearch.yml").read_text()
    for token in ("ref: autoresearch/ratchet", "state/*", "escaped state/ write boundary"):
        if token not in workflow:
            fail(f"autoresearch containment token missing: {token}")

    ext = json.loads((ROOT / "control/external_references.json").read_text())
    for ref in ext.get("references", []):
        if ref.get("kind") == "git-reference" and not ref.get("commit"):
            fail(f"floating git reference: {ref.get('id')}")
        if ref.get("kind") == "library-artifact" and not ref.get("sha256"):
            fail(f"unhashed library artifact: {ref.get('id')}")

    print("OK: repository contracts, containment, provenance pins, and canonical/derived boundary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
