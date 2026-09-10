from pathlib import Path
import json, pandas as pd
r=Path('results')
v=json.loads((r/'controlled_validation.json').read_text())
cv=pd.read_csv(r/'controlled_repeated_cv.csv')
ext={}
if (r/'external_metrics.json').exists(): ext=json.loads((r/'external_metrics.json').read_text())
lines=['# SIDT Reproducibility Report','', 'Generated automatically from executable results.','', '## Controlled validation', f"- Instances: {v['instances']} ({v['affine_instances']} affine; {v['nonlinear_instances']} nonlinear)", f"- Exact affine identity violations: {v['affine_identity_violations']}", f"- Locality lower-bound violations: {v['locality_bound_violations']}",'', '## Repeated cross-validation','', cv.to_markdown(index=False),'']
if ext: lines += ['## External benchmark parsing',f"- Parsed instances: {ext['parsed_instances']}",f"- Fukuoka GF(2): {ext['fukuoka_instances']}",f"- DIMACS: {ext['dimacs_instances']}",'']
lines += ['## Interpretation','M4 is compared with M3 only as an incremental-prediction test. The software does not label SIDT superior unless the measured difference is materially and reproducibly positive.']
Path('RESULTS.md').write_text('\n'.join(lines)); print('\n'.join(lines))
