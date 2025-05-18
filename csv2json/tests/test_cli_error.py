import subprocess

from .conftest import BIN


def test_missing_input_file(tmp_path):
    missing = tmp_path / "missing.csv"
    out = tmp_path / "out.json"

    res = subprocess.run(
        [BIN, "-i", missing, "-o", out], capture_output=True, text=True, check=False
    )

    assert res.returncode != 0
    assert not out.exists()


def test_no_data(empty_csv, tmp_path):
    out = tmp_path / "out.json"

    res = subprocess.run(
        [BIN, "--pretty", "-i", empty_csv, "-o", out],
        capture_output=True,
        text=True,
        check=False,
    )

    assert "No data found in the CSV file." in res.stdout


def test_invalid_filter_expr(sample_csv, tmp_path):
    out = tmp_path / "out.json"
    res = subprocess.run(
        [BIN, "-i", sample_csv, "-o", out, "--filter", "invalid_expr"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert res.returncode == 1
    assert not out.exists()
