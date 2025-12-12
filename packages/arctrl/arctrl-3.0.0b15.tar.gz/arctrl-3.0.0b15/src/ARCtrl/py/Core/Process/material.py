from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from ...fable_modules.fable_library.list import (length, empty, FSharpList, choose)
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.reflection import (TypeInfo, string_type, option_type, list_type, record_type)
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.fable_library.types import (to_string, Record)
from ..ontology_annotation import OntologyAnnotation
from .material_attribute_value import (MaterialAttributeValue, MaterialAttributeValue_reflection)
from .material_type import (MaterialType as MaterialType_1, MaterialType__get_AsString, MaterialType_reflection)

def _expr758() -> TypeInfo:
    return record_type("ARCtrl.Process.Material", [], Material, lambda: [("ID", option_type(string_type)), ("Name", option_type(string_type)), ("MaterialType", option_type(MaterialType_reflection())), ("Characteristics", option_type(list_type(MaterialAttributeValue_reflection()))), ("DerivesFrom", option_type(list_type(Material_reflection())))])


@dataclass(eq = False, repr = False, slots = True)
class Material(Record):
    ID: str | None
    Name: str | None
    MaterialType: MaterialType_1 | None
    Characteristics: FSharpList[MaterialAttributeValue] | None
    DerivesFrom: FSharpList[Material] | None
    def Print(self, __unit: None=None) -> str:
        this: Material = self
        return to_string(this)

    def PrintCompact(self, __unit: None=None) -> str:
        this: Material = self
        chars: int = length(default_arg(this.Characteristics, empty())) or 0
        match_value: MaterialType_1 | None = this.MaterialType
        if match_value is None:
            arg_3: str = Material__get_NameText(this)
            return to_text(printf("%s [%i characteristics]"))(arg_3)(chars)

        else: 
            t: MaterialType_1 = match_value
            arg: str = Material__get_NameText(this)
            arg_1: str = MaterialType__get_AsString(t)
            return to_text(printf("%s [%s; %i characteristics]"))(arg)(arg_1)(chars)



Material_reflection = _expr758

def Material_make(id: str | None=None, name: str | None=None, material_type: MaterialType_1 | None=None, characteristics: FSharpList[MaterialAttributeValue] | None=None, derives_from: FSharpList[Material] | None=None) -> Material:
    return Material(id, name, material_type, characteristics, derives_from)


def Material_create_Z66909A6D(Id: str | None=None, Name: str | None=None, MaterialType: MaterialType_1 | None=None, Characteristics: FSharpList[MaterialAttributeValue] | None=None, DerivesFrom: FSharpList[Material] | None=None) -> Material:
    return Material_make(Id, Name, MaterialType, Characteristics, DerivesFrom)


def Material_get_empty(__unit: None=None) -> Material:
    return Material_create_Z66909A6D()


def Material__get_NameText(this: Material) -> str:
    return default_arg(this.Name, "")


def Material_getUnits_ZBCDEB61(m: Material) -> FSharpList[OntologyAnnotation]:
    def chooser(c: MaterialAttributeValue, m: Any=m) -> OntologyAnnotation | None:
        return c.Unit

    return choose(chooser, default_arg(m.Characteristics, empty()))


def Material_setCharacteristicValues(values: FSharpList[MaterialAttributeValue], m: Material) -> Material:
    return Material(m.ID, m.Name, m.MaterialType, values, m.DerivesFrom)


__all__ = ["Material_reflection", "Material_make", "Material_create_Z66909A6D", "Material_get_empty", "Material__get_NameText", "Material_getUnits_ZBCDEB61", "Material_setCharacteristicValues"]

