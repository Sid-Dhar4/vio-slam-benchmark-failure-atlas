# Host Audit

Date: 2026-05-27

Observed setup:
- Ubuntu 24.04.4 LTS
- Kernel: 6.17.0-23-generic
- GCC/G++: 13.3.0
- CMake: 3.28.3
- Ninja: 1.11.1
- Python: 3.12.3 system Python
- Conda: available
- Docker: not installed yet
- NVIDIA driver: nvidia-smi cannot communicate with driver
- ROS 2 Jazzy: ros2 command found

Decision:
- Use Conda for Python tooling, evo, plotting, and tests.
- Do not build ORB-SLAM3/OpenVINS natively until Docker/backend strategy is pinned.
- Do not fix NVIDIA driver as part of the initial benchmark unless it becomes necessary.

## Docker installation update

Docker Engine was installed after the dataset foundation was completed.
Verification command:
sudo docker run --rm hello-world

Reason for Docker:
- Avoid native Ubuntu 24.04 dependency drift for ORB-SLAM3/OpenVINS.
- Keep backend builds reproducible and isolated.
