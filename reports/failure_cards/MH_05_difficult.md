# Failure Card: MH_05_difficult

Stress sequence in the current benchmark. Useful for inspecting bad-IMU and lost-frame evidence.

## Metrics

| System | Status | Poses | Runtime (s) | APE RMSE SE3 (m) | RPE trans RMSE (m) |
|---|---|---:|---:|---:|---:|
| orbslam3 | completed | 2082 | 123.69 | 0.075237 | 0.005066 |
| openvins | completed_with_shutdown_exception | 1845 | 17.53 | 0.242839 | 0.004271 |

## Trajectory coverage

| System | Poses | Start timestamp (s) | End timestamp (s) | Duration (s) |
|---|---:|---:|---:|---:|
| groundtruth | 22212 | 1403638519.492830 | 1403638630.547830 | 111.055 |
| orbslam3 | 2082 | 1403638527.627830 | 1403638631.677830 | 104.050 |
| openvins | 1845 | 1403638539.292190 | 1403638631.627920 | 92.336 |

## Failure event counts

Counts are log-line counts for selected patterns, not guaranteed unique physical events.

| System | static init fail | not enough accel | not enough motion | reset evidence | bad IMU | frames set lost | unload exception |
|---|---:|---:|---:|---:|---:|---:|---:|
| orbslam3 | 0 | 78 | 16 | 18 | 1 | 1 | 0 |
| openvins | 289 | 0 | 0 | 0 | 0 | 0 | 1 |

## Interpretation

This is the strongest failure case. ORB-SLAM3 shows bad-IMU and lost-frame evidence but still produces the lower aligned APE. OpenVINS shows many static initialization failures and the repeatable shutdown exception.

## Suggested next improvement

Prioritize error-timeline plots and event markers for bad-IMU reset and explicit lost-frame evidence.

