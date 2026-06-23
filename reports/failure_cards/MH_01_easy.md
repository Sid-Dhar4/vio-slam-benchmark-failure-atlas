# Failure Card: MH_01_easy

Sanity-check sequence. Both systems produced trajectories; useful for validating the benchmark pipeline.

## Metrics

| System | Status | Poses | Runtime (s) | APE RMSE SE3 (m) | RPE trans RMSE (m) |
|---|---|---:|---:|---:|---:|
| orbslam3 | completed | 3678 | 203.00 | 0.048717 | 0.003445 |
| openvins | completed_with_shutdown_exception | 2767 | 23.64 | 0.090810 | 0.002152 |

## Trajectory coverage

| System | Poses | Start timestamp (s) | End timestamp (s) | Duration (s) |
|---|---:|---:|---:|---:|
| groundtruth | 36382 | 1403636580.838556 | 1403636762.743556 | 181.905 |
| orbslam3 | 3678 | 1403636579.963556 | 1403636763.813555 | 183.850 |
| openvins | 2767 | 1403636624.662620 | 1403636763.763540 | 139.101 |

## Failure event counts

Counts are log-line counts for selected patterns, not guaranteed unique physical events.

| System | static init fail | not enough accel | not enough motion | reset evidence | bad IMU | frames set lost | unload exception |
|---|---:|---:|---:|---:|---:|---:|---:|
| orbslam3 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| openvins | 87 | 0 | 0 | 0 | 0 | 0 | 1 |

## Interpretation

ORB-SLAM3 has lower aligned APE, while OpenVINS has lower local RPE. Treat this as a sanity-check result with OpenVINS start-offset and shutdown caveats.

## Suggested next improvement

Use fair-overlap metrics and verify whether OpenVINS local RPE remains lower on the common time interval.

