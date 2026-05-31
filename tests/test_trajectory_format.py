import pytest

from trajectory_io.tum_format import Pose, parse_tum_line, read_tum, write_tum


def test_parse_tum_line():
    pose = parse_tum_line("1.5 1 2 3 0 0 0 1")
    assert pose.timestamp == 1.5
    assert pose.tx == 1.0
    assert pose.ty == 2.0
    assert pose.tz == 3.0
    assert pose.qx == 0.0
    assert pose.qy == 0.0
    assert pose.qz == 0.0
    assert pose.qw == 1.0


def test_read_write_round_trip(tmp_path):
    poses = [
        Pose(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0),
        Pose(1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0),
    ]
    path = tmp_path / "traj.tum"
    write_tum(path, poses)
    loaded = read_tum(path)
    assert loaded == poses


def test_rejects_wrong_column_count():
    with pytest.raises(ValueError, match="Expected 8 TUM columns"):
        parse_tum_line("0.0 1.0 2.0")


def test_rejects_non_increasing_timestamps(tmp_path):
    path = tmp_path / "bad.tum"
    path.write_text("1.0 0 0 0 0 0 0 1\n1.0 1 0 0 0 0 0 1\n")
    with pytest.raises(ValueError, match="strictly increasing"):
        read_tum(path)
