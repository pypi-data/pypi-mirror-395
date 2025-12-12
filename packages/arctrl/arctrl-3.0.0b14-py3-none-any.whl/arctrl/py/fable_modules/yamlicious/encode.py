from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_library.date import to_string as to_string_1
from ..fable_library.list import (of_seq, map as map_1, of_array, FSharpList)
from ..fable_library.option import value as value_1
from ..fable_library.seq import map
from ..fable_library.types import (to_string, Array)
from ..fable_library.util import (int32_to_string, IEnumerable_1)
from .writer import write as write_1
from .yamlicious_types import (YAMLContent_create_27AED5E3, YAMLElement, Config)

_A = TypeVar("_A")

def int_1(value: int) -> YAMLElement:
    return YAMLElement(1, YAMLContent_create_27AED5E3(int32_to_string(value)))


def float_1(value: float) -> YAMLElement:
    return YAMLElement(1, YAMLContent_create_27AED5E3(str(value)))


def char(value: str) -> YAMLElement:
    return YAMLElement(1, YAMLContent_create_27AED5E3(value))


def bool_1(value: bool) -> YAMLElement:
    return YAMLElement(1, YAMLContent_create_27AED5E3(to_string(value)))


def datetime(value: Any) -> YAMLElement:
    return YAMLElement(1, YAMLContent_create_27AED5E3(to_string_1(value, "O", {})))


def datetime_offset(value: Any) -> YAMLElement:
    return YAMLElement(1, YAMLContent_create_27AED5E3(to_string_1(value, "O", {})))


def string(value: str) -> YAMLElement:
    return YAMLElement(1, YAMLContent_create_27AED5E3(value))


def seq(encoder: Callable[[_A], YAMLElement], s: IEnumerable_1[Any]) -> YAMLElement:
    return YAMLElement(2, of_seq(map(encoder, s)))


def array(encoder: Callable[[_A], YAMLElement], arr: Array[Any]) -> YAMLElement:
    return YAMLElement(2, map_1(encoder, of_array(arr)))


def resizearray(encoder: Callable[[_A], YAMLElement], arr: Array[Any]) -> YAMLElement:
    return YAMLElement(2, map_1(encoder, of_seq(arr)))


def list_1(encoder: Callable[[_A], YAMLElement], l: FSharpList[Any]) -> YAMLElement:
    return YAMLElement(2, map_1(encoder, l))


def values(encoder: Callable[[_A], str], values_1: IEnumerable_1[Any]) -> YAMLElement:
    def mapping(arg_1: _A | None=None, encoder: Any=encoder, values_1: Any=values_1) -> YAMLElement:
        return YAMLElement(1, YAMLContent_create_27AED5E3(encoder(arg_1)))

    return YAMLElement(3, of_seq(map(mapping, values_1)))


def comment(string_1: str) -> YAMLElement:
    return YAMLElement(4, string_1)


nil: YAMLElement = YAMLElement(5)

def try_include(name: str, encoder: Callable[[_A], YAMLElement], value: Any | None=None) -> tuple[str, YAMLElement]:
    return (name, encoder(value_1(value)) if (value is not None) else nil)


def write(whitespaces: int, ele: YAMLElement) -> str:
    def _arrow379(c: Config, whitespaces: Any=whitespaces, ele: Any=ele) -> Config:
        return Config(whitespaces, c.Level)

    return write_1(ele, _arrow379)


__all__ = ["int_1", "float_1", "char", "bool_1", "datetime", "datetime_offset", "string", "seq", "array", "resizearray", "list_1", "values", "comment", "nil", "try_include", "write"]

