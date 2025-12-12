from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from ...fable_modules.fable_library.option import (map, bind, default_arg)
from ...fable_modules.fable_library.reflection import (TypeInfo, string_type, option_type, record_type)
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.fable_library.types import (to_string, Record)
from ...fable_modules.fable_library.util import int32_to_string
from ..ontology_annotation import (OntologyAnnotation, OntologyAnnotation_reflection)
from ..value import (Value as Value_1, Value_reflection)
from .material_attribute import (MaterialAttribute__get_NameText, MaterialAttribute, MaterialAttribute_reflection, MaterialAttribute__get_TryNameText, MaterialAttribute__MapCategory_658CFBF6, MaterialAttribute_create_A220A8A, MaterialAttribute__SetCategory_ZDED3A0F)

def _expr756() -> TypeInfo:
    return record_type("ARCtrl.Process.MaterialAttributeValue", [], MaterialAttributeValue, lambda: [("ID", option_type(string_type)), ("Category", option_type(MaterialAttribute_reflection())), ("Value", option_type(Value_reflection())), ("Unit", option_type(OntologyAnnotation_reflection()))])


@dataclass(eq = False, repr = False, slots = True)
class MaterialAttributeValue(Record):
    ID: str | None
    Category: MaterialAttribute | None
    Value: Value_1 | None
    Unit: OntologyAnnotation | None
    def Print(self, __unit: None=None) -> str:
        this: MaterialAttributeValue = self
        return to_string(this)

    def PrintCompact(self, __unit: None=None) -> str:
        this: MaterialAttributeValue = self
        category: str | None = map(MaterialAttribute__get_NameText, this.Category)
        def mapping_1(oa: OntologyAnnotation) -> str:
            return oa.NameText

        unit: str | None = map(mapping_1, this.Unit)
        def mapping_2(v: Value_1) -> str:
            s: str = v.PrintCompact()
            if unit is None:
                return s

            else: 
                return (s + " ") + unit


        value: str | None = map(mapping_2, this.Value)
        def _arrow753(__unit: None=None) -> str:
            value_2: str = value
            return value_2

        def _arrow754(__unit: None=None) -> str:
            category_2: str = category
            return (category_2 + ":") + "No Value"

        def _arrow755(__unit: None=None) -> str:
            category_1: str = category
            value_1: str = value
            return (category_1 + ":") + value_1

        return ("" if (value is None) else _arrow753()) if (category is None) else (_arrow754() if (value is None) else _arrow755())

    def AlternateName(self, __unit: None=None) -> str | None:
        return None

    def MeasurementMethod(self, __unit: None=None) -> str | None:
        return None

    def Description(self, __unit: None=None) -> str | None:
        return None

    def GetCategory(self, __unit: None=None) -> OntologyAnnotation | None:
        this: MaterialAttributeValue = self
        def binder(x: MaterialAttribute) -> OntologyAnnotation | None:
            return x.CharacteristicType

        return bind(binder, this.Category)

    def GetValue(self, __unit: None=None) -> Value_1 | None:
        this: MaterialAttributeValue = self
        return this.Value

    def GetUnit(self, __unit: None=None) -> OntologyAnnotation | None:
        this: MaterialAttributeValue = self
        return this.Unit

    def GetAdditionalType(self, __unit: None=None) -> str:
        return "MaterialAttributeValue"


MaterialAttributeValue_reflection = _expr756

def MaterialAttributeValue_make(id: str | None=None, category: MaterialAttribute | None=None, value: Value_1 | None=None, unit: OntologyAnnotation | None=None) -> MaterialAttributeValue:
    return MaterialAttributeValue(id, category, value, unit)


def MaterialAttributeValue_create_ZE1D108D(Id: str | None=None, Category: MaterialAttribute | None=None, Value: Value_1 | None=None, Unit: OntologyAnnotation | None=None) -> MaterialAttributeValue:
    return MaterialAttributeValue_make(Id, Category, Value, Unit)


def MaterialAttributeValue_get_empty(__unit: None=None) -> MaterialAttributeValue:
    return MaterialAttributeValue_create_ZE1D108D()


def MaterialAttributeValue__get_NameText(this: MaterialAttributeValue) -> str:
    def mapping(oa: MaterialAttribute, this: Any=this) -> str:
        return MaterialAttribute__get_NameText(oa)

    return default_arg(map(mapping, this.Category), "")


