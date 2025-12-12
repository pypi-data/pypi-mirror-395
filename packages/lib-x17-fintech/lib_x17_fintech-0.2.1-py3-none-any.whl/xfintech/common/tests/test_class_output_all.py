import pytest

from xfintech.common.output import Output
from xfintech.fabric.column.columninfo import ColumnInfo
from xfintech.fabric.datakind.datakind import DataKind
from xfintech.fabric.table.tableinfo import TableInfo


def test_output_basic_init():
    out = Output(
        name="processed",
        tableinfo=TableInfo(
            desc="Processed dataset",
            columns=[
                ColumnInfo(name="id", kind="integer"),
                ColumnInfo(name="score", kind="float"),
            ],
        ),
    )
    assert out.name == "processed"
    assert isinstance(out.tableinfo, TableInfo)
    assert "id" in out.tableinfo.columns
    assert len(out.identifier) == 64


def test_output_from_dict():
    data = {
        "name": "daily_data",
        "tableinfo": {
            "desc": "Daily dataset",
            "columns": [
                {"name": "open", "kind": "float"},
                {"name": "close", "kind": "float"},
            ],
        },
    }
    out = Output.from_dict(data)
    assert out.name == "daily_data"
    assert isinstance(out.tableinfo, TableInfo)
    assert "open" in out.tableinfo.columns
    assert out.tableinfo.get_column("open").kind == DataKind.FLOAT


def test_output_identifier_stability():
    o1 = Output(
        name="x",
        tableinfo=TableInfo(columns=[ColumnInfo("a", kind="float")]),
    )
    o2 = Output(
        name="x",
        tableinfo=TableInfo(columns=[ColumnInfo("a", kind="float")]),
    )
    assert o1.identifier == o2.identifier


def test_output_identifier_changes_when_schema_changes():
    o1 = Output(
        name="x",
        tableinfo=TableInfo(columns=[ColumnInfo("a", kind="float")]),
    )
    o2 = Output(
        name="x",
        tableinfo=TableInfo(columns=[ColumnInfo("a", kind="integer")]),
    )
    assert o1.identifier != o2.identifier


def test_output_str_and_repr():
    out = Output(name="result")
    assert str(out) == "result"
    assert "result" in repr(out)


def test_output_default_tableinfo():
    out = Output(name="empty")
    assert isinstance(out.tableinfo, TableInfo)
    assert out.tableinfo.columns == {}


def test_output_invalid_name():
    with pytest.raises(ValueError):
        Output(name="")
