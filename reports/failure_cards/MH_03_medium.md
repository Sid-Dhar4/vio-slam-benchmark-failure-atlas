# Failure Card: MH_03_medium

Moderate-difficulty sequence. Useful for inspecting repeated initialization and reset behavior.

## Metrics

| System | Status | Poses | Runtime (s) | APE RMSE SE3 (m) | RPE trans RMSE (m) |
|---|---|---:|---:|---:|---:|
| orbslam3 | completed | 2696 | 146.18 | 0.034222 | 0.004600 |
| openvins | completed_with_shutdown_exception | 2302 | 21.34 | 0.137622 | 0.004873 |

## Trajectory coverage

| System | Poses | Start timestamp (s) | End timestamp (s) | Duration (s) |
|---|---:|---:|---:|---:|
| groundtruth | 26302 | 1403637132.888319 | 1403637264.393319 | 131.505 |
| orbslam3 | 2696 | 1403637130.738319 | 1403637265.488319 | 134.750 |
| openvins | 2302 | 1403637149.987150 | 1403637265.438400 | 115.451 |

## Failure event counts

Counts are log-line counts for selected patterns, not guaranteed unique physical events.

| System | static init fail | not enough accel | not enough motion | reset evidence | bad IMU | frames set lost | unload exception |
|---|---:|---:|---:|---:|---:|---:|---:|
| orbslam3 | 0 | 2 | 55 | 55 | 0 | 0 | 0 |
| openvins | 260 | 0 | 0 | 0 | 0 | 0 | 1 |

## Interpretation

ORB-SLAM3 has lower aligned APE, but its logs show repeated initialization/reset evidence. Local RPE values are close, so global error and local motion should be interpreted separately.

## Suggested next improvement

Inspect ORB-SLAM3 initialization windows and add error-over-time plots around reset-heavy regions.

