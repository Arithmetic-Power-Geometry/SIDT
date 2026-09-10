from pathlib import Path
import argparse, json, statistics
import pandas as pd
from sidt.parsers import parse_dimacs, parse_fukuoka_gf2
from sidt.core import approx_treewidth

def main(input_dir,out_csv):
    base=Path(input_dir); rows=[]
    for p in base.rglob('*'):
        if not p.is_file(): continue
        low=p.name.lower()
        try:
            if low.endswith(('.cnf','.dimacs')):
                x=parse_dimacs(p); rows.append({'dataset':'DIMACS','file':str(p.relative_to(base)),'n':x['n'],'m':x['m'],'mean_constraint_support':statistics.mean(map(len,x['supports'])) if x['supports'] else 0,'tw_approx':approx_treewidth(x['n'],x['supports'])})
            elif low.endswith(('.txt','.mq','.in')):
                x=parse_fukuoka_gf2(p); rows.append({'dataset':'Fukuoka-GF2','file':str(p.relative_to(base)),'n':x['n'],'m':x['m'],'mean_constraint_support':float('nan'),'tw_approx':float('nan'),'mean_nonzero_coefficients':x['mean_nonzero_coefficients'],'seed':x['seed']})
        except Exception:
            pass
    out=Path(out_csv); out.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame(rows).to_csv(out,index=False)
    summary={'parsed_instances':len(rows),'fukuoka_instances':sum(r['dataset']=='Fukuoka-GF2' for r in rows),'dimacs_instances':sum(r['dataset']=='DIMACS' for r in rows)}; out.with_suffix('.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--input',default='data/external'); ap.add_argument('--out',default='results/external_metrics.csv'); a=ap.parse_args(); main(a.input,a.out)
