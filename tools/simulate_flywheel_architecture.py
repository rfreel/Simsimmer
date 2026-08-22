from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROLES = ["task_graph","routing","coordination","lifecycle","memory","qa","security","remote_execution","spec_basis","trace_compiler"]
MODES = ["none","native","external","hybrid"]
STATEFUL = {"task_graph","coordination","lifecycle","memory","spec_basis","trace_compiler"}
EXTERNAL_STRENGTH = {"task_graph":3.0,"routing":4.0,"coordination":4.0,"lifecycle":3.0,"memory":4.0,"qa":4.0,"security":3.0,"remote_execution":3.0,"spec_basis":1.0,"trace_compiler":1.0}
COMPLEXITY = {"none":0.0,"native":1.0,"external":1.25,"hybrid":1.8}
BOOTSTRAP_ACTIVE_ROLE_CAP = 7
REQUIRED_FROM_BOOTSTRAP = {"spec_basis","trace_compiler"}


def score(cfg: dict[str,str], stage: str) -> float:
    if any(cfg[r] == "none" for r in REQUIRED_FROM_BOOTSTRAP):
        return float("-inf")
    if stage == "bootstrap" and sum(m != "none" for m in cfg.values()) > BOOTSTRAP_ACTIVE_ROLE_CAP:
        return float("-inf")
    total = 0.0
    for role, mode in cfg.items():
        if mode == "none": continue
        base = EXTERNAL_STRENGTH[role]
        if mode == "native": total += 2.6 + (1.4 if role in STATEFUL else 0.0)
        elif mode == "external": total += base
        else: total += 2.6 + base + (1.8 if role in STATEFUL else 0.5)
        total -= COMPLEXITY[mode] * (1.0 if stage == "bootstrap" else 0.45)
    for role in STATEFUL:
        if cfg[role] == "external": return float("-inf")
    if cfg["routing"] != "none" and cfg["task_graph"] == "none": return float("-inf")
    if cfg["remote_execution"] != "none" and cfg["qa"] == "none": return float("-inf")
    if cfg["trace_compiler"] != "none" and cfg["memory"] == "none": return float("-inf")
    if cfg["spec_basis"] != "none" and cfg["task_graph"] == "none": return float("-inf")
    if cfg["task_graph"] != "none" and cfg["routing"] != "none": total += 3.0
    if cfg["coordination"] != "none" and cfg["task_graph"] != "none": total += 2.5
    if cfg["memory"] != "none" and cfg["qa"] != "none": total += 2.2
    if cfg["spec_basis"] != "none" and cfg["trace_compiler"] != "none": total += 3.2
    if cfg["trace_compiler"] != "none" and cfg["memory"] != "none": total += 2.8
    if stage == "bootstrap": total -= 1.3 * sum(m != "none" for m in cfg.values())
    else: total += 0.8 * sum(m == "hybrid" for m in cfg.values())
    return total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="experiments/flywheel-architecture/receipt.json")
    args = ap.parse_args()
    best: dict[str, tuple[float,dict[str,str]]] = {}
    count = 0
    for modes in itertools.product(MODES, repeat=len(ROLES)):
        cfg = dict(zip(ROLES, modes)); count += 1
        for stage in ("bootstrap","long_term"):
            value = score(cfg, stage)
            if stage not in best or value > best[stage][0]: best[stage] = (value, dict(cfg))
    receipt = {
        "schema":"simsimmer/flywheel-architecture-sim-v2",
        "space_size":count,
        "bootstrap_active_role_cap":BOOTSTRAP_ACTIVE_ROLE_CAP,
        "required_from_bootstrap":sorted(REQUIRED_FROM_BOOTSTRAP),
        "bootstrap":{"score":best["bootstrap"][0],"configuration":best["bootstrap"][1]},
        "long_term":{"score":best["long_term"][0],"configuration":best["long_term"][1]},
        "classification":"synthetic architecture evidence",
        "limits":["finite declared topology only","hand-authored score model","requires downstream empirical validation"],
    }
    payload = json.dumps(receipt, sort_keys=True, separators=(",",":"))
    receipt["receipt_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print(json.dumps(receipt,indent=2,sort_keys=True)); return 0

if __name__ == "__main__": raise SystemExit(main())
