from __future__ import annotations

from abc import abstractmethod
from typing import Any, Protocol, runtime_checkable

from xfintech.engine.kernel.kernel import Kernel


@runtime_checkable
class BridgeProtocol(Protocol):
    upstream: Kernel
    downstream: Kernel
    name: str
    priority: int

    def can_handle(self, obj: Any) -> bool: ...
    def to_table(self, obj: Any) -> Any: ...


class BaseBridge(BridgeProtocol):
    def __init__(
        self,
        upstream: Kernel,
        downstream: Kernel,
        *,
        priority: int = 100,
    ):
        self.upstream = upstream
        self.downstream = downstream
        self.priority = int(priority)
        self.name = f"{self.upstream.value}->{self.downstream.value}"

    def __str__(self):
        return f"{self.name!r}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, priority={self.priority})"

    @abstractmethod
    def can_handle(self, obj: Any) -> bool:
        raise NotImplementedError

    @abstractmethod
    def to_table(self, obj: Any) -> Any:
        raise NotImplementedError
