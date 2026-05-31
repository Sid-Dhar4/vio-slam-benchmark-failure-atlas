from __future__ import annotations

import csv
from pathlib import Path

from trajectory_io.tum_format import Pose, validate_timestamps_increasing, write_tum


REQUIRED_COLUMNS = {
    "timestamp": "timestamp_ns",
    "p_rs_r_x": "tx",
    "p_rs_r_y": "ty",
    "p_rs_r_z": "tz",
    "q_rs_w": "qw",
    "q_rs_x": "qx",
    "q_rs_y": "qy",
    "q_rs_z": "qz",
}


def normalize_euroc_header_name(name: str) -> str:
    """Normalize EuRoC CSV headers such as "#timestamp [ns]" -> "timestamp"."""
    name = name.strip().lstrip("#").strip()
    name = name.split("[", 1)[0].strip()
    return name.lower()


def _build_column_index(header: list[str]) -> dict[str, int]:
    normalized = {normalize_euroc_header_name(name): idx for idx, name in enumerate(header)}
    missing = [name for name in REQUIRED_COLUMNS if name not in normalized]
    if missing:
        raise ValueError(f"Missing required EuRoC ground-truth columns: {missing}")
    return {name: normalized[name] for name in REQUIRED_COLUMNS}


def _row_to_pose(row: list[str], column_index: dict[str, int]) -> Pose:
    timestamp_ns = float(row[column_index["timestamp"]])
    timestamp_s = timestamp_ns * 1e-9

    tx = float(row[column_index["p_rs_r_x"]])
    ty = float(row[column_index["p_rs_r_y"]])
    tz = float(row[column_index["p_rs_r_z"]])

    qw = float(row[column_index["q_rs_w"]])
    qx = float(row[column_index["q_rs_x"]])
    qy = float(row[column_index["q_rs_y"]])
    qz = float(row[column_index["q_rs_z"]])

    return Pose(timestamp_s, tx, ty, tz, qx, qy, qz, qw)


def read_euroc_groundtruth_csv(path: str | Path) -> list[Pose]:
    path = Path(path)
    with path.open("r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            raise ValueError(f"Empty EuRoC CSV file: {path}")

        column_index = _build_column_index(header)
        poses = []

        for line_no, row in enumerate(reader, start=2):
            if not row or all(not cell.strip() for cell in row):
                continue
            try:
                poses.append(_row_to_pose(row, column_index))
            except (IndexError, ValueError) as exc:
                raise ValueError(f"{path}:{line_no}: invalid EuRoC ground-truth row: {row}") from exc

    validate_timestamps_increasing(poses)
    return poses


def convert_euroc_groundtruth_to_tum(input_csv: str | Path, output_tum: str | Path) -> None:
    poses = read_euroc_groundtruth_csv(input_csv)
    write_tum(output_tum, poses)
