import pytest

from xfintech.engine.bridge.pandastopolars import PandasToPolars
from xfintech.engine.kernel.kernel import Kernel


def test_can_handle_and_meta():
    import pandas as pd

    b = PandasToPolars()
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    assert b.can_handle(df) is True
    assert b.upstream == Kernel.PANDAS
    assert b.downstream == Kernel.POLARS
    assert b.name == "pandas->polars"
    assert b.priority == 100


def test_to_table_basic():
    import pandas as pd
    import polars as pl

    df = pd.DataFrame({"x": [1, 2, 3], "y": [10, 20, 30]})
    b = PandasToPolars()
    pldf = b.to_table(df)
    assert isinstance(pldf, pl.DataFrame)
    assert pldf.shape == (3, 2)
    assert pldf.columns == ["x", "y"]


def test_wrong_input_type_raises():
    b = PandasToPolars()
    with pytest.raises(TypeError):
        b.to_table({"x": [1, 2]})


def test_runtime_error_monkeypatch(monkeypatch):
    import pandas as pd
    import polars as pl

    df = pd.DataFrame({"a": [1, 2]})
    b = PandasToPolars()

    def boom(*args, **kwargs):
        raise ValueError("boom")

    monkeypatch.setattr(pl, "from_pandas", boom)

    with pytest.raises(RuntimeError) as e:
        b.to_table(df)
    assert "convert failed" in str(e.value)


def test_direct_conversion():
    import pandas as pd
    import polars as pl

    df = pd.DataFrame({"m": [5, 6], "n": [7, 8]})
    pldf = PandasToPolars.to_table(df)
    assert isinstance(pldf, pl.DataFrame)
    assert pldf.shape == (2, 2)
    assert pldf.columns == ["m", "n"]


def test_direct_can_handle():
    import pandas as pd

    df = pd.DataFrame({"p": [9, 10]})
    assert PandasToPolars.can_handle(df) is True


def test_direct_can_handle_wrong_type():
    assert PandasToPolars.can_handle([1, 2, 3]) is False
