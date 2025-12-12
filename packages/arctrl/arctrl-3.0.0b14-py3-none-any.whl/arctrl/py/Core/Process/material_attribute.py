from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from ...fable_modules.fable_library.option import (default_arg, map, bind)
from ...fable_modules.fable_library.reflection import (TypeInfo, string_type, option_type, record_type)
from ...fable_modules.fable_library.types import (to_string, Record, Array)
from ..comment import Comment
from ..Helper.collections_ import Option_fromValueWithDefault
from ..ontology_annotation import (OntologyAnnotation, OntologyAnnotation_reflection)

def _expr751() -> TypeInfo:
    return record_type("ARCtrl.Process.MaterialAttribute", [], MaterialAttribute, lambda: [("ID", option_type(string_type)), ("CharacteristicType", option_type(OntologyAnnotation_reflection()))])


@dataclass(eq = False, repr = False, slots = True)
class MaterialAttribute(Record):
    ID: str | None
    CharacteristicType: OntologyAnnotation | None
    def Print(self, __unit: None=None) -> str:
        this: MaterialAttribute = self
        return to_string(this)

    def PrintCompact(self, __unit: None=None) -> str:
        this: MaterialAttribute = self
        return "OA " + MaterialAttribute__get_NameText(this)


MaterialAttribute_reflection = _expr751

def MaterialAttribute_make(id: str | None=None, characteristic_type: OntologyAnnotation | None=None) -> MaterialAttribute:
    return MaterialAttribute(id, characteristic_type)


def MaterialAttribute_create_A220A8A(Id: str | None=None, CharacteristicType: OntologyAnnotation | None=None) -> MaterialAttribute:
    return MaterialAttribute_make(Id, CharacteristicType)


def MaterialAttribute_get_empty(__unit: None=None) -> MaterialAttribute:
    return MaterialAttribute_create_A220A8A()


def MaterialAttribute_fromString_5980DC03(term: str, source: str, accession: str, comments: Array[Comment] | None=None) -> MaterialAttribute:
    oa: OntologyAnnotation = OntologyAnnotation.create(term, source, accession, comments)
    return MaterialAttribute_make(None, Option_fromValueWithDefault(OntologyAnnotation(), oa))


def MaterialAttribute_toStringObject_Z1E3B85DD(ma: MaterialAttribute) -> dict[str, Any]:
    value: dict[str, Any] = {
        "TermAccessionNumber": "",
        "TermName": "",
        "TermSourceREF": ""
    }
    def mapping(oa: OntologyAnnotation, ma: Any=ma) -> dict[str, Any]:
        return OntologyAnnotation.to_string_object(oa)

    return default_arg(map(mapping, ma.CharacteristicType), value)


def MaterialAttribute__get_NameText(this: MaterialAttribute) -> str:
    def mapping(oa: OntologyAnnotation, this: Any=this) -> str:
        return oa.NameText

    return default_arg(map(mapping, this.CharacteristicType), "")


def MaterialAttribute__get_TryNameText(this: MaterialAttribute) -> str | None:
    def binder(oa: OntologyAnnotation, this: Any=this) -> str | None:
        return oa.Name

    return bind(binder, this.CharacteristicType)


def MaterialAttribute__MapCategory_658CFBF6(this: MaterialAttribute, f: Callable[[OntologyAnnotation], OntologyAnnotation]) -> MaterialAttribute:
    return MaterialAttribute(this.ID, map(f, this.CharacteristicType))


def MaterialAttribute__SetCategory_ZDED3A0F(this: MaterialAttribute, c: OntologyAnnotation) -> MaterialAttribute:
    return MaterialAttribute(this.ID, c)


def MaterialAttribute_tryGetNameText_Z1E3B85DD(ma: MaterialAttribute) -> str:
    return MaterialAttribute__get_NameText(ma)


def MaterialAttribute_getNameText_Z1E3B85DD(ma: MaterialAttribute) -> str | None:
    return MaterialAttribute__get_TryNameText(ma)


def MaterialAttribute_nameEqualsString(name: str, ma: MaterialAttribute) -> bool:
    return MaterialAttribute__get_NameText(ma) == name


__all__ = ["MaterialAttribute_reflection", "MaterialAttribute_make", "MaterialAttribute_create_A220A8A", "MaterialAttribute_get_empty", "MaterialAttribute_fromString_5980DC03", "MaterialAttribute_toStringObject_Z1E3B85DD", "MaterialAttribute__get_NameText", "MaterialAttribute__get_TryNameText", "MaterialAttribute__MapCategory_658CFBF6", "MaterialAttribute__SetCategory_ZDED3A0F", "MaterialAttribute_tryGetNameText_Z1E3B85DD", "MaterialAttribute_getNameText_Z1E3B85DD", "MaterialAttribute_nameEqualsString"]

