#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from trajectory_io.tum_format import Pose, write_tum


def read_orbslam3_euroc(path: Path) -> list[Pose]:
    poses = []
    for line_no, line in enumerate(path.read_text().splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = stripped.split()
        if len(parts) != 8:
            raise ValueError(f"{path}:{line_no}: expected 8 columns, got {len(parts)}")
        timestamp_raw = float(parts[0])
        timestamp_s = timestamp_raw * 1e-9 if timestamp_raw > 1e12 else timestamp_raw
        tx, ty, tz, qx, qy, qz, qw = map(float, parts[1:])
        poses.append(Pose(timestamp_s, tx, ty, tz, qx, qy, qz, qw))
    return poses


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert ORB-SLAM3 EuRoC trajectory output to TUM seconds format.")
    parser.add_argument("--input", required=True, help="ORB-SLAM3 raw EuRoC trajectory file")
    parser.add_argument("--output", required=True, help="Output TUM trajectory path")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    poses = read_orbslam3_euroc(input_path)
    write_tum(output_path, poses)

    print(f"Converted {len(poses)} poses")
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}")
    if poses:
        print(f"Start time: {poses[0].timestamp:.9f}")
        print(f"End time:   {poses[-1].timestamp:.9f}")


if __name__ == "__main__":
    main()
