from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import safe_hash
from .cwltypes import CWLType
from .hash_helpers import (box_hash_array, box_hash_seq, hash_1, box_hash_option)

def _expr516() -> TypeInfo:
    return class_type("ARCtrl.CWL.CWLParameterReference", None, CWLParameterReference)


class CWLParameterReference:
    def __init__(self, key: str, values: Array[str] | None=None, type_: CWLType | None=None) -> None:
        self._key: str = key
        self._values: Array[str] = default_arg(values, [])
        self._type: CWLType | None = type_

    @property
    def Key(self, __unit: None=None) -> str:
        this: CWLParameterReference = self
        return this._key

    @Key.setter
    def Key(self, value: str) -> None:
        this: CWLParameterReference = self
        this._key = value

    @property
    def Values(self, __unit: None=None) -> Array[str]:
        this: CWLParameterReference = self
        return this._values

    @Values.setter
    def Values(self, value: Array[str]) -> None:
        this: CWLParameterReference = self
        this._values = value

    @property
    def Type(self, __unit: None=None) -> CWLType | None:
        this: CWLParameterReference = self
        return this._type

    @Type.setter
    def Type(self, value: CWLType | None=None) -> None:
        this: CWLParameterReference = self
        this._type = value

    def __hash__(self, __unit: None=None) -> Any:
        this: CWLParameterReference = self
        return box_hash_array([box_hash_seq(this.Values), hash_1(this.Key), box_hash_option(this.Type)])

    def __eq__(self, obj: Any=None) -> bool:
        this: CWLParameterReference = self
        return this.StructurallyEquals(obj)

    def StructurallyEquals(self, other: CWLParameterReference) -> bool:
        this: CWLParameterReference = self
        return safe_hash(this) == safe_hash(other)

    def ReferenceEquals(self, other: CWLParameterReference) -> bool:
        this: CWLParameterReference = self
        return this is other


CWLParameterReference_reflection = _expr516

def CWLParameterReference__ctor_Z6E62A082(key: str, values: Array[str] | None=None, type_: CWLType | None=None) -> CWLParameterReference:
    return CWLParameterReference(key, values, type_)


__all__ = ["CWLParameterReference_reflection"]

