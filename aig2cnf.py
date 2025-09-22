#!/usr/bin/env python3
"""
Translate ASCII AIGER (.aig) into DIMACS CNF while preserving mapping.

Outputs:
  problem.cnf   - DIMACS CNF with clauses
  mapping.json  - var <-> signal mapping

Supports optional assignments:
  python aig_to_cnf.py top.aig d=1 f=0 g=1
"""

import sys, json

if len(sys.argv) < 2:
    print("Usage: python aig_to_cnf.py <aigfile> [signal=value ...]")
    sys.exit(1)

aigfile = sys.argv[1]
assignments = {}
for arg in sys.argv[2:]:
    if "=" not in arg:
        continue
    sig, val = arg.split("=")
    assignments[sig.strip()] = int(val)

with open(aigfile) as f:
    lines = [ln.strip() for ln in f if ln.strip()]

hdr = lines[0].split()
assert hdr[0] == "aag", "Need ASCII AIGER input"
M, I, L, O, A = map(int, hdr[1:])

inputs  = lines[1:1+I]
latches = lines[1+I:1+I+L]
outputs = lines[1+I+L:1+I+L+O]
ands    = lines[1+I+L+O:1+I+L+O+A]

symbols = {}
for ln in lines[1+I+L+O+A:]:
    if ln[0] in ("i","o","l"):
        typ = ln[0]
        idx, name = ln[1:].split(" ",1)
        symbols[(typ,int(idx))] = name

def lit2var(lit):
    return lit//2, bool(lit&1)

clauses = []

def encode_and(z, x, xinv, y, yinv):
    # z = (x ^ xinv) & (y ^ yinv)
    # Clause 1: (¬(x^xinv) ∨ ¬(y^yinv) ∨ z)
    clauses.append([ -( -x if xinv else x ),
                     -( -y if yinv else y ),
                      z ])
    # Clause 2: ((x^xinv) ∨ ¬z)
    clauses.append([ (-x if xinv else x), -z ])
    # Clause 3: ((y^yinv) ∨ ¬z)
    clauses.append([ (-y if yinv else y), -z ])

# Encode ANDs
for ln in ands:
    lhs, rhs0, rhs1 = map(int, ln.split())
    z, zinv = lit2var(lhs)
    if zinv:
        raise RuntimeError("Unexpected inverted AND lhs")
    x, xinv = lit2var(rhs0)
    y, yinv = lit2var(rhs1)
    encode_and(z, x, xinv, y, yinv)

# Build mapping
signal2var, var2signal = {}, {}
for (typ, idx), name in symbols.items():
    if typ=="i":
        aigvar = int(inputs[idx])//2
        signal2var[name] = aigvar
        var2signal[aigvar] = name
    elif typ=="o":
        lit = int(outputs[idx])
        v, inv = lit2var(lit)
        signal2var[name] = v
        var2signal[v] = name

# Apply assignments
for sig, val in assignments.items():
    if sig not in signal2var:
        print(f"Warning: signal {sig} not found in mapping, skipping")
        continue
    v = signal2var[sig]
    lit = v if val==1 else -v
    clauses.append([lit])

# Save mapping
with open("mapping.json","w") as f:
    json.dump({"var_to_signal": var2signal}, f, indent=2)

# Save CNF
num_vars = M
num_clauses = len(clauses)
with open("problem.cnf","w") as f:
    for v,n in var2signal.items():
        f.write(f"c var {v} {n}\n")
    f.write(f"p cnf {num_vars} {num_clauses}\n")
    for cl in clauses:
        f.write(" ".join(str(l) for l in cl) + " 0\n")

print(f"Wrote problem.cnf with {num_vars} vars, {num_clauses} clauses")
print("Mapping saved to mapping.json")
if assignments:
    print("Applied assignments:", assignments)
