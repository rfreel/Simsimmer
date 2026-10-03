import argparse
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import autoresearch as controller
from tools.statecharts.research import InvalidTransition, ResearchLifecycle


def metric(fitness=1., basis=10.):
    return SimpleNamespace(fitness=fitness, active_basis=basis, solved_rate=0., transfer_rate=0., rediscovery_rate=0., compute_per_task=0.)


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.args = argparse.Namespace(variant='exploit', iterations=1, seed=42, write=False)
        self.machine = ResearchLifecycle()
        self.enterContext(patch.object(controller, 'STATE_DIR', self.root))
        self.enterContext(patch.object(controller, 'RESULTS', self.root / 'results.jsonl'))
        self.lock = self.enterContext(patch.object(controller, 'check_lock'))
        self.enterContext(patch.object(controller, 'load_variant', return_value={}))
        self.enterContext(patch.object(controller, 'load_policy', return_value={'candidate': False}))
        self.enterContext(patch.object(controller, 'mutate', return_value=({'candidate': True}, 'mutation')))
        self.evaluation = self.enterContext(patch.object(controller, 'evaluate', side_effect=[(metric(), metric()), (metric(2), metric(2))]))
        self.canonical = self.enterContext(patch.object(controller, 'canonical_evaluate', return_value=metric(2)))
        self.enterContext(patch.object(controller, 'metrics_dict', side_effect=vars))

    def execute(self):
        output = io.StringIO()
        with redirect_stdout(output):
            code = controller.run(self.args, self.machine)
        self.assertEqual(code, 0)
        self.assertEqual(self.machine.state, 'complete')
        return json.loads(output.getvalue())

    def events(self):
        return [step['event'] for step in self.machine.trace]

    def test_keep_and_dry_run(self):
        receipt = self.execute()
        self.assertEqual(receipt['trials'][0]['status'], 'KEEP')
        self.assertTrue(receipt['policy']['candidate'])
        self.assertIn('keep', self.events())
        self.assertEqual(self.events()[-1], 'dry_run')
        self.assertEqual(list(self.root.iterdir()), [])

    def test_reject_preserves_policy(self):
        self.evaluation.side_effect = [(metric(), metric()), (metric(0), metric(0))]
        receipt = self.execute()
        self.assertEqual(receipt['trials'][0]['status'], 'REJECT')
        self.assertFalse(receipt['policy']['candidate'])
        self.assertIn('reject', self.events())

    def test_holdout_floor_and_compression_alternative(self):
        self.args.variant = 'compress'
        self.evaluation.side_effect = [(metric(), metric()), (metric(0), metric(.96, 9))]
        receipt = self.execute()
        self.assertEqual(receipt['trials'][0]['status'], 'KEEP')

    def test_train_improvement_cannot_override_holdout_failure(self):
        self.evaluation.side_effect = [(metric(), metric()), (metric(2), metric(.8))]
        self.assertEqual(self.execute()['trials'][0]['status'], 'REJECT')

    def test_lock_failure_stops_before_evaluation_or_writes(self):
        self.args.write = True
        self.lock.side_effect = SystemExit('evaluator lock mismatch')
        with self.assertRaises(SystemExit):
            controller.run(self.args, self.machine)
        self.evaluation.assert_not_called()
        self.assertEqual(self.machine.state, 'failed')
        self.assertEqual(list(self.root.iterdir()), [])
        self.assertNotIn('reject', self.events())

    def test_evaluation_error_is_not_reject(self):
        self.evaluation.side_effect = [(metric(), metric()), RuntimeError('infrastructure')]
        with self.assertRaisesRegex(RuntimeError, 'infrastructure'):
            controller.run(self.args, self.machine)
        self.assertEqual(self.machine.state, 'failed')
        self.assertNotIn('reject', self.events())
        self.assertEqual(list(self.root.iterdir()), [])

    def test_invalid_initial_transition_has_no_side_effects(self):
        self.machine.state = 'complete'
        with self.assertRaises(InvalidTransition):
            controller.run(self.args, self.machine)
        self.lock.assert_not_called()
        self.assertEqual(list(self.root.iterdir()), [])

    def test_promotion_boundaries(self):
        # Separate real writes in isolated state directories; old champion retained
        # byte-for-byte when canonical score/basis gates do not authorize promotion.
        for new_score, new_basis, expected in [(3., 11., True), (2., 9., True), (2., 10., False), (1., 1., False), (2. + 5e-10, 10., False), (2., 10. - 5e-10, False)]:
            with self.subTest(score=new_score, basis=new_basis):
                old = '{"canonical_holdout_fitness":2.0,"canonical_holdout":{"active_basis":10.0},"sentinel":true}'
                champion = self.root / 'champion.json'
                champion.write_text(old)
                self.machine = ResearchLifecycle()
                self.args.write = True
                self.args.iterations = 0
                self.evaluation.side_effect = [(metric(), metric())]
                self.canonical.return_value = metric(new_score, new_basis)
                self.execute()
                self.assertEqual(champion.read_text() != old, expected)
                self.assertIn('promote' if expected else 'retain', self.events())
                self.assertTrue((self.root / 'exploit.json').exists())

    def test_persistence_failure_propagates(self):
        self.args.write = True
        with patch.object(Path, 'write_text', side_effect=OSError('disk full')):
            with redirect_stdout(io.StringIO()), self.assertRaisesRegex(OSError, 'disk full'):
                controller.run(self.args, self.machine)
        self.assertEqual(self.machine.state, 'failed')
        self.assertNotIn('champion_written', self.events())

    def test_rejected_write_transition_prevents_all_persistence(self):
        self.args.write = True
        send = self.machine.send
        def reject_write(event, **guards):
            if event == 'write_requested':
                raise InvalidTransition('write blocked')
            send(event, **guards)
        with patch.object(self.machine, 'send', side_effect=reject_write):
            with redirect_stdout(io.StringIO()), self.assertRaisesRegex(InvalidTransition, 'write blocked'):
                controller.run(self.args, self.machine)
        self.assertEqual(list(self.root.iterdir()), [])
        self.assertEqual(self.machine.state, 'failed')

    def test_rejected_promotion_preserves_champion(self):
        self.args.write = True
        champion = self.root / 'champion.json'
        old = '{"canonical_holdout_fitness":1.0,"canonical_holdout":{"active_basis":10.0}}'
        champion.write_text(old)
        send = self.machine.send
        def reject_promotion(event, **guards):
            if event == 'promote':
                raise InvalidTransition('promotion blocked')
            send(event, **guards)
        with patch.object(self.machine, 'send', side_effect=reject_promotion):
            with redirect_stdout(io.StringIO()), self.assertRaisesRegex(InvalidTransition, 'promotion blocked'):
                controller.run(self.args, self.machine)
        self.assertEqual(champion.read_text(), old)
        self.assertTrue((self.root / 'exploit.json').exists())
        self.assertTrue((self.root / 'results.jsonl').exists())
        self.assertEqual(self.machine.state, 'failed')


class MachineTests(unittest.TestCase):
    def test_forbidden_and_false_guard_leave_machine_unchanged(self):
        machine = ResearchLifecycle(state='verified')
        for event, guards in [('promote', {'promotable': True}), ('write_requested', {'write_enabled': False}), ('write_requested', {}), ('write_requested', {'write_enabled': 1})]:
            with self.assertRaises(InvalidTransition):
                machine.send(event, **guards)
            self.assertEqual(machine.state, 'verified')
            self.assertEqual(machine.trace, [])
        machine.send('write_requested', write_enabled=True)
        self.assertEqual(machine.state, 'persisting')

    def test_duplicate_terminal_event_rejected(self):
        machine = ResearchLifecycle(state='verified')
        machine.send('dry_run', dry_run=True)
        with self.assertRaises(InvalidTransition):
            machine.send('dry_run', dry_run=True)
        self.assertEqual(machine.state, 'complete')
