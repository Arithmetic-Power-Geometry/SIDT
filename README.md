# SIDT Reproducibility Package

Structural Inversion Dimension Theory (SIDT): executable validation and benchmarking software.

Copyright (C) 2026 Mohammad Amir Khusru Akhtar  
License: Apache License 2.0

## Scope

This repository contains **software, tests, benchmark adapters, generated experimental results, and CI only**. It contains no article/manuscript source.

SIDT studies observation-conditioned residual inversion structure under explicitly declared admissibility restrictions. The software is for defensive and research evaluation on controlled or public benchmark instances. It does not claim a practical break of AES, BitLocker, or any deployed cryptosystem.

## Reproduce locally

```bash
bash reproduce.sh
```

The default reproducibility run:
1. runs unit tests;
2. generates 5,000 controlled instances with frozen seed `20260910`;
3. validates the exact affine identity and locality lower bound;
4. runs repeated cross-validation for M1--M4 predictor families;
5. downloads the public Fukuoka MQ Challenge Type-I GF(2) toy benchmarks (`n=10,15,20`);
6. parses external structural metrics;
7. writes machine-readable CSV/JSON results and PDF figures;
8. writes `RESULTS.md`.

## Experimental comparison

- M1: problem size / basic algebraic descriptors.
- M2: M1 + locality information.
- M3: conventional structural descriptors, including approximate primal treewidth.
- M4: M3 + SIDT residual-dimension features.

The software does not predeclare M4 superior. `Delta R2 = R2(M4)-R2(M3)` is reported as a falsifiable incremental-prediction test.

## GitHub Actions artifact

Every push to `main` runs the full workflow and uploads a `SIDT-results-<commit>` artifact containing:
- generated CSV/JSON results,
- generated figures,
- the automated reproducibility report,
- environment metadata.

## External data

Public benchmark data are downloaded at workflow/runtime and are **not redistributed** in this repository. The Fukuoka MQ Challenge GF(2) Type-I toy instances are used as an external parser/structure validation set. DIMACS import support is included for SAT benchmark studies.

## Safety

Use only controlled, public challenge, or authorized research instances. The package is not designed for unauthorized key recovery against real systems.
