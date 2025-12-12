import pyarrow as pa
import pytest

from xfintech.engine.bridge.polarstoarrow import PolarsToArrow
from xfintech.engine.kernel.kernel import Kernel


def test_can_handle_and_metadata():
    import polars as pl

    b = PolarsToArrow()
    df = pl.DataFrame({"x": [1, 2], "y": ["a", "b"]})
    assert b.can_handle(df) is True
    assert b.upstream == Kernel.POLARS
    assert b.downstream == Kernel.ARROW
    assert b.name == "polars->arrow"
    assert b.priority == 100


def test_to_table_roundtrip():
    import polars as pl

    df = pl.DataFrame({"x": [1, 2, 3], "y": ["a", "b", "c"]})
    b = PolarsToArrow()
    tbl = b.to_table(df)
    assert isinstance(tbl, pa.Table)
    assert tbl.num_rows == 3
    assert tbl.schema.names == ["x", "y"]


def test_error_on_wrong_type():
    b = PolarsToArrow()
    with pytest.raises(TypeError):
        b.to_table({"x": [1, 2]})


def test_runtime_error_via_monkeypatch(monkeypatch):
    import polars as pl

    df = pl.DataFrame({"x": [1, 2]})
    b = PolarsToArrow()

    def boom(**kwargs):
        raise ValueError("boom")

    monkeypatch.setattr(df, "to_arrow", boom)

    with pytest.raises(RuntimeError) as e:
        b.to_table(df)
    assert "convert failed" in str(e.value)


def test_direct_conversion():
    import polars as pl

    df = pl.DataFrame({"m": [5, 6], "n": ["x", "y"]})
    tbl = PolarsToArrow.to_table(df)
    assert isinstance(tbl, pa.Table)
    assert tbl.num_rows == 2
    assert tbl.schema.names == ["m", "n"]


def test_direct_can_handle():
    import polars as pl

    df = pl.DataFrame({"a": [1, 2], "b": ["c", "d"]})
    assert PolarsToArrow.can_handle(df) is True


def test_direct_can_handle_false():
    import pandas as pd

    df = pd.DataFrame({"a": [1, 2], "b": ["c", "d"]})
    assert PolarsToArrow.can_handle(df) is False