def MaterialAttributeValue__get_TryNameText(this: MaterialAttributeValue) -> str | None:
    def binder(oa: MaterialAttribute, this: Any=this) -> str | None:
        return MaterialAttribute__get_TryNameText(oa)

    return bind(binder, this.Category)


def MaterialAttributeValue__get_ValueText(this: MaterialAttributeValue) -> str:
    def mapping(oa: Value_1, this: Any=this) -> str:
        if oa.tag == 2:
            return to_string(oa.fields[0])

        elif oa.tag == 1:
            return int32_to_string(oa.fields[0])

        elif oa.tag == 3:
            return oa.fields[0]

        else: 
            return oa.fields[0].NameText


    return default_arg(map(mapping, this.Value), "")


def MaterialAttributeValue__get_ValueWithUnitText(this: MaterialAttributeValue) -> str:
    def mapping(oa: OntologyAnnotation, this: Any=this) -> str:
        return oa.NameText

    unit: str | None = map(mapping, this.Unit)
    v: str = MaterialAttributeValue__get_ValueText(this)
    if unit is None:
        return v

    else: 
        u: str = unit
        return to_text(printf("%s %s"))(v)(u)



def MaterialAttributeValue__MapCategory_658CFBF6(this: MaterialAttributeValue, f: Callable[[OntologyAnnotation], OntologyAnnotation]) -> MaterialAttributeValue:
    def mapping(p: MaterialAttribute, this: Any=this, f: Any=f) -> MaterialAttribute:
        return MaterialAttribute__MapCategory_658CFBF6(p, f)

    return MaterialAttributeValue(this.ID, map(mapping, this.Category), this.Value, this.Unit)


def MaterialAttributeValue__SetCategory_ZDED3A0F(this: MaterialAttributeValue, c: OntologyAnnotation) -> MaterialAttributeValue:
    def _arrow757(__unit: None=None, this: Any=this, c: Any=c) -> MaterialAttribute | None:
        match_value: MaterialAttribute | None = this.Category
        return MaterialAttribute_create_A220A8A(None, c) if (match_value is None) else MaterialAttribute__SetCategory_ZDED3A0F(match_value, c)

    return MaterialAttributeValue(this.ID, _arrow757(), this.Value, this.Unit)


def MaterialAttributeValue_tryGetNameText_Z772273B8(mv: MaterialAttributeValue) -> str | None:
    return MaterialAttributeValue__get_TryNameText(mv)


def MaterialAttributeValue_getNameAsString_Z772273B8(mv: MaterialAttributeValue) -> str | None:
    return MaterialAttributeValue__get_TryNameText(mv)


def MaterialAttributeValue_nameEqualsString(name: str, mv: MaterialAttributeValue) -> bool:
    return MaterialAttributeValue__get_NameText(mv) == name


def MaterialAttributeValue_createAsPV(alternate_name: str | None=None, measurement_method: str | None=None, description: str | None=None, category: OntologyAnnotation | None=None, value: Value_1 | None=None, unit: OntologyAnnotation | None=None) -> MaterialAttributeValue:
    def mapping(c: OntologyAnnotation, alternate_name: Any=alternate_name, measurement_method: Any=measurement_method, description: Any=description, category: Any=category, value: Any=value, unit: Any=unit) -> MaterialAttribute:
        return MaterialAttribute_create_A220A8A(None, c)

    return MaterialAttributeValue_create_ZE1D108D(None, map(mapping, category), value, unit)


__all__ = ["MaterialAttributeValue_reflection", "MaterialAttributeValue_make", "MaterialAttributeValue_create_ZE1D108D", "MaterialAttributeValue_get_empty", "MaterialAttributeValue__get_NameText", "MaterialAttributeValue__get_TryNameText", "MaterialAttributeValue__get_ValueText", "MaterialAttributeValue__get_ValueWithUnitText", "MaterialAttributeValue__MapCategory_658CFBF6", "MaterialAttributeValue__SetCategory_ZDED3A0F", "MaterialAttributeValue_tryGetNameText_Z772273B8", "MaterialAttributeValue_getNameAsString_Z772273B8", "MaterialAttributeValue_nameEqualsString", "MaterialAttributeValue_createAsPV"]

