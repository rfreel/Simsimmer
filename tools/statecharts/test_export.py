import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.statecharts.export import ROOT, contract, trace
from tools.statecharts.research import ResearchLifecycle


class ExportTests(unittest.TestCase):
    def test_contract_binds_actual_sources_and_unique_edges(self):
        model = contract()
        for name, digest in model['source_bindings'].items():
            self.assertEqual(digest, hashlib.sha256((ROOT / name).read_bytes()).hexdigest())
        ids = [edge['id'] for edge in model['transitions']]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual({state['id'] for state in model['states'] if state['final']}, {'complete', 'failed'})

    def test_trace_preserves_observed_guards_and_digest(self):
        machine = ResearchLifecycle(state='verified')
        machine.send('dry_run', dry_run=True)
        result = trace(machine, b'model', {'source': 'a' * 64})
        self.assertEqual(result['contract_sha256'], hashlib.sha256(b'model').hexdigest())
        self.assertEqual(result['steps'], [{'event': 'dry_run', 'transition': 'verified_dry_run',
                                          'target': 'complete', 'guards': {'dry_run': True}}])

    def test_cli_real_dry_run_and_preserve_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            model = Path(directory) / 'model.json'
            observed = Path(directory) / 'trace.json'
            command = [sys.executable, '-m', 'tools.statecharts.export', '--contract-out', str(model),
                       '--trace-out', str(observed), '--iterations', '0', '--seed', '42']
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            observation = json.loads(observed.read_text())
            self.assertEqual(observation['contract_sha256'], hashlib.sha256(model.read_bytes()).hexdigest())
            self.assertEqual(observation['steps'][-1]['event'], 'dry_run')
            self.assertEqual(observation['steps'][-1]['target'], 'complete')
            before = model.read_bytes(), observed.read_bytes()
            rerun = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(rerun.returncode, 2)
            self.assertEqual(before, (model.read_bytes(), observed.read_bytes()))
