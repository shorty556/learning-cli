import json

from csv2json.core import convert


def test_convert_basic(sample_csv, tmp_path):
    out = tmp_path / "out.json "
    convert(sample_csv, out, indent=0, expr=None)

    data = json.loads(out.read_text())
    assert len(data) == 3
    assert data[0]["Name"] == "Alice"


def test_progress_callback_called(sample_csv, tmp_path):
    out = tmp_path / "out.json"
    calls = []

    convert(
        sample_csv,
        out,
        indent=0,
        expr=None,
        progress=lambda done, total: calls.append(done),
    )
    assert calls[-1] == sample_csv.stat().st_size
