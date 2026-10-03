#!/usr/bin/env python3
"""Run Simsimmer's native CI checks locally without writing research state."""
import argparse
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    ("Repository doctor", ("scripts/doctor.py",), None),
    ("Research lifecycle tests", ("-m", "unittest", "discover", "-s", "tools/statecharts", "-v"), None),
    ("Research lifecycle diagram", ("-m", "tools.statecharts.render", "--check"), None),
    ("Simulator tests", ("-m", "unittest", "discover", "-s", "tests", "-v"), None),
    ("Specification basis tests", ("decompose-task-space/spec/tests/test_spec_basis.py", "-v"), None),
    ("Autoresearch smoke", ("autoresearch.py", "--variant", "exploit", "--iterations", "3", "--seed", "42"), None),
    ("Specification scheduler smoke", ("decompose-task-space/spec/simulate_spec_basis.py", "--limit", "16"), "spec-probes.json"),
    ("Architecture replay", ("tools/simulate_flywheel_architecture.py", "--out", "{temporary}/flywheel-receipt.json"), None),
    ("Bead graph verification", ("experiments/decomposition-policy/verify_decomposition_beads.py",), None),
)


def run_checks(checks=CHECKS):
    with tempfile.TemporaryDirectory(prefix="simsimmer-check-") as temporary:
        for name, arguments, output in checks:
            argv = [sys.executable, *(value.replace("{temporary}", temporary) for value in arguments)]
            print(f"CHECK {name}", flush=True)
            if output:
                with (Path(temporary) / output).open("w") as handle:
                    result = subprocess.run(argv, cwd=ROOT, stdout=handle)
            else:
                result = subprocess.run(argv, cwd=ROOT)
            if result.returncode:
                return max(1, result.returncode)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="Show checks without running them")
    args = parser.parse_args()
    if args.list:
        for name, _, _ in CHECKS:
            print(name)
        return 0
    return run_checks()


if __name__ == "__main__":
    raise SystemExit(main())
