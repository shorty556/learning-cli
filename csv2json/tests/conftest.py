# csv2json/tests/conftest.py
import csv
import sys
from pathlib import Path

import pytest

BIN = Path(sys.executable).parent / "csv2json"


@pytest.fixture
def sample_csv(tmp_path: Path):
    data = [
        {"Name": "Alice", "Age": "34", "City": "Tokyo"},
        {"Name": "Bob", "Age": "28", "City": "Osaka"},
        {"Name": "Carol", "Age": "42", "City": "Nagoya"},
    ]
    fp = tmp_path / "sample.csv"
    with fp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    return fp


@pytest.fixture
def empty_csv(tmp_path: Path):
    fp = tmp_path / "empty.csv"
    with fp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Age", "City"])
        writer.writeheader()  # データ行を書かない
    return fp
