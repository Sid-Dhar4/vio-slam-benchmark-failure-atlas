#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

SEQUENCE_ORDER = {
    "MH_01_easy": 0,
    "MH_03_medium": 1,
    "MH_05_difficult": 2,
}


def clean_cell(value: str) -> str:
    return value.replace("|", "/").strip()


def main() -> None:
    metrics_path = Path("results/metrics.csv")
    output_path = Path("results/tables/benchmark_summary.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with metrics_path.open(newline="") as f:
        rows = list(csv.DictReader(f))

    rows.sort(key=lambda row: (SEQUENCE_ORDER.get(row["sequence"], 99), row["system"]))

    lines = [
        "| System | Sequence | Status | Poses | Runtime (s) | APE RMSE SE3 (m) | RPE trans RMSE (m) | Notes |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ]

    for row in rows:
        lines.append(
            "| {} | {} | {} | {} | {} | {} | {} | {} |".format(
                clean_cell(row["system"]),
                clean_cell(row["sequence"]),
                clean_cell(row["status"]),
                clean_cell(row["num_poses"]),
                clean_cell(row["runtime_wall_clock_s"]),
                clean_cell(row["ape_rmse_m_se3_align"]),
                clean_cell(row["rpe_trans_rmse_m_delta1_align"]),
                clean_cell(row["notes"]),
            )
        )

    output_path.write_text("\n".join(lines) + "\n")
    print(output_path.read_text())


if __name__ == "__main__":
    main()
