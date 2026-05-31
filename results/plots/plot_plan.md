# Plot Plan

Goal: generate trajectory overlay plots for each MVP EuRoC sequence.

Planned plots:
- MH_01_easy: ground truth vs ORB-SLAM3 vs OpenVINS
- MH_03_medium: ground truth vs ORB-SLAM3 vs OpenVINS
- MH_05_difficult: ground truth vs ORB-SLAM3 vs OpenVINS

Important caveat:
OpenVINS trajectories use Machine Hall start offsets, so plots should be interpreted over the overlapping timestamp region rather than as full-sequence coverage.

Preferred plotting method:
- use evo_traj with ground-truth reference and SE(3) alignment when possible
- save static plot files under results/plots/trajectories/

## Generated files

evo_traj expands each requested save_plot prefix into multiple PNG files:

- *_xy_trajectories.png
- *_xy_xyz.png
- *_xy_rpy.png
- *_xy_speeds.png

Current MVP plot set:

- results/plots/trajectories/MH_01_easy_xy_rpy.png
- results/plots/trajectories/MH_01_easy_xy_speeds.png
- results/plots/trajectories/MH_01_easy_xy_trajectories.png
- results/plots/trajectories/MH_01_easy_xy_xyz.png
- results/plots/trajectories/MH_03_medium_xy_rpy.png
- results/plots/trajectories/MH_03_medium_xy_speeds.png
- results/plots/trajectories/MH_03_medium_xy_trajectories.png
- results/plots/trajectories/MH_03_medium_xy_xyz.png
- results/plots/trajectories/MH_05_difficult_xy_rpy.png
- results/plots/trajectories/MH_05_difficult_xy_speeds.png
- results/plots/trajectories/MH_05_difficult_xy_trajectories.png
- results/plots/trajectories/MH_05_difficult_xy_xyz.png

## Labeling note

The plotting script creates temporary labeled trajectory paths before calling evo_traj, so the plot legends distinguish:

- groundtruth_SEQUENCE
- orbslam3_SEQUENCE
- openvins_SEQUENCE
