from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

EXPECTED_JSONL_SHA = '326e4a72c98647cde55aaba877c8d654be96cdfe402b52c4718aea51f512aaed'
EXPECTED_TODO_SHA = 'f0e657253ed7ebe6ddbe9e370dd0085e6410696bb1157c6c6f91123832773222'
PHASE_TITLES = {
'P0':'Truth surface','P1':'Canonical graph kernel v2','P2':'Verifier / replay / CI','P3':'Materiality adjudication',
'P4':'Relation-instance graph','P5':'Requirement compiler','P6':'Query + impact runtime','P7':'Mutation / promotion protocol','P8':'Holdout + resaturation'}
GATES = [
'Catalog size is not evidence of graph quality.',
'Zero rejected candidates is a suspicious adjudicator signal, not success.',
'Relation-type coverage is not relation-instance coverage.',
'Schema-valid is not semantically valid.',
'Passing tests are evidence, not proof of total correctness.',
'Generated closure is not silently promoted to canonical truth.',
'Every material canonical claim has provenance.',
'Every destructive canonical change has rollback and lineage.',
'Every saturation claim names grammar, source basis, holdout, simulator, and stopping rule.',
'New enumeration is blocked while a higher-value structural residual remains open.',
]

def sha(data: bytes) -> str: return hashlib.sha256(data).hexdigest()

def build(root: Path, out: Path) -> tuple[str,str]:
    phase_dir = root / 'beads' / 'phases'
    pieces = [(phase_dir / f'P{i}.jsonl').read_bytes() for i in range(9)]
    jsonl = b''.join(pieces)
    rows = [json.loads(x) for x in jsonl.decode().splitlines() if x.strip()]
    text = '# Beads TODO — Repository / Distinction Graph\n\n'
    text += 'Decomposition policy: **dependency-atomic** (winner of immutable-context-sim comparison).\n\n'
    text += '- Work beads: **106**\n- DAG: **acyclic**\n- Unit-weight critical path: **57 beads**\n- Initial runnable frontier: `RG-P0-01`\n\n'
    text += '## Closure rule\n\nA bead closes only when its single named outcome exists, its acceptance check passes, and the evidence/receipt is attributable to that bead. Discovery/decision, mutation, verification, and promotion remain separate when crossing an authority or rollback boundary.\n\n'
    text += '## Global acceptance gates\n\n'
    for i,g in enumerate(GATES,1): text += f'- **G{i}** — {g}\n'
    text += '\n'
    for p in [f'P{i}' for i in range(9)]:
        text += f'## {p} — {PHASE_TITLES[p]}\n\n'
        for r in [x for x in rows if x['phase']==p]:
            deps = ', '.join(r['depends_on']) if r['depends_on'] else 'none'
            text += f"- [ ] **{r['id']} — {r['title']}**\n  - Depends: `{deps}`\n  - Close when: {r['acceptance']}\n"
        if p != 'P8': text += '\n'
    out.mkdir(parents=True, exist_ok=True)
    (out/'BEADS.jsonl').write_bytes(jsonl)
    (out/'BEADS_TODO.md').write_text(text)
    js, ts = sha(jsonl), sha(text.encode())
    if js != EXPECTED_JSONL_SHA: raise SystemExit(f'BEADS.jsonl hash mismatch {js}')
    if ts != EXPECTED_TODO_SHA: raise SystemExit(f'BEADS_TODO.md hash mismatch {ts}')
    print(f'BEADS.jsonl {js}')
    print(f'BEADS_TODO.md {ts}')
    return js, ts

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parent); ap.add_argument('--out', type=Path, default=Path('/tmp/simsimmer-beads'))
    a=ap.parse_args(); build(a.root,a.out)
if __name__=='__main__': main()
