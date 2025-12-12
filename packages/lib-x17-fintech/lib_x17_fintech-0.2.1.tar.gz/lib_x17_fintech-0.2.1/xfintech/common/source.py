from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Optional

from xfintech.fabric.column.columninfo import ColumnInfo
from xfintech.fabric.table.tableinfo import TableInfo


class Source:
    """
    描述: 数据源配置类 <br>

    参数:
    - name: str, 数据源名称
    - url: str, 数据源URL地址
    - args: Dict[str, Any], 数据源参数说明
    - tableinfo: TableInfo, 数据源表信息

    例子:
    ```python
        source = Source(
            name="tushare_market_dayline",
            url="https://api.tushare.pro",
            args={
                "ts_code": "000001.SZ",
                "trade_date": "20241101",
            },
            tableinfo=TableInfo(
                desc="股票日线行情数据",
                meta={"source": "tushare"},
                columns=[
                    ColumnInfo(name="open", kind="Float", desc="开盘价"),
                    ColumnInfo(name="close", kind="Float", desc="收盘价"),
                ],
            ),
        )
        print(source.describe())
    ```
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Source":
        if isinstance(data, Source):
            return data
        return cls(
            name=data.get("name"),
            url=data.get("url"),
            args=data.get("args"),
            tableinfo=data.get("tableinfo"),
        )

    def __init__(
        self,
        name: str,
        url: Optional[str] = None,
        args: Optional[Dict[str, Any]] = None,
        tableinfo: Optional[TableInfo | Dict[str, Any]] = None,
    ) -> None:
        self.name = self._resolve_name(name)
        self.url = url or ""
        self.args = self._resolve_args(args)
        self.tableinfo = self._resolve_tableinfo(tableinfo)

    @property
    def identifier(self) -> str:
        arggen = {str(k): str(v) for k, v in sorted(self.args.items())}
        gen = {
            "name": self.name,
            "url": self.url,
            "args": arggen,
            "tableinfo": self.tableinfo.to_dict(),
        }
        dna = json.dumps(
            gen,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        return hashlib.sha256(dna.encode("utf-8")).hexdigest()

    def _resolve_name(
        self,
        name: Optional[str],
    ) -> str:
        if not name:
            raise ValueError("Source name must be provided.")
        return name.strip().lower()

    def _resolve_args(
        self,
        args: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        return args.copy() if args else {}

    def _resolve_tableinfo(
        self,
        tableinfo: Optional[TableInfo | Dict[str, Any]],
    ) -> TableInfo:
        if isinstance(tableinfo, TableInfo):
            return tableinfo
        elif isinstance(tableinfo, dict):
            return TableInfo.from_dict(tableinfo)
        else:
            return TableInfo()

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    def list_columns(self) -> List[ColumnInfo]:
        return self.tableinfo.list_columns()

    def list_column_names(self) -> List[str]:
        return [col.name for col in self.list_columns()]

    def describe(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "name": self.name,
            "url": self.url,
            "args": self.args,
            "tableinfo": self.tableinfo.describe(),
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "name": self.name,
            "url": self.url,
            "args": self.args,
            "tableinfo": self.tableinfo.to_dict(),
        }
