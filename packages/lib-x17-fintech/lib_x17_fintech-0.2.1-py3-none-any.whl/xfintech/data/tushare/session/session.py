from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict

import tushare as ts


class Session:
    """
    描述: Tushare API会话管理类 <br>

    参数:
    - credential: str, 必需, Tushare API令牌

    例子:
    ```python
        session = Session(credential="your_tushare_token")
        print(session.describe())
        # 使用session创建Job
        job = SomeJob(session=session, conf=...)
        session.disconnect()  # 断开连接
    ```
    """

    def __init__(
        self,
        credential: str,
    ) -> None:
        self._credential = credential
        self.id = str(uuid.uuid4())[:8]
        self.connection = None
        self.start = None
        self.finish = None
        self.connect()

    @property
    def duration(self) -> float:
        if self.start and self.finish:
            delta = self.finish - self.start
            return delta.total_seconds()
        return 0.0

    @property
    def connected(self) -> bool:
        return self.connection is not None

    def __str__(self) -> str:
        return f"{self.id}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, connected={self.connected})"

    def connect(self) -> object:
        if self.connected:
            return self.connection

        ts.set_token(self._credential)
        self.connection = ts.pro_api()
        self.start = datetime.now()
        return self.connection

    def disconnect(self) -> None:
        self.connection = None
        self.finish = datetime.now()

    def describe(self) -> Dict[str, Any]:
        start = self.start.strftime("%Y-%m-%d %H:%M:%S.%f") if self.start else None
        finish = self.finish.strftime("%Y-%m-%d %H:%M:%S.%f") if self.finish else None
        return {
            "id": self.id,
            "connected": self.connected,
            "start": start,
            "finish": finish,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "connected": self.connected,
            "start": self.start,
            "finish": self.finish,
        }
