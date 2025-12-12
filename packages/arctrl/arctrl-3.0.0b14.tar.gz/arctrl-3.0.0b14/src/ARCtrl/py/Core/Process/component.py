from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from ...fable_modules.fable_library.option import (map, default_arg)
from ...fable_modules.fable_library.reflection import (TypeInfo, option_type, record_type)
from ...fable_modules.fable_library.reg_exp import (get_item, groups)
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.fable_library.types import (Record, Array)
from ..comment import Comment
from ..Helper.collections_ import Option_fromValueWithDefault
from ..Helper.regex import ActivePatterns__007CRegex_007C__007C
from ..ontology_annotation import (OntologyAnnotation, OntologyAnnotation_reflection)
from ..value import (Value, Value_reflection)

def _expr762() -> TypeInfo:
    return record_type("ARCtrl.Process.Component", [], Component, lambda: [("ComponentValue", option_type(Value_reflection())), ("ComponentUnit", option_type(OntologyAnnotation_reflection())), ("ComponentType", option_type(OntologyAnnotation_reflection()))])


@dataclass(eq = False, repr = False, slots = True)
class Component(Record):
    ComponentValue: Value | None
    ComponentUnit: OntologyAnnotation | None
    ComponentType: OntologyAnnotation | None
    def AlternateName(self, __unit: None=None) -> str | None:
        this: Component = self
        return Component__get_ComponentName(this)

    def MeasurementMethod(self, __unit: None=None) -> str | None:
        return None

    def Description(self, __unit: None=None) -> str | None:
        return None

    def GetCategory(self, __unit: None=None) -> OntologyAnnotation | None:
        this: Component = self
        return this.ComponentType

    def GetAdditionalType(self, __unit: None=None) -> str:
        return "Component"

    def GetValue(self, __unit: None=None) -> Value | None:
        this: Component = self
        return this.ComponentValue

    def GetUnit(self, __unit: None=None) -> OntologyAnnotation | None:
        this: Component = self
        return this.ComponentUnit


Component_reflection = _expr762

def Component__get_ComponentName(this: Component) -> str | None:
    def mapping(v: Value, this: Any=this) -> str:
        return Component_composeName(v, this.ComponentUnit)

    return map(mapping, this.ComponentValue)


def Component_make(value: Value | None=None, unit: OntologyAnnotation | None=None, component_type: OntologyAnnotation | None=None) -> Component:
    return Component(value, unit, component_type)


def Component_create_Z2F0B38C7(value: Value | None=None, unit: OntologyAnnotation | None=None, component_type: OntologyAnnotation | None=None) -> Component:
    return Component_make(value, unit, component_type)


def Component_get_empty(__unit: None=None) -> Component:
    return Component_create_Z2F0B38C7()


def Component_composeName(value: Value, unit: OntologyAnnotation | None=None) -> str:
    if value.tag == 0:
        oa: OntologyAnnotation = value.fields[0]
        return ((("" + oa.NameText) + " (") + oa.TermAccessionShort) + ")"

    elif unit is not None:
        u: OntologyAnnotation = unit
        return ((((("" + value.Text) + " ") + u.NameText) + " (") + u.TermAccessionShort) + ")"

    else: 
        return ("" + value.Text) + ""



def Component_decomposeName_Z721C83C5(name: str) -> tuple[Value, OntologyAnnotation | None]:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^(?<value>[\\d\\.]+) (?<unit>.+) \\((?<ontology>[^(]*:[^)]*)\\)", name)
    if active_pattern_result is not None:
        unitr: Any = active_pattern_result
        oa: OntologyAnnotation
        tan: str = get_item(groups(unitr), "ontology") or ""
        oa = OntologyAnnotation.from_term_annotation(tan)
        v: Value
        value: str = get_item(groups(unitr), "value") or ""
        v = Value.from_string(value)
        u: str = get_item(groups(unitr), "unit") or ""
        oa.Name = u
        return (v, oa)

    else: 
        active_pattern_result_1: Any | None = ActivePatterns__007CRegex_007C__007C("^(?<value>[^\\(]+) \\((?<ontology>[^(]*:[^)]*)\\)", name)
        if active_pattern_result_1 is not None:
            r: Any = active_pattern_result_1
            oa_1: OntologyAnnotation
            tan_1: str = get_item(groups(r), "ontology") or ""
            oa_1 = OntologyAnnotation.from_term_annotation(tan_1)
            v_1: str = get_item(groups(r), "value") or ""
            oa_1.Name = v_1
            return (Value(0, oa_1), None)

        else: 
            active_pattern_result_2: Any | None = ActivePatterns__007CRegex_007C__007C("^(?<value>[^\\(\\)]+) \\(\\)", name)
            if active_pattern_result_2 is not None:
                r_1: Any = active_pattern_result_2
                return (Value(0, OntologyAnnotation(get_item(groups(r_1), "value") or "")), None)

            else: 
                return (Value(3, name), None)





