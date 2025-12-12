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


class Concept(Job):
    """
    描述: 获取同花顺概念板块资金流向数据，用于分析板块资金流动情况 <br>
    说明: 单次最大提取5000条, 可以通过日期参数循环调取 <br>
    使用: 5000积分可以调取 <br>

    参数:
    - session: Session, 必需, Tushare API会话对象
    - conf: Conf | Dict[str, Any], 可选, 作业配置, 支持以下参数:
        - params: Dict, 可选, 请求参数
            - ts_code: str, 可选, 概念代码(支持多个概念, 逗号分隔)
            - trade_date: str, 可选, 交易日期(YYYYMMDD)
            - start_date: str, 可选, 开始日期(YYYYMMDD)
            - end_date: str, 可选, 结束日期(YYYYMMDD)
        - limit: int, 可选, 最大迭代次数, 默认10000
        - size: int, 可选, 每次提取数据量, 建议不超过5000
        - coolant: float, 可选, 请求间隔时间(秒), 默认1.0
    - retry: Retry, 可选, 重试配置

    例子:
    ```python
        # 获取某日全部概念板块资金流向
        concept_job = Concept(
            session=session,
            conf=Conf(
                params={
                    "trade_date": "20241201"
                },
                size=5000
            )
        )
        result = concept_job.run()
        concept_job.clean()  # 清理缓存
    ```
    """

    _SIZE = 5000
    _FREQ = 1.0
    _ARGS = {
        "ts_code": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "概念代码(支持多个概念同时提取, 逗号分隔)",
        },
        "trade_date": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "交易日期(YYYYMMDD)",
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
        desc="同花顺概念板块资金流向数据",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="trade_date", kind=DataKind.STRING, desc="交易日期"),
            ColumnInfo(name="ts_code", kind=DataKind.STRING, desc="板块代码"),
            ColumnInfo(name="name", kind=DataKind.STRING, desc="板块名称"),
            ColumnInfo(name="lead_stock", kind=DataKind.STRING, desc="领涨股票名称"),
            ColumnInfo(name="close_price", kind=DataKind.FLOAT, desc="最新价"),
            ColumnInfo(name="pct_change", kind=DataKind.FLOAT, desc="行业涨跌幅"),
            ColumnInfo(name="industry_index", kind=DataKind.FLOAT, desc="板块指数"),
            ColumnInfo(name="company_num", kind=DataKind.INTEGER, desc="公司数量"),
            ColumnInfo(name="pct_change_stock", kind=DataKind.FLOAT, desc="领涨股涨跌幅"),
            ColumnInfo(name="net_buy_amount", kind=DataKind.FLOAT, desc="流入资金(亿元)"),
            ColumnInfo(name="net_sell_amount", kind=DataKind.FLOAT, desc="流出资金(亿元)"),
            ColumnInfo(name="net_amount", kind=DataKind.FLOAT, desc="净额(亿元)"),
        ],
    )
    _OUT = TableInfo(
        desc="同花顺概念板块资金流向数据",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="code", kind=DataKind.STRING, desc="板块代码"),
            ColumnInfo(name="date", kind=DataKind.DATETIME, desc="交易日期"),
            ColumnInfo(name="datecode", kind=DataKind.STRING, desc="交易日期代码(YYYYMMDD)"),
            ColumnInfo(name="name", kind=DataKind.STRING, desc="板块名称"),
            ColumnInfo(name="lead_stock", kind=DataKind.STRING, desc="领涨股票名称"),
            ColumnInfo(name="close", kind=DataKind.FLOAT, desc="最新价"),
            ColumnInfo(name="percent_change", kind=DataKind.FLOAT, desc="行业涨跌幅"),
            ColumnInfo(name="industry_index", kind=DataKind.FLOAT, desc="板块指数"),
            ColumnInfo(name="company_num", kind=DataKind.INTEGER, desc="公司数量"),
            ColumnInfo(name="pct_change_stock", kind=DataKind.FLOAT, desc="领涨股涨跌幅"),
            ColumnInfo(name="net_buy_amount", kind=DataKind.FLOAT, desc="流入资金(亿元)"),
            ColumnInfo(name="net_sell_amount", kind=DataKind.FLOAT, desc="流出资金(亿元)"),
            ColumnInfo(name="net_amount", kind=DataKind.FLOAT, desc="净额(亿元)"),
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
                name="moneyflow_cnt_ths",
                url="https://tushare.pro/document/2?doc_id=371",
                args=self._ARGS,
                tableinfo=self._IN,
            ),
            output=Output(
                name="concept",
                tableinfo=self._OUT,
            ),
            retry=retry,
            tags={
                "name": "concept",
                "module": "stock",
                "level": "capflow",
                "frequency": "interday",
                "scope": "moneyflow_cnt_ths",
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
            api=self.connection.moneyflow_cnt_ths,
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
        out["name"] = out["name"].astype(str)
        out["percent_change"] = pd.to_numeric(out["pct_change"], errors="coerce")
        out["close"] = pd.to_numeric(out["close_price"], errors="coerce")
        numeric_fields = [
            "industry_index",
            "company_num",
            "pct_change_stock",
            "net_buy_amount",
            "net_sell_amount",
            "net_amount",
        ]
        for field in numeric_fields:
            out[field] = pd.to_numeric(out[field], errors="coerce")

        out = out[cols].drop_duplicates()
        return out.sort_values(["code", "date"]).reset_index(drop=True)
