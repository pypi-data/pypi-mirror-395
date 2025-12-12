from __future__ import annotations

from enum import Enum


class DataKind(str, Enum):
    INTEGER = "Integer"
    FLOAT = "Float"
    STRING = "String"
    BOOLEAN = "Boolean"
    DATETIME = "Datetime"
    CATEGORICAL = "Categorical"
    # Add more column types as needed
    UNKNOWN = "Unknown"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        return DataKind.UNKNOWN

    @classmethod
    def from_str(cls, string: str) -> DataKind:
        for dkind in DataKind:
            if dkind.value.lower() == string.lower():
                return dkind
        return DataKind.UNKNOWN

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.value.lower() == other.lower()
        return super().__eq__(other)

    def __ne__(self, value):
        return not self.__eq__(value)
