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


class Ipo(Job):
    """
    描述: 获取新股上市列表数据 <br>
    限量: 单次最大2000条, 总量不限制 <br>
    积分: 用户需要至少120积分才可以调取 <br>

    参数:
    - conf: Conf | Dict[str, Any], 可选, 作业配置, 其中params支持以下参数:
        - params: 非必需, 请求参数字典
            - start_date: str, 非必需, 开始日期(YYYYMMDD)
            - end_date: str, 非必需, 结束日期(YYYYMMDD)
            - trade_date: str, 非必需, 交易日期(YYYYMMDD)
            - year: str, 非必需, 年份
        - limit: 非必需, 最大迭代次数, 默认为10000
        - size: 非必需, 每次提取数据量, 应小于2000
        - coolant: 非必需, 请求间隔时间(秒), 默认为0
    - retry: Retry, 可选, 重试配置

    例子:
    ```python
        ipo_job = Ipo(
            session=session,
            conf=Conf(
                params={
                    "year": "2023",
                }
            ),
        )
        result = ipo_job.run()
        print(ipo_job.describe())  # Display the fetched IPO data
        codes = ipo_job.list_codes()  # List of IPO stock codes
        names = ipo_job.list_names()  # List of IPO stock names
        ipo_job.clean()  # Clear cached data
    ```
    """

    _ARGS = {
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
        "year": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "年份(YYYY)",
        },
    }
    _IN = TableInfo(
        desc="获取新股发行上市信息，包括发行价、市盈率、募资额等",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="ts_code", kind=DataKind.STRING, desc="TS股票代码"),
            ColumnInfo(name="sub_code", kind=DataKind.STRING, desc="申购代码"),
            ColumnInfo(name="name", kind=DataKind.STRING, desc="股票名称"),
            ColumnInfo(name="ipo_date", kind=DataKind.STRING, desc="发行日期"),
            ColumnInfo(name="issue_date", kind=DataKind.STRING, desc="上市日期"),
            ColumnInfo(name="amount", kind=DataKind.FLOAT, desc="发行总量(万股)"),
            ColumnInfo(name="market_amount", kind=DataKind.FLOAT, desc="上网发行量(万股)"),
            ColumnInfo(name="price", kind=DataKind.FLOAT, desc="发行价格"),
            ColumnInfo(name="pe", kind=DataKind.FLOAT, desc="发行市盈率"),
            ColumnInfo(name="limit_amount", kind=DataKind.FLOAT, desc="个人申购上限(万股)"),
            ColumnInfo(name="funds", kind=DataKind.FLOAT, desc="募集资金(亿元)"),
            ColumnInfo(name="ballot", kind=DataKind.FLOAT, desc="中签率(%)"),
        ],
    )
    _OUT = TableInfo(
        desc="获取新股发行上市信息，包括发行价、市盈率、募资额等",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="code", kind=DataKind.STRING, desc="TS股票代码"),
            ColumnInfo(name="sub_code", kind=DataKind.STRING, desc="申购代码"),
            ColumnInfo(name="name", kind=DataKind.STRING, desc="股票名称"),
            ColumnInfo(name="ipo_date", kind=DataKind.DATETIME, desc="发行日期"),
            ColumnInfo(name="ipo_datecode", kind=DataKind.STRING, desc="发行日期代码"),
            ColumnInfo(name="issue_date", kind=DataKind.DATETIME, desc="上市日期"),
            ColumnInfo(name="issue_datecode", kind=DataKind.STRING, desc="上市日期代码"),
            ColumnInfo(name="amount", kind=DataKind.FLOAT, desc="发行总量(万股)"),
            ColumnInfo(name="market_amount", kind=DataKind.FLOAT, desc="上网发行量(万股)"),
            ColumnInfo(name="price", kind=DataKind.FLOAT, desc="发行价格"),
            ColumnInfo(name="pe", kind=DataKind.FLOAT, desc="发行市盈率"),
            ColumnInfo(name="limit_amount", kind=DataKind.FLOAT, desc="个人申购上限(万股)"),
            ColumnInfo(name="funds", kind=DataKind.FLOAT, desc="募集资金(亿元)"),
            ColumnInfo(name="ballot", kind=DataKind.FLOAT, desc="中签率(%)"),
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
                name="new_share",
                url="http://tushare.pro/document/2?doc_id=123",
                args=self._ARGS,
                tableinfo=self._IN,
            ),
            output=Output(
                name="ipo",
                tableinfo=self._OUT,
            ),
            retry=retry,
            tags={
                "name": "ipo",
                "module": "stock",
                "level": "basic",
                "frequency": "interday",
                "scope": "new_share",
            },
        )

    @staticmethod
    def _resolve_conf(
        conf: Optional[Conf | Dict[str, Any]] = None,
    ) -> Conf:
        if conf is None:
            obj = Conf(size=2000)
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

        if obj.size > 2000:
            obj.set_size(2000)

        return obj

    def _run(self) -> object:
        params = dict(self.conf.get_params() or {})
        df = self._fetchall(
            api=self.connection.new_share,
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
        out["sub_code"] = out["sub_code"].astype(str)
        out["name"] = out["name"].astype(str)
        out["ipo_date"] = pd.to_datetime(
            out["ipo_date"],
            format="%Y%m%d",
            errors="coerce",
        )
        out["ipo_datecode"] = out["ipo_date"].dt.strftime("%Y%m%d")
        out["issue_date"] = pd.to_datetime(
            out["issue_date"],
            format="%Y%m%d",
            errors="coerce",
        )
        out["issue_datecode"] = out["issue_date"].dt.strftime("%Y%m%d")
        out["amount"] = pd.to_numeric(out["amount"], errors="coerce")
        out["market_amount"] = pd.to_numeric(out["market_amount"], errors="coerce")
        out["price"] = pd.to_numeric(out["price"], errors="coerce")
        out["pe"] = pd.to_numeric(out["pe"], errors="coerce")
        out["limit_amount"] = pd.to_numeric(out["limit_amount"], errors="coerce")
        out["funds"] = pd.to_numeric(out["funds"], errors="coerce")
        out["ballot"] = pd.to_numeric(out["ballot"], errors="coerce")
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
