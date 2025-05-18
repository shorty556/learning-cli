import json
import re
import subprocess

from .conftest import BIN


def test_pretty_table(sample_csv, tmp_path):
    out = tmp_path / "out.json"

    res = subprocess.run(
        [BIN, "--pretty", "-i", sample_csv, "-o", out],
        text=True,
        capture_output=True,
        check=True,
    )

    table = res.stdout

    # fancy grid
    assert "╒" in table and "╕" in table

    # header
    assert re.search(r"Name\s*|\s*Age\s*|\s*City", table)

    # json
    data = json.loads(out.read_text())
    assert len(data) == 3
