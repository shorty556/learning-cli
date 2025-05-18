import json
import subprocess

from .conftest import BIN


def test_cli_roundtrip(sample_csv, tmp_path):
    out = tmp_path / "out.json"
    subprocess.run(
        [BIN, "-i", sample_csv, "-o", out, "--indent", "0"],
        capture_output=True,
        text=True,
        check=True,
    )

    assert out.exists()
    assert json.loads(out.read_text())[1]["Name"] == "Bob"
