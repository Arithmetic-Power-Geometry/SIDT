#!/usr/bin/env python3
"""Parse Fukuoka MQ Challenge GF(2) text files into SIDT structural summaries.
Does not solve challenge instances. Safe for public research benchmarks.
"""
from pathlib import Path
import argparse, re, json
import networkx as nx

def parse(path):
    text=Path(path).read_text(errors='ignore')
    n=int(re.search(r'Number of variables \(n\)\s*:\s*(\d+)', text).group(1))
    m=int(re.search(r'Number of equations \(m\)\s*:\s*(\d+)', text).group(1))
    body=text.split('*'*10)[-1]
    rows=[]
    for line in body.splitlines():
        if ';' not in line: continue
        vals=[int(x) for x in re.findall(r'\b[01]\b', line.split(';')[0])]
        if vals: rows.append(vals)
    expected=n*(n+1)//2+n+1
    if len(rows)!=m or any(len(r)!=expected for r in rows):
        raise ValueError(f'Unexpected format: n={n}, m={m}, equations={len(rows)}, expected coeffs={expected}')
    supports=[]; degrees=[]; mons=[]
    for j in range(1,n+1):
        for i in range(1,j+1): mons.append((i-1,j-1))
    for eq in rows:
        supp=set(); deg=0
        for c,mon in zip(eq[:len(mons)],mons):
            if c:
                supp.update(mon); deg=max(deg,1 if mon[0]==mon[1] else 2)
        linear=eq[len(mons):len(mons)+n]
        for i,c in enumerate(linear):
            if c: supp.add(i); deg=max(deg,1)
        supports.append(sorted(supp)); degrees.append(deg)
    G=nx.Graph(); G.add_nodes_from(range(n))
    for s in supports:
        for i in range(len(s)):
            for j in range(i+1,len(s)): G.add_edge(s[i],s[j])
    tw=0 if G.number_of_edges()==0 else nx.algorithms.approximation.treewidth_min_fill_in(G)[0]
    return dict(source='Fukuoka MQ Challenge GF(2)',file=Path(path).name,n=n,m=m,max_degree=max(degrees),mean_support=sum(map(len,supports))/m,tw_approx=int(tw),density=G.number_of_edges()/(n*(n-1)/2) if n>1 else 0)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('files',nargs='+'); ap.add_argument('--out',default='results/fukuoka_structural.csv'); a=ap.parse_args()
    out=[parse(f) for f in a.files]
    import pandas as pd; p=Path(a.out); p.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame(out).to_csv(p,index=False); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
