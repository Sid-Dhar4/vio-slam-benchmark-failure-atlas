#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


REQUIRED_RELATIVE_PATHS = [
    "mav0/cam0/data.csv",
    "mav0/cam0/data",
    "mav0/cam1/data.csv",
    "mav0/cam1/data",
    "mav0/imu0/data.csv",
    "mav0/state_groundtruth_estimate0/data.csv",
]


def load_sequence_names(config_path: Path) -> list[str]:
    data = yaml.safe_load(config_path.read_text())
    sequences = data.get("sequences", [])
    names = [item["name"] for item in sequences]
    if not names:
        raise ValueError(f"No sequences found in {config_path}")
    return names


def check_sequence(root: Path, sequence_name: str) -> list[Path]:
    sequence_dir = root / sequence_name
    missing = []

    for relative in REQUIRED_RELATIVE_PATHS:
        path = sequence_dir / relative
        if not path.exists():
            missing.append(path)

    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description="Check expected EuRoC ASL-style dataset layout.")
    parser.add_argument("--root", default="~/datasets/euroc", help="EuRoC dataset root")
    parser.add_argument("--config", default="configs/datasets/euroc_sequences.yaml", help="Sequence config YAML")
    args = parser.parse_args()

    root = Path(args.root).expanduser()
    config_path = Path(args.config)

    print(f"Dataset root: {root}")
    print(f"Sequence config: {config_path}")

    sequence_names = load_sequence_names(config_path)
    any_missing = False

    for sequence_name in sequence_names:
        missing = check_sequence(root, sequence_name)
        if missing:
            any_missing = True
            print(f"\n[MISSING] {sequence_name}")
            for path in missing:
                print(f"  - {path}")
        else:
            print(f"\n[OK] {sequence_name}")

    if any_missing:
        print("\nDataset check failed: at least one required file/folder is missing.")
        return 1

    print("\nDataset check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
