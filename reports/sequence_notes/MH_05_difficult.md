# MH_05_difficult

Status: dataset prepared for ground-truth evaluation. ORB-SLAM3 and OpenVINS have not been run yet.

## Dataset prep
Local sequence path: ~/datasets/euroc/MH_05_difficult
Required EuRoC ASL-style files were verified by scripts/check_euroc_dataset.py.

## Ground-truth conversion
Generated file: results/trajectories/groundtruth/MH_05_difficult.tum
- Poses: 22,212
- Start time: 1403638519.492829561
- End time: 1403638630.547829628
- Duration: 111.055 seconds

## Validation
- Project parser successfully loaded the converted TUM trajectory.
- evo APE self-check RMSE: 0.000000 m

## Backend status
- ORB-SLAM3: not run yet
- OpenVINS: not run yet

## ORB-SLAM3 run 1

Backend: ORB-SLAM3 stereo-inertial EuRoC example.

Run status: completed successfully.

Raw outputs:
- results/trajectories/orbslam3/raw/MH_05_difficult/f_MH_05_difficult.txt
- results/trajectories/orbslam3/raw/MH_05_difficult/kf_MH_05_difficult.txt

Converted output:
- results/trajectories/orbslam3/MH_05_difficult.tum

Observed run details:
- Runtime wall clock: 2:03.69
- Full trajectory poses: 2,082
- Keyframes: 159
- Log: results/logs/orbslam3/MH_05_difficult.log

Initial evo result:
- No alignment APE RMSE: 13.945373 m
- SE(3)-aligned APE RMSE: 0.075237 m
- RPE translation delta=1 aligned RMSE: 0.005066 m

Failure/behavior notes:
- The log repeatedly reported not enough acceleration and not enough motion during initialization.
- ORB-SLAM3 reported a reset caused by a bad IMU flag.
- The log reported 109 frames set to lost.
- The run still completed and saved full-frame and keyframe trajectories.
- This sequence should be emphasized in the failure atlas as the first difficult/stress case.

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
- results/trajectories/openvins/raw/MH_05_difficult/estimate.txt
- results/timing/openvins/MH_05_difficult/timing.txt

Converted output:
- results/trajectories/openvins/MH_05_difficult.tum

Observed run details:
- Runtime wall clock: 0:17.53
- Converted trajectory poses: 1,845
- Estimate file lines: 1,846 including header
- Timing file lines: 1,846 including header
- Log: results/logs/openvins/MH_05_difficult.log

Initial evo result:
- No alignment APE RMSE: 5.157668 m
- SE(3)-aligned APE RMSE: 0.242839 m
- RPE translation delta=1 aligned RMSE: 0.004271 m

Failure/behavior notes:
- The run produced trajectory and timing files.
- The log reported class_loader::LibraryUnloadException at shutdown.
- The process reported ov_msckf exit code -6 during shutdown, so the status is not marked as a clean completed run.
- The run used bag_start=5 seconds; comparisons should use overlapping timestamp association and document the crop.
