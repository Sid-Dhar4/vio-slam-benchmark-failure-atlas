#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import numpy as np

SEQUENCES = ["MH_01_easy", "MH_03_medium", "MH_05_difficult"]
SYSTEMS = ["orbslam3", "openvins"]
ALL_TRAJECTORIES = ["groundtruth", "orbslam3", "openvins"]
MAX_TIME_DIFF_S = 0.02

@dataclass(frozen=True)
class FairOverlapRow:
    sequence: str
    system: str
    overlap_start_s: float
    overlap_end_s: float
    overlap_duration_s: float
    matched_poses: int
    ape_rmse_m: float
    local_delta_rmse_m: float

def trajectory_path(system: str, sequence: str) -> Path:
    if system == "groundtruth":
        return Path("results/trajectories/groundtruth") / f"{sequence}.tum"
    return Path("results/trajectories") / system / f"{sequence}.tum"

def read_tum_positions(path: Path) -> tuple[np.ndarray, np.ndarray]:
    timestamps = []
    positions = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            timestamps.append(float(parts[0]))
            positions.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return np.asarray(timestamps), np.asarray(positions)

def common_overlap_interval(sequence: str) -> tuple[float, float]:
    starts = []
    ends = []
    for system in ALL_TRAJECTORIES:
        timestamps, _ = read_tum_positions(trajectory_path(system, sequence))
        starts.append(float(timestamps[0]))
        ends.append(float(timestamps[-1]))
    start = max(starts)
    end = min(ends)
    if end <= start:
        raise ValueError(f"No common overlap interval for {sequence}")
    return start, end

def crop_time(t: np.ndarray, p: np.ndarray, start: float, end: float) -> tuple[np.ndarray, np.ndarray]:
    mask = (t >= start) & (t <= end)
    return t[mask], p[mask]

def associate_by_timestamp(est_t, est_p, ref_t, ref_p, max_dt: float):
    matched_t = []
    matched_est = []
    matched_ref = []
    j = 0
    for t, p in zip(est_t, est_p):
        while j + 1 < len(ref_t) and abs(ref_t[j + 1] - t) <= abs(ref_t[j] - t):
            j += 1
        if abs(ref_t[j] - t) <= max_dt:
            matched_t.append(t)
            matched_est.append(p)
            matched_ref.append(ref_p[j])
    return np.asarray(matched_t), np.asarray(matched_est), np.asarray(matched_ref)

def rigid_align_positions(est: np.ndarray, ref: np.ndarray) -> np.ndarray:
    if len(est) < 3:
        raise ValueError("Need at least three matched poses for alignment.")
    est_mean = est.mean(axis=0)
    ref_mean = ref.mean(axis=0)
    est_centered = est - est_mean
    ref_centered = ref - ref_mean
    h = est_centered.T @ ref_centered
    u, _, vt = np.linalg.svd(h)
    r = vt.T @ u.T
    if np.linalg.det(r) < 0:
        vt[-1, :] *= -1
        r = vt.T @ u.T
    offset = ref_mean - r @ est_mean
    return (r @ est.T).T + offset

def local_delta_rmse(aligned_est: np.ndarray, ref: np.ndarray) -> float:
    if len(aligned_est) < 2:
        return float("nan")
    est_delta = np.diff(aligned_est, axis=0)
    ref_delta = np.diff(ref, axis=0)
    delta_error = np.linalg.norm(est_delta - ref_delta, axis=1)
    return float(np.sqrt(np.mean(delta_error ** 2)))

def compute_row(sequence: str, system: str) -> FairOverlapRow:
    start, end = common_overlap_interval(sequence)
    ref_t, ref_p = read_tum_positions(trajectory_path("groundtruth", sequence))
    est_t, est_p = read_tum_positions(trajectory_path(system, sequence))
    ref_t, ref_p = crop_time(ref_t, ref_p, start, end)
    est_t, est_p = crop_time(est_t, est_p, start, end)
    matched_t, matched_est, matched_ref = associate_by_timestamp(est_t, est_p, ref_t, ref_p, MAX_TIME_DIFF_S)
    aligned_est = rigid_align_positions(matched_est, matched_ref)
    errors = np.linalg.norm(aligned_est - matched_ref, axis=1)
    ape_rmse = float(np.sqrt(np.mean(errors ** 2)))
    local_rmse = local_delta_rmse(aligned_est, matched_ref)
    return FairOverlapRow(sequence, system, start, end, end - start, len(matched_t), ape_rmse, local_rmse)

def make_markdown(rows: list[FairOverlapRow]) -> str:
    lines: list[str] = []
    lines.append("# Fair-Overlap Metrics")
    lines.append("")
    lines.append("This table recomputes trajectory errors after cropping each sequence to the common timestamp interval shared by ground truth, ORB-SLAM3, and OpenVINS.")
    lines.append("")
    lines.append("APE RMSE is computed after rigid position alignment on the common interval. Local delta RMSE measures frame-to-frame translation delta disagreement on timestamp-associated poses; it is a local consistency metric, not a full evo pose RPE replacement.")
    lines.append("")
    lines.append("| Sequence | System | Overlap start (s) | Overlap end (s) | Overlap duration (s) | Matched poses | Fair APE RMSE (m) | Local delta RMSE (m) |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
    for row in rows:
        lines.append(f"| {row.sequence} | {row.system} | {row.overlap_start_s:.6f} | {row.overlap_end_s:.6f} | {row.overlap_duration_s:.3f} | {row.matched_poses} | {row.ape_rmse_m:.6f} | {row.local_delta_rmse_m:.6f} |")
    lines.append("")
    return "\n".join(lines)

def main() -> int:
    rows: list[FairOverlapRow] = []
    for sequence in SEQUENCES:
        for system in SYSTEMS:
            rows.append(compute_row(sequence, system))
    output_path = Path("results/tables/fair_overlap_summary.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown = make_markdown(rows)
    output_path.write_text(markdown + "\n")
    print(f"Wrote {output_path}")
    print(markdown)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
