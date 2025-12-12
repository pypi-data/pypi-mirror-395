from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Optional

from xfintech.fabric.column.columninfo import ColumnInfo
from xfintech.fabric.table.tableinfo import TableInfo


class Output:
    """
    描述: 数据输出配置类 <br>

    参数:
    - name: str, 输出名称
    - tableinfo: TableInfo, 输出表信息

    例子:
    ```python
        output = Output(
            name="processed_data",
            tableinfo=TableInfo(
                desc="Processed data output",
                meta={"version": "1.0"},
                columns=[
                    ColumnInfo(name="id", kind=DataKind.INTEGER, desc="Record ID"),
                    ColumnInfo(name="value", kind=DataKind.FLOAT, desc="Value"),
                ],
            ),
        )
        print(output.describe())
    ```
    """

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "Output":
        return cls(
            name=data.get("name"),
            tableinfo=data.get("tableinfo"),
        )

    def __init__(
        self,
        name: str,
        tableinfo: Optional[TableInfo | Dict[str, Any]] = None,
    ) -> None:
        self.name = self._resolve_name(name)
        self.tableinfo = self._resolve_tableinfo(tableinfo)

    @property
    def identifier(self) -> str:
        gen = {
            "name": self.name,
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
            raise ValueError("Output name must be provided.")
        return name.strip().lower()

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
            "tableinfo": self.tableinfo.describe(),
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "name": self.name,
            "tableinfo": self.tableinfo.to_dict(),
        }
