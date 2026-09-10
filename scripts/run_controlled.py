from pathlib import Path
import argparse, json, math, time
import numpy as np, pandas as pd
from sidt.core import gf2_rank, locality_lower_bound, approx_treewidth

def affine_case(rng,n,q,ell):
    rows=[]; supports=[]
    for _ in range(q):
        support=sorted(rng.choice(n,size=min(ell,n),replace=False).tolist())
        row=np.zeros(n,dtype=np.uint8); vals=rng.integers(0,2,size=len(support),dtype=np.uint8)
        if not vals.any(): vals[0]=1
        for j,v in zip(support,vals): row[j]=v
        rows.append(row); supports.append(np.flatnonzero(row).tolist())
    A=np.vstack(rows); rank=gf2_rank(A); sid=n-rank
    return dict(family='affine',n=n,q=q,degree=1,locality=ell,rank=rank,sid_exact=float(sid),residual_count=float(2**sid),tw_approx=approx_treewidth(n,supports),locality_lb=locality_lower_bound(n,supports),runtime_s=float('nan'))

def nonlinear_case(rng,n,q,degree,ell):
    secret=int(rng.integers(0,1<<n)); obs=[]; supports=[]
    for _ in range(q):
        s=sorted(rng.choice(n,size=min(ell,n),replace=False).tolist()); supports.append(s); mons=[]
        for __ in range(max(2,min(ell,degree+2))):
            d=int(rng.integers(1,min(degree,len(s))+1)); mons.append(tuple(sorted(rng.choice(s,size=d,replace=False).tolist())))
        y=0
        for mon in mons:
            v=1
            for j in mon: v &= (secret>>j)&1
            y ^= v
        obs.append((tuple(mons),y))
    def pred(x):
        for mons,y in obs:
            z=0
            for mon in mons:
                v=1
                for j in mon: v &= (x>>j)&1
                z ^= v
            if z!=y: return False
        return True
    t0=time.perf_counter(); cnt=sum(1 for x in range(1<<n) if pred(x)); elapsed=time.perf_counter()-t0
    return dict(family='nonlinear',n=n,q=q,degree=degree,locality=ell,rank=float('nan'),sid_exact=math.log2(cnt),residual_count=cnt,tw_approx=approx_treewidth(n,supports),locality_lb=locality_lower_bound(n,supports),runtime_s=elapsed)

def main(outdir,instances,seed):
    out=Path(outdir); out.mkdir(parents=True,exist_ok=True); rng=np.random.default_rng(seed); rows=[]; n_aff=int(instances*0.80)
    for _ in range(n_aff):
        n=int(rng.choice([8,12,16,24,32,48,64,96])); q=int(rng.integers(1,min(2*n,96)+1)); ell=int(rng.integers(1,min(n,16)+1)); rows.append(affine_case(rng,n,q,ell))
    for _ in range(instances-n_aff):
        n=int(rng.choice([8,9,10,11,12,13,14])); degree=int(rng.choice([2,3,4])); q=int(rng.integers(2,min(2*n,24)+1)); ell=int(rng.integers(degree,min(n,8)+1)); rows.append(nonlinear_case(rng,n,q,degree,ell))
    df=pd.DataFrame(rows); df.to_csv(out/'controlled_instances.csv',index=False); aff=df[df.family=='affine']
    val={'seed':seed,'instances':len(df),'affine_instances':len(aff),'nonlinear_instances':int((df.family=='nonlinear').sum()),'affine_identity_violations':int((aff.sid_exact!=(aff.n-aff['rank'])).sum()),'locality_bound_violations':int((df.sid_exact+1e-12<df.locality_lb).sum())}
    (out/'controlled_validation.json').write_text(json.dumps(val,indent=2)); print(json.dumps(val,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--outdir',default='results'); ap.add_argument('--instances',type=int,default=5000); ap.add_argument('--seed',type=int,default=20260910); a=ap.parse_args(); main(a.outdir,a.instances,a.seed)
