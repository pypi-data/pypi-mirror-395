from __future__ import annotations

from enum import Enum


class Kernel(str, Enum):
    """
    底层数据依赖内核类型
    每个成员带有能力标记：
      - support: 是否当前可用
      - distributed: 是否支持分布式
      - bytesio: 是否支持原生 bytes IO
      - internal: 是否作为框架内部核心内核

    """

    PANDAS = (
        "pandas",
        True,
        False,
        False,
        False,
    )
    DASK = (
        "dask",
        False,
        True,
        False,
        False,
    )
    POLARS = (
        "polars",
        True,
        True,
        False,
        False,
    )
    ARROW = (
        "arrow",
        True,
        True,
        True,
        True,
    )
    SPARK = (
        "spark",
        False,
        True,
        True,
        True,
    )
    DEFAULT = ARROW

    def __new__(
        cls,
        value: str,
        support: bool,
        distributed: bool,
        bytesio: bool,
        internal: bool,
    ):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.support = support
        obj.distributed = distributed
        obj.bytesio = bytesio
        obj.internal = internal
        return obj

    @classmethod
    def list(cls) -> list[str]:
        return [m.value for m in cls]

    @classmethod
    def internals(cls) -> list[str]:
        return [m.value for m in cls if m.internal]

    @classmethod
    def externals(cls) -> list[str]:
        return [m.value for m in cls if not m.internal]

    @classmethod
    def supports(cls) -> list[str]:
        return [m.value for m in cls if m.support]

    @classmethod
    def has(cls, value: str) -> bool:
        return value in cls._value2member_map_
