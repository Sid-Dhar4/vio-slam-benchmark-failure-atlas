#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

SEQUENCES = ["MH_01_easy", "MH_03_medium", "MH_05_difficult"]
SYSTEMS = ["orbslam3", "openvins"]

DESCRIPTIONS = {
    "MH_01_easy": "Sanity-check sequence. Both systems produced trajectories; useful for validating the benchmark pipeline.",
    "MH_03_medium": "Moderate-difficulty sequence. Useful for inspecting repeated initialization and reset behavior.",
    "MH_05_difficult": "Stress sequence in the current benchmark. Useful for inspecting bad-IMU and lost-frame evidence.",
}

INTERPRETATIONS = {
    "MH_01_easy": "ORB-SLAM3 has lower aligned APE, while OpenVINS has lower local RPE. Treat this as a sanity-check result with OpenVINS start-offset and shutdown caveats.",
    "MH_03_medium": "ORB-SLAM3 has lower aligned APE, but its logs show repeated initialization/reset evidence. Local RPE values are close, so global error and local motion should be interpreted separately.",
    "MH_05_difficult": "This is the strongest failure case. ORB-SLAM3 shows bad-IMU and lost-frame evidence but still produces the lower aligned APE. OpenVINS shows many static initialization failures and the repeatable shutdown exception.",
}

IMPROVEMENTS = {
    "MH_01_easy": "Use fair-overlap metrics and verify whether OpenVINS local RPE remains lower on the common time interval.",
    "MH_03_medium": "Inspect ORB-SLAM3 initialization windows and add error-over-time plots around reset-heavy regions.",
    "MH_05_difficult": "Prioritize error-timeline plots and event markers for bad-IMU reset and explicit lost-frame evidence.",
}

METRIC_COLUMNS = {
    "status": "status",
    "poses": "num_poses",
    "runtime": "runtime_wall_clock_s",
    "ape": "ape_rmse_m_se3_align",
    "rpe": "rpe_trans_rmse_m_delta1_align",
}

COVERAGE_COLUMNS = {
    "poses": "Poses",
    "start": "Start timestamp (s)",
    "end": "End timestamp (s)",
    "duration": "Duration (s)",
}

EVENT_COLUMNS = [
    "openvins_static_init_failures",
    "not_enough_acceleration",
    "not_enough_motion_initialization",
    "local_mapping_reset",
    "bad_imu_reset",
    "frames_set_lost",
    "library_unload_exception",
]


def read_metrics() -> dict[tuple[str, str], dict[str, str]]:
    with Path("results/metrics.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    return {(row["system"], row["sequence"]): row for row in rows}


def parse_markdown_table(path: Path) -> list[dict[str, str]]:
    table_lines: list[str] = []
    for line in path.read_text().splitlines():
        if not line.startswith("|"):
            continue
        stripped = line.replace("|", "").strip()
        if stripped and set(stripped) <= {"-", ":"}:
            continue
        table_lines.append(line)

    if not table_lines:
        return []

    header = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []

    for line in table_lines[1:]:
        values = [cell.strip() for cell in line.strip("|").split("|")]
        if len(values) == len(header):
            rows.append(dict(zip(header, values)))

    return rows


def index_rows(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    indexed: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        system = row.get("System", "").lower()
        sequence = row.get("Sequence", "")
        if system and sequence:
            indexed[(system, sequence)] = row
    return indexed


def metric_row(system: str, sequence: str, metrics: dict[tuple[str, str], dict[str, str]]) -> str:
    row = metrics[(system, sequence)]
    return (
        f"| {system} | {row[METRIC_COLUMNS['status']]} | {row[METRIC_COLUMNS['poses']]} | "
        f"{row[METRIC_COLUMNS['runtime']]} | {row[METRIC_COLUMNS['ape']]} | "
        f"{row[METRIC_COLUMNS['rpe']]} |"
    )


def coverage_row(system: str, sequence: str, coverage: dict[tuple[str, str], dict[str, str]]) -> str:
    row = coverage[(system, sequence)]
    return (
        f"| {system} | {row.get(COVERAGE_COLUMNS['poses'], '-')} | "
        f"{row.get(COVERAGE_COLUMNS['start'], '-')} | "
        f"{row.get(COVERAGE_COLUMNS['end'], '-')} | "
        f"{row.get(COVERAGE_COLUMNS['duration'], '-')} |"
    )


def event_row(system: str, sequence: str, events: dict[tuple[str, str], dict[str, str]]) -> str:
    row = events[(system, sequence)]
    values = [row.get(key, "0") for key in EVENT_COLUMNS]
    return "| " + system + " | " + " | ".join(values) + " |"


def make_card(sequence: str, metrics, events, coverage) -> str:
    lines: list[str] = []
    lines.append(f"# Failure Card: {sequence}")
    lines.append("")
    lines.append(DESCRIPTIONS[sequence])
    lines.append("")
    lines.append("## Metrics")
    lines.append("")
    lines.append("| System | Status | Poses | Runtime (s) | APE RMSE SE3 (m) | RPE trans RMSE (m) |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for system in SYSTEMS:
        lines.append(metric_row(system, sequence, metrics))
    lines.append("")
    lines.append("## Trajectory coverage")
    lines.append("")
    lines.append("| System | Poses | Start timestamp (s) | End timestamp (s) | Duration (s) |")
    lines.append("|---|---:|---:|---:|---:|")
    for system in ["groundtruth", "orbslam3", "openvins"]:
        lines.append(coverage_row(system, sequence, coverage))
    lines.append("")
    lines.append("## Failure event counts")
    lines.append("")
    lines.append("Counts are log-line counts for selected patterns, not guaranteed unique physical events.")
    lines.append("")
    lines.append("| System | static init fail | not enough accel | not enough motion | reset evidence | bad IMU | frames set lost | unload exception |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for system in SYSTEMS:
        lines.append(event_row(system, sequence, events))
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(INTERPRETATIONS[sequence])
    lines.append("")
    lines.append("## Suggested next improvement")
    lines.append("")
    lines.append(IMPROVEMENTS[sequence])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    metrics = read_metrics()
    events = index_rows(parse_markdown_table(Path("results/tables/event_summary.md")))
    coverage = index_rows(parse_markdown_table(Path("results/tables/trajectory_coverage.md")))

    output_dir = Path("reports/failure_cards")
    output_dir.mkdir(parents=True, exist_ok=True)

    for sequence in SEQUENCES:
        path = output_dir / f"{sequence}.md"
        path.write_text(make_card(sequence, metrics, events, coverage) + "\n")
        print(f"Wrote {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
