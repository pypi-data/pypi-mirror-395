from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.option import value
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import LDNode

def _expr1730() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDOrganization", None, LDOrganization)


class LDOrganization:
    @staticmethod
    def schema_type() -> str:
        return "http://schema.org/Organization"

    @staticmethod
    def name() -> str:
        return "http://schema.org/name"

    @staticmethod
    def try_get_name_as_string(o: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = o.TryGetPropertyAsSingleton(LDOrganization.name(), context)
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
    def get_name_as_string(o: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = o.TryGetPropertyAsSingleton(LDOrganization.name(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                n: str = value(match_value)
                return n

            else: 
                raise Exception(("Property of `name` of object with @id `" + o.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `name` of object with @id `" + o.Id) + "`")


    @staticmethod
    def set_name_as_string(o: LDNode, n: str, context: LDContext | None=None) -> Any:
        return o.SetProperty(LDOrganization.name(), n, context)

    @staticmethod
    def gen_id(name: str) -> str:
        return clean(("#Organization_" + name) + "")

    @staticmethod
    def validate(o: LDNode, context: LDContext | None=None) -> bool:
        return o.HasProperty(LDOrganization.name(), context) if o.HasType(LDOrganization.schema_type(), context) else False

    @staticmethod
    def create(name: str, id: str | None=None, context: LDContext | None=None) -> LDNode:
        o: LDNode = LDNode(LDOrganization.gen_id(name) if (id is None) else id, [LDOrganization.schema_type()], None, context)
        o.SetProperty(LDOrganization.name(), name, context)
        return o


LDOrganization_reflection = _expr1730

__all__ = ["LDOrganization_reflection"]

