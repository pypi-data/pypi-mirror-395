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
from .factor import (Factor, Factor_reflection)

def _expr749() -> TypeInfo:
    return record_type("ARCtrl.Process.FactorValue", [], FactorValue, lambda: [("ID", option_type(string_type)), ("Category", option_type(Factor_reflection())), ("Value", option_type(Value_reflection())), ("Unit", option_type(OntologyAnnotation_reflection()))])


@dataclass(eq = False, repr = False, slots = True)
class FactorValue(Record):
    ID: str | None
    Category: Factor | None
    Value: Value_1 | None
    Unit: OntologyAnnotation | None
    def Print(self, __unit: None=None) -> str:
        this: FactorValue = self
        return to_string(this)

    def PrintCompact(self, __unit: None=None) -> str:
        this: FactorValue = self
        def mapping(f: Factor) -> str:
            return f.NameText

        category: str | None = map(mapping, this.Category)
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
        def _arrow746(__unit: None=None) -> str:
            value_2: str = value
            return value_2

        def _arrow747(__unit: None=None) -> str:
            category_2: str = category
            return (category_2 + ":") + "No Value"

        def _arrow748(__unit: None=None) -> str:
            category_1: str = category
            value_1: str = value
            return (category_1 + ":") + value_1

        return ("" if (value is None) else _arrow746()) if (category is None) else (_arrow747() if (value is None) else _arrow748())

    def AlternateName(self, __unit: None=None) -> str | None:
        return None

    def MeasurementMethod(self, __unit: None=None) -> str | None:
        return None

    def Description(self, __unit: None=None) -> str | None:
        return None

    def GetCategory(self, __unit: None=None) -> OntologyAnnotation | None:
        this: FactorValue = self
        def binder(f: Factor) -> OntologyAnnotation | None:
            return f.FactorType

        return bind(binder, this.Category)

    def GetValue(self, __unit: None=None) -> Value_1 | None:
        this: FactorValue = self
        return this.Value

    def GetUnit(self, __unit: None=None) -> OntologyAnnotation | None:
        this: FactorValue = self
        return this.Unit

    def GetAdditionalType(self, __unit: None=None) -> str:
        return "FactorValue"


FactorValue_reflection = _expr749

def FactorValue_make(id: str | None=None, category: Factor | None=None, value: Value_1 | None=None, unit: OntologyAnnotation | None=None) -> FactorValue:
    return FactorValue(id, category, value, unit)


def FactorValue_create_30BDC49(Id: str | None=None, Category: Factor | None=None, Value: Value_1 | None=None, Unit: OntologyAnnotation | None=None) -> FactorValue:
    return FactorValue_make(Id, Category, Value, Unit)


def FactorValue_get_empty(__unit: None=None) -> FactorValue:
    return FactorValue_create_30BDC49()


def FactorValue__get_ValueText(this: FactorValue) -> str:
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


def FactorValue__get_ValueWithUnitText(this: FactorValue) -> str:
    def mapping(oa: OntologyAnnotation, this: Any=this) -> str:
        return oa.NameText

    unit: str | None = map(mapping, this.Unit)
    v: str = FactorValue__get_ValueText(this)
    if unit is None:
        return v

    else: 
        u: str = unit
        return to_text(printf("%s %s"))(v)(u)



def FactorValue__get_NameText(this: FactorValue) -> str:
    def mapping(factor: Factor, this: Any=this) -> str:
        return factor.NameText

    return default_arg(map(mapping, this.Category), "")


def FactorValue__MapCategory_658CFBF6(this: FactorValue, f: Callable[[OntologyAnnotation], OntologyAnnotation]) -> FactorValue:
    def mapping(p: Factor, this: Any=this, f: Any=f) -> Factor:
        return p.MapCategory(f)

    return FactorValue(this.ID, map(mapping, this.Category), this.Value, this.Unit)


def FactorValue__SetCategory_ZDED3A0F(this: FactorValue, c: OntologyAnnotation) -> FactorValue:
    def _arrow750(__unit: None=None, this: Any=this, c: Any=c) -> Factor | None:
        match_value: Factor | None = this.Category
        if match_value is None:
            return Factor.create(None, c)

        else: 
            p: Factor = match_value
            return p.SetCategory(c)


    return FactorValue(this.ID, _arrow750(), this.Value, this.Unit)


def FactorValue_getNameAsString_7105C732(fv: FactorValue) -> str:
    return FactorValue__get_NameText(fv)


def FactorValue_nameEqualsString(name: str, fv: FactorValue) -> bool:
    return FactorValue__get_NameText(fv) == name


def FactorValue_createAsPV(alternate_name: str | None=None, measurement_method: str | None=None, description: str | None=None, category: OntologyAnnotation | None=None, value: Value_1 | None=None, unit: OntologyAnnotation | None=None) -> FactorValue:
    def mapping(c: OntologyAnnotation, alternate_name: Any=alternate_name, measurement_method: Any=measurement_method, description: Any=description, category: Any=category, value: Any=value, unit: Any=unit) -> Factor:
        return Factor.create(None, c)

    return FactorValue_create_30BDC49(None, map(mapping, category), value, unit)


__all__ = ["FactorValue_reflection", "FactorValue_make", "FactorValue_create_30BDC49", "FactorValue_get_empty", "FactorValue__get_ValueText", "FactorValue__get_ValueWithUnitText", "FactorValue__get_NameText", "FactorValue__MapCategory_658CFBF6", "FactorValue__SetCategory_ZDED3A0F", "FactorValue_getNameAsString_7105C732", "FactorValue_nameEqualsString", "FactorValue_createAsPV"]

