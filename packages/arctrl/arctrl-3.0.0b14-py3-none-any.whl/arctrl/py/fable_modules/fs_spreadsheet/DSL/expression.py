from __future__ import annotations
from typing import (Any, Generic, TypeVar)
from ...fable_library.reflection import (TypeInfo, class_type)

_T = TypeVar("_T")

def _expr237(gen0: TypeInfo) -> TypeInfo:
    return class_type("FsSpreadsheet.DSL.Expression.OptionalSource`1", [gen0], OptionalSource_1)


class OptionalSource_1(Generic[_T]):
    def __init__(self, s: Any | None=None) -> None:
        self.s: _T = s


OptionalSource_1_reflection = _expr237

def OptionalSource_1__ctor_2B595(s: Any | None=None) -> OptionalSource_1[_T]:
    return OptionalSource_1(s)


def OptionalSource_1__get_Source(this: OptionalSource_1[Any]) -> Any:
    return this.s


def _expr238(gen0: TypeInfo) -> TypeInfo:
    return class_type("FsSpreadsheet.DSL.Expression.RequiredSource`1", [gen0], RequiredSource_1)


class RequiredSource_1(Generic[_T]):
    def __init__(self, s: Any | None=None) -> None:
        self.s: _T = s


RequiredSource_1_reflection = _expr238

def RequiredSource_1__ctor_2B595(s: Any | None=None) -> RequiredSource_1[_T]:
    return RequiredSource_1(s)


def RequiredSource_1__get_Source(this: RequiredSource_1[Any]) -> Any:
    return this.s


def _expr239(gen0: TypeInfo) -> TypeInfo:
    return class_type("FsSpreadsheet.DSL.Expression.ExpressionSource`1", [gen0], ExpressionSource_1)


class ExpressionSource_1(Generic[_T]):
    def __init__(self, s: Any | None=None) -> None:
        self.s: _T = s


ExpressionSource_1_reflection = _expr239

def ExpressionSource_1__ctor_2B595(s: Any | None=None) -> ExpressionSource_1[_T]:
    return ExpressionSource_1(s)


def ExpressionSource_1__get_Source(this: ExpressionSource_1[Any]) -> Any:
    return this.s


__all__ = ["OptionalSource_1_reflection", "OptionalSource_1__get_Source", "RequiredSource_1_reflection", "RequiredSource_1__get_Source", "ExpressionSource_1_reflection", "ExpressionSource_1__get_Source"]

