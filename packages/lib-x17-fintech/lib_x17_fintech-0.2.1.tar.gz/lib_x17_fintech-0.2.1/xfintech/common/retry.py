from __future__ import annotations

from functools import wraps
from typing import Any, Callable, Iterable, Type

import backoff


class Retry:
    """
    重试包装器，用于函数调用时的自动重试机制。

    参数:
    - retry: 最大重试次数（包含最后一次尝试）
    - wait: 初始等待秒数
    - offrate: 退避倍率；=1.0 固定间隔，>1.0 使用指数退避
    - exceptions: 需要触发重试的异常类型 tuple

    例子:
    ```python
    retry = Retry(retry=5, wait=1.0, offrate=2.0, exceptions=(ValueError,))
    function = <function_to_retry>
    retry(function)(param1, param2)
    ```

    """

    def __init__(
        self,
        retry: int = 3,
        wait: float = 0.5,
        offrate: float = 1.0,
        exceptions: Iterable[Type[BaseException]] = None,
    ) -> None:
        self.retry = retry
        self.wait = wait
        self.offrate = offrate
        self.exceptions = tuple(exceptions or (Exception,))

    def __call__(self, func: Callable) -> Callable:
        if self.offrate == 1.0:
            deco = backoff.on_exception(
                backoff.constant,
                self.exceptions,
                max_tries=self.retry,
                interval=self.wait,
            )
        else:
            deco = backoff.on_exception(
                backoff.expo,
                self.exceptions,
                max_tries=self.retry,
                base=self.wait,
                factor=self.offrate,
            )
        wrapped_function = deco(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return wrapped_function(*args, **kwargs)

        return wrapper

    def __str__(self) -> str:
        return f"{self.retry}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(retry={self.retry}, "
            f"wait={self.wait}, offrate={self.offrate}, "
            f"exceptions={self.exceptions})"
        )

    def describe(self) -> str:
        return self.to_dict()

    def to_dict(self) -> dict[str, Any]:
        return {
            "retry": self.retry,
            "wait": self.wait,
            "offrate": self.offrate,
            "exceptions": [exc.__name__ for exc in self.exceptions],
        }
