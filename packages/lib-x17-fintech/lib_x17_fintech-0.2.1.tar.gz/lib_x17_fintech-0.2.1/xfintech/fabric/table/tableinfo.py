from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Optional

from xfintech.fabric.column.columninfo import ColumnInfo
from xfintech.fabric.datakind.datakind import DataKind


class TableInfo:
    """
    描述: 表信息。
    参数:
    - desc: str, optional, 表描述信息。 默认为空字符串。
    - meta: Dict[str, Any], optional, 表元数据。 默认为空字典。
    - columns: List[ColumnInfo], optional, 列字段信息列表。 默认为空。

    例子:
    ```python
        from xfintech.fabric.table.tableinfo import TableInfo
        from xfintech.fabric.column.columninfo import ColumnInfo
        from xfintech.fabric.datakind.datakind import DataKind

        table = TableInfo(
            desc="日线行情表",
            meta={"source": "tushare"},
            columns=[
                ColumnInfo(name="price", kind="Float", desc="收盘价"),
                ColumnInfo(name="volume", kind=DataKind.INTEGER, desc="成交量"),
            ],
        )
        print(table.describe())
    ```
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TableInfo":
        return cls(
            desc=data.get("desc"),
            meta=data.get("meta"),
            columns=data.get("columns"),
        )

    def __init__(
        self,
        desc: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
        columns: Optional[List[ColumnInfo | Dict[str, Any]]] = None,
    ):
        self.desc = self._resolve_desc(desc)
        self.meta = self._resolve_meta(meta)
        self.columns = self._resolve_columns(columns)

    @property
    def identifier(self) -> str:
        gen = {
            "desc": self.desc,
            "meta": self.meta,
            "columns": [c.to_dict() for c in self.list_columns()],
        }
        dna = json.dumps(
            gen,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        return hashlib.sha256(dna.encode("utf-8")).hexdigest()

    def _resolve_desc(
        self,
        value: Optional[str],
    ) -> Optional[str]:
        if value is None:
            return ""
        else:
            return value.strip()

    def _resolve_meta(
        self,
        meta: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        if meta is None:
            return {}
        resolved: Dict[str, Any] = {}
        for k, v in meta.items():
            if isinstance(v, bytes):
                v = v.decode("utf8")
            if isinstance(k, bytes):
                k = k.decode("utf8")
            resolved[k] = v
        return resolved

    def _resolve_columns(
        self,
        columns: Optional[List[ColumnInfo | Dict[str, Any]]],
    ) -> Dict[str, ColumnInfo]:
        if columns is None:
            return {}

        resolved: Dict[str, ColumnInfo] = {}
        for item in columns:
            if isinstance(item, ColumnInfo):
                resolved[item.name] = item
            elif isinstance(item, dict):
                col = ColumnInfo.from_dict(item)
                resolved[col.name] = col
            else:
                raise TypeError(f"Invalid column type: {type(item)}")
        return resolved

    def __str__(self) -> str:
        return self.columns.__str__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(identifier={self.identifier})"

    def get_column(
        self,
        name: str,
    ) -> Optional[ColumnInfo]:
        return self.columns.get(name.lower())

    def remove_column(
        self,
        name: str,
    ) -> None:
        key = name.lower()
        if key in self.columns:
            del self.columns[key]
        return self

    def add_column(
        self,
        column: ColumnInfo | Dict[str, Any],
    ) -> None:
        if isinstance(column, dict):
            column = ColumnInfo.from_dict(column)
        self.columns[column.name] = column
        return self

    def update_column(
        self,
        name: str,
        new: Optional[str] = None,
        kind: Optional[DataKind | str] = None,
        desc: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        oldkey = name.lower()
        if oldkey in self.columns:
            self.columns[oldkey].update(
                kind=kind,
                desc=desc,
                meta=meta,
            )
            if new is not None:
                self.rename_column(
                    old=name,
                    new=new,
                )
        return self

    def rename_column(
        self,
        old: str,
        new: str,
    ) -> None:
        oldkey = old.lower()
        newkey = new.lower()
        if oldkey in self.columns:
            self.columns[oldkey].update(name=new)
            self.columns[newkey] = self.columns[oldkey]
            del self.columns[oldkey]
        return self

    def list_columns(self) -> List[ColumnInfo]:
        return list(self.columns.values())

    def describe(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "desc": self.desc,
            "meta": self.meta,
            "columns": [c.describe() for c in self.list_columns()],
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "desc": self.desc,
            "meta": self.meta,
            "columns": [c.to_dict() for c in self.list_columns()],
        }
