from __future__ import annotations
from abc import abstractmethod
from typing import (Protocol, Generic, Any, TypeVar)
from ..fable_library.list import FSharpList
from ..fable_library.reflection import (TypeInfo, string_type, tuple_type, list_type, union_type, char_type, float64_type, bool_type, class_type, array_type, uint32_type)
from ..fable_library.result import FSharpResult_2
from ..fable_library.types import (Array, float32, uint32, Union)
from ..fable_library.util import IEnumerable_1

_JSONVALUE = TypeVar("_JSONVALUE")

_T = TypeVar("_T")

class IDecoderHelpers_1(Protocol, Generic[_JSONVALUE]):
    @abstractmethod
    def any_to_string(self, __arg0: _JSONVALUE) -> str:
        ...

    @abstractmethod
    def as_array(self, __arg0: _JSONVALUE) -> Array[_JSONVALUE]:
        ...

    @abstractmethod
    def as_boolean(self, __arg0: _JSONVALUE) -> bool:
        ...

    @abstractmethod
    def as_float(self, __arg0: _JSONVALUE) -> float:
        ...

    @abstractmethod
    def as_float32(self, __arg0: _JSONVALUE) -> float32:
        ...

    @abstractmethod
    def as_int(self, __arg0: _JSONVALUE) -> int:
        ...

    @abstractmethod
    def as_string(self, __arg0: _JSONVALUE) -> str:
        ...

    @abstractmethod
    def get_properties(self, __arg0: _JSONVALUE) -> IEnumerable_1[str]:
        ...

    @abstractmethod
    def get_property(self, __arg0: str, __arg1: _JSONVALUE) -> _JSONVALUE:
        ...

    @abstractmethod
    def has_property(self, __arg0: str, __arg1: _JSONVALUE) -> bool:
        ...

    @abstractmethod
    def is_array(self, __arg0: _JSONVALUE) -> bool:
        ...

    @abstractmethod
    def is_boolean(self, __arg0: _JSONVALUE) -> bool:
        ...

    @abstractmethod
    def is_integral_value(self, __arg0: _JSONVALUE) -> bool:
        ...

    @abstractmethod
    def is_null_value(self, __arg0: _JSONVALUE) -> bool:
        ...

    @abstractmethod
    def is_number(self, __arg0: _JSONVALUE) -> bool:
        ...

    @abstractmethod
    def is_object(self, __arg0: _JSONVALUE) -> bool:
        ...

    @abstractmethod
    def is_string(self, __arg0: _JSONVALUE) -> bool:
        ...


class IEncoderHelpers_1(Protocol, Generic[_JSONVALUE]):
    @abstractmethod
    def encode_array(self, __arg0: Array[_JSONVALUE]) -> _JSONVALUE:
        ...

    @abstractmethod
    def encode_bool(self, __arg0: bool) -> _JSONVALUE:
        ...

    @abstractmethod
    def encode_char(self, __arg0: str) -> _JSONVALUE:
        ...

    @abstractmethod
    def encode_decimal_number(self, __arg0: float) -> _JSONVALUE:
        ...

    @abstractmethod
    def encode_list(self, __arg0: FSharpList[_JSONVALUE]) -> _JSONVALUE:
        ...

    @abstractmethod
    def encode_null(self) -> _JSONVALUE:
        ...

    @abstractmethod
    def encode_object(self, __arg0: IEnumerable_1[tuple[str, _JSONVALUE]]) -> _JSONVALUE:
        ...

    @abstractmethod
    def encode_resize_array(self, __arg0: Array[_JSONVALUE]) -> _JSONVALUE:
        ...

    @abstractmethod
    def encode_seq(self, __arg0: IEnumerable_1[_JSONVALUE]) -> _JSONVALUE:
        ...

    @abstractmethod
    def encode_signed_integral_number(self, __arg0: int) -> _JSONVALUE:
        ...

    @abstractmethod
    def encode_string(self, __arg0: str) -> _JSONVALUE:
        ...

    @abstractmethod
    def encode_unsigned_integral_number(self, __arg0: uint32) -> _JSONVALUE:
        ...


def _expr40(gen0: TypeInfo) -> TypeInfo:
    return union_type("Thoth.Json.Core.ErrorReason`1", [gen0], ErrorReason_1, lambda: [[("Item1", string_type), ("Item2", gen0)], [("Item1", string_type), ("Item2", gen0), ("Item3", string_type)], [("Item1", string_type), ("Item2", gen0)], [("Item1", string_type), ("Item2", gen0)], [("Item1", string_type), ("Item2", gen0), ("Item3", string_type)], [("Item1", string_type), ("Item2", gen0)], [("Item", string_type)], [("Item", list_type(tuple_type(string_type, ErrorReason_1_reflection(gen0))))]])


class ErrorReason_1(Union, Generic[_JSONVALUE]):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["BadPrimitive", "BadPrimitiveExtra", "BadType", "BadField", "BadPath", "TooSmallArray", "FailMessage", "BadOneOf"]


ErrorReason_1_reflection = _expr40

class Decoder_1(Protocol, Generic[_T]):
    @abstractmethod
    def Decode(self, helpers: IDecoderHelpers_1[_JSONVALUE], value: _JSONVALUE) -> FSharpResult_2[_T, tuple[str, ErrorReason_1[_JSONVALUE]]]:
        ...


def _expr41() -> TypeInfo:
    return union_type("Thoth.Json.Core.Json", [], Json, lambda: [[("Item", string_type)], [("Item", char_type)], [("Item", float64_type)], [], [("Item", bool_type)], [("Item", class_type("System.Collections.Generic.IEnumerable`1", [tuple_type(string_type, Json_reflection())]))], [("Item", array_type(Json_reflection()))], [("Item", uint32_type)], []])


class Json(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["String", "Char", "DecimalNumber", "Null", "Boolean", "Object", "Array", "IntegralNumber", "Unit"]


Json_reflection = _expr41

class IEncodable(Protocol):
    @abstractmethod
    def Encode(self, helpers: IEncoderHelpers_1[_JSONVALUE]) -> _JSONVALUE:
        ...


__all__ = ["ErrorReason_1_reflection", "Json_reflection"]

