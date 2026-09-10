from pathlib import Path
import json
import pandas as pd, numpy as np
from scipy.stats import spearmanr
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parents[1]
df=pd.read_csv(root/'results'/'benchmark_results.csv')
non=df[df.family=='nonlinear'].copy(); non['log_runtime']=np.log10(non['enum_runtime'].clip(lower=1e-9))
feature_sets={
'basic':['n','q','degree'],
'structural':['n','q','degree','locality','tw_approx'],
'structural_plus_sidt':['n','q','degree','locality','tw_approx','sid_exact','locality_lb']}
rows=[]
for name,cols in feature_sets.items():
    X=non[cols].fillna(0); y=non['log_runtime']; Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.30,random_state=42)
    model=RandomForestRegressor(n_estimators=200,random_state=42,min_samples_leaf=3); model.fit(Xtr,ytr); pred=model.predict(Xte)
    rows.append(dict(model=name,r2=r2_score(yte,pred),mae=mean_absolute_error(yte,pred)))
pd.DataFrame(rows).to_csv(root/'results'/'predictive_ablation.csv',index=False)

corr=[]
for c in ['n','q','degree','locality','tw_approx','sid_exact','locality_lb']:
    rho,p=spearmanr(non[c],non['log_runtime'],nan_policy='omit'); corr.append(dict(feature=c,spearman_rho=rho,p_value=p))
pd.DataFrame(corr).to_csv(root/'results'/'spearman_correlations.csv',index=False)

fig=plt.figure(figsize=(6,4)); plt.scatter(non['sid_exact'],non['log_runtime'],s=10,alpha=.55); plt.xlabel('Exact residual dimension (log2 candidate count)'); plt.ylabel('log10 exact-enumeration runtime (s)'); plt.tight_layout(); plt.savefig(root/'figures'/'sid_vs_runtime.pdf'); plt.close(fig)
aff=df[df.family=='affine']; fig=plt.figure(figsize=(6,4)); plt.scatter(aff['rank'],aff['sid_exact'],s=9,alpha=.45); plt.xlabel('GF(2) rank'); plt.ylabel('Exact affine SID'); plt.tight_layout(); plt.savefig(root/'figures'/'affine_rank_sid.pdf'); plt.close(fig)
summary={'nonlinear_instances':int(len(non)),'ablation':pd.DataFrame(rows).to_dict('records'),'correlations':pd.DataFrame(corr).to_dict('records')}; (root/'results'/'analysis_summary.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
