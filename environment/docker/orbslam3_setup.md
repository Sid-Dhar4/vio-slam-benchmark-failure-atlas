# ORB-SLAM3 Setup Notes

ORB-SLAM3 source is kept outside this benchmark repository.

Local external source path:
~/projects/vio_slam_external/ORB_SLAM3

Reason:
- Keep the benchmark repo focused on scripts, configs, results, and documentation.
- Avoid vendoring third-party backend source code.
- Build/run commands should mount the external backend path into Docker.

## Build status

ORB-SLAM3 was built inside the Docker dependency image:

```text
vio-slam-orbslam3-deps:22.04
```

External build path:

```text
~/projects/vio_slam_external/ORB_SLAM3
```

Observed build outputs:
- lib/libORB_SLAM3.so
- Vocabulary/ORBvoc.txt
- Examples/Stereo-Inertial/stereo_inertial_euroc

Build log:

```text
results/logs/setup/orbslam3_build_20260528_171148.log
```
