"""Export the native model and a real dry-run trace for Repo Defaults auditing.

No write-mode option is exposed. Source hashes bind model and controller bytes;
this trace proves model conformance only, alongside independent controller tests.
"""
import argparse
from contextlib import redirect_stdout
import hashlib
import json
from pathlib import Path
import sys

from .research import ACTIVE, TRANSITIONS, ResearchLifecycle

ROOT = Path(__file__).resolve().parents[2]


def contract():
    edges = list(TRANSITIONS) + [(state, 'infrastructure_error', 'failed', None) for state in sorted(ACTIVE)]
    states = sorted({item for source, _, target, _ in edges for item in (source, target)})
    return {
        'version': 1,
        'id': 'SimsimmerResearch',
        'initial': 'idle',
        'source_bindings': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                            for name in ('autoresearch.py', 'tools/statecharts/research.py', 'tools/statecharts/export.py')},
        'states': [{'id': state, 'final': state in {'complete', 'failed'}} for state in states],
        'transitions': [dict(id=f'{source}_{event}', source=source, event=event, target=target,
                             **({'guard': guard} if guard else {})) for source, event, target, guard in edges],
    }


def trace(machine, model_bytes, bindings):
    return {'version': 1, 'contract_sha256': hashlib.sha256(model_bytes).hexdigest(),
            'source_bindings': bindings, 'initial': 'idle',
            'steps': [{'transition': f"{step['source']}_{step['event']}", 'event': step['event'],
                       'target': step['target'], 'guards': step['guards']} for step in machine.trace]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--contract-out', type=Path, required=True)
    parser.add_argument('--trace-out', type=Path)
    parser.add_argument('--variant', choices=['explore', 'exploit', 'transfer', 'compress'], default='exploit')
    parser.add_argument('--iterations', type=int, default=3)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    destinations = [path for path in (args.contract_out, args.trace_out) if path]
    if len({path.resolve() for path in destinations}) != len(destinations):
        parser.error('contract and trace outputs must differ')
    # Outputs are derived evidence. Never overwrite an existing file or source.
    if any(path.exists() or path.is_symlink() for path in destinations):
        parser.error('choose new output paths; existing files are preserved')
    model = contract()
    raw = (json.dumps(model, indent=2, sort_keys=True) + '\n').encode()
    observation = None
    if args.trace_out:
        import autoresearch
        machine = ResearchLifecycle()
        with redirect_stdout(sys.stderr):
            autoresearch.run(argparse.Namespace(variant=args.variant, iterations=args.iterations,
                                               seed=args.seed, write=False), machine)
        observation = trace(machine, raw, model['source_bindings'])
    with args.contract_out.open('xb') as handle:
        handle.write(raw)
    if observation is not None:
        with args.trace_out.open('x', encoding='utf-8') as handle:
            handle.write(json.dumps(observation, indent=2, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
