#!/usr/bin/env bash
set -euo pipefail
python -m pip install -e .
python -m pip install pytest tabulate
pytest -q
python scripts/run_controlled.py --instances 5000 --seed 20260910
python scripts/analyze_controlled.py
bash scripts/fetch_public_benchmarks.sh
python scripts/analyze_external.py
python scripts/build_report.py
