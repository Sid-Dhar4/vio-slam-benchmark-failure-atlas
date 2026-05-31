from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_euroc_dataset.py"
SPEC = importlib.util.spec_from_file_location("check_euroc_dataset", MODULE_PATH)
check_euroc_dataset = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(check_euroc_dataset)


def test_load_sequence_names(tmp_path):
    config_path = tmp_path / "euroc_sequences.yaml"
    config_path.write_text(
        "sequences:\n"
        "  - name: MH_01_easy\n"
        "  - name: MH_03_medium\n"
    )

    names = check_euroc_dataset.load_sequence_names(config_path)

    assert names == ["MH_01_easy", "MH_03_medium"]


def test_check_sequence_reports_missing_paths(tmp_path):
    root = tmp_path / "euroc"
    sequence_dir = root / "MH_01_easy"
    sequence_dir.mkdir(parents=True)

    missing = check_euroc_dataset.check_sequence(root, "MH_01_easy")

    assert len(missing) == len(check_euroc_dataset.REQUIRED_RELATIVE_PATHS)
    assert sequence_dir / "mav0/cam0/data.csv" in missing


def test_check_sequence_passes_when_required_layout_exists(tmp_path):
    root = tmp_path / "euroc"
    sequence_dir = root / "MH_01_easy"

    for relative_path in check_euroc_dataset.REQUIRED_RELATIVE_PATHS:
        path = sequence_dir / relative_path
        if relative_path.endswith("data"):
            path.mkdir(parents=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("placeholder\n")

    missing = check_euroc_dataset.check_sequence(root, "MH_01_easy")

    assert missing == []
