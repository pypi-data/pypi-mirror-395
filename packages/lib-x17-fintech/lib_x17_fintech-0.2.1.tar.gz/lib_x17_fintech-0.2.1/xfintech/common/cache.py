from __future__ import annotations

import hashlib
import pickle
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional


class Cache:
    """
    描述: 文件缓存，用于避免重复的 API 调用。 <br>
    参数:
    - name: str, 可选, 缓存的名称，默认使用随机生成的 UUID 作为名称。
    - parent: str | Path, 可选, 缓存的父目录路径，默认使用 /tmp/xfintech/cache 目录。

    例子:
    ```python
        cache = Cache(name="my-cache")
        cache.set("my-key", {"data": 123})
        value = cache.get("my-key")
        print(value)  # 输出: {'data': 123}
    ```
    """

    def __init__(
        self,
        name: Optional[str] = None,
        parent: Optional[str | Path] = None,
    ) -> None:
        self.name = self._resolve_name(name)
        self.parent = self._resolve_parent(parent)
        self.path = self.parent / self.name
        self.ensure_path()

    def _resolve_name(
        self,
        name: str | None,
    ) -> str:
        if name is not None:
            return name
        else:
            return uuid.uuid4().hex[0:8]

    def _resolve_parent(
        self,
        parent_path: str | Path | None,
    ) -> Path:
        if parent_path is not None:
            return Path(parent_path)
        else:
            return Path("/tmp/xfintech/cache")

    def _resolve_unitpath(self, key: str) -> Path:
        hashed = hashlib.md5(key.encode("utf-8")).hexdigest()
        return self.path / f"{hashed}.pkl"

    def __contains__(self, key: str) -> bool:
        unitpath = self._resolve_unitpath(key)
        return unitpath.exists()

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, path={self.path})"

    def ensure_path(self) -> None:
        if not self.path.exists():
            self.path.mkdir(parents=True, exist_ok=True)

    def get(
        self,
        key: str,
    ) -> Any | None:
        unitpath = self._resolve_unitpath(key)
        if not unitpath.exists():
            return None

        try:
            with unitpath.open("rb") as f:
                payload = pickle.load(f)
                value = payload.get("value")
            return value
        except Exception:
            return None

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        unitpath = self._resolve_unitpath(key)
        payload = {"value": value}
        with unitpath.open("wb") as f:
            pickle.dump(payload, f)

    def list(
        self,
    ) -> List[str]:
        keys = []
        for file in self.path.glob("*.pkl"):
            keys.append(file.stem)
        return keys

    def clear(self) -> None:
        for file in self.path.glob("*.pkl"):
            try:
                file.unlink()
            except Exception:
                pass

    def describe(
        self,
    ) -> Dict[str, Any]:
        return self.to_dict()

    def to_dict(
        self,
    ) -> Dict[str, Any]:
        return {
            "name": self.name,
            "path": str(self.path),
            "parent": str(self.parent),
            "units": self.list(),
        }
