| System | Sequence | Status | Poses | Runtime (s) | APE RMSE SE3 (m) | RPE trans RMSE (m) | Notes |
|---|---|---|---:|---:|---:|---:|---|
| openvins | MH_01_easy | completed_with_shutdown_exception | 2767 | 23.64 | 0.090810 | 0.002152 | bag_start=40; trajectory saved; shutdown LibraryUnloadException observed |
| orbslam3 | MH_01_easy | completed | 3678 | 203.00 | 0.048717 | 0.003445 | first ORB-SLAM3 stereo-inertial run; early initialization reset observed |
| openvins | MH_03_medium | completed_with_shutdown_exception | 2302 | 21.34 | 0.137622 | 0.004873 | bag_start=5; trajectory saved; shutdown LibraryUnloadException observed |
| orbslam3 | MH_03_medium | completed | 2696 | 146.18 | 0.034222 | 0.004600 | controlled ORB-SLAM3 stereo-inertial rerun; repeated initialization resets observed |
| openvins | MH_05_difficult | completed_with_shutdown_exception | 1845 | 17.53 | 0.242839 | 0.004271 | bag_start=5; trajectory saved; shutdown LibraryUnloadException observed |
| orbslam3 | MH_05_difficult | completed | 2082 | 123.69 | 0.075237 | 0.005066 | controlled ORB-SLAM3 stereo-inertial run; bad IMU/reset/lost-frame behavior observed |