def Component_fromISAString_7C9A7CF8(name: str | None=None, term: str | None=None, source: str | None=None, accession: str | None=None, comments: Array[Comment] | None=None) -> Component:
    c_type: OntologyAnnotation | None
    v: OntologyAnnotation = OntologyAnnotation.create(term, source, accession, comments)
    c_type = Option_fromValueWithDefault(OntologyAnnotation(), v)
    if name is None:
        return Component_make(None, None, c_type)

    else: 
        pattern_input: tuple[Value, OntologyAnnotation | None] = Component_decomposeName_Z721C83C5(name)
        return Component_make(Option_fromValueWithDefault(Value(3, ""), pattern_input[0]), pattern_input[1], c_type)



def Component_toStringObject_Z685B8F25(c: Component) -> tuple[str, dict[str, Any]]:
    oa_1: dict[str, Any]
    value: dict[str, Any] = {
        "TermAccessionNumber": "",
        "TermName": "",
        "TermSourceREF": ""
    }
    def mapping(oa: OntologyAnnotation, c: Any=c) -> dict[str, Any]:
        return OntologyAnnotation.to_string_object(oa)

    oa_1 = default_arg(map(mapping, c.ComponentType), value)
    return (default_arg(Component__get_ComponentName(c), ""), oa_1)


def Component__get_NameText(this: Component) -> str:
    def mapping(c: OntologyAnnotation, this: Any=this) -> str:
        return c.NameText

    return default_arg(map(mapping, this.ComponentType), "")


def Component__get_UnitText(this: Component) -> str:
    def mapping(c: OntologyAnnotation, this: Any=this) -> str:
        return c.NameText

    return default_arg(map(mapping, this.ComponentUnit), "")


def Component__get_ValueText(this: Component) -> str:
    def mapping(c: Value, this: Any=this) -> str:
        return c.Text

    return default_arg(map(mapping, this.ComponentValue), "")


def Component__get_ValueWithUnitText(this: Component) -> str:
    def mapping(oa: OntologyAnnotation, this: Any=this) -> str:
        return oa.NameText

    unit: str | None = map(mapping, this.ComponentUnit)
    v: str = Component__get_ValueText(this)
    if unit is None:
        return v

    else: 
        u: str = unit
        return to_text(printf("%s %s"))(v)(u)



def Component__MapCategory_658CFBF6(this: Component, f: Callable[[OntologyAnnotation], OntologyAnnotation]) -> Component:
    return Component(this.ComponentValue, this.ComponentUnit, map(f, this.ComponentType))


def Component__SetCategory_ZDED3A0F(this: Component, c: OntologyAnnotation) -> Component:
    return Component(this.ComponentValue, this.ComponentUnit, c)


def Component_createAsPV(alternate_name: str | None=None, measurement_method: str | None=None, description: str | None=None, category: OntologyAnnotation | None=None, value: Value | None=None, unit: OntologyAnnotation | None=None) -> Component:
    return Component_create_Z2F0B38C7(value, unit, category)


__all__ = ["Component_reflection", "Component__get_ComponentName", "Component_make", "Component_create_Z2F0B38C7", "Component_get_empty", "Component_composeName", "Component_decomposeName_Z721C83C5", "Component_fromISAString_7C9A7CF8", "Component_toStringObject_Z685B8F25", "Component__get_NameText", "Component__get_UnitText", "Component__get_ValueText", "Component__get_ValueWithUnitText", "Component__MapCategory_658CFBF6", "Component__SetCategory_ZDED3A0F", "Component_createAsPV"]

