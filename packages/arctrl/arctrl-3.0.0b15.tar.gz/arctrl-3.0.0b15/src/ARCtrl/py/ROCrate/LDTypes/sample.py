from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.array_ import contains
from ...fable_modules.fable_library.option import value
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import string_hash
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import (LDNode, LDGraph)
from .property_value import LDPropertyValue

def _expr1770() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDSample", None, LDSample)


class LDSample:
    @staticmethod
    def schema_type() -> str:
        return "https://bioschemas.org/Sample"

    @staticmethod
    def name() -> str:
        return "http://schema.org/name"

    @staticmethod
    def additional_property() -> str:
        return "http://schema.org/additionalProperty"

    @staticmethod
    def try_get_name_as_string(s: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = s.TryGetPropertyAsSingleton(LDSample.name(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_name_as_string(s: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = s.TryGetPropertyAsSingleton(LDSample.name(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            raise Exception(("Could not access property `name` of object with @id `" + s.Id) + "`")


    @staticmethod
    def set_name_as_string(s: LDNode, n: str) -> None:
        s.SetProperty(LDSample.name(), n)

    @staticmethod
    def get_additional_properties(s: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDPropertyValue.validate(ld_object, context_1)

        return s.GetPropertyNodes(LDSample.additional_property(), filter, graph, context)

    @staticmethod
    def set_additional_properties(s: LDNode, additional_properties: Array[LDNode], context: LDContext | None=None) -> Any:
        return s.SetProperty(LDSample.additional_property(), additional_properties, context)

    @staticmethod
    def get_characteristics(s: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDPropertyValue.validate_characteristic_value(ld_object, context_1)

        return s.GetPropertyNodes(LDSample.additional_property(), filter, graph, context)

    @staticmethod
    def get_factors(s: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDPropertyValue.validate_factor_value(ld_object, context_1)

        return s.GetPropertyNodes(LDSample.additional_property(), filter, graph, context)

    @staticmethod
    def validate(s: LDNode, context: LDContext | None=None) -> bool:
        return s.HasProperty(LDSample.name(), context) if s.HasType(LDSample.schema_type(), context) else False

    @staticmethod
    def gen_idsample(name: str) -> str:
        return clean(("#Sample_" + name) + "")

    @staticmethod
    def gen_idsource(name: str) -> str:
        return clean(("#Source_" + name) + "")

    @staticmethod
    def gen_idmaterial(name: str) -> str:
        return clean(("#Material_" + name) + "")

    @staticmethod
    def validate_sample(s: LDNode, context: LDContext | None=None) -> bool:
        class ObjectExpr1765:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1764(x: str, y: str) -> bool:
                    return x == y

                return _arrow1764

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        return contains("Sample", s.AdditionalType, ObjectExpr1765()) if LDSample.validate(s, context) else False

    @staticmethod
    def validate_source(s: LDNode, context: LDContext | None=None) -> bool:
        class ObjectExpr1767:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1766(x: str, y: str) -> bool:
                    return x == y

                return _arrow1766

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        return contains("Source", s.AdditionalType, ObjectExpr1767()) if LDSample.validate(s, context) else False

    @staticmethod
    def validate_material(s: LDNode, context: LDContext | None=None) -> bool:
        class ObjectExpr1769:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1768(x: str, y: str) -> bool:
                    return x == y

                return _arrow1768

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        return contains("Material", s.AdditionalType, ObjectExpr1769()) if LDSample.validate(s, context) else False

    @staticmethod
    def create(id: str, name: str, additional_properties: Array[LDNode] | None=None, context: LDContext | None=None) -> LDNode:
        s: LDNode = LDNode(id, [LDSample.schema_type()], None, context)
        s.SetProperty(LDSample.name(), name, context)
        s.SetOptionalProperty(LDSample.additional_property(), additional_properties, context)
        return s

    @staticmethod
    def create_sample(name: str, id: str | None=None, additional_properties: Array[LDNode] | None=None, context: LDContext | None=None) -> LDNode:
        id_2: str = LDSample.gen_idsample(name) if (id is None) else id
        s: LDNode = LDSample.create(id_2, name, additional_properties, context)
        s.AdditionalType = ["Sample"]
        return s

    @staticmethod
    def create_source(name: str, id: str | None=None, additional_properties: Array[LDNode] | None=None, context: LDContext | None=None) -> LDNode:
        id_2: str = LDSample.gen_idsource(name) if (id is None) else id
        s: LDNode = LDSample.create(id_2, name, additional_properties, context)
        s.AdditionalType = ["Source"]
        return s

    @staticmethod
    def create_material(name: str, id: str | None=None, additional_properties: Array[LDNode] | None=None, context: LDContext | None=None) -> LDNode:
        id_2: str = LDSample.gen_idmaterial(name) if (id is None) else id
        s: LDNode = LDSample.create(id_2, name, additional_properties, context)
        s.AdditionalType = ["Material"]
        return s


LDSample_reflection = _expr1770

__all__ = ["LDSample_reflection"]

