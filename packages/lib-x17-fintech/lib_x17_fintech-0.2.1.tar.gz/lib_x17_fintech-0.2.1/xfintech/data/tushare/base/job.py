from __future__ import annotations

import uuid
from typing import Any, Callable, Dict, List, Optional

import pandas as pd

from xfintech.common.cache import Cache
from xfintech.common.metric import Metric
from xfintech.common.output import Output
from xfintech.common.retry import Retry
from xfintech.common.source import Source
from xfintech.data.tushare.base.conf import Conf


class Job:
    """
    描述: 作业类, 用于管理数据请求的作业

    参数:
    - session: object, 必需, 数据请求会话对象
    - name: str, 可选, 作业名称，默认使用类名小写
    - source: Source | Dict[str, Any], 可选, 数据源配置
    - output: Output | Dict[str, Any], 可选, 数据输出配置
    - conf: Conf | Dict[str, Any], 可选, 作业配置
    - retry: Retry, 可选, 重试配置
    - tags: Dict[str, str], 可选, 额外标签信息

    例子:
    ```python
        job = Job(
            session=session,
            name="my-job",
            source={"type": "api", "name": "tushare"},
            output={"type": "dataframe"},
            conf={"params": {"ts_code": "000001.SZ"}},
            retry=Retry(max_attempts=3, delay=2),
            tags={"project": "finance"},
        )
        result = job.run()
    ```
    """

    def __init__(
        self,
        session: object,
        name: Optional[str] = None,
        source: Optional[Source | Dict[str, Any]] = None,
        output: Optional[Output | Dict[str, Any]] = None,
        conf: Optional[Conf | Dict[str, Any]] = None,
        cache: Optional[Cache] = None,
        retry: Optional[Retry] = None,
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        self.id = self._resolve_id()
        self.name = self._resolve_name(name)
        self.connection = self._resolve_connection(session)
        self.source = self._resolve_source(source)
        self.output = self._resolve_output(output)
        self.conf = conf or Conf()
        self.retry = retry or Retry()
        self.cache = cache or Cache(name=self.name)
        self.metric = Metric(name=self.name)
        self.tags: Dict[str, str] = tags or {}

    @property
    def connected(self) -> bool:
        return self.connection is not None

    def _resolve_id(self) -> str:
        return str(uuid.uuid4())[:8]

    def _resolve_name(self, name) -> str:
        if name:
            return name.strip().lower()
        return str(self.__class__.__name__).lower()

    def _resolve_connection(
        self,
        session,
    ) -> object:
        if session and hasattr(session, "connection"):
            return session.connection
        return None

    def _resolve_source(
        self,
        source: Source | Dict[str, Any] | None,
    ) -> Source:
        if isinstance(source, Source):
            return source
        elif isinstance(source, dict):
            return Source.from_dict(source)
        else:
            return Source(name=self.name)

    def _resolve_output(
        self,
        output: Output | Dict[str, Any] | None,
    ) -> Output:
        if isinstance(output, Output):
            return output
        elif isinstance(output, dict):
            return Output.from_dict(output)
        else:
            return Output(name=self.name)

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    def run(self) -> Any:
        wrapped = self.retry(self._run)
        with self.metric:
            return wrapped()

    def _run(self) -> object:
        raise NotImplementedError("Subclasses must implement this method.")

    def _fetchall(
        self,
        api: Callable,
        **params: Any,
    ):
        self.conf.reset()
        batch: List[pd.DataFrame] = []
        for _ in range(self.conf.limit):
            page = api(
                limit=self.conf.size,
                offset=self.conf.offset,
                **params,
            )
            if page is None or len(page) == 0:
                break
            else:
                batch.append(page)

            if len(page) < self.conf.size:
                break
            else:
                self.conf.next()
                self.conf.cool()

        if not batch:
            return pd.DataFrame()
        else:
            return pd.concat(batch, ignore_index=True)

    def clean(self) -> None:
        self.cache.clear()
        self.metric.reset()

    def describe(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "connected": self.connected,
            "output": self.output.describe(),
            "conf": self.conf.describe(),
            "retry": self.retry.describe(),
            "cache": self.cache.describe(),
            "metric": self.metric.describe(),
            "tags": self.tags,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "connected": self.connected,
            "source": self.source.to_dict(),
            "output": self.output.to_dict(),
            "conf": self.conf.to_dict(),
            "retry": self.retry.to_dict(),
            "cache": self.cache.to_dict(),
            "metric": self.metric.to_dict(),
            "tags": self.tags,
        }
