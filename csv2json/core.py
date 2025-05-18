import csv
import io
import json
import logging
import re
from pathlib import Path
from typing import Callable, Dict, Iterable, List

import chardet

log = logging.getLogger(__name__)
ProgressFn = Callable[[int, int], None]  # (processed, total) -> None


def detect_encoding(path: Path, sample: int = 10000) -> str:
    with path.open("rb") as f:
        raw = f.read(sample)
        return chardet.detect(raw)["encoding"] or "utf-8"


def filter_rows(
    rows: Iterable[Dict[str, str]], expr: str | None
) -> list[Dict[str, str]]:
    if not expr:
        return list(rows)
    key, op, val = re.match(r"(\w+)\s*(==|>=|<=|>|<)\s*(.+)", expr).groups()

    def ok(row):
        a, b = row[key], val
        return eval(f"{a}{op}{b}", {}, {})

    return [r for r in rows if ok(r)]


def convert(
    src: Path,
    dst: Path,
    indent: int,
    expr: str | None,
    progress: ProgressFn | None = None,
) -> None:
    total_bytes = src.stat().st_size
    enc = detect_encoding(src)

    rows: List[Dict[str, str]] = []

    with src.open("rb") as raw:
        text = io.TextIOWrapper(raw, encoding=enc, newline="")
        reader = csv.DictReader(text)
        for row in reader:
            rows.append(row)
            if progress:
                progress(raw.tell(), total_bytes)

    data = filter_rows(rows, expr)
    dst.write_text(json.dumps(data, indent=indent, ensure_ascii=False))
    log.info(
        "Converted %s rows -> %s -(%.1f kB)", len(data), dst, dst.stat().st_size / 1024
    )
