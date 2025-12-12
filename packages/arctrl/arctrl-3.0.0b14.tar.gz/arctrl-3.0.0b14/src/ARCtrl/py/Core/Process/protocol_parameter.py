from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from ...fable_modules.fable_library.option import (default_arg, map, bind)
from ...fable_modules.fable_library.reflection import (TypeInfo, string_type, option_type, record_type)
from ...fable_modules.fable_library.types import (Array, to_string, Record)
from ..comment import Comment
from ..Helper.collections_ import Option_fromValueWithDefault
from ..ontology_annotation import (OntologyAnnotation, OntologyAnnotation_reflection)

def _expr761() -> TypeInfo:
    return record_type("ARCtrl.Process.ProtocolParameter", [], ProtocolParameter, lambda: [("ID", option_type(string_type)), ("ParameterName", option_type(OntologyAnnotation_reflection()))])


@dataclass(eq = False, repr = False, slots = True)
class ProtocolParameter(Record):
    ID: str | None
    ParameterName: OntologyAnnotation | None
    @staticmethod
    def make(id: str | None=None, parameter_name: OntologyAnnotation | None=None) -> ProtocolParameter:
        return ProtocolParameter(id, parameter_name)

    @staticmethod
    def create(Id: str | None=None, ParameterName: OntologyAnnotation | None=None) -> ProtocolParameter:
        return ProtocolParameter.make(Id, ParameterName)

    @staticmethod
    def empty() -> ProtocolParameter:
        return ProtocolParameter.create()

    @staticmethod
    def from_string(term: str, source: str, accession: str, comments: Array[Comment] | None=None) -> ProtocolParameter:
        oa: OntologyAnnotation = OntologyAnnotation.create(term, source, accession, comments)
        parameter_name: OntologyAnnotation | None = Option_fromValueWithDefault(OntologyAnnotation(), oa)
        return ProtocolParameter.make(None, parameter_name)

    @staticmethod
    def to_string_object(pp: ProtocolParameter) -> dict[str, Any]:
        value: dict[str, Any] = {
            "TermAccessionNumber": "",
            "TermName": "",
            "TermSourceREF": ""
        }
        def mapping(oa: OntologyAnnotation) -> dict[str, Any]:
            return OntologyAnnotation.to_string_object(oa)

        return default_arg(map(mapping, pp.ParameterName), value)

    @property
    def NameText(self, __unit: None=None) -> str:
        this: ProtocolParameter = self
        def mapping(oa: OntologyAnnotation) -> str:
            return oa.NameText

        return default_arg(map(mapping, this.ParameterName), "")

    @property
    def TryNameText(self, __unit: None=None) -> str | None:
        this: ProtocolParameter = self
        def binder(oa: OntologyAnnotation) -> str | None:
            return oa.Name

        return bind(binder, this.ParameterName)

    def MapCategory(self, f: Callable[[OntologyAnnotation], OntologyAnnotation]) -> ProtocolParameter:
        this: ProtocolParameter = self
        return ProtocolParameter(this.ID, map(f, this.ParameterName))

    def SetCategory(self, c: OntologyAnnotation) -> ProtocolParameter:
        this: ProtocolParameter = self
        return ProtocolParameter(this.ID, c)

    @staticmethod
    def try_get_name_text(pp: ProtocolParameter) -> str | None:
        return pp.TryNameText

    @staticmethod
    def get_name_text(pp: ProtocolParameter) -> str:
        return default_arg(ProtocolParameter.try_get_name_text(pp), "")

    @staticmethod
    def name_equals_string(name: str, pp: ProtocolParameter) -> bool:
        return pp.NameText == name

    def Print(self, __unit: None=None) -> str:
        this: ProtocolParameter = self
        return to_string(this)

    def PrintCompact(self, __unit: None=None) -> str:
        this: ProtocolParameter = self
        return "OA " + this.NameText


ProtocolParameter_reflection = _expr761

__all__ = ["ProtocolParameter_reflection"]

