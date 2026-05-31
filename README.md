# Reproducible VIO/SLAM Benchmark and Failure Atlas

## Summary

This repository contains a reproducible benchmark comparing ORB-SLAM3 and OpenVINS on EuRoC Machine Hall visual-inertial sequences. The project automates dataset checks, trajectory conversion to TUM format, evo APE/RPE evaluation, runtime logging, trajectory visualization, and sequence-level failure analysis.

Current benchmark scope:

- Systems: ORB-SLAM3 and OpenVINS
- Dataset: EuRoC MAV Machine Hall
- Sequences: MH_01_easy, MH_03_medium, MH_05_difficult
- Metrics: evo APE translation RMSE, evo RPE translation RMSE, logged wall-clock runtime
- Outputs: raw trajectories, converted TUM trajectories, metrics.csv, logs, timing files, plots, benchmark brief, and failure atlas

## Why this project

Visual-inertial SLAM systems fail for concrete engineering reasons: initialization issues, poor motion excitation, feature tracking failures, IMU assumptions, timestamp synchronization problems, and calibration sensitivity. This project reports accuracy and documents observed failure behavior from backend logs.

## Systems compared

- ORB-SLAM3: feature-based visual/visual-inertial SLAM with keyframes, mapping, and optimization.
- OpenVINS: filter-based visual-inertial odometry framework using a ROS 1 serial EuRoC workflow in this benchmark.

## Dataset

The current benchmark uses EuRoC MAV Machine Hall sequences: MH_01_easy, MH_03_medium, and MH_05_difficult. Raw datasets are stored outside this repository under `~/datasets/euroc/`. See `docs/dataset_layout.md` and `docs/dataset_download_notes.md`.

## Pipeline

```text
EuRoC dataset -> backend runner -> raw trajectory -> TUM conversion -> evo APE/RPE -> metrics.csv -> plots -> failure atlas
```

Important scripts:

- `scripts/check_euroc_dataset.py`
- `scripts/convert_euroc_groundtruth.py`
- `scripts/convert_orbslam3_euroc_to_tum.py`
- `scripts/convert_openvins_to_tum.py`
- `scripts/write_metrics_row.py`
- `scripts/make_benchmark_summary.py`
- `scripts/make_trajectory_plots.sh`

## Results

Main machine-readable results are in `results/metrics.csv`. The summary table below is generated from `results/tables/benchmark_summary.md`.

| System | Sequence | Status | Poses | Runtime (s) | APE RMSE SE3 (m) | RPE trans RMSE (m) | Notes |
|---|---|---|---:|---:|---:|---:|---|
| openvins | MH_01_easy | completed_with_shutdown_exception | 2767 | 23.64 | 0.090810 | 0.002152 | bag_start=40; trajectory saved; shutdown LibraryUnloadException observed |
| orbslam3 | MH_01_easy | completed | 3678 | 203.00 | 0.048717 | 0.003445 | first ORB-SLAM3 stereo-inertial run; early initialization reset observed |
| openvins | MH_03_medium | completed_with_shutdown_exception | 2302 | 21.34 | 0.137622 | 0.004873 | bag_start=5; trajectory saved; shutdown LibraryUnloadException observed |
| orbslam3 | MH_03_medium | completed | 2696 | 146.18 | 0.034222 | 0.004600 | controlled ORB-SLAM3 stereo-inertial rerun; repeated initialization resets observed |
| openvins | MH_05_difficult | completed_with_shutdown_exception | 1845 | 17.53 | 0.242839 | 0.004271 | bag_start=5; trajectory saved; shutdown LibraryUnloadException observed |
| orbslam3 | MH_05_difficult | completed | 2082 | 123.69 | 0.075237 | 0.005066 | controlled ORB-SLAM3 stereo-inertial run; bad IMU/reset/lost-frame behavior observed |

## Plots

Trajectory plots were generated with `scripts/make_trajectory_plots.sh`.

- `results/plots/trajectories/MH_01_easy_xy_trajectories.png`
- `results/plots/trajectories/MH_03_medium_xy_trajectories.png`
- `results/plots/trajectories/MH_05_difficult_xy_trajectories.png`

Additional generated plots include xyz, rpy, and speed plots for each sequence.

## Failure atlas

See `reports/failure_atlas.md` for sequence-level observations and failure notes.

Observed behavior includes ORB-SLAM3 initialization resets, map resets, bad IMU flag behavior, and lost-frame behavior. OpenVINS produced trajectory and timing files on all three sequences, but each run ended with a ROS shutdown `LibraryUnloadException`; those runs are marked `completed_with_shutdown_exception`.

## Reproduce

Run tests:

```bash
./scripts/run_tests.sh
```

Check EuRoC dataset layout:

```bash
PYTHONPATH=src python scripts/check_euroc_dataset.py --root ~/datasets/euroc
```

Regenerate summary table:

```bash
python scripts/make_benchmark_summary.py
```

Regenerate trajectory plots:

```bash
./scripts/make_trajectory_plots.sh
```

Backend build notes are in `environment/docker/orbslam3_setup.md` and `environment/docker/openvins_setup.md`.

## Tests

The project includes tests for trajectory format utilities, EuRoC conversion, dataset layout checking, and result schema behavior.

## Limitations

- OpenVINS runs use Machine Hall start offsets from the ROS serial workflow; ORB-SLAM3 runs use full sequence timestamps.
- Current evo comparisons use timestamp association over overlapping estimated poses, so plots and metrics should be interpreted with the start-offset caveat.
- OpenVINS runs produced usable outputs but ended with a repeatable shutdown `LibraryUnloadException`.
- Runtime values are logged, but they are not yet a fair speed benchmark because the backend example pipelines differ.
- Metrics are recorded in `metrics.csv`; future work should parse evo result archives automatically.
- Raw EuRoC datasets and third-party backend source repositories are kept outside this repository.

## Future work

- Add more EuRoC sequences.
- Add TUM-VI extension.
- Add a third backend such as Basalt or VINS-Fusion.
- Add ablations for feature count, dropped frames, timestamp offset, and calibration perturbation.
- Parse evo result archives automatically into `metrics.csv`.
- Add APE/RPE over-time plots.
