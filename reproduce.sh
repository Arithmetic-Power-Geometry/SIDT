#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(pwd)/src:${PYTHONPATH:-}"
pytest -q tests
python scripts/run_benchmarks.py --outdir results --instances 1200 --seed 20260910
python scripts/analyze_results.py
