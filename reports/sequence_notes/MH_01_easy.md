# MH_01_easy

Status: dataset prepared for ground-truth evaluation. ORB-SLAM3 and OpenVINS have not been run yet.

## Dataset prep

Local sequence path: ~/datasets/euroc/MH_01_easy

Verified required EuRoC ASL-style files:
- mav0/cam0/data.csv
- mav0/cam0/data/
- mav0/cam1/data.csv
- mav0/cam1/data/
- mav0/imu0/data.csv
- mav0/state_groundtruth_estimate0/data.csv

## Ground-truth conversion

Generated file: results/trajectories/groundtruth/MH_01_easy.tum

Observed conversion summary:
- Poses: 36,382
- Start time: 1403636580.838555813
- End time: 1403636762.743555784
- Duration: 181.905 seconds

## Validation

- Project parser successfully loaded the converted TUM trajectory.
- evo APE self-check RMSE: 0.000000 m
- evo RPE self-check RMSE: 0.000000 m

## Backend status

- ORB-SLAM3: not run yet
- OpenVINS: not run yet

## ORB-SLAM3 run 1

Backend: ORB-SLAM3 stereo-inertial EuRoC example.

Run status: completed successfully.

Raw outputs:
- results/trajectories/orbslam3/raw/MH_01_easy/f_MH_01_easy.txt
- results/trajectories/orbslam3/raw/MH_01_easy/kf_MH_01_easy.txt

Converted output:
- results/trajectories/orbslam3/MH_01_easy.tum

Observed run details:
- Runtime wall clock: 3:23.00
- Full trajectory poses: 3,678
- Keyframes: 128
- Log: results/logs/orbslam3/MH_01_easy.log

Initial evo APE result:
- No alignment APE RMSE: 6.272498 m
- SE(3)-aligned APE RMSE: 0.048717 m

Failure/behavior notes:
- The log reported early IMU/initialization messages including not enough acceleration and not enough motion for initializing.
- The system reset early but later saved a trajectory and keyframe trajectory.
- This should be revisited in the failure atlas after OpenVINS is run.

## OpenVINS run 1

Backend: OpenVINS ROS 1 serial EuRoC run.

Run status: completed_with_shutdown_exception.

Run settings:
- mode: stereo
- max_cameras: 2
- use_stereo: true
- config: euroc_mav
- bag_start: 40 seconds

Raw outputs:
- results/trajectories/openvins/raw/MH_01_easy/estimate.txt
- results/timing/openvins/MH_01_easy/timing.txt

Converted output:
- results/trajectories/openvins/MH_01_easy.tum

Observed run details:
- Runtime wall clock: 0:23.64
- Converted trajectory poses: 2,767
- Estimate file lines: 2,768 including header
- Timing file lines: 2,768 including header
- Log: results/logs/openvins/MH_01_easy.log

Initial evo result:
- No alignment APE RMSE: 12.130369 m
- SE(3)-aligned APE RMSE: 0.090810 m
- RPE translation delta=1 aligned RMSE: 0.002152 m

Failure/behavior notes:
- The run produced trajectory and timing files.
- The log still reported class_loader::LibraryUnloadException at shutdown.
- The process reported ov_msckf exit code -6 during shutdown, so the status is not marked as a clean completed run.
- The run used bag_start=40 seconds, matching OpenVINS Machine Hall guidance; comparisons should use overlapping timestamp association and document the crop.
