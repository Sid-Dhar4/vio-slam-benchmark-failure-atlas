# Result Interpretation and Technical Defense

This document explains how to interpret the benchmark results in this repository and summarizes the main caveats that affect the comparison between ORB-SLAM3 and OpenVINS.

## Goal

The goal of this benchmark is not only to report one final accuracy number. The goal is to make visual-inertial SLAM and VIO behavior easier to inspect by combining trajectory outputs, evo metrics, plots, runtime logs, backend status, and sequence-level failure notes.

This matters because a SLAM or VIO system can produce a trajectory while still showing important failure symptoms such as initialization resets, lost frames, poor local consistency, shutdown exceptions, or sensitivity to start time.

## Systems compared

- ORB-SLAM3: feature-based visual-inertial SLAM using keyframes, mapping, and optimization.
- OpenVINS: filter-based visual-inertial odometry run through a ROS 1 serial EuRoC workflow.

The current benchmark uses MH_01_easy, MH_03_medium, and MH_05_difficult from the EuRoC MAV Machine Hall dataset.

## Trajectory format

Backend outputs are converted into TUM trajectory format before evaluation.

A TUM trajectory row has this form:

```text
timestamp tx ty tz qx qy qz qw
```

The timestamp is in seconds. The values tx, ty, tz are position. The values qx, qy, qz, qw are orientation as a quaternion.

## evo metrics

The project uses evo to compute trajectory metrics. The two main metrics are APE and RPE.

## APE: Absolute Pose Error

APE measures global trajectory error against ground truth. In this repository, the main APE value is APE RMSE after SE(3) alignment, measured in meters.

APE answers: after placing the estimated trajectory into the ground-truth frame, how close is the estimated path globally?

## RPE: Relative Pose Error

RPE measures local relative motion error between nearby poses. In this repository, the main RPE value is translational RPE RMSE, measured in meters.

RPE answers: was the local motion estimate smooth and locally consistent?

## Why APE and RPE can disagree

APE and RPE measure different behavior. A system can have low RPE but high APE if local motion is smooth but the global path drifts. A system can also have lower global APE while showing slightly higher local RPE.

This is why the benchmark reports both. In the current results, ORB-SLAM3 has lower SE(3)-aligned APE on all three sequences. OpenVINS has competitive RPE on some sequences, which suggests local motion can be smooth even when global aligned trajectory error is higher.

## SE(3) alignment

SE(3) alignment means the estimated trajectory is rigidly aligned to the ground truth before computing APE.

SE(3) includes 3D rotation and 3D translation. It does not include scale correction. This is appropriate for visual-inertial systems because metric scale should come from the estimator, not from a post-hoc scale fit.

## Timestamp association and overlap

Trajectory evaluation requires matching estimated poses to ground-truth poses by timestamp. The current benchmark uses timestamp association over overlapping estimated poses.

Important caveat:

- ORB-SLAM3 runs use full sequence timestamps.
- OpenVINS runs use Machine Hall start offsets from the ROS serial workflow.
- OpenVINS uses bag_start=40 seconds for MH_01_easy.
- OpenVINS uses bag_start=5 seconds for MH_03_medium and MH_05_difficult.

Because of this, current comparisons should be interpreted over overlapping timestamp regions, not as a perfectly identical full-sequence comparison.

The current trajectory timestamp ranges are summarized in `results/tables/trajectory_coverage.md`.

Selected failure-related log patterns are summarized in `results/tables/event_summary.md`.

## Fair-overlap metrics

A stronger future version should explicitly compute fair-overlap metrics by cropping ground truth, ORB-SLAM3, and OpenVINS trajectories to the same common timestamp interval before running evo.

The intended fair-overlap process is:

1. Find the common timestamp interval shared by the compared trajectories.
2. Crop all trajectories to that interval.
3. Run evo APE and RPE on the cropped trajectories.
4. Report both original metrics and fair-overlap metrics.

## Runtime caveat

Runtime is logged for transparency, but it is not yet a fair speed benchmark.

Reasons:

- ORB-SLAM3 and OpenVINS were run through different example pipelines.
- OpenVINS was run through a ROS 1 serial workflow.
- Some OpenVINS runs use start offsets.
- Wall-clock runtime includes more than estimator computation.

Runtime should therefore be interpreted as logged runtime for this experiment setup, not proof that one backend is computationally faster than the other.

## Backend status is part of the result

OpenVINS produced trajectory and timing files on all three sequences, but the runs ended with a repeatable ROS shutdown LibraryUnloadException. These rows are marked completed_with_shutdown_exception.

This is reported honestly because an estimator can produce useful outputs while still showing engineering or runtime issues.

## Interview defense summary

I built a reproducible VIO/SLAM benchmark comparing ORB-SLAM3 and OpenVINS on EuRoC Machine Hall sequences. I converted ground truth and backend estimates into TUM trajectory format, evaluated them with evo using APE and RPE, generated trajectory plots, logged runtime, and documented backend-specific failure behavior.

I report both global aligned error and local relative error because they measure different failure modes. I also explicitly document the caveats: OpenVINS uses Machine Hall start offsets, the current comparison uses timestamp association over overlapping poses, and runtime is not yet a fair speed benchmark because the backend pipelines differ.

