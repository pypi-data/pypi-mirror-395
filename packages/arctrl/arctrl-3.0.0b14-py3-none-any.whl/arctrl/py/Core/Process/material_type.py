from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.reflection import (TypeInfo, union_type)
from ...fable_modules.fable_library.types import (Array, Union)

def _expr752() -> TypeInfo:
    return union_type("ARCtrl.Process.MaterialType", [], MaterialType, lambda: [[], []])


class MaterialType(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["ExtractName", "LabeledExtractName"]


MaterialType_reflection = _expr752

def MaterialType_create_Z721C83C5(t: str) -> MaterialType:
    if t == "Extract Name":
        return MaterialType(0)

    elif t == "Labeled Extract Name":
        return MaterialType(1)

    else: 
        raise Exception("No other value than \"Extract Name\" or \"Labeled Extract Name\" allowed for materialtype")



def MaterialType__get_AsString(this: MaterialType) -> str:
    if this.tag == 1:
        return "Labeled Extract"

    else: 
        return "Extract"



__all__ = ["MaterialType_reflection", "MaterialType_create_Z721C83C5", "MaterialType__get_AsString"]

