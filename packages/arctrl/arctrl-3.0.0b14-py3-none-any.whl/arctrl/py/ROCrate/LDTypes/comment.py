from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.option import value
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import LDNode

def _expr1654() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDComment", None, LDComment)


class LDComment:
    @staticmethod
    def schema_type() -> str:
        return "http://schema.org/Comment"

    @staticmethod
    def text() -> str:
        return "http://schema.org/text"

    @staticmethod
    def name() -> str:
        return "http://schema.org/name"

    @staticmethod
    def try_get_text_as_string(dt: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = dt.TryGetPropertyAsSingleton(LDComment.text(), context)
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
    def get_text_as_string(dt: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = dt.TryGetPropertyAsSingleton(LDComment.text(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                tc: str = value(match_value)
                return tc

            else: 
                raise Exception(("Property of `text` of object with @id `" + dt.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `text` of object with @id `" + dt.Id) + "`")


    @staticmethod
    def set_text_as_string(dt: LDNode, text: str, context: LDContext | None=None) -> Any:
        return dt.SetProperty(LDComment.text(), text, context)

    @staticmethod
    def try_get_name_as_string(dt: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = dt.TryGetPropertyAsSingleton(LDComment.name(), context)
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
        match_value: Any | None = dt.TryGetPropertyAsSingleton(LDComment.name(), context)
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
        return dt.SetProperty(LDComment.name(), name, context)

    @staticmethod
    def gen_id(name: str, text: str | None=None) -> str:
        return clean((("#LDComment_" + name) + "") if (text is None) else (((("#LDComment_" + name) + "_") + text) + ""))

    @staticmethod
    def validate(dt: LDNode, context: LDContext | None=None) -> bool:
        return dt.HasProperty(LDComment.name(), context) if dt.HasType(LDComment.schema_type(), context) else False

    @staticmethod
    def create(name: str, id: str | None=None, text: str | None=None, context: LDContext | None=None) -> LDNode:
        dt: LDNode = LDNode(LDComment.gen_id(name, text) if (id is None) else id, [LDComment.schema_type()], None, context)
        dt.SetProperty(LDComment.name(), name, context)
        dt.SetOptionalProperty(LDComment.text(), text, context)
        return dt


LDComment_reflection = _expr1654

__all__ = ["LDComment_reflection"]

