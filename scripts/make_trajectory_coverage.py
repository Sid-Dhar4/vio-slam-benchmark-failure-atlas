#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CoverageRow:
    system: str
    sequence: str
    poses: int
    start_s: float
    end_s: float
    duration_s: float

def read_timestamps(path: Path) -> list[float]:
    timestamps: list[float] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            timestamps.append(float(line.split()[0]))
    return timestamps

def coverage_for_file(path: Path) -> CoverageRow:
    timestamps = read_timestamps(path)
    if not timestamps:
        raise ValueError(f"No poses found in {path}")
    system = path.parent.name
    sequence = path.stem
    start_s = timestamps[0]
    end_s = timestamps[-1]
    return CoverageRow(system, sequence, len(timestamps), start_s, end_s, end_s - start_s)

def make_markdown(rows: list[CoverageRow]) -> str:
    lines: list[str] = []
    lines.append("# Trajectory Coverage")
    lines.append("")
    lines.append("This table reports the timestamp coverage of each trajectory used in the current benchmark.")
    lines.append("")
    lines.append("It makes the start-offset caveat explicit: OpenVINS trajectories begin later than the ground-truth and ORB-SLAM3 trajectories because the current OpenVINS EuRoC workflow uses Machine Hall bag_start offsets.")
    lines.append("")
    lines.append("| System | Sequence | Poses | Start timestamp (s) | End timestamp (s) | Duration (s) |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for row in rows:
        lines.append(f"| {row.system} | {row.sequence} | {row.poses} | {row.start_s:.6f} | {row.end_s:.6f} | {row.duration_s:.3f} |")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("- ORB-SLAM3 trajectories generally cover full or near-full sequence timestamps.")
    lines.append("- OpenVINS trajectories start later because of the ROS serial EuRoC bag_start settings.")
    lines.append("- Fair-overlap metrics should crop all compared trajectories to a common timestamp interval before recomputing APE/RPE.")
    lines.append("")
    return "\n".join(lines)

def main() -> int:
    trajectory_root = Path("results/trajectories")
    output_path = Path("results/tables/trajectory_coverage.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = [coverage_for_file(path) for path in sorted(trajectory_root.glob("*/*.tum"))]
    rows.sort(key=lambda row: (row.sequence, row.system))

    markdown = make_markdown(rows)
    output_path.write_text(markdown + "\n")
    print(f"Wrote {output_path}")
    print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
