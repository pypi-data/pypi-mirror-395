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


class Company(Job):
    """
    描述: 获取上市公司基础信息, 单次提取4500条, 可以根据交易所分批提取 <br>
    积分: 用户需要至少120积分才可以调取 <br>

    参数:
    - conf: Conf | Dict[str, Any], 可选, 作业配置, 其中params支持以下参数:
        - params: 非必需, 请求参数字典
            - ts_code: str, 非必需, TS股票代码
            - exchange: str, 非必需, 交易所, SSE上交所, SZSE深交所, BSE北交所
        - limit: 非必需, 最大迭代次数, 默认为10000
        - size: 非必需, 每次提取数据量, 应小于4000
        - coolant: 非必需, 请求间隔时间(秒), 默认为0
    - retry: Retry, 可选, 重试配置

    例子:
    ```python
        company_profile_job = Company(
            session=session,
        )
        result = company_profile_job.run()
        print(result)  # Display the fetched company profile data
    ```
    """

    _EXCHANGES = ["SSE", "SZSE", "BSE"]
    _ARGS = {
        "ts_code": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": "TS股票代码",
        },
        "exchange": {
            "type": DataKind.STRING,
            "required": "N",
            "desc": f"交易所{_EXCHANGES}",
        },
    }
    _IN = TableInfo(
        desc="上市公司基本信息",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="ts_code", kind=DataKind.STRING, desc="TS股票代码"),
            ColumnInfo(name="com_name", kind=DataKind.STRING, desc="公司全称"),
            ColumnInfo(name="com_id", kind=DataKind.STRING, desc="统一社会信用代码"),
            ColumnInfo(name="exchange", kind=DataKind.STRING, desc="交易所"),
            ColumnInfo(name="short_name", kind=DataKind.STRING, desc="公司简称"),
            ColumnInfo(name="chairman", kind=DataKind.STRING, desc="法人代表"),
            ColumnInfo(name="manager", kind=DataKind.STRING, desc="总经理"),
            ColumnInfo(name="secretary", kind=DataKind.STRING, desc="董秘"),
            ColumnInfo(name="reg_capital", kind=DataKind.FLOAT, desc="注册资本(万元)"),
            ColumnInfo(name="setup_date", kind=DataKind.STRING, desc="注册日期"),
            ColumnInfo(name="province", kind=DataKind.STRING, desc="所在省份"),
            ColumnInfo(name="city", kind=DataKind.STRING, desc="所在城市"),
            ColumnInfo(name="introduction", kind=DataKind.STRING, desc="公司介绍"),
            ColumnInfo(name="website", kind=DataKind.STRING, desc="公司主页"),
            ColumnInfo(name="email", kind=DataKind.STRING, desc="电子邮件"),
            ColumnInfo(name="office", kind=DataKind.STRING, desc="办公室"),
            ColumnInfo(name="employees", kind=DataKind.INTEGER, desc="员工人数"),
            ColumnInfo(name="main_business", kind=DataKind.STRING, desc="主要业务及产品"),
            ColumnInfo(name="business_scope", kind=DataKind.STRING, desc="经营范围"),
        ],
    )
    _OUT = TableInfo(
        desc="上市公司基本信息",
        meta={"source": "tushare"},
        columns=[
            ColumnInfo(name="stockcode", kind=DataKind.STRING, desc="TS股票代码"),
            ColumnInfo(name="company_name", kind=DataKind.STRING, desc="公司全称"),
            ColumnInfo(name="company_id", kind=DataKind.STRING, desc="统一社会信用代码"),
            ColumnInfo(name="exchange", kind=DataKind.STRING, desc="交易所"),
            ColumnInfo(name="chairman", kind=DataKind.STRING, desc="法人代表"),
            ColumnInfo(name="manager", kind=DataKind.STRING, desc="总经理"),
            ColumnInfo(name="secretary", kind=DataKind.STRING, desc="董秘"),
            ColumnInfo(name="reg_capital", kind=DataKind.FLOAT, desc="注册资本(万元)"),
            ColumnInfo(name="setup_date", kind=DataKind.DATETIME, desc="注册日期"),
            ColumnInfo(name="province", kind=DataKind.STRING, desc="所在省份"),
            ColumnInfo(name="city", kind=DataKind.STRING, desc="所在城市"),
            ColumnInfo(name="introduction", kind=DataKind.STRING, desc="公司介绍"),
            ColumnInfo(name="website", kind=DataKind.STRING, desc="公司主页"),
            ColumnInfo(name="email", kind=DataKind.STRING, desc="电子邮件"),
            ColumnInfo(name="office", kind=DataKind.STRING, desc="办公室"),
            ColumnInfo(name="employees", kind=DataKind.INTEGER, desc="员工人数"),
            ColumnInfo(name="main_business", kind=DataKind.STRING, desc="主要业务及产品"),
            ColumnInfo(name="business_scope", kind=DataKind.STRING, desc="经营范围"),
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
                url="http://tushare.pro/document/2?doc_id=112",
                name="stock_company",
                args=self._ARGS,
                tableinfo=self._IN,
            ),
            output=Output(
                name="company",
                tableinfo=self._OUT,
            ),
            retry=retry,
            tags={
                "name": "company",
                "module": "stock",
                "level": "basic",
                "frequency": "interday",
                "scope": "stock_company",
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
        if "exchange" in params:
            df = self._fetchall(
                api=self.connection.stock_company,
                **params,
                fields=",".join(fields),
            )
        else:
            batch: List[pd.DataFrame] = []
            for exchange in self._EXCHANGES:
                params["exchange"] = exchange
                df = self._fetchall(
                    api=self.connection.stock_company,
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
        out["stockcode"] = out["ts_code"].astype(str)
        out["company_name"] = out["com_name"].astype(str)
        out["company_id"] = out["com_id"].astype(str)
        out["exchange"] = out["exchange"].astype(str)
        out["chairman"] = out["chairman"].astype(str)
        out["manager"] = out["manager"].astype(str)
        out["secretary"] = out["secretary"].astype(str)
        out["reg_capital"] = pd.to_numeric(out["reg_capital"], errors="coerce")
        out["setup_date"] = pd.to_datetime(
            out["setup_date"],
            format="%Y%m%d",
            errors="coerce",
        )
        out["province"] = out["province"].astype(str)
        out["city"] = out["city"].astype(str)
        out["introduction"] = out["introduction"].astype(str)
        out["website"] = out["website"].astype(str)
        out["email"] = out["email"].astype(str)
        out["office"] = out["office"].astype(str)
        out["employees"] = pd.to_numeric(out["employees"], errors="coerce").astype("Int64")
        out["main_business"] = out["main_business"].astype(str)
        out["business_scope"] = out["business_scope"].astype(str)
        out = out[cols].drop_duplicates()
        return out.sort_values("stockcode").reset_index(drop=True)

    def list_codes(self) -> List[str]:
        if "_run" not in self.cache:
            df = self.run()
        else:
            df = self.cache.get("_run")
        result = df["stockcode"].unique().tolist()
        if self.conf.use_cache:
            self.cache.set("list_codes", result)
        return result

    def list_names(self) -> List[str]:
        if "_run" not in self.cache:
            df = self.run()
        else:
            df = self.cache.get("_run")
        result = df["company_name"].unique().tolist()
        result.sort()
        if self.conf.use_cache:
            self.cache.set("list_names", result)
        return result
