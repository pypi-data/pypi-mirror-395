from __future__ import annotations

from typing import Any

from xfintech.engine.bridge.basebridge import BaseBridge
from xfintech.engine.kernel.kernel import Kernel


class PandasToPolars(BaseBridge):
    """
    将 pandas.DataFrame 转为 polars.DataFrame 的单向桥。
    - 懒加载 pandas / polars, 不把可选依赖外溢
    """

    def __init__(self):
        super().__init__(
            upstream=Kernel.PANDAS,
            downstream=Kernel.POLARS,
            priority=100,
        )

    @staticmethod
    def can_handle(
        obj: Any,
    ) -> bool:
        try:
            import pandas as pd

            return isinstance(obj, pd.DataFrame)
        except Exception:
            return False

    @staticmethod
    def to_table(
        obj: Any,
        **kwargs: Any,
    ):
        handleable = PandasToPolars.can_handle(obj)
        if not handleable:
            raise TypeError(
                f"{PandasToPolars.__name__}: expects pandas.DataFrame, got {type(obj)}",
            )
        try:
            import polars as pl

            return pl.from_pandas(obj, **kwargs)
        except Exception as e:
            raise RuntimeError(f"{PandasToPolars.__name__}: convert failed: {e}")
