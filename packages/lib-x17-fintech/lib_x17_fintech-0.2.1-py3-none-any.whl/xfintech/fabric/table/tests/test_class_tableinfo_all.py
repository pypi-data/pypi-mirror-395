from xfintech.fabric.column.columninfo import ColumnInfo
from xfintech.fabric.datakind.datakind import DataKind
from xfintech.fabric.table.tableinfo import TableInfo


def test_tableinfo_basic_init_with_columns():
    price = ColumnInfo(
        name="price",
        kind="Float",
        desc="收盘价",
    )
    vol = ColumnInfo(
        name="volume",
        kind=DataKind.INTEGER,
        desc="成交量",
    )
    table = TableInfo(
        desc="  日线行情表 ",
        meta={"source": "tushare"},
        columns=[price, vol],
    )
    assert table.desc == "日线行情表"
    assert table.meta == {"source": "tushare"}

    cols = table.list_columns()
    assert [c.name for c in cols] == ["price", "volume"]
    assert table.get_column("price").kind == DataKind.FLOAT
    assert table.get_column("VOLUME").kind == DataKind.INTEGER


def test_tableinfo_init_columns_from_dicts():
    table = TableInfo(
        columns=[
            {
                "name": "price",
                "kind": "Float",
                "desc": "收盘价",
                "meta": {"unit": "CNY"},
            },
            {
                "name": "volume",
                "kind": "Integer",
                "desc": "成交量",
                "meta": None,
            },
        ],
    )
    price_col = table.get_column("PRICE")
    vol_col = table.get_column("volume")
    assert price_col is not None
    assert price_col.kind == DataKind.FLOAT
    assert price_col.desc == "收盘价"
    assert price_col.meta == {"unit": "CNY"}

    assert vol_col is not None
    assert vol_col.kind == DataKind.INTEGER
    assert vol_col.desc == "成交量"
    assert vol_col.meta == {}


def test_tableinfo_meta_bytes_decoding():
    table = TableInfo(
        meta={
            b"source": b"tushare",
            "env": b"prod",
        },
    )
    assert table.meta == {
        "source": "tushare",
        "env": "prod",
    }


def test_tableinfo_get_and_add_and_remove_column():
    table = TableInfo()
    assert table.get_column("price") is None

    table.add_column(ColumnInfo(name="price", kind="Float"))
    assert table.get_column("PRICE") is not None
    assert table.get_column("price").kind == DataKind.FLOAT

    table.add_column(
        {
            "name": "volume",
            "kind": "Integer",
            "desc": "成交量",
            "meta": None,
        }
    )
    assert table.get_column("volume").kind == DataKind.INTEGER

    table.remove_column("PRICE")
    assert table.get_column("price") is None

    table.remove_column("not_exist")


def test_tableinfo_update_column_existing():
    table = TableInfo(
        columns=[
            ColumnInfo(
                name="price",
                kind="Float",
                desc="old",
                meta={"unit": "CNY"},
            )
        ],
    )
    table.update_column(
        name="price",
        new="new_price",
        kind="Integer",
        desc="新价格",
        meta={"scale": 2},
    )
    col = table.get_column("new_price")
    assert col is not None
    assert col.kind == DataKind.INTEGER
    assert col.desc == "新价格"
    assert col.meta == {"unit": "CNY", "scale": 2}


def test_tableinfo_update_column_missing_is_silent():
    table = TableInfo()
    table.update_column(
        name="not_exist",
        kind="Float",
        desc="should_not_exist",
        meta={"x": 1},
    )
    assert table.get_column("not_exist") is None


def test_tableinfo_rename_column_basic():
    table = TableInfo(
        columns=[ColumnInfo(name="close", kind="Float")],
    )
    table.rename_column("CLOSE", "adj_close")
    assert table.get_column("close") is None

    new_col = table.get_column("adj_close")
    assert new_col is not None
    assert new_col.kind == DataKind.FLOAT
    assert new_col.name == "adj_close"


def test_tableinfo_rename_column_overwrite_existing():
    table = TableInfo(
        columns=[
            ColumnInfo(name="close", kind="Float"),
            ColumnInfo(name="adj_close", kind="Float", desc="old adj"),
        ],
    )
    table.rename_column("close", "adj_close")
    col = table.get_column("adj_close")
    assert col is not None
    assert col.desc == ""


def test_tableinfo_list_columns_order():
    table = TableInfo(
        columns=[
            ColumnInfo(name="a", kind="String"),
            ColumnInfo(name="b", kind="Integer"),
        ],
    )
    table.add_column(ColumnInfo(name="c", kind="Float"))
    names = [c.name for c in table.list_columns()]
    assert names == ["a", "b", "c"]


def test_tableinfo_to_dict_and_from_dict_roundtrip():
    table = TableInfo(
        desc="日线行情",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(
                name="price",
                kind="Float",
                desc="收盘价",
                meta={"unit": "CNY"},
            ),
            ColumnInfo(
                name="volume",
                kind="Integer",
                desc="成交量",
            ),
        ],
    )
    d = table.to_dict()
    table2 = TableInfo.from_dict(d)
    assert table2.desc == "日线行情"
    assert table2.meta == {"source": "tushare"}

    cols2 = table2.list_columns()
    assert [c.name for c in cols2] == ["price", "volume"]
    assert cols2[0].kind == DataKind.FLOAT
    assert cols2[0].meta == {"unit": "CNY"}
    assert cols2[1].kind == DataKind.INTEGER


def test_tableinfo_identifier_consistency():
    table1 = TableInfo(
        desc="日线行情",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(
                name="price",
                kind="Float",
                desc="收盘价",
                meta={"unit": "CNY"},
            ),
            ColumnInfo(
                name="volume",
                kind="Integer",
                desc="成交量",
            ),
        ],
    )
    table2 = TableInfo(
        desc="日线行情",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(
                name="price",
                kind="Float",
                desc="收盘价",
                meta={"unit": "CNY"},
            ),
            ColumnInfo(
                name="volume",
                kind="Integer",
                desc="成交量",
            ),
        ],
    )
    assert table1.identifier == table2.identifier


def test_tableinfo_identifier_changes_on_modification():
    table = TableInfo(
        desc="日线行情",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(
                name="price",
                kind="Float",
                desc="收盘价",
                meta={"unit": "CNY"},
            ),
            ColumnInfo(
                name="volume",
                kind="Integer",
                desc="成交量",
            ),
        ],
    )
    original_id = table.identifier
    table.desc = "修改后的日线行情"
    assert table.identifier != original_id

    modified_id = table.identifier
    table.desc = "日线行情"
    assert table.identifier == original_id

    table.add_column(
        ColumnInfo(
            name="open",
            kind="Float",
            desc="开盘价",
        )
    )
    assert table.identifier != original_id
    assert table.identifier != modified_id


def test_list_columns_empty_by_default():
    table = TableInfo()
    cols = table.list_columns()
    assert cols == []


def test_list_columns():
    table = TableInfo(
        columns=[
            ColumnInfo(name="a", kind="String"),
            ColumnInfo(name="b", kind="Integer"),
        ],
    )
    cols = table.list_columns()
    assert len(cols) == 2
    assert cols[0].name == "a"
    assert cols[1].name == "b"
