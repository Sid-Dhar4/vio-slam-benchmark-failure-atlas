# Benchmark Brief

Status: core two-backend benchmark complete.

This benchmark currently compares ORB-SLAM3 and OpenVINS on three EuRoC Machine Hall visual-inertial sequences:

- MH_01_easy
- MH_03_medium
- MH_05_difficult

Artifacts generated:
- raw backend trajectories
- converted TUM trajectories
- evo APE/RPE metrics
- runtime logs
- OpenVINS timing logs
- sequence-level notes
- metrics.csv

Important limitation:
OpenVINS runs used EuRoC Machine Hall start offsets from its ROS launch workflow. ORB-SLAM3 runs used the full sequence timestamps. The current evo metrics use timestamp association over overlapping estimates, but the README and failure atlas should clearly document this difference.

OpenVINS status note:
All three OpenVINS runs produced trajectory and timing files but ended with a ROS shutdown LibraryUnloadException. They are marked completed_with_shutdown_exception rather than clean completed runs.
