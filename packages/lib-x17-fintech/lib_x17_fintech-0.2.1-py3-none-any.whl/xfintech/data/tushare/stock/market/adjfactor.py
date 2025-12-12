from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

import pandas as pd

from xfintech.common.output import Output
from xfintech.common.retry import Retry
from xfintech.common.source import Source
from xfintech.data.tushare.base.conf import Conf
from xfintech.data.tushare.base.job import Job
from xfintech.data.tushare.session.session import Session
from xfintech.fabric.column.columninfo import ColumnInfo
from xfintech.fabric.datakind.datakind import DataKind
from xfintech.fabric.table.tableinfo import TableInfo


class AdjFactor(Job):
    """
    描述: 获取A股复权因子数据 <br>
    说明: 盘前9点15~20分完成当日复权因子入库, 本接口由Tushare自行生产 <br>
    使用: 2000积分起, 5000以上可高频调取, 可提取单只股票全部历史复权因子 <br>

    参数:
    - session: Session, 必需, Tushare API会话对象
    - conf: Conf | Dict[str, Any], 可选, 作业配置, 支持以下参数:
        - params: Dict, 可选, 请求参数
            - ts_code: str, 可选, 股票代码
            - trade_date: str, 可选, 特定交易日期(YYYYMMDD)
            - start_date: str, 可选, 开始日期(YYYYMMDD)
            - end_date: str, 可选, 结束日期(YYYYMMDD)
        - limit: int, 可选, 最大迭代次数, 默认10000
        - size: int, 可选, 每次提取数据量, 建议不超过5000
        - coolant: float, 可选, 请求间隔时间(秒), 默认0.1
    - retry: Retry, 可选, 重试配置

    例子:
    ```python
        # 获取单只股票全部复权因子
        adjfactor_job = AdjFactor(
            session=session,
            conf=Conf(
                params={
                    "ts_code": "000001.SZ"
                }
            )
        )
        result = adjfactor_job.run()

        # 获取某交易日全市场复权因子
        market_adj = AdjFactor(
            session=session,
            conf=Conf(
                params={
                    "trade_date": "20241201"
                },
                size=5000
            )
        )
        result = market_adj.run()
        adjfactor_job.clean()  # 清理缓存
    ```
    """

    _SIZE = 2000
    _FREQ = 0.05
    _ARGS = {
        "ts_code": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "股票代码",
        },
        "trade_date": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "特定交易日期(YYYYMMDD)",
        },
        "start_date": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "开始日期(YYYYMMDD)",
        },
        "end_date": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "结束日期(YYYYMMDD)",
        },
    }
    _IN = TableInfo(
        desc="A股复权因子数据输入格式",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="ts_code", kind=DataKind.STRING, desc="股票代码"),
            ColumnInfo(name="trade_date", kind=DataKind.STRING, desc="交易日期"),
            ColumnInfo(name="adj_factor", kind=DataKind.FLOAT, desc="复权因子"),
        ],
    )
    _OUT = TableInfo(
        desc="A股复权因子数据标准化输出格式",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="code", kind=DataKind.STRING, desc="股票代码"),
            ColumnInfo(name="date", kind=DataKind.DATETIME, desc="交易日期"),
            ColumnInfo(name="datecode", kind=DataKind.STRING, desc="交易日期代码(YYYYMMDD)"),
            ColumnInfo(name="adj_factor", kind=DataKind.STRING, desc="复权因子"),
        ],
    )

    def __init__(
        self,
        session: Session,
        conf: Optional[Conf | Dict[str, Any]] = None,
        retry: Optional[Retry] = None,
    ) -> None:
        super().__init__(
            session=session,
            conf=self._resolve_conf(conf),
            source=Source(
                name="adj_factor",
                url="http://tushare.pro/document/2?doc_id=28",
                args=self._ARGS,
                tableinfo=self._IN,
            ),
            output=Output(
                name="adjfactor",
                tableinfo=self._OUT,
            ),
            retry=retry,
            tags={
                "name": "adjfactor",
                "module": "stock",
                "level": "market",
                "frequency": "interday",
                "scope": "adj_factor",
            },
        )

    @classmethod
    def _resolve_conf(
        cls,
        conf: Optional[Conf | Dict[str, Any]] = None,
    ) -> Conf:
        if conf is None:
            obj = Conf(size=cls._SIZE, coolant=cls._FREQ)
        else:
            obj = Conf.from_dict(conf)

        params = obj.get_params() or {}

        if "trade_date" in params:
            trade_date = params.get("trade_date")
            if isinstance(trade_date, datetime):
                params["trade_date"] = trade_date.strftime("%Y%m%d")

        if "start_date" in params and "end_date" in params:
            start_date = params["start_date"]
            end_date = params["end_date"]
            if isinstance(start_date, datetime):
                params["start_date"] = start_date.strftime("%Y%m%d")
            if isinstance(end_date, datetime):
                params["end_date"] = end_date.strftime("%Y%m%d")

        obj.set_params(params)

        if obj.size > cls._SIZE:
            obj.set_size(cls._SIZE)

        if obj.coolant < cls._FREQ:
            obj.coolant = cls._FREQ

        return obj

    def _run(self) -> object:
        params = dict(self.conf.get_params() or {})
        df = self._fetchall(
            api=self.connection.adj_factor,
            **params,
        )
        df = self.transform(df)
        if self.conf.use_cache:
            self.cache.set("_run", df)
        return df

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        cols = self.output.list_column_names()
        if data is None or data.empty:
            return pd.DataFrame(columns=cols)

        out = data.copy()
        out["code"] = out["ts_code"].astype(str)
        out["date"] = pd.to_datetime(
            out["trade_date"],
            format="%Y%m%d",
            errors="coerce",
        )
        out["datecode"] = out["date"].dt.strftime("%Y%m%d")
        out["adj_factor"] = out["adj_factor"].astype(str)
        out = out[cols].drop_duplicates()
        return out.sort_values(["code", "date"]).reset_index(drop=True)
