from __future__ import annotations

import time
from datetime import datetime
from typing import Any, Dict, Optional


class Conf:
    """
    描述: Job配置, 用于管理数据请求的参数和分页设置

    参数:
    - params: Dict[str, Any], 非必需, 请求参数字典
    - limit: int, 非必需, 最大迭代次数, 默认为10000
    - size: int, 非必需, 每页数据条数, 默认为5000
    - offset: int, 非必需, 数据偏移量, 默认为0
    - coolant: int, 非必需, 请求间隔时间(秒), 默认为0

    例子:
    ```python
        job_conf = JobConf(
            params={
                "ts_code": "000001.SZ",
                "start_date": "20240101",
                "end_date": "20241101"
            },
            limit=200,
            size=1000,
            offset=0,
            coolant=1,
            use_cache=True,
        )
        print(job_conf)
    ```
    """

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> Conf:
        if isinstance(data, Conf):
            return data
        return cls(
            params=data.get("params"),
            limit=data.get("limit"),
            size=data.get("size"),
            offset=data.get("offset"),
            coolant=data.get("coolant"),
            use_cache=data.get("use_cache"),
        )

    def __init__(
        self,
        params: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        size: Optional[int] = None,
        offset: Optional[int] = None,
        coolant: Optional[int] = None,
        use_cache: Optional[bool] = False,
    ) -> None:
        self.params = self._resolve_params(params)
        self.limit = limit or 10000
        self.size = size or 5000
        self.offset = offset or 0
        self.coolant = coolant or 0
        self.use_cache = use_cache

    def _resolve_params(
        self,
        params: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        if not params:
            return {}
        else:
            params = params.copy()

        for key, value in params.items():
            if isinstance(value, datetime):
                params[key] = value.strftime("%Y%m%d")
        return {k: v for k, v in params.items() if v is not None}

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self):
        return f"{self.__class__.__name__}(limit={self.limit}, size={self.size})"

    def get_params(self) -> Dict[str, Any]:
        return self.params.copy()

    def set_params(
        self,
        params: Dict[str, Any],
    ) -> None:
        self.params = self._resolve_params(params)

    def set_limit(
        self,
        limit: int,
    ) -> None:
        self.limit = limit

    def set_size(
        self,
        size: int,
    ) -> None:
        self.size = size

    def next(self) -> int:
        self.offset += self.size
        self.cool()
        return self.offset

    def reset(self) -> int:
        self.offset = 0
        return self.offset

    def cool(self) -> None:
        if self.coolant > 0:
            time.sleep(self.coolant)

    def describe(self) -> Dict[str, Any]:
        return self.to_dict()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "params": self.params,
            "limit": self.limit,
            "size": self.size,
            "offset": self.offset,
            "coolant": self.coolant,
            "use_cache": self.use_cache,
        }
