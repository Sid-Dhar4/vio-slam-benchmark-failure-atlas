# Ground Truth Conversion

This project converts EuRoC ground-truth CSV files into TUM trajectory format before running evo evaluation.

EuRoC ground truth input:

```text
mav0/state_groundtruth_estimate0/data.csv
```

TUM output format:

```text
timestamp tx ty tz qx qy qz qw
```

Important conversion details:

- EuRoC timestamps are nanoseconds; TUM timestamps are seconds.
- EuRoC quaternion order is read as qw qx qy qz.
- TUM quaternion order is written as qx qy qz qw.
- Timestamps must be strictly increasing.

Example command:

```bash
PYTHONPATH=src python scripts/convert_euroc_groundtruth.py \
  --input ~/datasets/euroc/MH_01_easy/mav0/state_groundtruth_estimate0/data.csv \
  --output results/trajectories/groundtruth/MH_01_easy.tum
```
