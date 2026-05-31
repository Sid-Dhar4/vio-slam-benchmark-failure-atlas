#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p results/plots/trajectories

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

for SEQ in MH_01_easy MH_03_medium MH_05_difficult; do
  echo "Plotting ${SEQ}"

  REF="$TMP_DIR/groundtruth_${SEQ}.tum"
  ORB="$TMP_DIR/orbslam3_${SEQ}.tum"
  OPENVINS="$TMP_DIR/openvins_${SEQ}.tum"

  ln -sf "$PWD/results/trajectories/groundtruth/${SEQ}.tum" "$REF"
  ln -sf "$PWD/results/trajectories/orbslam3/${SEQ}.tum" "$ORB"
  ln -sf "$PWD/results/trajectories/openvins/${SEQ}.tum" "$OPENVINS"

  MPLBACKEND=Agg evo_traj tum \
    "$ORB" \
    "$OPENVINS" \
    --ref "$REF" \
    --sync \
    --align \
    --t_max_diff 0.02 \
    --plot_mode xy \
    --save_plot "results/plots/trajectories/${SEQ}_xy.png" \
    --no_warnings
done

echo "Generated plots:"
find results/plots/trajectories -maxdepth 1 -type f -name "*.png" -print | sort
