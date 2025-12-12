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


class Individual(Job):
    """
    描述: 获取个股资金流向数据，用于分析主力资金动向 <br>
    说明: 单次最大提取6000条, 可以通过日期参数循环调取 <br>
    使用: 5000积分可以调取, 每分钟内最多调取200次 <br>
    注意: 小单=5万以下 中单=5万-20万 大单=20-100万 特大单：成交额>=100万 <br>

    参数:
    - session: Session, 必需, Tushare API会话对象
    - conf: Conf | Dict[str, Any], 可选, 作业配置, 支持以下参数:
        - params: Dict, 可选, 请求参数
            - ts_code: str, 可选, 股票代码
            - trade_date: str, 可选, 交易日期(YYYYMMDD)
            - start_date: str, 可选, 开始日期(YYYYMMDD)
            - end_date: str, 可选, 结束日期(YYYYMMDD)
        - limit: int, 可选, 最大迭代次数, 默认10000
        - size: int, 可选, 每次提取数据量, 建议不超过6000
        - coolant: float, 可选, 请求间隔时间(秒), 默认0.5
    - retry: Retry, 可选, 重试配置

    例子:
    ```python
        # 获取单只股票资金流向
        individual_job = Individual(
            session=session,
            conf=Conf(
                params={
                    "ts_code": "000001.SZ",
                    "start_date": "20241101",
                    "end_date": "20241130"
                }
            )
        )
        result = individual_job.run()
        individual_job.clean()  # 清理缓存
    ```
    """

    _SIZE = 6000
    _FREQ = 0.5
    _ARGS = {
        "ts_code": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "股票代码",
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
        desc="个股资金流向数据输入格式",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="ts_code", kind=DataKind.STRING, desc="股票代码"),
            ColumnInfo(name="trade_date", kind=DataKind.STRING, desc="交易日期"),
            ColumnInfo(name="buy_sm_vol", kind=DataKind.FLOAT, desc="小单买入量(手)"),
            ColumnInfo(name="buy_sm_amount", kind=DataKind.FLOAT, desc="小单买入金额(万元)"),
            ColumnInfo(name="sell_sm_vol", kind=DataKind.FLOAT, desc="小单卖出量(手)"),
            ColumnInfo(name="sell_sm_amount", kind=DataKind.FLOAT, desc="小单卖出金额(万元)"),
            ColumnInfo(name="buy_md_vol", kind=DataKind.FLOAT, desc="中单买入量(手)"),
            ColumnInfo(name="buy_md_amount", kind=DataKind.FLOAT, desc="中单买入金额(万元)"),
            ColumnInfo(name="sell_md_vol", kind=DataKind.FLOAT, desc="中单卖出量(手)"),
            ColumnInfo(name="sell_md_amount", kind=DataKind.FLOAT, desc="中单卖出金额(万元)"),
            ColumnInfo(name="buy_lg_vol", kind=DataKind.FLOAT, desc="大单买入量(手)"),
            ColumnInfo(name="buy_lg_amount", kind=DataKind.FLOAT, desc="大单买入金额(万元)"),
            ColumnInfo(name="sell_lg_vol", kind=DataKind.FLOAT, desc="大单卖出量(手)"),
            ColumnInfo(name="sell_lg_amount", kind=DataKind.FLOAT, desc="大单卖出金额(万元)"),
            ColumnInfo(name="buy_elg_vol", kind=DataKind.FLOAT, desc="特大单买入量(手)"),
            ColumnInfo(name="buy_elg_amount", kind=DataKind.FLOAT, desc="特大单买入金额(万元)"),
            ColumnInfo(name="sell_elg_vol", kind=DataKind.FLOAT, desc="特大单卖出量(手)"),
            ColumnInfo(name="sell_elg_amount", kind=DataKind.FLOAT, desc="特大单卖出金额(万元)"),
            ColumnInfo(name="net_mf_vol", kind=DataKind.FLOAT, desc="净流入量(手)"),
            ColumnInfo(name="net_mf_amount", kind=DataKind.FLOAT, desc="净流入金额(万元)"),
        ],
    )
    _OUT = TableInfo(
        desc="个股资金流向数据标准化输出格式",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="code", kind=DataKind.STRING, desc="股票代码"),
            ColumnInfo(name="date", kind=DataKind.DATETIME, desc="交易日期"),
            ColumnInfo(name="datecode", kind=DataKind.STRING, desc="交易日期代码(YYYYMMDD)"),
            ColumnInfo(name="buy_sm_vol", kind=DataKind.FLOAT, desc="小单买入量(手)"),
            ColumnInfo(name="buy_sm_amount", kind=DataKind.FLOAT, desc="小单买入金额(万元)"),
            ColumnInfo(name="sell_sm_vol", kind=DataKind.FLOAT, desc="小单卖出量(手)"),
            ColumnInfo(name="sell_sm_amount", kind=DataKind.FLOAT, desc="小单卖出金额(万元)"),
            ColumnInfo(name="buy_md_vol", kind=DataKind.FLOAT, desc="中单买入量(手)"),
            ColumnInfo(name="buy_md_amount", kind=DataKind.FLOAT, desc="中单买入金额(万元)"),
            ColumnInfo(name="sell_md_vol", kind=DataKind.FLOAT, desc="中单卖出量(手)"),
            ColumnInfo(name="sell_md_amount", kind=DataKind.FLOAT, desc="中单卖出金额(万元)"),
            ColumnInfo(name="buy_lg_vol", kind=DataKind.FLOAT, desc="大单买入量(手)"),
            ColumnInfo(name="buy_lg_amount", kind=DataKind.FLOAT, desc="大单买入金额(万元)"),
            ColumnInfo(name="sell_lg_vol", kind=DataKind.FLOAT, desc="大单卖出量(手)"),
            ColumnInfo(name="sell_lg_amount", kind=DataKind.FLOAT, desc="大单卖出金额(万元)"),
            ColumnInfo(name="buy_elg_vol", kind=DataKind.FLOAT, desc="特大单买入量(手)"),
            ColumnInfo(name="buy_elg_amount", kind=DataKind.FLOAT, desc="特大单买入金额(万元)"),
            ColumnInfo(name="sell_elg_vol", kind=DataKind.FLOAT, desc="特大单卖出量(手)"),
            ColumnInfo(name="sell_elg_amount", kind=DataKind.FLOAT, desc="特大单卖出金额(万元)"),
            ColumnInfo(name="net_mf_vol", kind=DataKind.FLOAT, desc="净流入量(手)"),
            ColumnInfo(name="net_mf_amount", kind=DataKind.FLOAT, desc="净流入金额(万元)"),
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
                name="moneyflow",
                url="https://tushare.pro/document/2?doc_id=170",
                args=self._ARGS,
                tableinfo=self._IN,
            ),
            output=Output(
                name="individual",
                tableinfo=self._OUT,
            ),
            retry=retry,
            tags={
                "name": "individual",
                "module": "stock",
                "level": "capflow",
                "frequency": "interday",
                "scope": "moneyflow",
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
            api=self.connection.moneyflow,
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
        numeric_fields = [
            "buy_sm_vol",
            "buy_sm_amount",
            "sell_sm_vol",
            "sell_sm_amount",
            "buy_md_vol",
            "buy_md_amount",
            "sell_md_vol",
            "sell_md_amount",
            "buy_lg_vol",
            "buy_lg_amount",
            "sell_lg_vol",
            "sell_lg_amount",
            "buy_elg_vol",
            "buy_elg_amount",
            "sell_elg_vol",
            "sell_elg_amount",
            "net_mf_vol",
            "net_mf_amount",
        ]
        for field in numeric_fields:
            out[field] = pd.to_numeric(out[field], errors="coerce")

        out = out[cols].drop_duplicates()
        return out.sort_values(["code", "date"]).reset_index(drop=True)
