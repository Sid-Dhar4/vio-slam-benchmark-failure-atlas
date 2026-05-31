#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from trajectory_io.euroc_format import convert_euroc_groundtruth_to_tum, read_euroc_groundtruth_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert EuRoC ground-truth CSV to TUM trajectory format.")
    parser.add_argument("--input", required=True, help="Path to EuRoC mav0/state_groundtruth_estimate0/data.csv")
    parser.add_argument("--output", required=True, help="Output TUM trajectory path")
    args = parser.parse_args()

    input_csv = Path(args.input)
    output_tum = Path(args.output)

    poses = read_euroc_groundtruth_csv(input_csv)
    convert_euroc_groundtruth_to_tum(input_csv, output_tum)

    print(f"Converted {len(poses)} poses")
    print(f"Input:  {input_csv}")
    print(f"Output: {output_tum}")
    if poses:
        print(f"Start time: {poses[0].timestamp:.9f}")
        print(f"End time:   {poses[-1].timestamp:.9f}")


if __name__ == "__main__":
    main()
