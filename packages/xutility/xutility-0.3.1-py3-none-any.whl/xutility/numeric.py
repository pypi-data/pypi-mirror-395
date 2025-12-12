import decimal
from typing import Literal, Type

import numpy as np


class Cast:
    def __init__(
        self,
        v: decimal.Decimal | float | np.float64 | int | str | None,
        allow_none: bool = True,
    ) -> None:
        if v is None and allow_none == False:
            raise ValueError("Get None value but allow_none=False")
        self.orignal_v = v
        self._from_type = type(v)
        if self.orignal_v is not None and self._from_type not in [float, np.float64, decimal.Decimal, int, str]:
            raise TypeError(f"Unsupported input type {self._from_type}")

    @property
    def precision(self) -> int:
        tick: decimal.Decimal = self.to(to_type=decimal.Decimal, precision=None)  # type: ignore
        tick_str = str(tick)
        tick_str = tick_str if tick_str.find(".") == -1 else tick_str.rstrip("0")
        return -int(decimal.Decimal(tick_str).as_tuple().exponent)

    def set_precision(
        self,
        precision: int,
        rounding: Literal["ROUND_UP", "ROUND_DOWN", "ROUND_05UP"] = "ROUND_05UP",
    ) -> decimal.Decimal:
        intermediate_v = decimal.Decimal(str(self.orignal_v))
        exp = decimal.Decimal("1." + "0" * precision)
        if rounding == "ROUND_05UP":
            return intermediate_v.quantize(exp, rounding=decimal.ROUND_HALF_EVEN)
        elif rounding == "ROUND_UP":
            return intermediate_v.quantize(exp, rounding=decimal.ROUND_UP)
        elif rounding == "ROUND_DOWN":
            return intermediate_v.quantize(exp, rounding=decimal.ROUND_DOWN)

    def quantize(
        self,
        tick: decimal.Decimal | float,
        round_down: bool = False,
    ) -> decimal.Decimal | None:
        if self.orignal_v is None:
            return None
        elif not isinstance(self.orignal_v, decimal.Decimal):
            self.orignal_v = decimal.Decimal(self.orignal_v)

        _tick = decimal.Decimal(str(tick))
        return (
            _tick * int(self.orignal_v / _tick)
            if round_down or self.orignal_v % _tick == 0
            else _tick * (int(self.orignal_v / _tick) + 1)
        )

    def to(
        self,
        to_type: Type[float] | Type[np.float64] | Type[decimal.Decimal] | Type[int] | Type[str],
        precision: int | None = None,
        rounding: Literal["ROUND_UP", "ROUND_DOWN", "ROUND_05UP"] = "ROUND_05UP",
    ) -> float | decimal.Decimal | int | str | None:
        # sanity check
        assert rounding in ["ROUND_UP", "ROUND_DOWN", "ROUND_05UP"], "Invalid `rounding`"
        assert precision is None or precision >= 0, "Invalid `precision`"

        if self.orignal_v is None:
            return None

        if to_type is int:
            if self._from_type is int:
                return self.orignal_v
            else:
                return int(self.set_precision(0, rounding))
        elif to_type in [float, np.float64, decimal.Decimal, str]:
            if precision is None:
                if self._from_type == to_type:
                    return self.orignal_v
                else:
                    return to_type(str(self.orignal_v))
            else:
                return to_type(self.set_precision(precision, rounding))
        else:
            raise ValueError(f"Unsupported to_type {to_type}")
