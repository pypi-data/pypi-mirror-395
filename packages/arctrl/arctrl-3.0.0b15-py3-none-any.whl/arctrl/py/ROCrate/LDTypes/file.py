from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.option import (value, default_arg)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import Array
from ..ldcontext import LDContext
from ..ldobject import (LDNode, LDGraph)
from .comment import LDComment
from .defined_term import LDDefinedTerm
from .formal_parameter import LDFormalParameter

def _expr1773() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDFile", None, LDFile)


class LDFile:
    @staticmethod
    def schema_type() -> str:
        return "http://schema.org/MediaObject"

    @staticmethod
    def name() -> str:
        return "http://schema.org/name"

    @staticmethod
    def comment() -> str:
        return "http://schema.org/comment"

    @staticmethod
    def disambiguating_description() -> str:
        return "http://schema.org/disambiguatingDescription"

    @staticmethod
    def usage_info() -> str:
        return "http://schema.org/usageInfo"

    @staticmethod
    def encoding_format() -> str:
        return "http://schema.org/encodingFormat"

    @staticmethod
    def pattern() -> str:
        return "http://schema.org/pattern"

    @staticmethod
    def about() -> str:
        return "http://schema.org/about"

    @staticmethod
    def example_of_work() -> str:
        return "http://schema.org/exampleOfWork"

    @staticmethod
    def try_get_name_as_string(dt: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = dt.TryGetPropertyAsSingleton(LDFile.name(), context)
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
        match_value: Any | None = dt.TryGetPropertyAsSingleton(LDFile.name(), context)
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
        return dt.SetProperty(LDFile.name(), name, context)

    @staticmethod
    def get_comments(dt: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDComment.validate(ld_object, context_1)

        return dt.GetPropertyNodes(LDFile.comment(), filter, graph, context)

    @staticmethod
    def set_comments(dt: LDNode, comment: Array[LDNode], context: LDContext | None=None) -> Any:
        return dt.SetProperty(LDFile.comment(), comment, context)

    @staticmethod
    def try_get_disambiguating_description_as_string(dt: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = dt.TryGetPropertyAsSingleton(LDFile.disambiguating_description(), context)
        (pattern_matching_result, dd) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                dd = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return dd

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_disambiguating_description_as_string(dt: LDNode, disambiguating_description: str, context: LDContext | None=None) -> Any:
        return dt.SetProperty(LDFile.disambiguating_description(), disambiguating_description, context)

    @staticmethod
    def try_get_encoding_format_as_string(dt: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = dt.TryGetPropertyAsSingleton(LDFile.encoding_format(), context)
        (pattern_matching_result, ef) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                ef = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return ef

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_encoding_format_as_string(dt: LDNode, encoding_format: str, context: LDContext | None=None) -> Any:
        return dt.SetProperty(LDFile.encoding_format(), encoding_format, context)

    @staticmethod
    def try_get_example_of_work(dt: LDNode, context: LDContext | None=None) -> Any | None:
        return dt.TryGetPropertyAsSingleton(LDFile.example_of_work(), context)

    @staticmethod
    def try_get_example_of_work_as_formal_parameter(dt: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = dt.TryGetPropertyAsSingleNode(LDFile.example_of_work(), graph, context)
        if match_value is not None:
            def _arrow1771(__unit: None=None) -> bool:
                fp: LDNode = match_value
                return LDFormalParameter.validate(fp, context)

            if _arrow1771():
                fp_1: LDNode = match_value
                return fp_1

            else: 
                raise Exception(("Property of `exampleOfWork` of object with @id `" + dt.Id) + "` was not a FormalParameter")


        else: 
            return None


    @staticmethod
    def set_example_of_work(pv: LDNode, example_of_work: LDNode, context: LDContext | None=None) -> Any:
        return pv.SetProperty(LDFile.example_of_work(), example_of_work, context)

    @staticmethod
    def try_get_usage_info_as_string(dt: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = dt.TryGetPropertyAsSingleton(LDFile.usage_info(), context)
        (pattern_matching_result, ui) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                ui = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return ui

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_usage_info_as_string(dt: LDNode, usage_info: str, context: LDContext | None=None) -> Any:
        return dt.SetProperty(LDFile.usage_info(), usage_info, context)

    @staticmethod
    def try_get_pattern_as_defined_term(dt: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = dt.TryGetPropertyAsSingleNode(LDFile.pattern(), graph, context)
        if match_value is not None:
            def _arrow1772(__unit: None=None) -> bool:
                dt_1: LDNode = match_value
                return LDDefinedTerm.validate(dt_1, context)

            if _arrow1772():
                dt_2: LDNode = match_value
                return dt_2

            else: 
                raise Exception(("Property of `pattern` of object with @id `" + dt.Id) + "` was not a DefinedTerm")


        else: 
            return None


    @staticmethod
    def set_pattern_as_defined_term(dt: LDNode, pattern: LDNode, context: LDContext | None=None) -> Any:
        return dt.SetProperty(LDFile.pattern(), pattern, context)

    @staticmethod
    def try_get_about(dt: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        return dt.TryGetPropertyAsSingleNode(LDFile.about(), graph, context)

    @staticmethod
    def set_about(dt: LDNode, about: LDNode, context: LDContext | None=None) -> Any:
        return dt.SetProperty(LDFile.about(), about, context)

    @staticmethod
    def gen_id(name: str) -> str:
        return ("" + name) + ""

    @staticmethod
    def validate(dt: LDNode, context: LDContext | None=None) -> bool:
        return dt.HasProperty(LDFile.name(), context) if dt.HasType(LDFile.schema_type(), context) else False

    @staticmethod
    def validate_cwlparameter(dt: LDNode, context: LDContext | None=None) -> bool:
        return dt.HasProperty(LDFile.example_of_work(), context) if LDFile.validate(dt, context) else False

    @staticmethod
    def create(name: str, id: str | None=None, comments: Array[LDNode] | None=None, disambiguating_description: str | None=None, encoding_format: str | None=None, usage_info: str | None=None, context: LDContext | None=None) -> LDNode:
        dt: LDNode = LDNode(LDFile.gen_id(name) if (id is None) else id, [LDFile.schema_type()], None, context)
        dt.SetProperty(LDFile.name(), name, context)
        dt.SetOptionalProperty(LDFile.comment(), comments, context)
        dt.SetOptionalProperty(LDFile.disambiguating_description(), disambiguating_description, context)
        dt.SetOptionalProperty(LDFile.encoding_format(), encoding_format, context)
        dt.SetOptionalProperty(LDFile.usage_info(), usage_info, context)
        return dt

    @staticmethod
    def create_cwlparameter(name: str, example_of_work: LDNode, id: str | None=None, context: LDContext | None=None) -> LDNode:
        dt: LDNode = LDNode(default_arg(id, name), [LDFile.schema_type()], None, context)
        dt.SetProperty(LDFile.name(), name, context)
        dt.SetProperty(LDFile.example_of_work(), example_of_work, context)
        return dt


LDFile_reflection = _expr1773

__all__ = ["LDFile_reflection"]

