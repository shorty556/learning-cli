"""
filter_rows のユニットテスト

- 数値比較（>=, <, ==）
- 式を省略した場合（expr=None もしくは ""）
"""

import pytest

from csv2json.core import filter_rows

# ---- サンプル行（テスト専用・固定データ） ------------------------------

ROWS = [
    {"Name": "Alice", "Age": "25", "City": "Tokyo"},
    {"Name": "Bob", "Age": "30", "City": "Osaka"},
    {"Name": "Carol", "Age": "35", "City": "Nagoya"},
]

# ---- パラメタライズで演算子ごとに検証 -----------------------------------


@pytest.mark.parametrize(
    "expr, expected_names",
    [
        ("Age>=30", ["Bob", "Carol"]),
        ("Age<30", ["Alice"]),
        ("Age==35", ["Carol"]),
    ],
)
def test_filter_numeric(expr, expected_names):
    """Age 列に対する数値比較が想定件数になるか"""
    result = filter_rows(ROWS, expr)
    names = [r["Name"] for r in result]
    assert names == expected_names


def test_filter_no_expression_returns_all():
    """expr を省略すると全行が返る"""
    assert filter_rows(ROWS, None) == ROWS
    assert filter_rows(ROWS, "") == ROWS
