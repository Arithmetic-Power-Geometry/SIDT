from __future__ import annotations
import argparse, math, time
from pathlib import Path
import numpy as np, pandas as pd
from sidt.core import gf2_rank, locality_lower_bound, approx_treewidth

def make_affine_instance(rng, n, q, locality):
    rows=[]; supports=[]
    for _ in range(q):
        k=min(locality,n); s=sorted(rng.choice(n,size=k,replace=False).tolist())
        row=np.zeros(n,dtype=np.uint8); row[s]=rng.integers(0,2,size=k,dtype=np.uint8)
        if not row.any(): row[s[0]]=1
        rows.append(row); supports.append([i for i in s if row[i]])
    A=np.vstack(rows) if rows else np.zeros((0,n),dtype=np.uint8)
    rank=gf2_rank(A); sid=n-rank
    return dict(family='affine',n=n,q=q,degree=1,locality=locality,rank=rank,
                sid_exact=float(sid),residual_count=float(2**sid),
                tw_approx=approx_treewidth(n,supports),
                locality_lb=locality_lower_bound(n,supports),supports=supports)

def make_planted_nonlinear_instance(rng,n,q,degree,locality):
    secret=int(rng.integers(0,1<<n)); supports=[]; monomials=[]; ys=[]
    for _ in range(q):
        k=min(locality,n); supp=sorted(rng.choice(n,size=k,replace=False).tolist()); supports.append(supp)
        mons=[]; num=max(1,min(k,degree+1))
        for __ in range(num):
            d=int(rng.integers(1,min(degree,k)+1))
            mons.append(tuple(sorted(rng.choice(supp,size=d,replace=False).tolist())))
        monomials.append(mons); y=0
        for mon in mons:
            v=1
            for j in mon: v &= (secret>>j)&1
            y ^= v
        ys.append(y)
    def ok(x):
        for mons,y in zip(monomials,ys):
            z=0
            for mon in mons:
                v=1
                for j in mon: v &= (x>>j)&1
                z ^= v
            if z!=y: return False
        return True
    t0=time.perf_counter(); cnt=sum(ok(x) for x in range(1<<n)); runtime=time.perf_counter()-t0
    sid=math.log2(cnt) if cnt else float('nan')
    return dict(family='nonlinear',n=n,q=q,degree=degree,locality=locality,rank=float('nan'),
                sid_exact=sid,residual_count=cnt,tw_approx=approx_treewidth(n,supports),
                locality_lb=locality_lower_bound(n,supports),enum_runtime=runtime,supports=supports)

def main(outdir, n_instances=1200, seed=20260910):
    out=Path(outdir); out.mkdir(parents=True,exist_ok=True); rng=np.random.default_rng(seed); rows=[]
    for _ in range(int(n_instances*0.75)):
        n=int(rng.choice([8,12,16,24,32,48,64])); q=int(rng.integers(1,min(2*n,80)+1)); locality=int(rng.integers(1,min(n,12)+1))
        rows.append(make_affine_instance(rng,n,q,locality))
    for _ in range(n_instances-len(rows)):
        n=int(rng.choice([8,9,10,11,12,13,14])); q=int(rng.integers(2,min(2*n,24)+1)); degree=int(rng.choice([2,3,4])); locality=int(rng.integers(degree,min(n,8)+1))
        rows.append(make_planted_nonlinear_instance(rng,n,q,degree,locality))
    df=pd.DataFrame(rows); df['gap_to_locality_lb']=df['sid_exact']-df['locality_lb']; df.to_csv(out/'benchmark_results.csv',index=False)
    summary={'instances':int(len(df)),'affine_instances':int((df.family=='affine').sum()),'nonlinear_instances':int((df.family=='nonlinear').sum()),'affine_formula_violations':int(((df.family=='affine') & (df.sid_exact != (df.n-df['rank']))).sum()),'locality_bound_violations':int((df.sid_exact + 1e-12 < df.locality_lb).sum()),'seed':seed}
    import json; (out/'validation_summary.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--outdir',default='results'); ap.add_argument('--instances',type=int,default=1200); ap.add_argument('--seed',type=int,default=20260910); a=ap.parse_args(); main(a.outdir,a.instances,a.seed)
