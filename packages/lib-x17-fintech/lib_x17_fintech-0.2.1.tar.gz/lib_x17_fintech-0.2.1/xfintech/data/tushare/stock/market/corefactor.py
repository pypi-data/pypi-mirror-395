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


class CoreFactor(Job):
    """
    描述: 获取A股每日基本面指标数据 <br>
    说明: 交易日每日15点-17点之间更新, 全部股票每日重要的基本面指标 <br>
    使用: 至少2000积分才可以调取, 5000积分无总量限制, 单次最大返回6000条数据 <br>

    参数:
    - session: Session, 必需, Tushare API会话对象
    - conf: Conf | Dict[str, Any], 可选, 作业配置, 支持以下参数:
        - params: Dict, 可选, 请求参数
            - ts_code: str, 可选, 股票代码
            - trade_date: str, 可选, 特定交易日期(YYYYMMDD)
            - start_date: str, 可选, 开始日期(YYYYMMDD)
            - end_date: str, 可选, 结束日期(YYYYMMDD)
        - limit: int, 可选, 最大迭代次数, 默认10000
        - size: int, 可选, 每次提取数据量, 建议不超过6000
        - coolant: float, 可选, 请求间隔时间(秒), 默认0.1
    - retry: Retry, 可选, 重试配置

    例子:
    ```python
        # 获取单只股票基本面数据
        corefactor_job = CoreFactor(
            session=session,
            conf=Conf(
                params={
                    "ts_code": "000001.SZ",
                    "start_date": "20241101",
                    "end_date": "20241201"
                }
            )
        )
        result = corefactor_job.run()

        # 获取某交易日全市场基本面数据
        market_basic = CoreFactor(
            session=session,
            conf=Conf(
                params={
                    "trade_date": "20241201"
                },
                size=6000
            )
        )
        result = market_basic.run()
        corefactor_job.clean()  # 清理缓存
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
        desc="A股每日基本面指标数据输入格式",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="ts_code", kind=DataKind.STRING, desc="股票代码"),
            ColumnInfo(name="trade_date", kind=DataKind.STRING, desc="交易日期"),
            ColumnInfo(name="close", kind=DataKind.FLOAT, desc="当日收盘价"),
            ColumnInfo(name="turnover_rate", kind=DataKind.FLOAT, desc="换手率(%)"),
            ColumnInfo(name="turnover_rate_f", kind=DataKind.FLOAT, desc="换手率(自由流通股)"),
            ColumnInfo(name="volume_ratio", kind=DataKind.FLOAT, desc="量比"),
            ColumnInfo(name="pe", kind=DataKind.FLOAT, desc="市盈率(总市值/净利润， 亏损的PE为空)"),
            ColumnInfo(name="pe_ttm", kind=DataKind.FLOAT, desc="市盈率(TTM, 亏损的PE为空)"),
            ColumnInfo(name="pb", kind=DataKind.FLOAT, desc="市净率(总市值/净资产)"),
            ColumnInfo(name="ps", kind=DataKind.FLOAT, desc="市销率"),
            ColumnInfo(name="ps_ttm", kind=DataKind.FLOAT, desc="市销率(TTM)"),
            ColumnInfo(name="dv_ratio", kind=DataKind.FLOAT, desc="股息率 (%)"),
            ColumnInfo(name="dv_ttm", kind=DataKind.FLOAT, desc="股息率(TTM)(%)"),
            ColumnInfo(name="total_share", kind=DataKind.FLOAT, desc="总股本 (万股)"),
            ColumnInfo(name="float_share", kind=DataKind.FLOAT, desc="流通股本 (万股)"),
            ColumnInfo(name="free_share", kind=DataKind.FLOAT, desc="自由流通股本 (万)"),
            ColumnInfo(name="total_mv", kind=DataKind.FLOAT, desc="总市值 (万元)"),
            ColumnInfo(name="circ_mv", kind=DataKind.FLOAT, desc="流通市值(万元)"),
        ],
    )
    _OUT = TableInfo(
        desc="A股每日基本面指标数据标准化输出格式",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="code", kind=DataKind.STRING, desc="股票代码"),
            ColumnInfo(name="date", kind=DataKind.DATETIME, desc="交易日期"),
            ColumnInfo(name="datecode", kind=DataKind.STRING, desc="交易日期代码(YYYYMMDD)"),
            ColumnInfo(name="close", kind=DataKind.FLOAT, desc="当日收盘价"),
            ColumnInfo(name="turnover_rate", kind=DataKind.FLOAT, desc="换手率(%)"),
            ColumnInfo(name="turnover_rate_f", kind=DataKind.FLOAT, desc="换手率(自由流通股)"),
            ColumnInfo(name="volume_ratio", kind=DataKind.FLOAT, desc="量比"),
            ColumnInfo(name="pe", kind=DataKind.FLOAT, desc="市盈率(总市值/净利润， 亏损的PE为空)"),
            ColumnInfo(name="pe_ttm", kind=DataKind.FLOAT, desc="市盈率(TTM, 亏损的PE为空)"),
            ColumnInfo(name="pb", kind=DataKind.FLOAT, desc="市净率(总市值/净资产)"),
            ColumnInfo(name="ps", kind=DataKind.FLOAT, desc="市销率"),
            ColumnInfo(name="ps_ttm", kind=DataKind.FLOAT, desc="市销率(TTM)"),
            ColumnInfo(name="dv_ratio", kind=DataKind.FLOAT, desc="股息率 (%)"),
            ColumnInfo(name="dv_ttm", kind=DataKind.FLOAT, desc="股息率(TTM)(%)"),
            ColumnInfo(name="total_share", kind=DataKind.FLOAT, desc="总股本 (万股)"),
            ColumnInfo(name="float_share", kind=DataKind.FLOAT, desc="流通股本 (万股)"),
            ColumnInfo(name="free_share", kind=DataKind.FLOAT, desc="自由流通股本 (万)"),
            ColumnInfo(name="total_mv", kind=DataKind.FLOAT, desc="总市值 (万元)"),
            ColumnInfo(name="circle_mv", kind=DataKind.FLOAT, desc="流通市值(万元)"),
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
                name="daily_basic",
                url="http://tushare.pro/document/2?doc_id=32",
                args=self._ARGS,
                tableinfo=self._IN,
            ),
            output=Output(
                name="corefactor",
                tableinfo=self._OUT,
            ),
            retry=retry,
            tags={
                "name": "corefactor",
                "module": "stock",
                "level": "market",
                "frequency": "interday",
                "scope": "daily_basic",
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
            api=self.connection.daily_basic,
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

        # Convert all numeric fields to proper types
        numeric_fields = [
            "close",
            "turnover_rate",
            "turnover_rate_f",
            "volume_ratio",
            "pe",
            "pe_ttm",
            "pb",
            "ps",
            "ps_ttm",
            "dv_ratio",
            "dv_ttm",
            "total_share",
            "float_share",
            "free_share",
            "total_mv",
        ]

        for field in numeric_fields:
            if field in out.columns:
                out[field] = pd.to_numeric(out[field], errors="coerce")

        if "circ_mv" in out.columns:
            out["circle_mv"] = pd.to_numeric(out["circ_mv"], errors="coerce")

        out = out[cols].drop_duplicates()
        return out.sort_values(["code", "date"]).reset_index(drop=True)

    def list_codes(self) -> List[str]:
        if "_run" not in self.cache:
            self.run()
        df = self.cache.get("_run")
        result = df["code"].unique().tolist()
        if self.conf.use_cache:
            self.cache.set("list_codes", result)
        return result

    def list_dates(self) -> List[str]:
        if "_run" not in self.cache:
            self.run()
        df = self.cache.get("_run")
        result = df["datecode"].unique().tolist()
        result.sort()
        if self.conf.use_cache:
            self.cache.set("list_dates", result)
        return result
