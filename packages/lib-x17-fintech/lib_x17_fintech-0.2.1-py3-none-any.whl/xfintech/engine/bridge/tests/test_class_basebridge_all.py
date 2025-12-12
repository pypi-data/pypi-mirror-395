from __future__ import annotations

from typing import Any

import pytest

from xfintech.engine.bridge.basebridge import BaseBridge, BridgeProtocol
from xfintech.engine.kernel.kernel import Kernel


class PandasToArrowBridge(BaseBridge):
    def __init__(self):
        super().__init__(
            upstream=Kernel.PANDAS,
            downstream=Kernel.ARROW,
            priority=10,
        )

    def can_handle(self, obj) -> bool:
        import pandas as pd

        return isinstance(obj, pd.DataFrame)

    def to_table(self, obj) -> Any:
        import pyarrow as pa

        return pa.Table.from_pandas(obj)


def test_basebridge_shape_and_defaults():
    b = PandasToArrowBridge()
    assert isinstance(b, BridgeProtocol)
    assert b.upstream == Kernel.PANDAS
    assert b.downstream == Kernel.ARROW
    assert b.priority == 10
    assert b.name == "pandas->arrow"
    assert "PandasToArrowBridge" in repr(b)


def test_abstract_methods_contract():
    class BadBridge(BaseBridge):
        pass

    with pytest.raises(TypeError):
        BadBridge(Kernel.PANDAS, Kernel.ARROW)

    class DummyBridge(BaseBridge):
        def can_handle(self, obj):
            return obj == "ok"

        def to_table(self, obj):
            return {"ok": True}

    d = DummyBridge(Kernel.ARROW, Kernel.ARROW, priority=77)
    assert d.can_handle("ok") is True
    assert d.can_handle("nope") is False
    assert d.to_table("ok") == {"ok": True}
    assert d.priority == 77


def test_pandas_to_arrow_bridge_happy_path():
    import pandas as pd
    import pyarrow as pa

    df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})

    b = PandasToArrowBridge()
    assert b.can_handle(df) is True

    table = b.to_table(df)
    assert isinstance(table, pa.Table)
    assert table.num_rows == 2
    assert table.num_columns == 2


def test_can_handle_returns_false_for_other_types():
    b = PandasToArrowBridge()
    assert b.can_handle({"x": [1, 2]}) is False
