#!/usr/bin/env python3
"""Structural summary for public DIMACS CNF benchmarks. Does not perform key recovery."""
from pathlib import Path
import argparse, json
import networkx as nx
import pandas as pd

def parse(path):
    n=m=None; clauses=[]
    for line in Path(path).read_text(errors='ignore').splitlines():
        line=line.strip()
        if not line or line.startswith('c'): continue
        if line.startswith('p cnf'):
            _,_,n,m=line.split()[:4]; n=int(n); m=int(m); continue
        lits=[int(x) for x in line.split() if x!='0']
        if lits: clauses.append(lits)
    if n is None: raise ValueError('Missing p cnf header')
    G=nx.Graph(); G.add_nodes_from(range(1,n+1)); maxw=0
    for cl in clauses:
        vs=sorted({abs(x) for x in cl}); maxw=max(maxw,len(vs))
        for i in range(len(vs)):
            for j in range(i+1,len(vs)): G.add_edge(vs[i],vs[j])
    tw=0 if G.number_of_edges()==0 else nx.algorithms.approximation.treewidth_min_fill_in(G)[0]
    return dict(source='DIMACS CNF',file=Path(path).name,n=n,m=m,clause_width=maxw,tw_approx=int(tw),edge_density=G.number_of_edges()/(n*(n-1)/2) if n>1 else 0)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('files',nargs='+'); ap.add_argument('--out',default='results/dimacs_structural.csv'); a=ap.parse_args()
    rows=[parse(f) for f in a.files]; p=Path(a.out); p.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame(rows).to_csv(p,index=False); print(json.dumps(rows,indent=2))
if __name__=='__main__': main()
