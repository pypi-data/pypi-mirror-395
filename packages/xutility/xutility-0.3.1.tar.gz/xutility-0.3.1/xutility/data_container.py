from dataclasses import asdict, is_dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, ParamSpec

P = ParamSpec("P")


class EasyDumpClass:
    def _to_json_compatible(self, v: Any) -> Any:
        if v is None:
            return None
        elif isinstance(v, EasyDumpClass):
            return v.to_dict()
        elif isinstance(v, Enum):
            return v.name
        elif isinstance(v, datetime):
            return v.isoformat()
        elif isinstance(v, Decimal):
            return str(v)
        elif isinstance(v, list):
            return [self._to_json_compatible(vv) for vv in v]
        elif isinstance(v, tuple):
            return (self._to_json_compatible(vv) for vv in v)
        elif isinstance(v, (int, float, str, bool)):
            return v
        else:
            return str(v)

    def to_dict(self) -> Dict[str, Any]:
        """Can be overridden

        CAVEAT:
            Must deal with decimal properly
        """
        if is_dataclass(self):
            return {_k: self._to_json_compatible(_v) for _k, _v in asdict(self).items()}
        else:
            raise NotImplementedError


class StrEnum(Enum):
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
