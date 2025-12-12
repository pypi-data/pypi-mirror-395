from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from ..fable_modules.dynamic_obj.dynamic_obj import (DynamicObj, DynamicObj_reflection)
from ..fable_modules.dynamic_obj.dyn_obj import set_optional_property
from ..fable_modules.fable_library.option import value
from ..fable_modules.fable_library.reflection import (TypeInfo, string_type, option_type, record_type, class_type)
from ..fable_modules.fable_library.types import (Record, FSharpRef)
from .cwltypes import CWLType

def _expr509() -> TypeInfo:
    return record_type("ARCtrl.CWL.OutputBinding", [], OutputBinding, lambda: [("Glob", option_type(string_type))])


@dataclass(eq = False, repr = False, slots = True)
class OutputBinding(Record):
    Glob: str | None

OutputBinding_reflection = _expr509

def OutputBinding_create_6DFDD678(glob: str | None=None) -> OutputBinding:
    return OutputBinding(glob)


def _expr510() -> TypeInfo:
    return class_type("ARCtrl.CWL.CWLOutput", None, CWLOutput, DynamicObj_reflection())


class CWLOutput(DynamicObj):
    def __init__(self, name: str, type_: CWLType | None=None, output_binding: OutputBinding | None=None, output_source: str | None=None) -> None:
        super().__init__()
        this: FSharpRef[CWLOutput] = FSharpRef(None)
        self.name: str = name
        this.contents = self
        self.init_004013: int = 1
        set_optional_property("type", type_, this.contents)
        set_optional_property("outputBinding", output_binding, this.contents)
        set_optional_property("outputSource", output_source, this.contents)

    @property
    def Name(self, __unit: None=None) -> str:
        this: CWLOutput = self
        return this.name

    @property
    def Type_(self, __unit: None=None) -> CWLType | None:
        this: CWLOutput = self
        match_value: Any | None = this.TryGetPropertyValue("type")
        if match_value is not None:
            o: Any = value(match_value)
            return o if isinstance(o, CWLType) else None

        else: 
            return None


    @property
    def OutputBinding(self, __unit: None=None) -> OutputBinding | None:
        this: CWLOutput = self
        match_value: Any | None = this.TryGetPropertyValue("outputBinding")
        if match_value is not None:
            o: Any = value(match_value)
            return o if isinstance(o, OutputBinding) else None

        else: 
            return None


    @property
    def OutputSource(self, __unit: None=None) -> str | None:
        this: CWLOutput = self
        match_value: Any | None = this.TryGetPropertyValue("outputSource")
        if match_value is not None:
            o: Any = value(match_value)
            return o if (str(type(o)) == "<class \'str\'>") else None

        else: 
            return None



CWLOutput_reflection = _expr510

def CWLOutput__ctor_744035D(name: str, type_: CWLType | None=None, output_binding: OutputBinding | None=None, output_source: str | None=None) -> CWLOutput:
    return CWLOutput(name, type_, output_binding, output_source)


__all__ = ["OutputBinding_reflection", "OutputBinding_create_6DFDD678", "CWLOutput_reflection"]

