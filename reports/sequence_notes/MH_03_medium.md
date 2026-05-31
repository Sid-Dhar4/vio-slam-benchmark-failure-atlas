# MH_03_medium

Status: dataset prepared for ground-truth evaluation. ORB-SLAM3 and OpenVINS have not been run yet.

## Dataset prep
Local sequence path: ~/datasets/euroc/MH_03_medium
Required EuRoC ASL-style files were verified by scripts/check_euroc_dataset.py.

## Ground-truth conversion
Generated file: results/trajectories/groundtruth/MH_03_medium.tum
- Poses: 26,302
- Start time: 1403637132.888319016
- End time: 1403637264.393318892
- Duration: 131.505 seconds

## Validation
- Project parser successfully loaded the converted TUM trajectory.
- evo APE self-check RMSE: 0.000000 m

## Backend status
- ORB-SLAM3: not run yet
- OpenVINS: not run yet

## ORB-SLAM3 run 1

Backend: ORB-SLAM3 stereo-inertial EuRoC example.

Run status: completed successfully after a controlled rerun.

Raw outputs:
- results/trajectories/orbslam3/raw/MH_03_medium/f_MH_03_medium.txt
- results/trajectories/orbslam3/raw/MH_03_medium/kf_MH_03_medium.txt

Converted output:
- results/trajectories/orbslam3/MH_03_medium.tum

Observed run details:
- Runtime wall clock: 2:26.18
- Full trajectory poses: 2,696
- Keyframes: 147
- Log: results/logs/orbslam3/MH_03_medium.log

Initial evo result:
- No alignment APE RMSE: 8.071921 m
- SE(3)-aligned APE RMSE: 0.034222 m
- RPE translation delta=1 aligned RMSE: 0.004600 m

Failure/behavior notes:
- The log repeatedly reported not enough motion for initializing and map reset messages.
- The run still completed and saved a full trajectory plus keyframe trajectory.
- This controlled rerun replaces the earlier accidental uncommitted run.

## OpenVINS run 1

Backend: OpenVINS ROS 1 serial EuRoC run.

Run status: completed_with_shutdown_exception.

Run settings:
- mode: stereo
- max_cameras: 2
- use_stereo: true
- config: euroc_mav
- bag_start: 5 seconds

Raw outputs:
- results/trajectories/openvins/raw/MH_03_medium/estimate.txt
- results/timing/openvins/MH_03_medium/timing.txt

Converted output:
- results/trajectories/openvins/MH_03_medium.tum

Observed run details:
- Runtime wall clock: 0:21.34
- Converted trajectory poses: 2,302
- Estimate file lines: 2,303 including header
- Timing file lines: 2,303 including header
- Log: results/logs/openvins/MH_03_medium.log

Initial evo result:
- No alignment APE RMSE: 10.969038 m
- SE(3)-aligned APE RMSE: 0.137622 m
- RPE translation delta=1 aligned RMSE: 0.004873 m

Failure/behavior notes:
- The run produced trajectory and timing files.
- The log reported class_loader::LibraryUnloadException at shutdown.
- The process reported ov_msckf exit code -6 during shutdown, so the status is not marked as a clean completed run.
- The run used bag_start=5 seconds; comparisons should use overlapping timestamp association and document the crop.
