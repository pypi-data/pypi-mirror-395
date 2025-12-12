from __future__ import annotations
from abc import abstractmethod
from datetime import datetime
from typing import (Any, Protocol)
from ...fable_library.date import (to_universal_time, to_string)
from ...fable_library.list import of_array
from ...thoth_json_core.decode import (map, datetime_local, one_of, bool_1, int_1, float_1, string)
from ...thoth_json_core.types import (Decoder_1, IEncodable, IEncoderHelpers_1)
from ..Cells.fs_cell import DataType

class DateTimeStatic(Protocol):
    @abstractmethod
    def from_time_stamp(self, timestamp: float) -> Any:
        ...


def PyTime_toUniversalTimePy(dt: Any) -> Any:
    timestamp: float = to_universal_time(dt).timestamp()
    return datetime.fromtimestamp(timestamp=timestamp)


Decode_datetime: Decoder_1[Any] = map(PyTime_toUniversalTimePy, datetime_local)

def encode(value: Any=None) -> IEncodable:
    if str(type(value)) == "<class \'str\'>":
        class ObjectExpr291(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr291()

    elif str(type(value)) == "<class \'float\'>":
        class ObjectExpr292(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers_1.encode_decimal_number(value)

        return ObjectExpr292()

    elif str(type(value)) == "<class \'int\'>":
        class ObjectExpr293(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers_2.encode_signed_integral_number(value)

        return ObjectExpr293()

    elif str(type(value)) == "<class \'bool\'>":
        class ObjectExpr294(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers_3.encode_bool(value)

        return ObjectExpr294()

    elif isinstance(value, datetime):
        value_5: str = to_string(value, "O", {}).split("+")[0]
        class ObjectExpr295(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers_4.encode_string(value_5)

        return ObjectExpr295()

    else: 
        class ObjectExpr296(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers_5.encode_null()

        return ObjectExpr296()



def ctor(b: bool) -> tuple[Any, DataType]:
    return (b, DataType(1))


def ctor_1(i: int) -> tuple[Any, DataType]:
    return (i, DataType(2))


def ctor_2(f: float) -> tuple[Any, DataType]:
    return (f, DataType(2))


def ctor_3(d_3: Any) -> tuple[Any, DataType]:
    return (d_3, DataType(3))


def ctor_4(s: str) -> tuple[Any, DataType]:
    return (s, DataType(0))


decode: Decoder_1[tuple[Any, DataType]] = one_of(of_array([map(ctor, bool_1), map(ctor_1, int_1), map(ctor_2, float_1), map(ctor_3, Decode_datetime), map(ctor_4, string)]))

__all__ = ["PyTime_toUniversalTimePy", "Decode_datetime", "encode", "decode"]

