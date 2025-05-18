import subprocess

from .conftest import BIN


def test_progress_100(sample_csv, tmp_path):
    out = tmp_path / "out.json"

    res = subprocess.run(
        [BIN, "--progress", "-i", sample_csv, "-o", out],
        capture_output=True,
        text=True,
        check=True,
    )

    total = sample_csv.stat().st_size
    assert f"{total}/{total} bytes" in res.stdout  # ← ここを stdout に
