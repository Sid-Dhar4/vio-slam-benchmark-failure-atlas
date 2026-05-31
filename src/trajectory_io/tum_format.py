from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Pose:
    timestamp: float
    tx: float
    ty: float
    tz: float
    qx: float
    qy: float
    qz: float
    qw: float


def parse_tum_line(line: str) -> Pose:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        raise ValueError("Cannot parse empty or comment line as a pose.")

    parts = stripped.split()
    if len(parts) != 8:
        raise ValueError(f"Expected 8 TUM columns, got {len(parts)}: {line!r}")

    values = [float(x) for x in parts]
    return Pose(*values)


def validate_timestamps_increasing(poses: Iterable[Pose]) -> None:
    previous = None
    for pose in poses:
        if previous is not None and pose.timestamp <= previous:
            raise ValueError("TUM timestamps must be strictly increasing.")
        previous = pose.timestamp


def read_tum(path: str | Path) -> list[Pose]:
    path = Path(path)
    poses: list[Pose] = []

    for line_no, line in enumerate(path.read_text().splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            poses.append(parse_tum_line(line))
        except ValueError as exc:
            raise ValueError(f"{path}:{line_no}: {exc}") from exc

    validate_timestamps_increasing(poses)
    return poses


def format_tum_line(pose: Pose) -> str:
    return f"{pose.timestamp:.9f} {pose.tx:.9f} {pose.ty:.9f} {pose.tz:.9f} {pose.qx:.9f} {pose.qy:.9f} {pose.qz:.9f} {pose.qw:.9f}"


def write_tum(path: str | Path, poses: Iterable[Pose]) -> None:
    path = Path(path)
    pose_list = list(poses)
    validate_timestamps_increasing(pose_list)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [format_tum_line(pose) for pose in pose_list]
    path.write_text("\n".join(lines) + "\n")
