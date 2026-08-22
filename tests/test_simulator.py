import json
import subprocess
import sys
import unittest
from pathlib import Path

from sim.simulator import BASELINE_POLICY, aggregate, normalize_policy

ROOT = Path(__file__).resolve().parents[1]

class SimulatorTests(unittest.TestCase):
    def test_deterministic(self):
        a = aggregate(BASELINE_POLICY, [101, 211], n_tasks=64, shift=0.2)
        b = aggregate(BASELINE_POLICY, [101, 211], n_tasks=64, shift=0.2)
        self.assertEqual(a, b)

    def test_policy_clamped(self):
        p = normalize_policy({"search_breadth": 999, "verify_rate": -4})
        self.assertEqual(p["search_breadth"], 10)
        self.assertEqual(p["verify_rate"], 0.0)

    def test_one_batch_runs(self):
        cp = subprocess.run(
            [sys.executable, str(ROOT / "autoresearch.py"), "--variant", "exploit", "--iterations", "3", "--seed", "42"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        receipt = json.loads(cp.stdout)
        self.assertEqual(receipt["variant"], "exploit")
        self.assertEqual(receipt["iterations"], 3)
        self.assertEqual(len(receipt["trials"]), 3)
        self.assertIn("canonical_holdout_fitness", receipt)
        self.assertTrue(all(t["status"] in {"KEEP", "REJECT"} for t in receipt["trials"]))

if __name__ == "__main__":
    unittest.main()
