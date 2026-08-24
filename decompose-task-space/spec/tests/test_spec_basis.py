from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

SPEC = Path(__file__).resolve().parents[1]
MOD_PATH = SPEC / "simulate_spec_basis.py"
spec = importlib.util.spec_from_file_location("simulate_spec_basis", MOD_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)


class SpecBasisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.basis = json.loads((SPEC / "data" / "distinctions.json").read_text())

    def test_required_decomposition_layers_are_distinct(self):
        terms = set(self.basis["distinctions"]["DECOMPOSITION"])
        for term in ("task containment", "execution dependency", "frame", "operator", "witness/delta"):
            self.assertIn(term, terms)

    def test_product_includes_distinction_and_domain_specialization(self):
        total, probes = mod.schedule(self.basis, 32, 0.0, ["generic", "software"])
        self.assertGreater(total, 32)
        self.assertEqual(len(probes), 32)
        self.assertEqual(len({p["probe_id"] for p in probes}), 32)
        self.assertTrue(all("spec_distinction" in p["coordinate"] for p in probes))
        self.assertTrue(all("domain_specialization" in p["coordinate"] for p in probes))

    def test_unevaluated_probes_are_residual_not_fake_discoveries(self):
        _, probes = mod.schedule(self.basis, 16, 0.25, ["generic"])
        self.assertTrue(all(p["classification"] == "RESIDUAL" for p in probes))
        self.assertTrue(all(not p["evidence"] for p in probes))

    def test_ablation_covers_every_distinction(self):
        expected = sum(len(x) for x in self.basis["distinctions"].values())
        plan = mod.ablation_plan(self.basis)
        self.assertEqual(len(plan), expected)
        self.assertEqual(len({x["ablation_id"] for x in plan}), expected)

    def test_classification_vocabulary_exact(self):
        self.assertEqual(set(mod.CLASSIFICATIONS), {"DERIVED","NEW_WITNESS","NEW_COMPOSITION","CANDIDATE_PRIMITIVE","REDUNDANT","RESIDUAL"})


if __name__ == "__main__":
    unittest.main()
