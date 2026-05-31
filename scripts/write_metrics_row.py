#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

FIELDNAMES = [
    "system",
    "sequence",
    "status",
    "trajectory_type",
    "num_poses",
    "num_keyframes",
    "runtime_wall_clock_s",
    "ape_rmse_m_no_align",
    "ape_rmse_m_se3_align",
    "rpe_trans_rmse_m_delta1_align",
    "log_path",
    "trajectory_path",
    "notes",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Write or update one benchmark metrics row.")
    parser.add_argument("--output", default="results/metrics.csv")
    parser.add_argument("--system", required=True)
    parser.add_argument("--sequence", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--trajectory-type", required=True)
    parser.add_argument("--num-poses", required=True)
    parser.add_argument("--num-keyframes", default="")
    parser.add_argument("--runtime-wall-clock-s", default="")
    parser.add_argument("--ape-rmse-m-no-align", default="")
    parser.add_argument("--ape-rmse-m-se3-align", default="")
    parser.add_argument("--rpe-trans-rmse-m-delta1-align", default="")
    parser.add_argument("--log-path", default="")
    parser.add_argument("--trajectory-path", default="")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    row = {
        "system": args.system,
        "sequence": args.sequence,
        "status": args.status,
        "trajectory_type": args.trajectory_type,
        "num_poses": args.num_poses,
        "num_keyframes": args.num_keyframes,
        "runtime_wall_clock_s": args.runtime_wall_clock_s,
        "ape_rmse_m_no_align": args.ape_rmse_m_no_align,
        "ape_rmse_m_se3_align": args.ape_rmse_m_se3_align,
        "rpe_trans_rmse_m_delta1_align": args.rpe_trans_rmse_m_delta1_align,
        "log_path": args.log_path,
        "trajectory_path": args.trajectory_path,
        "notes": args.notes,
    }

    rows = []
    if output.exists():
        with output.open("r", newline="") as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader if not (r["system"] == row["system"] and r["sequence"] == row["sequence"] and r["trajectory_type"] == row["trajectory_type"])]

    rows.append(row)

    with output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} row(s) to {output}")


if __name__ == "__main__":
    main()
