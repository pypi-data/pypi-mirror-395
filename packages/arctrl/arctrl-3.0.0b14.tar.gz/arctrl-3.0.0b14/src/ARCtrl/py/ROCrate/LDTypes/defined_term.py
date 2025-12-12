from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.option import value
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import LDNode

def _expr1655() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDDefinedTerm", None, LDDefinedTerm)


class LDDefinedTerm:
    @staticmethod
    def schema_type() -> str:
        return "http://schema.org/DefinedTerm"

    @staticmethod
    def term_code() -> str:
        return "http://schema.org/termCode"

    @staticmethod
    def name() -> str:
        return "http://schema.org/name"

    @staticmethod
    def try_get_term_code_as_string(dt: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = dt.TryGetPropertyAsSingleton(LDDefinedTerm.term_code(), context)
        (pattern_matching_result, tc) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                tc = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return tc

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_term_code_as_string(dt: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = dt.TryGetPropertyAsSingleton(LDDefinedTerm.term_code(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                tc: str = value(match_value)
                return tc

            else: 
                raise Exception(("Property of `termCode` of object with @id `" + dt.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `termCode` of object with @id `" + dt.Id) + "`")


    @staticmethod
    def set_term_code_as_string(dt: LDNode, term_code: str, context: LDContext | None=None) -> Any:
        return dt.SetProperty(LDDefinedTerm.term_code(), term_code, context)

    @staticmethod
    def try_get_name_as_string(dt: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = dt.TryGetPropertyAsSingleton(LDDefinedTerm.name(), context)
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
    def get_name_as_string(dt: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = dt.TryGetPropertyAsSingleton(LDDefinedTerm.name(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                n: str = value(match_value)
                return n

            else: 
                raise Exception(("Property of `name` of object with @id `" + dt.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `name` of object with @id `" + dt.Id) + "`")


    @staticmethod
    def set_name_as_string(dt: LDNode, name: str, context: LDContext | None=None) -> Any:
        return dt.SetProperty(LDDefinedTerm.name(), name, context)

    @staticmethod
    def gen_id(name: str, term_code: str | None=None) -> str:
        return clean(("#OA_" + name) + "") if (term_code is None) else (("" + term_code) + "")

    @staticmethod
    def validate(dt: LDNode, context: LDContext | None=None) -> bool:
        return dt.HasProperty(LDDefinedTerm.name(), context) if dt.HasType(LDDefinedTerm.schema_type(), context) else False

    @staticmethod
    def create(name: str, id: str | None=None, term_code: str | None=None, context: LDContext | None=None) -> LDNode:
        dt: LDNode = LDNode(LDDefinedTerm.gen_id(name, term_code) if (id is None) else id, [LDDefinedTerm.schema_type()], None, context)
        dt.SetProperty(LDDefinedTerm.name(), name, context)
        dt.SetOptionalProperty(LDDefinedTerm.term_code(), term_code, context)
        return dt


LDDefinedTerm_reflection = _expr1655

__all__ = ["LDDefinedTerm_reflection"]

