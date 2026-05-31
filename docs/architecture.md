# Architecture

Benchmark data flow:

EuRoC dataset -> backend runner -> trajectory conversion -> evo evaluation -> metrics.csv -> plots -> failure atlas

Backends:
- ORB-SLAM3 produces raw trajectory and logs.
- OpenVINS produces raw trajectory and logs.
- Python scripts convert outputs into common TUM trajectory format.
- evo computes ATE and RPE metrics.
