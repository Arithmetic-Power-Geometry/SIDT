from pathlib import Path
import json, argparse
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RepeatedKFold, cross_val_predict
from sklearn.metrics import r2_score, mean_absolute_error
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

def evaluate(df,repeats=3,splits=5):
    d=df[df.family=='nonlinear'].copy(); d['log_runtime']=np.log10(d.runtime_s.clip(lower=1e-9))
    models={'M1_basic':['n','q','degree'],'M2_rank_locality':['n','q','degree','locality','locality_lb'],'M3_structural':['n','q','degree','locality','locality_lb','tw_approx'],'M4_structural_plus_SIDT':['n','q','degree','locality','locality_lb','tw_approx','sid_exact']}
    rows=[]; rng=np.random.default_rng(20260910)
    for name,cols in models.items():
        metrics=[]
        for rep in range(repeats):
            order=np.arange(len(d)); rng.shuffle(order); dd=d.iloc[order].reset_index(drop=True)
            cv=RepeatedKFold(n_splits=splits,n_repeats=1,random_state=1000+rep)
            model=RandomForestRegressor(n_estimators=100,min_samples_leaf=3,random_state=2000+rep,n_jobs=-1)
            pred=cross_val_predict(model,dd[cols],dd.log_runtime,cv=cv,n_jobs=-1)
            metrics.append((r2_score(dd.log_runtime,pred),mean_absolute_error(dd.log_runtime,pred)))
        arr=np.array(metrics); rows.append(dict(model=name,r2_mean=arr[:,0].mean(),r2_sd=arr[:,0].std(ddof=1),mae_mean=arr[:,1].mean(),mae_sd=arr[:,1].std(ddof=1)))
    return d,pd.DataFrame(rows)

def main(results,figures):
    results=Path(results); figures=Path(figures); figures.mkdir(parents=True,exist_ok=True); df=pd.read_csv(results/'controlled_instances.csv'); d,tab=evaluate(df); tab.to_csv(results/'controlled_repeated_cv.csv',index=False)
    corr=[]
    for c in ['n','q','degree','locality','locality_lb','tw_approx','sid_exact']:
        rho,p=spearmanr(d[c],d.log_runtime); corr.append({'feature':c,'spearman_rho':rho,'p_value':p})
    pd.DataFrame(corr).to_csv(results/'controlled_correlations.csv',index=False)
    m3=float(tab.loc[tab.model=='M3_structural','r2_mean'].iloc[0]); m4=float(tab.loc[tab.model=='M4_structural_plus_SIDT','r2_mean'].iloc[0]); summary={'delta_r2_M4_minus_M3':m4-m3,'interpretation':'positive favors added SIDT features; near zero indicates no material incremental gain'}; (results/'controlled_summary.json').write_text(json.dumps(summary,indent=2))
    fig=plt.figure(figsize=(6.2,4.2)); plt.scatter(d.sid_exact,d.log_runtime,s=10,alpha=.45); plt.xlabel('Exact residual dimension, log2(|Omega|)'); plt.ylabel('log10 enumeration runtime (s)'); plt.tight_layout(); plt.savefig(figures/'sid_vs_runtime.pdf'); plt.close(fig)
    aff=df[df.family=='affine']; fig=plt.figure(figsize=(6.2,4.2)); plt.scatter(aff['rank'],aff.sid_exact,s=8,alpha=.35); plt.xlabel('GF(2) rank'); plt.ylabel('Exact affine SID'); plt.tight_layout(); plt.savefig(figures/'affine_rank_sid.pdf'); plt.close(fig)
    print(tab.to_string(index=False)); print(json.dumps(summary,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--results',default='results'); ap.add_argument('--figures',default='figures'); a=ap.parse_args(); main(a.results,a.figures)
