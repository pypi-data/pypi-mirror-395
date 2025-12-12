from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from ...fable_modules.fable_library.list import (try_find, FSharpList, exists, append, singleton, filter)
from ...fable_modules.fable_library.option import (default_arg, map)
from ...fable_modules.fable_library.reflection import (TypeInfo, string_type, option_type, array_type, record_type)
from ...fable_modules.fable_library.types import (Array, to_string, Record)
from ...fable_modules.fable_library.util import equals
from ..comment import (Comment, Comment_reflection)
from ..Helper.collections_ import (Option_fromValueWithDefault, ResizeArray_map)
from ..ontology_annotation import (OntologyAnnotation, OntologyAnnotation_reflection)

def _expr745() -> TypeInfo:
    return record_type("ARCtrl.Process.Factor", [], Factor, lambda: [("Name", option_type(string_type)), ("FactorType", option_type(OntologyAnnotation_reflection())), ("Comments", option_type(array_type(Comment_reflection())))])


@dataclass(eq = False, repr = False, slots = True)
class Factor(Record):
    Name: str | None
    FactorType: OntologyAnnotation | None
    Comments: Array[Comment] | None
    @staticmethod
    def make(name: str | None=None, factor_type: OntologyAnnotation | None=None, comments: Array[Comment] | None=None) -> Factor:
        return Factor(name, factor_type, comments)

    @staticmethod
    def create(Name: str | None=None, FactorType: OntologyAnnotation | None=None, Comments: Array[Comment] | None=None) -> Factor:
        return Factor.make(Name, FactorType, Comments)

    @staticmethod
    def empty() -> Factor:
        return Factor.create()

    @staticmethod
    def from_string(name: str, term: str, source: str, accession: str, comments: Array[Comment] | None=None) -> Factor:
        oa: OntologyAnnotation = OntologyAnnotation.create(term, source, accession, comments)
        name_1: str | None = Option_fromValueWithDefault("", name)
        factor_type: OntologyAnnotation | None = Option_fromValueWithDefault(OntologyAnnotation(), oa)
        return Factor.make(name_1, factor_type, None)

    @staticmethod
    def to_string_object(factor: Factor) -> dict[str, Any]:
        value: dict[str, Any] = {
            "TermAccessionNumber": "",
            "TermName": "",
            "TermSourceREF": ""
        }
        def mapping(oa: OntologyAnnotation) -> dict[str, Any]:
            return OntologyAnnotation.to_string_object(oa)

        return default_arg(map(mapping, factor.FactorType), value)

    @property
    def NameText(self, __unit: None=None) -> str:
        this: Factor = self
        return default_arg(this.Name, "")

    def MapCategory(self, f: Callable[[OntologyAnnotation], OntologyAnnotation]) -> Factor:
        this: Factor = self
        return Factor(this.Name, map(f, this.FactorType), this.Comments)

    def SetCategory(self, c: OntologyAnnotation) -> Factor:
        this: Factor = self
        return Factor(this.Name, c, this.Comments)

    @staticmethod
    def try_get_by_name(name: str, factors: FSharpList[Factor]) -> Factor | None:
        def _arrow742(f: Factor) -> bool:
            return equals(f.Name, name)

        return try_find(_arrow742, factors)

    @staticmethod
    def exists_by_name(name: str, factors: FSharpList[Factor]) -> bool:
        def _arrow743(f: Factor) -> bool:
            return equals(f.Name, name)

        return exists(_arrow743, factors)

    @staticmethod
    def add(factors: FSharpList[Factor], factor: Factor) -> FSharpList[Factor]:
        return append(factors, singleton(factor))

    @staticmethod
    def remove_by_name(name: str, factors: FSharpList[Factor]) -> FSharpList[Factor]:
        def _arrow744(f: Factor) -> bool:
            return not equals(f.Name, name)

        return filter(_arrow744, factors)

    @staticmethod
    def get_comments(factor: Factor) -> Array[Comment] | None:
        return factor.Comments

    @staticmethod
    def map_comments(f: Callable[[Array[Comment]], Array[Comment]], factor: Factor) -> Factor:
        return Factor(factor.Name, factor.FactorType, map(f, factor.Comments))

    @staticmethod
    def set_comments(factor: Factor, comments: Array[Comment]) -> Factor:
        return Factor(factor.Name, factor.FactorType, comments)

    @staticmethod
    def get_factor_type(factor: Factor) -> OntologyAnnotation | None:
        return factor.FactorType

    @staticmethod
    def map_factor_type(f: Callable[[OntologyAnnotation], OntologyAnnotation], factor: Factor) -> Factor:
        return Factor(factor.Name, map(f, factor.FactorType), factor.Comments)

    @staticmethod
    def set_factor_type(factor: Factor, factor_type: OntologyAnnotation) -> Factor:
        return Factor(factor.Name, factor_type, factor.Comments)

    @staticmethod
    def try_get_name(f: Factor) -> str | None:
        return f.Name

    @staticmethod
    def get_name_as_string(f: Factor) -> str:
        return f.NameText

    @staticmethod
    def name_equals_string(name: str, f: Factor) -> bool:
        return f.NameText == name

    def Copy(self, __unit: None=None) -> Factor:
        this: Factor = self
        def mapping(a: Array[Comment]) -> Array[Comment]:
            def f(c: Comment, a: Any=a) -> Comment:
                return c.Copy()

            return ResizeArray_map(f, a)

        comments: Array[Comment] | None = map(mapping, this.Comments)
        return Factor.make(this.Name, this.FactorType, comments)

    def Print(self, __unit: None=None) -> str:
        this: Factor = self
        return to_string(this)

    def PrintCompact(self, __unit: None=None) -> str:
        this: Factor = self
        return "OA " + this.NameText


Factor_reflection = _expr745

__all__ = ["Factor_reflection"]

