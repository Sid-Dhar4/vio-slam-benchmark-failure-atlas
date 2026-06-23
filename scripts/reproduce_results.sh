#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== Running tests =="
./scripts/run_tests.sh

echo
echo "== Regenerating benchmark summary =="
python scripts/make_benchmark_summary.py

echo
echo "== Regenerating trajectory coverage table =="
python scripts/make_trajectory_coverage.py

echo
echo "== Regenerating failure event summary =="
python scripts/extract_failure_events.py

echo
echo "== Regenerating sequence failure cards =="
python scripts/make_failure_cards.py

echo
echo "== Regenerating fair-overlap metrics =="
python scripts/make_fair_overlap_metrics.py

echo
echo "== Regenerating trajectory plots =="
./scripts/make_trajectory_plots.sh

echo
echo "== Regenerating error timeline plots =="
python scripts/make_error_timeline_plots.py

echo
echo "Reproduction complete."
