import pytest

from trajectory_io.euroc_format import convert_euroc_groundtruth_to_tum, read_euroc_groundtruth_csv
from trajectory_io.tum_format import read_tum


EUROC_HEADER = ",".join([
    "#timestamp [ns]",
    "p_RS_R_x [m]",
    "p_RS_R_y [m]",
    "p_RS_R_z [m]",
    "q_RS_w []",
    "q_RS_x []",
    "q_RS_y []",
    "q_RS_z []",
    "v_RS_R_x [m s^-1]",
])


def test_read_euroc_groundtruth_csv_converts_to_tum_pose_order(tmp_path):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text(
        EUROC_HEADER + "\n"
        + "1403636579758555392,1,2,3,0.707,0.1,0.2,0.3,99\n"
    )

    poses = read_euroc_groundtruth_csv(csv_path)

    assert len(poses) == 1
    pose = poses[0]
    assert pose.timestamp == pytest.approx(1403636579.7585554)
    assert pose.tx == 1.0
    assert pose.ty == 2.0
    assert pose.tz == 3.0
    assert pose.qx == 0.1
    assert pose.qy == 0.2
    assert pose.qz == 0.3
    assert pose.qw == 0.707


def test_convert_euroc_groundtruth_to_tum_writes_tum_file(tmp_path):
    csv_path = tmp_path / "data.csv"
    out_path = tmp_path / "groundtruth.tum"
    csv_path.write_text(
        EUROC_HEADER + "\n"
        + "1000000000,1,0,0,1,0,0,0,0\n"
        + "2000000000,2,0,0,1,0,0,0,0\n"
    )

    convert_euroc_groundtruth_to_tum(csv_path, out_path)
    poses = read_tum(out_path)

    assert [pose.timestamp for pose in poses] == [1.0, 2.0]
    assert [pose.tx for pose in poses] == [1.0, 2.0]


def test_missing_required_column_is_rejected(tmp_path):
    csv_path = tmp_path / "bad.csv"
    csv_path.write_text("#timestamp [ns],p_RS_R_x [m]\n1000000000,1\n")

    with pytest.raises(ValueError, match="Missing required EuRoC"):
        read_euroc_groundtruth_csv(csv_path)
