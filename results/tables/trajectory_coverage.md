# Trajectory Coverage

This table reports the timestamp coverage of each trajectory used in the current benchmark.

It makes the start-offset caveat explicit: OpenVINS trajectories begin later than the ground-truth and ORB-SLAM3 trajectories because the current OpenVINS EuRoC workflow uses Machine Hall bag_start offsets.

| System | Sequence | Poses | Start timestamp (s) | End timestamp (s) | Duration (s) |
|---|---|---:|---:|---:|---:|
| groundtruth | MH_01_easy | 36382 | 1403636580.838556 | 1403636762.743556 | 181.905 |
| openvins | MH_01_easy | 2767 | 1403636624.662620 | 1403636763.763540 | 139.101 |
| orbslam3 | MH_01_easy | 3678 | 1403636579.963556 | 1403636763.813555 | 183.850 |
| groundtruth | MH_03_medium | 26302 | 1403637132.888319 | 1403637264.393319 | 131.505 |
| openvins | MH_03_medium | 2302 | 1403637149.987150 | 1403637265.438400 | 115.451 |
| orbslam3 | MH_03_medium | 2696 | 1403637130.738319 | 1403637265.488319 | 134.750 |
| groundtruth | MH_05_difficult | 22212 | 1403638519.492830 | 1403638630.547830 | 111.055 |
| openvins | MH_05_difficult | 1845 | 1403638539.292190 | 1403638631.627920 | 92.336 |
| orbslam3 | MH_05_difficult | 2082 | 1403638527.627830 | 1403638631.677830 | 104.050 |

## Interpretation

- ORB-SLAM3 trajectories generally cover full or near-full sequence timestamps.
- OpenVINS trajectories start later because of the ROS serial EuRoC bag_start settings.
- Fair-overlap metrics should crop all compared trajectories to a common timestamp interval before recomputing APE/RPE.

