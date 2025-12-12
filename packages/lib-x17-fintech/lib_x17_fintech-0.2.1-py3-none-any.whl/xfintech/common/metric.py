from __future__ import annotations

import traceback
from typing import Optional

import pandas as pd


class Metric:
    """
    描述: 记录一个 Job 的执行情况 <br>

    参数:
    - name: str, 可选, 记录的名称

    例子:
    ```python
        metric = Metric(name="example_job")
        with metric:
            # 执行一些操作
            pass
        print(metric.describe())
    ```
    """

    def __init__(
        self,
        name: Optional[str] = None,
    ) -> None:
        self.name = name or None
        self.start_at = None
        self.finish_at = None
        self.error: list[str] = []
        self.marks: dict[str, pd.Timestamp] = {}

    @property
    def duration(self) -> float:
        if self.start_at is not None and self.finish_at is not None:
            diff = self.finish_at - self.start_at
            return diff.total_seconds()
        return 0.0

    def reset(self) -> None:
        self.start_at = None
        self.finish_at = None
        self.error = []
        self.marks = {}

    def __enter__(self):
        self.reset()
        self.start()
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):
        if exc_val:
            tb = traceback.format_exception(
                exc_type,
                exc_val,
                exc_tb,
            )
            self.error = [line.rstrip("\n") for line in tb]
        self.finish()
        return False

    def start(self) -> None:
        self.start_at = pd.Timestamp.now()

    def finish(self) -> None:
        self.finish_at = pd.Timestamp.now()

    def mark(self, name: str) -> None:
        self.marks[name] = pd.Timestamp.now()

    def describe(self) -> dict:
        start_at = self.start_at.isoformat() if self.start_at else None
        finish_at = self.finish_at.isoformat() if self.finish_at else None
        marks = {k: v.isoformat() for k, v in self.marks.items()}
        return {
            "name": self.name,
            "started_at": start_at,
            "finished_at": finish_at,
            "duration": self.duration,
            "error": self.error,
            "marks": marks,
        }

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "started_at": self.start_at,
            "finished_at": self.finish_at,
            "duration": self.duration,
            "error": self.error,
            "marks": self.marks,
        }
