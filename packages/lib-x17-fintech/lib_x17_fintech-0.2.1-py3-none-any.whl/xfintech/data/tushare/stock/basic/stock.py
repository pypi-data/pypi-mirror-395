from __future__ import annotations

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


class Stock(Job):
    """
    描述: 获取上市股票基本信息, 包括股票代码、名称、上市日期等基础数据 <br>
    限量: 单次最大4000条, 可以通过上市状态参数分批提取 <br>
    积分: 用户需要至少120积分才可以调取 <br>

    参数:
    - session: Session, 必需, Tushare API会话对象
    - conf: Conf | Dict[str, Any], 可选, 作业配置, 支持以下参数:
        - params: Dict, 可选, 请求参数
            - ts_code: str, 可选, TS股票代码
            - name: str, 可选, 股票名称
            - list_status: str, 可选, 上市状态(L=上市 D=退市 P=暂停上市)
            - exchange: str, 可选, 交易所(SSE=上交所 SZSE=深交所 BSE=北交所)
            - market: str, 可选, 市场类型(主板/创业板/科创板/CDR)
        - limit: int, 可选, 最大迭代次数, 默认10000
        - size: int, 可选, 每次提取数据量, 建议不超过4000
        - coolant: float, 可选, 请求间隔时间(秒), 默认0
    - retry: Retry, 可选, 重试配置

    例子:
    ```python
        # 获取所有上市股票信息
        stock_job = Stock(
            session=session,
            conf=Conf(
                params={
                    "list_status": "L"
                }
            )
        )
        result = stock_job.run()
        codes = stock_job.list_codes()  # 获取所有股票代码
        names = stock_job.list_names()  # 获取所有股票名称
        stock_job.clean()  # 清理缓存
    ```
    """

    _STATUSES = ["L", "D", "P"]
    _EXCHANGES = ["SSE", "SZSE", "BSE"]
    _ARGS = {
        "ts_code": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "TS股票代码",
        },
        "name": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "股票名称",
        },
        "list_status": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": f"上市状态{_STATUSES}",
        },
        "exchange": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": f"交易所{_EXCHANGES}",
        },
        "market": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "市场类型",
        },
    }
    _IN = TableInfo(
        desc="上市股票基本信息",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="ts_code", kind=DataKind.STRING, desc="TS代码"),
            ColumnInfo(name="symbol", kind=DataKind.STRING, desc="股票代码"),
            ColumnInfo(name="name", kind=DataKind.STRING, desc="股票名称"),
            ColumnInfo(name="area", kind=DataKind.STRING, desc="地域"),
            ColumnInfo(name="industry", kind=DataKind.STRING, desc="所属行业"),
            ColumnInfo(name="fullname", kind=DataKind.STRING, desc="股票全称"),
            ColumnInfo(name="enname", kind=DataKind.STRING, desc="英文全称"),
            ColumnInfo(name="cnspell", kind=DataKind.STRING, desc="拼音缩写"),
            ColumnInfo(name="market", kind=DataKind.STRING, desc="市场类型(主板/创业板/科创板/CDR)"),
            ColumnInfo(name="exchange", kind=DataKind.STRING, desc="交易所代码"),
            ColumnInfo(name="curr_type", kind=DataKind.STRING, desc="交易货币"),
            ColumnInfo(name="list_status", kind=DataKind.STRING, desc="上市状态 L上市 D退市 P暂停上市"),
            ColumnInfo(name="list_date", kind=DataKind.STRING, desc="上市日期"),
            ColumnInfo(name="delist_date", kind=DataKind.STRING, desc="退市日期"),
            ColumnInfo(name="is_hs", kind=DataKind.STRING, desc="是否沪深港通标"),
            ColumnInfo(name="act_name", kind=DataKind.STRING, desc="实控人名称"),
            ColumnInfo(name="act_ent_type", kind=DataKind.STRING, desc="实控人企业性质"),
        ],
    )
    _OUT = TableInfo(
        desc="上市股票基本信息结果",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="code", kind=DataKind.STRING, desc="TS代码"),
            ColumnInfo(name="symbol", kind=DataKind.STRING, desc="股票代码"),
            ColumnInfo(name="name", kind=DataKind.STRING, desc="股票名称"),
            ColumnInfo(name="area", kind=DataKind.STRING, desc="地域"),
            ColumnInfo(name="industry", kind=DataKind.STRING, desc="所属行业"),
            ColumnInfo(name="fullname", kind=DataKind.STRING, desc="股票全称"),
            ColumnInfo(name="enname", kind=DataKind.STRING, desc="英文全称"),
            ColumnInfo(name="cnspell", kind=DataKind.STRING, desc="拼音缩写"),
            ColumnInfo(name="market", kind=DataKind.STRING, desc="市场类型(主板/创业板/科创板/CDR)"),
            ColumnInfo(name="exchange", kind=DataKind.STRING, desc="交易所代码"),
            ColumnInfo(name="currency", kind=DataKind.STRING, desc="交易货币"),
            ColumnInfo(name="list_status", kind=DataKind.STRING, desc="上市状态 L上市 D退市 P暂停上市"),
            ColumnInfo(name="list_date", kind=DataKind.DATETIME, desc="上市日期"),
            ColumnInfo(name="delist_date", kind=DataKind.DATETIME, desc="退市日期"),
            ColumnInfo(name="is_hs", kind=DataKind.STRING, desc="是否沪深港通标"),
            ColumnInfo(name="ace_name", kind=DataKind.STRING, desc="实控人名称"),
            ColumnInfo(name="ace_type", kind=DataKind.STRING, desc="实控人企业性质"),
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
                url="http://tushare.pro/document/2?doc_id=25",
                name="stock_basic",
                args=self._ARGS,
                tableinfo=self._IN,
            ),
            output=Output(
                name="stock",
                tableinfo=self._OUT,
            ),
            retry=retry,
            tags={
                "name": "stock",
                "module": "stock",
                "level": "basic",
                "frequency": "interday",
                "scope": "stock_basic",
            },
        )

    @staticmethod
    def _resolve_conf(
        conf: Optional[Conf | Dict[str, Any]] = None,
    ) -> Conf:
        if conf is None:
            obj = Conf(size=4000)
        else:
            obj = Conf.from_dict(conf)

        if obj.size > 4000:
            obj.set_size(4000)

        return obj

    def _run(self) -> object:
        params = dict(self.conf.get_params() or {})
        fields = self.source.list_column_names()
        if "list_status" in params:
            df = self._fetchall(
                api=self.connection.stock_basic,
                **params,
                fields=",".join(fields),
            )
        else:
            batch: List[pd.DataFrame] = []
            for list_status in self._STATUSES:
                params["list_status"] = list_status
                df = self._fetchall(
                    api=self.connection.stock_basic,
                    **params,
                    fields=",".join(fields),
                )
                batch.append(df)
            df = pd.concat(batch, ignore_index=True)

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
        out["symbol"] = out["symbol"].astype(str)
        out["area"] = out["area"].astype(str)
        out["industry"] = out["industry"].astype(str)
        out["fullname"] = out["fullname"].astype(str)
        out["enname"] = out["enname"].astype(str)
        out["cnspell"] = out["cnspell"].astype(str)
        out["market"] = out["market"].astype(str)
        out["exchange"] = out["exchange"].astype(str)
        out["currency"] = out["curr_type"].astype(str)
        out["list_status"] = out["list_status"].astype(str)
        out["list_date"] = pd.to_datetime(
            out["list_date"],
            format="%Y%m%d",
            errors="coerce",
        )
        out["delist_date"] = pd.to_datetime(
            out["delist_date"],
            format="%Y%m%d",
            errors="coerce",
        )
        out["is_hs"] = out["is_hs"].astype(str)
        out["ace_name"] = out["act_name"].astype(str)
        out["ace_type"] = out["act_ent_type"].astype(str)
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
