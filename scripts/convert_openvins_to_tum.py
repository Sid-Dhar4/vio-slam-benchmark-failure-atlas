#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from trajectory_io.tum_format import Pose, write_tum

def read_openvins_estimate(path: Path) -> list[Pose]:
    poses = []
    for line_no, line in enumerate(path.read_text().splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = stripped.split()
        if len(parts) < 8:
            raise ValueError(f"{path}:{line_no}: expected at least 8 columns, got {len(parts)}")
        timestamp, tx, ty, tz, qx, qy, qz, qw = map(float, parts[:8])
        poses.append(Pose(timestamp, tx, ty, tz, qx, qy, qz, qw))
    return poses

def main() -> None:
    parser = argparse.ArgumentParser(description="Convert OpenVINS estimate.txt to TUM trajectory format.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    poses = read_openvins_estimate(Path(args.input))
    write_tum(args.output, poses)
    print(f"Converted {len(poses)} poses")
    print(f"Input:  {args.input}")
    print(f"Output: {args.output}")
    if poses:
        print(f"Start time: {poses[0].timestamp:.9f}")
        print(f"End time:   {poses[-1].timestamp:.9f}")

if __name__ == "__main__":
    main()
