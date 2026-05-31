# Dataset Layout

Raw datasets are stored outside this repository.

Expected local root:

```text
~/datasets/euroc/
```

Benchmark sequences:

```text
MH_01_easy
MH_03_medium
MH_05_difficult
```

Expected EuRoC ASL-style sequence layout:

```text
~/datasets/euroc/MH_01_easy/
  mav0/
    cam0/
      data.csv
      data/
    cam1/
      data.csv
      data/
    imu0/
      data.csv
    state_groundtruth_estimate0/
      data.csv
```

Why data is outside git:

- EuRoC sequences are large.
- GitHub should contain code, configs, docs, and generated summary results, not raw datasets.
- Reproduction docs should explain how to obtain and place the data.

First required ground-truth conversion command after downloading MH_01_easy:

```bash
PYTHONPATH=src python scripts/convert_euroc_groundtruth.py \
  --input ~/datasets/euroc/MH_01_easy/mav0/state_groundtruth_estimate0/data.csv \
  --output results/trajectories/groundtruth/MH_01_easy.tum
```
