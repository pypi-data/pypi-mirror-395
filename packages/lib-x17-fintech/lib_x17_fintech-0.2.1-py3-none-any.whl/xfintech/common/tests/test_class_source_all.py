import pytest

from xfintech.common.source import Source
from xfintech.fabric.column.columninfo import ColumnInfo
from xfintech.fabric.datakind.datakind import DataKind
from xfintech.fabric.table.tableinfo import TableInfo


def test_source_basic_init():
    src = Source(
        name="tushare_daily",
        url="https://api.tushare.pro",
        args={"ts_code": "000001.SZ", "trade_date": "20240101"},
        tableinfo=TableInfo(
            desc="daily bars",
            columns=[
                ColumnInfo(name="open", kind="float"),
                ColumnInfo(name="close", kind="float"),
            ],
        ),
    )

    assert src.name == "tushare_daily"
    assert src.url == "https://api.tushare.pro"
    assert src.args["ts_code"] == "000001.SZ"
    assert "open" in src.tableinfo.columns
    assert isinstance(src.identifier, str)
    assert len(src.identifier) == 64  # sha256 hex


def test_source_from_dict():
    data = {
        "name": "example",
        "url": "http://service",
        "args": {"a": 1, "b": 2},
        "tableinfo": {
            "desc": "test",
            "columns": [
                {"name": "id", "kind": "integer"},
                {"name": "value", "kind": "float"},
            ],
        },
    }

    src = Source.from_dict(data)
    assert src.name == "example"
    assert src.args["a"] == 1
    assert "id" in src.tableinfo.columns
    assert src.tableinfo.get_column("id").kind == DataKind.INTEGER


def test_identifier_stable():
    s1 = Source(
        name="abc",
        url="x",
        args={"b": 2, "a": 1},  # intentionally unsorted
        tableinfo=TableInfo(desc="x"),
    )
    s2 = Source(
        name="abc",
        url="x",
        args={"a": 1, "b": 2},  # sorted
        tableinfo=TableInfo(desc="x"),
    )

    assert s1.identifier == s2.identifier  # args 顺序不同 ID 相同


def test_identifier_changes_when_args_change():
    s1 = Source(name="a", url="u", args={"x": 1})
    s2 = Source(name="a", url="u", args={"x": 2})
    assert s1.identifier != s2.identifier


def test_identifier_changes_when_tableinfo_changes():
    s1 = Source(
        name="a",
        url="u",
        args={"x": 1},
        tableinfo=TableInfo(columns=[ColumnInfo("a", kind="float")]),
    )
    s2 = Source(
        name="a",
        url="u",
        args={"x": 1},
        tableinfo=TableInfo(columns=[ColumnInfo("a", kind="string")]),
    )
    assert s1.identifier != s2.identifier


def test_source_str_repr():
    s = Source(name="ts_daily")
    assert str(s) == "ts_daily"
    assert "ts_daily" in repr(s)


def test_source_empty_tableinfo():
    s = Source(name="none")
    assert isinstance(s.tableinfo, TableInfo)
    assert s.tableinfo.columns == {}


def test_source_invalid_name():
    with pytest.raises(ValueError):
        Source(name="")
