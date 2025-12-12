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

def _expr759() -> TypeInfo:
    return record_type("ARCtrl.Process.Source", [], Source, lambda: [("ID", option_type(string_type)), ("Name", option_type(string_type)), ("Characteristics", option_type(list_type(MaterialAttributeValue_reflection())))])


@dataclass(eq = False, repr = False, slots = True)
class Source(Record):
    ID: str | None
    Name: str | None
    Characteristics: FSharpList[MaterialAttributeValue] | None
    def Print(self, __unit: None=None) -> str:
        this: Source = self
        return to_string(this)

    def PrintCompact(self, __unit: None=None) -> str:
        this: Source = self
        l: int = length(default_arg(this.Characteristics, empty())) or 0
        arg: str = Source__get_NameAsString(this)
        return to_text(printf("%s [%i characteristics]"))(arg)(l)


Source_reflection = _expr759

def Source_make(id: str | None=None, name: str | None=None, characteristics: FSharpList[MaterialAttributeValue] | None=None) -> Source:
    return Source(id, name, characteristics)


def Source_create_Z5CA08497(Id: str | None=None, Name: str | None=None, Characteristics: FSharpList[MaterialAttributeValue] | None=None) -> Source:
    return Source_make(Id, Name, Characteristics)


def Source_get_empty(__unit: None=None) -> Source:
    return Source_create_Z5CA08497()


def Source__get_NameAsString(this: Source) -> str:
    return default_arg(this.Name, "")


def Source_getUnits_53E41069(m: Source) -> FSharpList[OntologyAnnotation]:
    def chooser(c: MaterialAttributeValue, m: Any=m) -> OntologyAnnotation | None:
        return c.Unit

    return choose(chooser, default_arg(m.Characteristics, empty()))


def Source_setCharacteristicValues(values: FSharpList[MaterialAttributeValue], m: Source) -> Source:
    return Source(m.ID, m.Name, values)


__all__ = ["Source_reflection", "Source_make", "Source_create_Z5CA08497", "Source_get_empty", "Source__get_NameAsString", "Source_getUnits_53E41069", "Source_setCharacteristicValues"]

