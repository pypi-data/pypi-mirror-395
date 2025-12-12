from __future__ import annotations

from typing import Any

from xfintech.engine.bridge.basebridge import BaseBridge
from xfintech.engine.kernel.kernel import Kernel


class PolarsToArrow(BaseBridge):
    """
    将 polars.DataFrame 转换为 pyarrow.Table 的单向桥。
    - 可选依赖：仅在 can_handle 时懒加载 polars

    """

    def __init__(self):
        super().__init__(
            upstream=Kernel.POLARS,
            downstream=Kernel.ARROW,
            priority=100,
        )

    @staticmethod
    def can_handle(
        obj: Any,
    ) -> bool:
        try:
            import polars as pl

            return isinstance(obj, pl.DataFrame)
        except Exception:
            return False

    @staticmethod
    def to_table(
        obj: Any,
        **kwargs: Any,
    ):
        handleable = PolarsToArrow.can_handle(obj)
        if not handleable:
            raise TypeError(
                f"{PolarsToArrow.__name__}: expects polars.DataFrame, got {type(obj)}",
            )
        try:
            return obj.to_arrow(**kwargs)
        except Exception as e:
            raise RuntimeError(f"{PolarsToArrow.__name__}: convert failed: {e}")
