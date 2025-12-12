from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Dict, Optional

from xfintech.fabric.datakind.datakind import DataKind


class ColumnInfo:
    """
    描述: 列字段信息。
    参数:
    - name: str, 列字段名称。
    - kind: DataKind | str, optional, 列字段数据类型。 默认为 DataKind.STRING。
    - desc: str, optional, 列字段描述信息。 默认为空字符串。
    - meta: Dict[str, Any], optional, 列字段元数据。 默认为空字典。

    例子:
    ```python
        from xfintech.fabric.datakind.datakind import DataKind

        f = ColumnInfo(
            name="price",
            kind="Float",
            desc="股票价格",
            meta={"unit": "CNY"},
        )

        f2 = ColumnInfo.from_dict({
            "name": "volume",
            "kind": "Integer",
            "desc": "交易量",
            "meta": {"unit": "shares"},
        })
    ```
    """

    _NAME_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    _DEFAULT_KIND = DataKind.STRING

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> ColumnInfo:
        return cls(
            name=data["name"],
            kind=data.get("kind"),
            desc=data.get("desc"),
            meta=data.get("meta"),
        )

    def __init__(
        self,
        name: str,
        kind: Optional[DataKind | str] = None,
        desc: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ):
        self.name = self._resolve_name(name)
        self.kind = self._resolve_kind(kind)
        self.desc = self._resolve_desc(desc)
        self.meta = self._resolve_meta(meta)

    @property
    def identifier(self) -> str:
        gen = {
            "name": self.name,
            "kind": str(self.kind),
            "desc": self.desc,
            "meta": self.meta,
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
        value: str,
    ) -> str:
        if not self._NAME_PATTERN.match(value):
            raise ValueError(f"Invalid field name: {value}")
        return value.lower()

    def _resolve_kind(
        self,
        value: Optional[DataKind | str],
    ) -> DataKind:
        if value is None:
            return self._DEFAULT_KIND
        if isinstance(value, DataKind):
            return value
        try:
            return DataKind.from_str(value)
        except ValueError:
            raise ValueError(f"Invalid field kind: {value!r}")

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

    def __str__(self) -> str:
        return f"{self.name}: {self.kind}"

    def __repr__(self) -> str:
        return self.to_dict().__repr__()

    def add_desc(self, desc: str) -> None:
        self.update(desc=desc)
        return self

    def add_meta(self, key: str, value: Any) -> None:
        self.meta[key] = value
        return self

    def add_kind(self, kind: DataKind | str) -> None:
        self.update(kind=kind)
        return self

    def update(
        self,
        name: Optional[str] = None,
        kind: Optional[DataKind | str] = None,
        desc: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        if name is not None:
            self.name = self._resolve_name(name)
        if kind is not None:
            self.kind = self._resolve_kind(kind)
        if desc is not None:
            self.desc = self._resolve_desc(desc)
        if meta is not None:
            self.meta.update(self._resolve_meta(meta))
        return self

    def describe(self) -> Dict[str, Any]:
        return self.to_dict()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "name": self.name,
            "kind": str(self.kind),
            "desc": self.desc,
            "meta": self.meta,
        }
