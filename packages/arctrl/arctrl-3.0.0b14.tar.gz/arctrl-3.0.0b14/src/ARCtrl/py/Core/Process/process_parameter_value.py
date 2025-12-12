from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from ...fable_modules.fable_library.option import (default_arg, map, bind)
from ...fable_modules.fable_library.reflection import (TypeInfo, option_type, record_type)
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.fable_library.types import (to_string, Record)
from ...fable_modules.fable_library.util import int32_to_string
from ..ontology_annotation import (OntologyAnnotation, OntologyAnnotation_reflection)
from ..value import (Value as Value_1, Value_reflection)
from .protocol_parameter import (ProtocolParameter, ProtocolParameter_reflection)

def _expr773() -> TypeInfo:
    return record_type("ARCtrl.Process.ProcessParameterValue", [], ProcessParameterValue, lambda: [("Category", option_type(ProtocolParameter_reflection())), ("Value", option_type(Value_reflection())), ("Unit", option_type(OntologyAnnotation_reflection()))])


@dataclass(eq = False, repr = False, slots = True)
class ProcessParameterValue(Record):
    Category: ProtocolParameter | None
    Value: Value_1 | None
    Unit: OntologyAnnotation | None
    @staticmethod
    def make(category: ProtocolParameter | None=None, value: Value_1 | None=None, unit: OntologyAnnotation | None=None) -> ProcessParameterValue:
        return ProcessParameterValue(category, value, unit)

    @staticmethod
    def create(Category: ProtocolParameter | None=None, Value: Value_1 | None=None, Unit: OntologyAnnotation | None=None) -> ProcessParameterValue:
        return ProcessParameterValue.make(Category, Value, Unit)

    @staticmethod
    def empty() -> ProcessParameterValue:
        return ProcessParameterValue.create()

    @property
    def NameText(self, __unit: None=None) -> str:
        this: ProcessParameterValue = self
        def mapping(oa: ProtocolParameter) -> str:
            return oa.NameText

        return default_arg(map(mapping, this.Category), "")

    @property
    def TryNameText(self, __unit: None=None) -> str | None:
        this: ProcessParameterValue = self
        def binder(oa: ProtocolParameter) -> str | None:
            return oa.TryNameText

        return bind(binder, this.Category)

    @property
    def ValueText(self, __unit: None=None) -> str:
        this: ProcessParameterValue = self
        def mapping(oa: Value_1) -> str:
            if oa.tag == 2:
                return to_string(oa.fields[0])

            elif oa.tag == 1:
                return int32_to_string(oa.fields[0])

            elif oa.tag == 3:
                return oa.fields[0]

            else: 
                return oa.fields[0].NameText


        return default_arg(map(mapping, this.Value), "")

    @property
    def ValueWithUnitText(self, __unit: None=None) -> str:
        this: ProcessParameterValue = self
        def mapping(oa: OntologyAnnotation) -> str:
            return oa.NameText

        unit: str | None = map(mapping, this.Unit)
        v: str = this.ValueText
        if unit is None:
            return v

        else: 
            u: str = unit
            return to_text(printf("%s %s"))(v)(u)


    def MapCategory(self, f: Callable[[OntologyAnnotation], OntologyAnnotation]) -> ProcessParameterValue:
        this: ProcessParameterValue = self
        def mapping(p: ProtocolParameter) -> ProtocolParameter:
            return p.MapCategory(f)

        return ProcessParameterValue(map(mapping, this.Category), this.Value, this.Unit)

    def SetCategory(self, c: OntologyAnnotation) -> ProcessParameterValue:
        this: ProcessParameterValue = self
        def _arrow769(__unit: None=None) -> ProtocolParameter | None:
            match_value: ProtocolParameter | None = this.Category
            if match_value is None:
                return ProtocolParameter.create(None, c)

            else: 
                p: ProtocolParameter = match_value
                return p.SetCategory(c)


        return ProcessParameterValue(_arrow769(), this.Value, this.Unit)

    @staticmethod
    def try_get_name_text(pv: ProcessParameterValue) -> str | None:
        return pv.TryNameText

    @staticmethod
    def get_name_text(pv: ProcessParameterValue) -> str:
        return pv.NameText

    @staticmethod
    def name_equals_string(name: str, pv: ProcessParameterValue) -> bool:
        return pv.NameText == name

    @staticmethod
    def get_category(pv: ProcessParameterValue) -> ProtocolParameter | None:
        return pv.Category

    @staticmethod
    def create_as_pv(alternate_name: str | None=None, measurement_method: str | None=None, description: str | None=None, category: OntologyAnnotation | None=None, value: Value_1 | None=None, unit: OntologyAnnotation | None=None) -> ProcessParameterValue:
        def mapping(c: OntologyAnnotation) -> ProtocolParameter:
            return ProtocolParameter.create(None, c)

        category_1: ProtocolParameter | None = map(mapping, category)
        return ProcessParameterValue.create(category_1, value, unit)

    def Print(self, __unit: None=None) -> str:
        this: ProcessParameterValue = self
        return to_string(this)

    def PrintCompact(self, __unit: None=None) -> str:
        this: ProcessParameterValue = self
        def mapping(f: ProtocolParameter) -> str:
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
        def _arrow770(__unit: None=None) -> str:
            value_2: str = value
            return value_2

        def _arrow771(__unit: None=None) -> str:
            category_2: str = category
            return (category_2 + ":") + "No Value"

        def _arrow772(__unit: None=None) -> str:
            category_1: str = category
            value_1: str = value
            return (category_1 + ":") + value_1

        return ("" if (value is None) else _arrow770()) if (category is None) else (_arrow771() if (value is None) else _arrow772())

    def AlternateName(self, __unit: None=None) -> str | None:
        return None

    def MeasurementMethod(self, __unit: None=None) -> str | None:
        return None

    def Description(self, __unit: None=None) -> str | None:
        return None

    def GetCategory(self, __unit: None=None) -> OntologyAnnotation | None:
        this: ProcessParameterValue = self
        def binder(p: ProtocolParameter) -> OntologyAnnotation | None:
            return p.ParameterName

        return bind(binder, this.Category)

    def GetAdditionalType(self, __unit: None=None) -> str:
        return "ProcessParameterValue"

    def GetValue(self, __unit: None=None) -> Value_1 | None:
        this: ProcessParameterValue = self
        return this.Value

    def GetUnit(self, __unit: None=None) -> OntologyAnnotation | None:
        this: ProcessParameterValue = self
        return this.Unit


ProcessParameterValue_reflection = _expr773

__all__ = ["ProcessParameterValue_reflection"]

