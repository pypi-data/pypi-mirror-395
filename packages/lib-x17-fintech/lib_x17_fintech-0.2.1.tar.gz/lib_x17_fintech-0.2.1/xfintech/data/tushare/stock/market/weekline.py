from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

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


class Weekline(Job):
    """
    描述: 获取A股周线行情数据 <br>
    说明: 每周最后一个交易日更新, 本接口是未复权行情 <br>
    使用: 用户需要至少2000积分才可以调取, 单次最大6000行 <br>

    参数:
    - session: Session, 必需, Tushare API会话对象
    - conf: Conf | Dict[str, Any], 可选, 作业配置, 支持以下参数:
        - params: Dict, 可选, 请求参数
            - ts_code: str, 可选, 股票代码
            - trade_date: str, 可选, 特定交易日期(YYYYMMDD)
                每周最后一个交易日期
            - start_date: str, 可选, 开始日期(YYYYMMDD)
            - end_date: str, 可选, 结束日期(YYYYMMDD)
        - limit: int, 可选, 最大迭代次数, 默认10000
        - size: int, 可选, 每次提取数据量, 建议不超过6000
        - coolant: float, 可选, 请求间隔时间(秒), 默认0.1
    - retry: Retry, 可选, 重试配置

    例子:
    ```python
        # 获取单只股票周线数据
        weekline_job = Weekline(
            session=session,
            conf=Conf(
                params={
                    "ts_code": "000001.SZ",
                    "trade_date": "20241130",
                    "start_date": "20241101",
                    "end_date": "20241201"
                }
            )
        )
        result = weekline_job.run()

        # 获取某个交易周全市场数据
        market_snapshot = Weekline(
            session=session,
            conf=Conf(
                params={
                    "trade_date": "20241129"  # 周五
                },
                size=6000
            )
        )
        result = market_snapshot.run()
        weekline_job.clean()  # 清理缓存
    ```
    """

    _SIZE = 6000
    _FREQ = 0.1
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
        desc="A股周线行情数据输入格式",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="ts_code", kind=DataKind.STRING, desc="股票代码"),
            ColumnInfo(name="trade_date", kind=DataKind.STRING, desc="交易日期"),
            ColumnInfo(name="open", kind=DataKind.FLOAT, desc="周开盘价"),
            ColumnInfo(name="high", kind=DataKind.FLOAT, desc="周最高价"),
            ColumnInfo(name="low", kind=DataKind.FLOAT, desc="周最低价"),
            ColumnInfo(name="close", kind=DataKind.FLOAT, desc="周收盘价"),
            ColumnInfo(name="pre_close", kind=DataKind.FLOAT, desc="上一周收盘价"),
            ColumnInfo(name="change", kind=DataKind.FLOAT, desc="周涨跌额"),
            ColumnInfo(name="pct_chg", kind=DataKind.FLOAT, desc="周涨跌幅"),
            ColumnInfo(name="vol", kind=DataKind.FLOAT, desc="周成交量"),
            ColumnInfo(name="amount", kind=DataKind.FLOAT, desc="周成交额"),
        ],
    )
    _OUT = TableInfo(
        desc="A股周线行情数据标准化输出格式",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="code", kind=DataKind.STRING, desc="股票代码"),
            ColumnInfo(name="date", kind=DataKind.DATETIME, desc="交易日期"),
            ColumnInfo(name="datecode", kind=DataKind.STRING, desc="交易日期代码(YYYYMMDD)"),
            ColumnInfo(name="open", kind=DataKind.FLOAT, desc="开盘价(元)"),
            ColumnInfo(name="high", kind=DataKind.FLOAT, desc="最高价(元)"),
            ColumnInfo(name="low", kind=DataKind.FLOAT, desc="最低价(元)"),
            ColumnInfo(name="close", kind=DataKind.FLOAT, desc="收盘价(元)"),
            ColumnInfo(name="pre_close", kind=DataKind.FLOAT, desc="昨收价(元，除权价)"),
            ColumnInfo(name="change", kind=DataKind.FLOAT, desc="涨跌额(元)"),
            ColumnInfo(name="percent_change", kind=DataKind.FLOAT, desc="涨跌幅(%)"),
            ColumnInfo(name="volume", kind=DataKind.FLOAT, desc="成交量(手)"),
            ColumnInfo(name="amount", kind=DataKind.FLOAT, desc="成交额(千元)"),
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
                name="weekly",
                url="http://tushare.pro/document/2?doc_id=144",
                args=self._ARGS,
                tableinfo=self._IN,
            ),
            output=Output(
                name="weekline",
                tableinfo=self._OUT,
            ),
            retry=retry,
            tags={
                "name": "weekline",
                "module": "stock",
                "level": "market",
                "frequency": "interday",
                "scope": "weekly",
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
            api=self.connection.weekly,
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
        out["open"] = pd.to_numeric(out["open"], errors="coerce")
        out["high"] = pd.to_numeric(out["high"], errors="coerce")
        out["low"] = pd.to_numeric(out["low"], errors="coerce")
        out["close"] = pd.to_numeric(out["close"], errors="coerce")
        out["pre_close"] = pd.to_numeric(out["pre_close"], errors="coerce")
        out["change"] = pd.to_numeric(out["change"], errors="coerce")
        out["percent_change"] = pd.to_numeric(out["pct_chg"], errors="coerce")
        out["volume"] = pd.to_numeric(out["vol"], errors="coerce")
        out["amount"] = pd.to_numeric(out["amount"], errors="coerce")
        out = out[cols].drop_duplicates()
        return out.sort_values(["code", "date"]).reset_index(drop=True)

    def list_codes(self) -> List[str]:
        if "_run" not in self.cache:
            df = self.run()
        result = df["code"].unique().tolist()
        if self.conf.use_cache:
            self.cache.set("list_codes", result)
        return result

    def list_dates(self) -> List[str]:
        if "_run" not in self.cache:
            df = self.run()
        result = df["date"].unique().tolist()
        result.sort()
        if self.conf.use_cache:
            self.cache.set("list_dates", result)
        return result
