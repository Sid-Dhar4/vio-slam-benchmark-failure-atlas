#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

REQUIRED_FILES = [
    Path("results/metrics.csv"),
    Path("results/tables/benchmark_summary.md"),
    Path("results/tables/trajectory_coverage.md"),
    Path("results/tables/fair_overlap_summary.md"),
    Path("results/tables/event_summary.md"),
    Path("reports/failure_atlas.md"),
    Path("reports/failure_cards/MH_01_easy.md"),
    Path("reports/failure_cards/MH_03_medium.md"),
    Path("reports/failure_cards/MH_05_difficult.md"),
    Path("results/plots/errors/MH_01_easy_error_timeline.png"),
    Path("results/plots/errors/MH_03_medium_error_timeline.png"),
    Path("results/plots/errors/MH_05_difficult_error_timeline.png"),
    Path("scripts/reproduce_results.sh"),
    Path("media/vio_failure_teaser.png"),
    Path("media/vio_failure_teaser.gif"),
]

TEXT_EXPECTATIONS = {
    Path("README.md"): [
        "Diagnostic artifacts",
        "Key failure case: MH_05_difficult",
        "./scripts/reproduce_results.sh",
    ],
    Path("docs/result_interpretation.md"): [
        "fair-overlap metrics in `results/tables/fair_overlap_summary.md`",
    ],
    Path("reports/failure_atlas.md"): [
        "Status: public benchmark release",
        "Future extensions",
    ],
}

FORBIDDEN_TEXT = [
    "first benchmark draft",
    "not run yet",
    "stronger future version should explicitly compute fair-overlap",
    "Add APE/RPE over-time plots",
    "trajectory overlay plots",
    "fairness note",
]

def check_png_signature(path: Path) -> str | None:
    if path.suffix.lower() != ".png":
        return None
    data = path.read_bytes()[:8]
    if data != b"\x89PNG\r\n\x1a\n":
        return f"{path} is not a valid PNG by signature"
    return None

def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required artifact: {path}")
            continue
        if path.stat().st_size == 0:
            errors.append(f"Required artifact is empty: {path}")
        png_error = check_png_signature(path)
        if png_error:
            errors.append(png_error)

    for path, expected_strings in TEXT_EXPECTATIONS.items():
        text = path.read_text()
        for expected in expected_strings:
            if expected not in text:
                errors.append(f"{path} is missing expected text: {expected}")

    searchable_files = [Path("README.md"), Path("docs/result_interpretation.md"), Path("reports/failure_atlas.md")]
    searchable_files.extend(Path("reports/sequence_notes").glob("*.md"))
    for path in searchable_files:
        text = path.read_text()
        for forbidden in FORBIDDEN_TEXT:
            if forbidden in text:
                errors.append(f"{path} contains stale text: {forbidden}")

    if errors:
        print("Artifact check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Artifact check passed for {len(REQUIRED_FILES)} required files.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
