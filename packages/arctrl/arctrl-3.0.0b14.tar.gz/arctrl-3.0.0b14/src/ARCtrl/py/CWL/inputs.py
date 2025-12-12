from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from ..fable_modules.dynamic_obj.dynamic_obj import (DynamicObj, DynamicObj_reflection)
from ..fable_modules.dynamic_obj.dyn_obj import set_optional_property
from ..fable_modules.fable_library.option import value
from ..fable_modules.fable_library.reflection import (TypeInfo, string_type, option_type, int32_type, bool_type, record_type, class_type)
from ..fable_modules.fable_library.types import (Record, FSharpRef)
from .cwltypes import CWLType

def _expr511() -> TypeInfo:
    return record_type("ARCtrl.CWL.InputBinding", [], InputBinding, lambda: [("Prefix", option_type(string_type)), ("Position", option_type(int32_type)), ("ItemSeparator", option_type(string_type)), ("Separate", option_type(bool_type))])


@dataclass(eq = False, repr = False, slots = True)
class InputBinding(Record):
    Prefix: str | None
    Position: int | None
    ItemSeparator: str | None
    Separate: bool | None

InputBinding_reflection = _expr511

def InputBinding_create_ZAC0108A(prefix: str | None=None, position: int | None=None, item_separator: str | None=None, separate: bool | None=None) -> InputBinding:
    return InputBinding(prefix, position, item_separator, separate)


def _expr512() -> TypeInfo:
    return class_type("ARCtrl.CWL.CWLInput", None, CWLInput, DynamicObj_reflection())


class CWLInput(DynamicObj):
    def __init__(self, name: str, type_: CWLType | None=None, input_binding: InputBinding | None=None, optional: bool | None=None) -> None:
        super().__init__()
        this: FSharpRef[CWLInput] = FSharpRef(None)
        self.name: str = name
        this.contents = self
        self.init_004031: int = 1
        set_optional_property("type", type_, this.contents)
        set_optional_property("inputBinding", input_binding, this.contents)
        set_optional_property("optional", optional, this.contents)

    @property
    def Name(self, __unit: None=None) -> str:
        this: CWLInput = self
        return this.name

    @property
    def Type_(self, __unit: None=None) -> CWLType | None:
        this: CWLInput = self
        match_value: Any | None = this.TryGetPropertyValue("type")
        if match_value is not None:
            o: Any = value(match_value)
            return o if isinstance(o, CWLType) else None

        else: 
            return None


    @property
    def InputBinding(self, __unit: None=None) -> InputBinding | None:
        this: CWLInput = self
        match_value: Any | None = this.TryGetPropertyValue("inputBinding")
        if match_value is not None:
            o: Any = value(match_value)
            return o if isinstance(o, InputBinding) else None

        else: 
            return None


    @property
    def Optional(self, __unit: None=None) -> bool | None:
        this: CWLInput = self
        match_value: Any | None = this.TryGetPropertyValue("optional")
        if match_value is not None:
            o: Any = value(match_value)
            return o if (str(type(o)) == "<class \'bool\'>") else None

        else: 
            return None



CWLInput_reflection = _expr512

def CWLInput__ctor_Z3A15BEDB(name: str, type_: CWLType | None=None, input_binding: InputBinding | None=None, optional: bool | None=None) -> CWLInput:
    return CWLInput(name, type_, input_binding, optional)


__all__ = ["InputBinding_reflection", "InputBinding_create_ZAC0108A", "CWLInput_reflection"]

