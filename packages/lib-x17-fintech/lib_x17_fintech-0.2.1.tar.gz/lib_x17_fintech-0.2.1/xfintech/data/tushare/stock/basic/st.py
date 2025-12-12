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


class St(Job):
    """
    描述: 获取ST股票列表, 可根据交易日期获取历史上每天的ST列表 <br>
    提示: 每天上午9:20更新, 单次最大返回1000行, 数据从20160101开始 <br>
    积分: 用户需要至少3000积分才可以调取 <br>

    参数:
    - conf: Conf | Dict[str, Any], 可选, 作业配置, 其中params支持以下参数:
        - params: 非必需, 请求参数字典
            - ts_code: str, 非必需, TS股票代码
            - trade_date: str, 非必需, 交易日期(YYYYMMDD格式)
            - start_date: str, 非必需, 开始日期(YYYYMMDD格式)
            - end_date: str, 非必需, 结束日期(YYYYMMDD格式)
            - year: str, 非必需, 年份
        - limit: 非必需, 最大迭代次数, 默认为10000
        - size: 非必需, 每次提取数据量, 默认1000
        - coolant: 非必需, 请求间隔时间(秒), 默认为0
    - retry: Retry, 可选, 重试配置

    例子:
    ```python
        st_job = St(
            session=session,
            conf=Conf(
                params={
                    "year": "2023",
                }
            ),
        )
        result = st_job.run()
        print(st_job.describe())  # Display the fetched ST stock data
    ```
    """

    _ARGS = {
        "ts_code": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "TS股票代码",
        },
        "year": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "年份(YYYY)",
        },
        "trade_date": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "交易日期(YYYYMMDD格式)",
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
        desc="ST股票列表",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="ts_code", kind=DataKind.STRING, desc="TS股票代码"),
            ColumnInfo(name="name", kind=DataKind.STRING, desc="股票名称"),
            ColumnInfo(name="trade_date", kind=DataKind.STRING, desc="交易日期"),
            ColumnInfo(name="type", kind=DataKind.STRING, desc="ST类型"),
            ColumnInfo(name="type_name", kind=DataKind.STRING, desc="ST类型名称"),
        ],
    )
    _OUT = TableInfo(
        desc="ST股票列表",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="code", kind=DataKind.STRING, desc="股票代码"),
            ColumnInfo(name="name", kind=DataKind.STRING, desc="股票名称"),
            ColumnInfo(name="date", kind=DataKind.DATETIME, desc="交易日期"),
            ColumnInfo(name="datecode", kind=DataKind.STRING, desc="交易日期字符串"),
            ColumnInfo(name="type", kind=DataKind.STRING, desc="ST类型"),
            ColumnInfo(name="type_name", kind=DataKind.STRING, desc="ST类型名称"),
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
            conf=self._resolve_conf(conf=conf),
            source=Source(
                name="stock_st",
                url="https://tushare.pro/document/2?doc_id=397",
                args=self._ARGS,
                tableinfo=self._IN,
            ),
            output=Output(
                name="st",
                tableinfo=self._OUT,
            ),
            retry=retry,
            tags={
                "name": "st",
                "module": "stock",
                "level": "basic",
                "frequency": "interday",
                "scope": "stock_st",
            },
        )

    @staticmethod
    def _resolve_conf(
        conf: Optional[Conf | Dict[str, Any]] = None,
    ) -> Conf:
        if conf is None:
            obj = Conf(size=1000)
        else:
            obj = Conf.from_dict(conf)

        params = obj.get_params() or {}
        if "trade_date" in params:
            trade_date = params.pop("trade_date")
            if isinstance(trade_date, datetime):
                trade_date = trade_date.strftime("%Y%m%d")
            params["start_date"] = trade_date
            params["end_date"] = trade_date
        elif "year" in params:
            year = str(params.pop("year"))
            params["start_date"] = f"{year}0101"
            params["end_date"] = f"{year}1231"
        obj.set_params(params)

        if obj.size > 1000:
            obj.set_size(1000)

        return obj

    def _run(self) -> object:
        params = dict(self.conf.get_params() or {})
        df = self._fetchall(
            api=self.connection.stock_st,
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
        out["name"] = out["name"].astype(str)
        out["date"] = pd.to_datetime(
            out["trade_date"],
            format="%Y%m%d",
            errors="coerce",
        )
        out["datecode"] = out["trade_date"].astype(str)
        out["type"] = out["type"].astype(str)
        out["type_name"] = out["type_name"].astype(str)
        out = out[cols].drop_duplicates()
        return out.sort_values("code").reset_index(drop=True)

    def list_codes(self) -> List[str]:
        if "_run" not in self.cache:
            df = self.run()
        else:
            df = self.cache.get("_run")
        result = df["code"].unique().tolist()
        result.sort()
        if self.conf.use_cache:
            self.cache.set("list_codes", result)
        return result

    def list_names(self) -> List[str]:
        if "_run" not in self.cache:
            df = self.run()
        else:
            df = self.cache.get("_run")
        result = df["name"].unique().tolist()
        result.sort()
        if self.conf.use_cache:
            self.cache.set("list_names", result)
        return result
