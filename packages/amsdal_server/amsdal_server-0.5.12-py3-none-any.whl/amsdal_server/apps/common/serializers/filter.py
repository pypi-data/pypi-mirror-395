from enum import Enum
from enum import auto
from typing import Any

from pydantic import BaseModel


# TODO: Extend to support IN, case-sensitive
class FilterType(Enum):
    eq = auto()
    neq = auto()
    gt = auto()
    gte = auto()
    lt = auto()
    lte = auto()
    contains = auto()
    icontains = auto()
    startswith = auto()
    istartswith = auto()
    endswith = auto()
    iendswith = auto()


class Filter(BaseModel):
    key: str
    filter_type: FilterType
    target: Any

    def __str__(self) -> str:
        return f"Filter('{self.key}' {self.filter_type.name} '{self.target}')"

    def __repr__(self) -> str:
        return str(self)
