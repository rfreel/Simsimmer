from __future__ import annotations
import argparse, hashlib, json, subprocess, sys, tempfile
from collections import Counter, deque
from pathlib import Path

EXPECTED_JSONL_SHA='326e4a72c98647cde55aaba877c8d654be96cdfe402b52c4718aea51f512aaed'
EXPECTED_TODO_SHA='f0e657253ed7ebe6ddbe9e370dd0085e6410696bb1157c6c6f91123832773222'
PHASE_COUNTS={'P0':10,'P1':14,'P2':15,'P3':15,'P4':15,'P5':7,'P6':11,'P7':10,'P8':9}
GATES={f'G{i}' for i in range(1,11)}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fail(msg): print('FAIL:',msg,file=sys.stderr); raise SystemExit(1)

def verify(root: Path):
    with tempfile.TemporaryDirectory() as td:
        subprocess.run([sys.executable, str(root/'build_decomposition_beads.py'),'--root',str(root),'--out',td],check=True)
        b=Path(td)/'BEADS.jsonl'; t=Path(td)/'BEADS_TODO.md'
        if sha(b)!=EXPECTED_JSONL_SHA or sha(t)!=EXPECTED_TODO_SHA: fail('generated artifact hash mismatch')
        rows=[json.loads(x) for x in b.read_text().splitlines() if x.strip()]
    ids=[r['id'] for r in rows]
    if len(rows)!=106 or len(set(ids))!=106: fail('bead count/uniqueness')
    idset=set(ids)
    missing=sorted({d for r in rows for d in r['depends_on'] if d not in idset})
    if missing: fail(f'missing dependencies {missing}')
    if Counter(r['phase'] for r in rows)!=Counter(PHASE_COUNTS): fail('phase counts')
    if any(set(r['global_gates'])!=GATES for r in rows): fail('global gate coverage')
    indeg={i:0 for i in ids}; succ={i:[] for i in ids}
    for r in rows:
        for d in r['depends_on']: indeg[r['id']]+=1; succ[d].append(r['id'])
    frontier=sorted(i for i,n in indeg.items() if n==0)
    if frontier!=['RG-P0-01']: fail(f'initial frontier {frontier}')
    q=deque(frontier); topo=[]; dist={i:1 for i in ids}
    while q:
        u=q.popleft(); topo.append(u)
        for v in succ[u]:
            dist[v]=max(dist[v],dist[u]+1); indeg[v]-=1
            if indeg[v]==0:q.append(v)
    if len(topo)!=106: fail('cycle detected')
    if max(dist.values())!=57: fail(f'critical path {max(dist.values())}')
    receipt=json.loads((root/'receipts'/'BEADS_RECEIPT.json').read_text())
    if receipt['bead_count']!=106 or not receipt['dag_acyclic'] or receipt['critical_path_unit_beads']!=57: fail('DAG receipt')
    if receipt['jsonl_sha256']!=EXPECTED_JSONL_SHA or receipt['todo_sha256']!=EXPECTED_TODO_SHA: fail('receipt hashes')
    sim=json.loads((root/'receipts'/'DECOMPOSE_SIM_RECEIPT.json').read_text())
    if sim['winner']!='dependency_atomic': fail('sim winner')
    if sim['aggregate_rank'][0]['strategy']!='dependency_atomic' or sim['aggregate_rank'][0]['wins']!=5: fail('sim aggregate rank')
    for regime, ranking in sim['rankings'].items():
        if ranking[0]!='dependency_atomic': fail(f'{regime} winner')
    m=sim['metrics']['dependency_atomic']
    if m['hidden_decisions']!=0 or m['mixed_mutation_verification']!=0 or m['invariant_gate_coverage']!=1.0: fail('atomicity invariants')
    print('OK: 106 dependency-atomic beads; DAG acyclic; frontier RG-P0-01; critical path 57; 10/10 gates; dependency_atomic wins 5/5 regimes')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent); a=ap.parse_args(); verify(a.root)
if __name__=='__main__':main()
