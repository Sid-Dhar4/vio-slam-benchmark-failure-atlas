# OpenVINS Setup Notes

OpenVINS will be kept outside this benchmark repository, similar to ORB-SLAM3.

Planned external source path:
~/projects/vio_slam_external/open_vins

Reason:
- Keep this repository focused on benchmark scripts, configs, results, and reports.
- Avoid vendoring a third-party VIO backend.
- Build and run OpenVINS through Docker for reproducibility.

Initial target:
- Run OpenVINS on MH_01_easy first.
- Then repeat on MH_03_medium and MH_05_difficult.
- Apply any dataset start offset consistently and document it in configs/datasets/euroc_sequences.yaml.

## Workspace path update

OpenVINS is built as a ROS 1 Catkin workspace:

```text
~/projects/vio_slam_external/openvins_ws/src/open_vins
```

The original direct clone path was moved into the workspace so that catkin_tools can build it cleanly.

## Build status

OpenVINS was built successfully inside the ROS 1 Noetic Docker image:

```text
vio-slam-openvins-ros1:noetic
```

Observed build outputs:
- devel/.private/ov_msckf/lib/ov_msckf/ros1_serial_msckf
- devel/.private/ov_eval/lib/ov_eval/pose_to_file
- devel/.private/ov_eval/lib/ov_eval/live_align_trajectory

Build log:

```text
results/logs/setup/openvins_build_20260528_183734.log
```
