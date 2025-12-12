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


class TradeDate(Job):
    """
    描述: 交易日历数据, 包括交易所的交易日期和非交易日期

    参数:
    - conf: Conf | Dict[str, Any], 可选, 作业配置, 其中params支持以下参数:
        - params: 非必需, 请求参数字典
            - exchange: str, 非必需, 交易所: SSE上交所 SZSE深交所 ...
            - year: str, 非必需, 年份: YYYY
            - start_date: str, 非必需, 开始日期: YYYYMMDD
            - end_date: str, 非必需, 结束日期: YYYYMMDD
            - is_open: str, 非必需, 是否交易: 0=休市
        - limit: 非必需, 最大迭代次数, 默认为10000
        - size: 非必需, 每次提取数据量, 应小于5000
        - coolant: 非必需, 请求间隔时间(秒), 默认为0
    - retry: Retry, 可选, 重试配置

    例子:
    ```python
        trade_date_job = TradeDate(
            session=session,
            conf=Conf(
                params={
                    "year": "2023",
                }
            ),
        )
        result = trade_date_job.run()
        print(trade_date_job.describe())  # Display the fetched trade date data
    ```
    """

    _EXCHANGES = ["SSE", "SZSE", "CFFEX", "SHFE", "CZCE", "DCE", "INE"]
    _ARGS = {
        "exchange": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": f"交易所: {_EXCHANGES}",
        },
        "start_date": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "开始日期: YYYYMMDD",
        },
        "end_date": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "结束日期: YYYYMMDD",
        },
        "is_open": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "是否交易: 0=休市, 1=交易",
        },
        "year": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "年份(YYYY)",
        },
    }
    _IN = TableInfo(
        desc="交易日历数据, 包括交易所的交易日期和非交易日期",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="exchange", kind=DataKind.STRING, desc="交易所"),
            ColumnInfo(name="start_date", kind=DataKind.STRING, desc="开始日期:YYYYMMDD"),
            ColumnInfo(name="end_date", kind=DataKind.STRING, desc="结束日期:YYYYMMDD"),
            ColumnInfo(name="is_open", kind=DataKind.STRING, desc="是否是交易日"),
        ],
    )
    _OUT = TableInfo(
        desc="交易日历数据, 包括交易所的交易日期和非交易日期",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="datecode", kind=DataKind.STRING, desc="日期代码:YYYYMMDD"),
            ColumnInfo(name="date", kind=DataKind.DATETIME, desc="日期"),
            ColumnInfo(name="exchange", kind=DataKind.STRING, desc="交易所"),
            ColumnInfo(name="previous", kind=DataKind.DATETIME, desc="前一个交易日"),
            ColumnInfo(name="is_open", kind=DataKind.INTEGER, desc="是否是交易日"),
            ColumnInfo(name="year", kind=DataKind.INTEGER, desc="年份"),
            ColumnInfo(name="month", kind=DataKind.INTEGER, desc="月份"),
            ColumnInfo(name="day", kind=DataKind.INTEGER, desc="日"),
            ColumnInfo(name="week", kind=DataKind.INTEGER, desc="周数"),
            ColumnInfo(name="weekday", kind=DataKind.STRING, desc="星期几"),
            ColumnInfo(name="quarter", kind=DataKind.INTEGER, desc="季度"),
        ],
    )

    @classmethod
    def check(
        cls,
        session: Session,
        date: Optional[datetime | str] = None,
    ) -> bool:
        if isinstance(date, datetime):
            date = date.date()
        elif isinstance(date, str):
            if "-" in date:
                date = datetime.strptime(date, "%Y-%m-%d").date()
            else:
                date = datetime.strptime(date, "%Y%m%d").date()
        else:
            date = datetime.now().date()

        datecode = date.strftime("%Y%m%d")
        job = cls(
            session=session,
            conf={
                "params": {
                    "start_date": datecode,
                    "end_date": datecode,
                    "is_open": "1",
                }
            },
        )
        result = job.run()
        return not result.empty and datecode in result["datecode"].values

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
                name="trade_cal",
                url="https://tushare.pro/document/2?doc_id=108",
                args=self._ARGS,
                tableinfo=self._IN,
            ),
            output=Output(
                name="tradedate",
                tableinfo=self._OUT,
            ),
            retry=retry,
            tags={
                "name": "tradedate",
                "module": "stock",
                "level": "basic",
                "frequency": "interday",
                "scope": "trade_date",
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
        if "year" in params:
            year = str(params.pop("year"))
            params["start_date"] = f"{year}0101"
            params["end_date"] = f"{year}1231"

        obj.set_params(params)

        if obj.size > 1000:
            obj.set_size(1000)

        return obj

    def _run(self) -> object:
        params = dict(self.conf.get_params() or {})
        if "is_open" in params:
            df = self._fetchall(
                api=self.connection.trade_cal,
                **params,
            )
        else:
            df_open = self._fetchall(
                api=self.connection.trade_cal,
                is_open="1",
                **params,
            )
            df_close = self._fetchall(
                api=self.connection.trade_cal,
                is_open="0",
                **params,
            )
            df = pd.concat([df_open, df_close], ignore_index=True)
        df = self.transform(df)
        if self.conf.use_cache:
            self.cache.set("_run", df)
        return df

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        cols = self.output.list_column_names()
        if data is None or data.empty:
            return pd.DataFrame(columns=cols)

        out = data.copy()
        out["date"] = pd.to_datetime(
            out["cal_date"],
            format="%Y%m%d",
            errors="coerce",
        )
        out["datecode"] = out["cal_date"].astype(str)
        out["is_open"] = out["is_open"].astype(int).eq(1)
        out["previous"] = pd.to_datetime(
            out["pretrade_date"],
            format="%Y%m%d",
            errors="coerce",
        )
        out["exchange"] = "ALL"
        out["year"] = out["date"].dt.year
        out["month"] = out["date"].dt.month
        out["day"] = out["date"].dt.day
        out["week"] = out["date"].dt.isocalendar().week.astype(int)
        out["weekday"] = out["date"].dt.day_name().str[:3]
        out["quarter"] = out["date"].dt.quarter
        out = out[cols].drop_duplicates()
        return out.sort_values("datecode").reset_index(drop=True)

    def list_dates(self) -> List[datetime]:
        if "_run" not in self.cache:
            df = self.run()
        else:
            df = self.cache.get("_run")
        result = df["date"].tolist()
        if self.conf.use_cache:
            self.cache.set("list_dates", result)
        return result

    def list_open_dates(self) -> List[datetime]:
        if "_run" not in self.cache:
            df = self.run()
        else:
            df = self.cache.get("_run")
        result = df.loc[df["is_open"], "date"].tolist()
        if self.conf.use_cache:
            self.cache.set("list_open_dates", result)
        return result

    def list_datecodes(self) -> List[str]:
        if "_run" not in self.cache:
            df = self.run()
        else:
            df = self.cache.get("_run")
        result = df["datecode"].tolist()
        if self.conf.use_cache:
            self.cache.set("list_datecodes", result)
        return result

    def list_open_datecodes(self) -> List[str]:
        if "_run" not in self.cache:
            df = self.run()
        else:
            df = self.cache.get("_run")
        result = df.loc[df["is_open"], "datecode"].tolist()
        if self.conf.use_cache:
            self.cache.set("list_open_datecodes", result)
        return result
