# SIDT — Structural Inversion Dimension Theory

**Copyright (C) 2026 Mohammad Amir Khusru Akhtar**  
Licensed under the Apache License 2.0.

SIDT is a reproducibility package for studying observation-conditioned residual inversion dimension under explicitly restricted structural capabilities. It does **not** claim a practical break of AES, BitLocker, or any deployed cryptosystem.

## What is implemented
- GF(2) rank and the exact affine identity `SID = n - rank(A)`.
- Locality and transcript/collapse lower bounds.
- Interaction-graph / approximate-treewidth diagnostics.
- Controlled affine and nonlinear benchmark generation.
- Exact residual counting for small nonlinear synthetic systems.
- Predictive ablation comparing basic, conventional structural, and SIDT-augmented features.
- Reproducible figures and CSV/JSON result artifacts.
- Pytest suite and GitHub Actions CI.

## Controlled result snapshot
The frozen seed-20260910 run contains 1,200 controlled instances (900 affine, 300 exact small nonlinear). It produced zero violations of the exact affine identity and zero locality-bound violations. The first runtime ablation is intentionally negative: SIDT features did not materially improve held-out prediction beyond conventional structural features on brute-force enumeration runtime. See `RESULTS.md`.

## Reproduce
```bash
python -m pip install -e .
pytest -q
python scripts/run_benchmarks.py --instances 1200
python scripts/analyze_results.py
```

## Public benchmark adapters
The manuscript identifies Fukuoka MQ Challenge GF(2), SAT Competition benchmarks, and selected research-only cryptographic SAT instances as external validation sources. This repository intentionally does not redistribute third-party datasets without their licenses. Adapter/import code can be extended using the documented formats.

## Safety / scope
The package operates on synthetic, public challenge, and research benchmark instances. It is not intended for unauthorized access or recovery of keys from real systems.
