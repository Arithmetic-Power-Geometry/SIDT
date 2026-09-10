# External benchmark protocol

SIDT separates internally generated theorem-validation data from third-party public benchmarks.

## Fukuoka MQ Challenge (GF(2))

The GitHub Actions workflow downloads the official Type-I GF(2) toy examples for n=10, 15, and 20 at runtime and does not redistribute them.

Run the same external validation locally with:

```bash
bash scripts/fetch_public_benchmarks.sh
python scripts/analyze_external.py
```

The external analyzer records structural metadata only; it does not attempt unauthorized key recovery against deployed systems.

## SAT Competition / DIMACS

Place authorized public `.cnf` or `.dimacs` files anywhere under `data/external/`, then run:

```bash
python scripts/analyze_external.py
```

The analyzer records variable/constraint counts, mean clause support, and approximate primal treewidth.

## Research-only cryptographic CNF

Public reduced-round or research benchmark CNFs may be analyzed through the same DIMACS path. Preserve provenance and licensing for each imported dataset. Reduced-round/research results must not be described as a break of full AES, BitLocker, or any deployed product.
