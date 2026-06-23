# Failure Event Summary

This table summarizes selected failure-related log patterns from the current ORB-SLAM3 and OpenVINS benchmark runs.

Counts are log-line counts for selected patterns, not guaranteed counts of unique physical events.

| System | Sequence | openvins_static_init_failures | not_enough_acceleration | not_enough_motion_initialization | local_mapping_reset | bad_imu_reset | frames_set_lost | library_unload_exception | shutdown | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| openvins | MH_01_easy | 87 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | static initialization failures observed; ROS shutdown LibraryUnloadException observed |
| orbslam3 | MH_01_easy | 0 | 2 | 1 | 1 | 0 | 0 | 0 | 1 | initialization excitation issues observed; map/local-mapping reset evidence observed |
| openvins | MH_03_medium | 260 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | static initialization failures observed; ROS shutdown LibraryUnloadException observed |
| orbslam3 | MH_03_medium | 0 | 2 | 55 | 55 | 0 | 0 | 0 | 1 | initialization excitation issues observed; map/local-mapping reset evidence observed |
| openvins | MH_05_difficult | 289 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | static initialization failures observed; ROS shutdown LibraryUnloadException observed |
| orbslam3 | MH_05_difficult | 0 | 78 | 16 | 18 | 1 | 1 | 0 | 1 | initialization excitation issues observed; map/local-mapping reset evidence observed; bad-IMU reset evidence observed; lost-frame evidence observed |

## Interpretation notes

- OpenVINS static initialization failures indicate repeated failed attempts to initialize under the current bag_start workflow.
- ORB-SLAM3 not-enough-acceleration and not-enough-motion messages indicate visual-inertial initialization sensitivity.
- Reset counts are log-line counts and may include multiple lines from one reset episode.
- Lost-frame counts only include explicit frame-loss lines such as `109 Frames set to lost`, not configuration strings containing the word Lost.
- LibraryUnloadException counts document the repeatable OpenVINS ROS shutdown exception after output files were produced.

