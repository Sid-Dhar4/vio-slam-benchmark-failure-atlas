# Backend Docker Setup

Backend builds are isolated in Docker instead of building directly on Ubuntu 24.04.

Reason:
- ORB-SLAM3 and OpenVINS have older dependency expectations.
- The host machine uses Ubuntu 24.04 and GCC 13, which can cause dependency drift.
- Docker keeps backend builds reproducible and separate from host ROS 2 Jazzy.

Planned backend order:
1. Build a generic C++/OpenCV/Eigen base image.
2. Build ORB-SLAM3 on top of the base image.
3. Run ORB-SLAM3 on MH_01_easy first.
4. Add OpenVINS after the ORB-SLAM3 data path is understood.
