from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from ..fable_library.reflection import (TypeInfo, string_type, bool_type, obj_type, lambda_type, unit_type, record_type)
from ..fable_library.types import Record

def _expr0() -> TypeInfo:
    return record_type("DynamicObj.PropertyHelper", [], PropertyHelper, lambda: [("Name", string_type), ("IsStatic", bool_type), ("IsDynamic", bool_type), ("IsMutable", bool_type), ("IsImmutable", bool_type), ("GetValue", lambda_type(obj_type, obj_type)), ("SetValue", lambda_type(obj_type, lambda_type(obj_type, unit_type))), ("RemoveValue", lambda_type(obj_type, unit_type))])


@dataclass(eq = False, repr = False, slots = True)
class PropertyHelper(Record):
    Name: str
    IsStatic: bool
    IsDynamic: bool
    IsMutable: bool
    IsImmutable: bool
    GetValue: Callable[[Any], Any]
    SetValue: Callable[[Any, Any], None]
    RemoveValue: Callable[[Any], None]

PropertyHelper_reflection = _expr0

__all__ = ["PropertyHelper_reflection"]

