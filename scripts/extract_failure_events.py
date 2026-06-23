#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

PATTERNS = {
    "openvins_static_init_failures": re.compile(r"failed static init", re.I),
    "not_enough_acceleration": re.compile(r"not enough acceleration", re.I),
    "not_enough_motion_initialization": re.compile(r"Not enough motion for initializing", re.I),
    "local_mapping_reset": re.compile(r"LM: Reseting current map|Reset map because", re.I),
    "bad_imu_reset": re.compile(r"bad imu flag", re.I),
    "frames_set_lost": re.compile(r"[0-9]+ Frames set to lost", re.I),
    "library_unload_exception": re.compile(r"LibraryUnloadException", re.I),
    "shutdown": re.compile(r"^Shutdown$|Initiating shutdown", re.I),
}

@dataclass(frozen=True)
class EventRow:
    system: str
    sequence: str
    counts: dict[str, int]
    notes: str

def infer_system_and_sequence(path: Path) -> tuple[str, str]:
    system = path.parent.name
    sequence = path.stem
    return system, sequence

def count_patterns(lines: list[str]) -> dict[str, int]:
    return {
        name: sum(1 for line in lines if pattern.search(line))
        for name, pattern in PATTERNS.items()
    }

def make_notes(system: str, sequence: str, counts: dict[str, int]) -> str:
    notes: list[str] = []
    if counts["openvins_static_init_failures"]:
        notes.append("static initialization failures observed")
    if counts["not_enough_motion_initialization"] or counts["not_enough_acceleration"]:
        notes.append("initialization excitation issues observed")
    if counts["local_mapping_reset"]:
        notes.append("map/local-mapping reset evidence observed")
    if counts["bad_imu_reset"]:
        notes.append("bad-IMU reset evidence observed")
    if counts["frames_set_lost"]:
        notes.append("lost-frame evidence observed")
    if counts["library_unload_exception"]:
        notes.append("ROS shutdown LibraryUnloadException observed")
    return "; ".join(notes) if notes else "no selected failure pattern matched"

def extract_row(path: Path) -> EventRow:
    system, sequence = infer_system_and_sequence(path)
    lines = path.read_text(errors="replace").splitlines()
    counts = count_patterns(lines)
    notes = make_notes(system, sequence, counts)
    return EventRow(system=system, sequence=sequence, counts=counts, notes=notes)

def make_markdown(rows: list[EventRow]) -> str:
    keys = list(PATTERNS.keys())
    lines: list[str] = []
    lines.append("# Failure Event Summary")
    lines.append("")
    lines.append("This table summarizes selected failure-related log patterns from the current ORB-SLAM3 and OpenVINS benchmark runs.")
    lines.append("")
    lines.append("Counts are log-line counts for selected patterns, not guaranteed counts of unique physical events.")
    lines.append("")
    header = ["System", "Sequence"] + keys + ["Notes"]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|---|---|" + "|".join(["---:" for _ in keys]) + "|---|")
    for row in rows:
        values = [row.system, row.sequence] + [str(row.counts[key]) for key in keys] + [row.notes]
        lines.append("| " + " | ".join(values) + " |")
    lines.append("")
    lines.append("## Interpretation notes")
    lines.append("")
    lines.append("- OpenVINS static initialization failures indicate repeated failed attempts to initialize under the current bag_start workflow.")
    lines.append("- ORB-SLAM3 not-enough-acceleration and not-enough-motion messages indicate visual-inertial initialization sensitivity.")
    lines.append("- Reset counts are log-line counts and may include multiple lines from one reset episode.")
    lines.append("- Lost-frame counts only include explicit frame-loss lines such as `109 Frames set to lost`, not configuration strings containing the word Lost.")
    lines.append("- LibraryUnloadException counts document the repeatable OpenVINS ROS shutdown exception after output files were produced.")
    lines.append("")
    return "\n".join(lines)

def main() -> int:
    log_paths = sorted(Path("results/logs").glob("*/*.log"))
    log_paths = [path for path in log_paths if path.parent.name in {"orbslam3", "openvins"}]
    rows = [extract_row(path) for path in log_paths]
    rows.sort(key=lambda row: (row.sequence, row.system))
    output_path = Path("results/tables/event_summary.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown = make_markdown(rows)
    output_path.write_text(markdown + "\n")
    print(f"Wrote {output_path}")
    print(markdown)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
