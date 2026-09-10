from __future__ import annotations
import re
from pathlib import Path

def parse_dimacs(path):
    path = Path(path); n = m_decl = None; clauses = []
    with path.open('r', encoding='utf-8', errors='replace') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('c'): continue
            if line.startswith('p '):
                parts = line.split()
                if len(parts) < 4 or parts[1] != 'cnf': raise ValueError("Expected DIMACS 'p cnf n m' header")
                n, m_decl = int(parts[2]), int(parts[3]); continue
            lits = [int(x) for x in line.split()]
            if 0 in lits: lits = lits[:lits.index(0)]
            if lits: clauses.append(lits)
    if n is None: raise ValueError('Missing DIMACS header')
    supports = [sorted({abs(x)-1 for x in c}) for c in clauses]
    return {'n':n,'m':len(clauses),'m_declared':m_decl,'clauses':clauses,'supports':supports}

def parse_fukuoka_gf2(path):
    path = Path(path); text = path.read_text(encoding='utf-8', errors='replace')
    n_match = re.search(r'Number of variables\s*\(n\)\s*:\s*(\d+)', text, re.I)
    m_match = re.search(r'Number of (?:equations|polynomials)\s*\(m\)\s*:\s*(\d+)', text, re.I)
    seed_match = re.search(r'Seed\s*:\s*(\d+)', text, re.I)
    if not n_match or not m_match: raise ValueError('Not a recognized Fukuoka GF(2) instance')
    n, m = int(n_match.group(1)), int(m_match.group(1))
    rows=[]
    for line in text.splitlines():
        if ';' not in line: continue
        vals=[int(v) for v in re.findall(r'(?<!\d)[01](?!\d)', line)]
        if vals: rows.append(vals)
    rows=rows[:m]
    if len(rows)!=m: raise ValueError(f'Expected {m} equations, parsed {len(rows)}')
    nonzero=[sum(r) for r in rows]
    return {'n':n,'m':m,'seed':int(seed_match.group(1)) if seed_match else None,'row_lengths':sorted({len(r) for r in rows}),'mean_nonzero_coefficients':sum(nonzero)/len(nonzero),'min_nonzero_coefficients':min(nonzero),'max_nonzero_coefficients':max(nonzero),'rows':rows}
