#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p results/plots/trajectories

for SEQ in MH_01_easy MH_03_medium MH_05_difficult; do
  echo "Plotting ${SEQ}"

  MPLBACKEND=Agg evo_traj tum \
    "results/trajectories/orbslam3/${SEQ}.tum" \
    "results/trajectories/openvins/${SEQ}.tum" \
    --ref "results/trajectories/groundtruth/${SEQ}.tum" \
    --sync \
    --align \
    --t_max_diff 0.02 \
    --plot_mode xy \
    --save_plot "results/plots/trajectories/${SEQ}_xy.png" \
    --no_warnings
done

echo "Generated plots:"
find results/plots/trajectories -maxdepth 1 -type f -name "*.png" -print | sort
