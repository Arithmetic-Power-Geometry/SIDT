# External benchmark protocol

SIDT separates internally generated theorem-validation data from third-party public benchmarks.

## Fukuoka MQ Challenge (GF(2))
Use Type I encryption instances and the published toy examples. Download from the official challenge site and run:

```bash
python scripts/import_fukuoka.py path/to/mq_file.txt --out results/fukuoka_structural.csv
```

The adapter computes structural descriptors only; it does not attempt unauthorized recovery against deployed systems.

## SAT Competition / DIMACS
For public CNF files:

```bash
python scripts/import_dimacs.py instance.cnf --out results/dimacs_structural.csv
```

## Research-only cryptographic CNF
Public reduced/research benchmark CNFs may be passed through the same DIMACS importer. Keep provenance and license information with every imported file. Do not treat reduced-round/research instances as evidence of a break of full AES or any deployed product.
