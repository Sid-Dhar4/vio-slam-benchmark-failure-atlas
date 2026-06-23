#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SEQUENCES = ["MH_01_easy", "MH_03_medium", "MH_05_difficult"]
SYSTEMS = ["orbslam3", "openvins"]
MAX_TIME_DIFF_S = 0.02

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
    t = ref_mean - r @ est_mean
    return (r @ est.T).T + t

def compute_error_timeline(sequence: str, system: str):
    ref_path = Path("results/trajectories/groundtruth") / f"{sequence}.tum"
    est_path = Path("results/trajectories") / system / f"{sequence}.tum"
    ref_t, ref_p = read_tum_positions(ref_path)
    est_t, est_p = read_tum_positions(est_path)
    matched_t, matched_est, matched_ref = associate_by_timestamp(est_t, est_p, ref_t, ref_p, MAX_TIME_DIFF_S)
    aligned_est = rigid_align_positions(matched_est, matched_ref)
    errors = np.linalg.norm(aligned_est - matched_ref, axis=1)
    rel_t = matched_t - ref_t[0]
    return rel_t, errors, len(matched_t)

def parse_event_summary() -> dict[tuple[str, str], dict[str, str]]:
    path = Path("results/tables/event_summary.md")
    lines = [line for line in path.read_text().splitlines() if line.startswith("|")]
    lines = [line for line in lines if not set(line.replace("|", "").strip()) <= {"-", ":"}]
    header = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows = {}
    for line in lines[1:]:
        values = [cell.strip() for cell in line.strip("|").split("|")]
        row = dict(zip(header, values))
        rows[(row["System"], row["Sequence"])] = row
    return rows

def event_text(sequence: str, events: dict[tuple[str, str], dict[str, str]]) -> str:
    orb = events[("orbslam3", sequence)]
    ov = events[("openvins", sequence)]

    return "\n".join(
        [
            "Log event counts",
            f"ORB init accel: {orb.get('not_enough_acceleration', '0')}",
            f"ORB init motion: {orb.get('not_enough_motion_initialization', '0')}",
            f"ORB reset evidence: {orb.get('local_mapping_reset', '0')}",
            f"ORB bad IMU/lost: {orb.get('bad_imu_reset', '0')}/{orb.get('frames_set_lost', '0')}",
            f"OpenVINS static init: {ov.get('openvins_static_init_failures', '0')}",
            f"OpenVINS unload exception: {ov.get('library_unload_exception', '0')}",
        ]
    )

def make_plot(sequence: str, events) -> None:
    output_dir = Path("results/plots/errors")
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11, 6))

    for system in SYSTEMS:
        rel_t, errors, matched = compute_error_timeline(sequence, system)
        rmse = float(np.sqrt(np.mean(errors ** 2)))
        label = f"{system} RMSE={rmse:.3f}m matched={matched}"
        ax.plot(rel_t, errors, label=label, linewidth=1.5)

    ax.set_title(f"{sequence}: translational error timeline after rigid alignment")
    ax.set_xlabel("Sequence time (s)")
    ax.set_ylabel("Translation error (m)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")

    ax.text(
        1.02,
        0.98,
        event_text(sequence, events),
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8,
        bbox={"boxstyle": "round", "alpha": 0.15},
    )

    fig.tight_layout(rect=[0.0, 0.0, 0.78, 1.0])

    output_path = output_dir / f"{sequence}_error_timeline.png"
    fig.savefig(output_path, dpi=160)
    plt.close(fig)
    print(f"Wrote {output_path}")

def main() -> int:
    events = parse_event_summary()
    for sequence in SEQUENCES:
        make_plot(sequence, events)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
