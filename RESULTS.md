# Reproducible results (controlled benchmark)

Seed: `20260910`.

- Total controlled instances: **1200**.
- Affine instances: **900**.
- Exact small nonlinear instances: **300**.
- Affine identity violations for `SID = n - rank(A)`: **0**.
- Locality lower-bound violations: **0**.
- Pytest: **5 passed**.

Predictive ablation on the deliberately simple exact-enumeration runtime target:

| Model | Held-out R² | MAE (log10 seconds) |
|---|---:|---:|
| Basic (`n,q,degree`) | 0.97620 | 0.06918 |
| Conventional structural (+ locality, approximate treewidth) | 0.97693 | **0.06880** |
| Structural + SIDT features | **0.97702** | 0.06910 |

The differences are negligible. This first controlled runtime experiment therefore **does not establish incremental predictive superiority for SIDT** over conventional structural features. The dominant predictor is problem size `n` (Spearman rho about 0.974). This negative-control result is retained intentionally and motivates external solver-based evaluation where cost is not mechanically dominated by exhaustive enumeration.

The collapse-budget theorem is not checked against the observed feasible-key fiber in this benchmark because that would be a category error: the counting theorem concerns the partition of the full domain induced by the quotient/transcript, not necessarily the conditional solution fiber after planted observations.
