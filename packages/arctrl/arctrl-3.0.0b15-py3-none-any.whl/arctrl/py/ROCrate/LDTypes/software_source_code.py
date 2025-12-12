from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.list import FSharpList
from ...fable_modules.fable_library.option import value
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import Array
from ...Core.Helper.identifier import create_missing_identifier
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import (LDNode, LDGraph)
from .comment import LDComment
from .organization import LDOrganization
from .person import LDPerson

def _expr1794() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDSoftwareSourceCode", None, LDSoftwareSourceCode)


class LDSoftwareSourceCode:
    @staticmethod
    def schema_type() -> str:
        return "http://schema.org/SoftwareSourceCode"

    @staticmethod
    def creator() -> str:
        return "http://schema.org/creator"

    @staticmethod
    def date_created() -> str:
        return "http://schema.org/dateCreated"

    @staticmethod
    def license() -> str:
        return "http://schema.org/license"

    @staticmethod
    def name() -> str:
        return "http://schema.org/name"

    @staticmethod
    def programming_language() -> str:
        return "http://schema.org/programmingLanguage"

    @staticmethod
    def sd_publisher() -> str:
        return "http://schema.org/sdPublisher"

    @staticmethod
    def url() -> str:
        return "http://schema.org/url"

    @staticmethod
    def version() -> str:
        return "http://schema.org/version"

    @staticmethod
    def description() -> str:
        return "http://schema.org/description"

    @staticmethod
    def has_part() -> str:
        return "http://schema.org/hasPart"

    @staticmethod
    def comment() -> str:
        return "http://schema.org/comment"

    @staticmethod
    def get_creator(ssc: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            if LDPerson.validate(ld_object, context_1):
                return True

            else: 
                return LDOrganization.validate(ld_object, context_1)


        return ssc.GetPropertyNodes(LDSoftwareSourceCode.creator(), filter, graph, context)

    @staticmethod
    def set_creator(ssc: LDNode, creator: LDNode, context: LDContext | None=None) -> Any:
        return ssc.SetProperty(LDSoftwareSourceCode.creator(), creator, context)

    @staticmethod
    def try_get_date_created(ssc: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = ssc.TryGetPropertyAsSingleton(LDSoftwareSourceCode.date_created(), context)
        (pattern_matching_result, d) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                d = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return d

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_date_created(ssc: LDNode, date: str, context: LDContext | None=None) -> Any:
        return ssc.SetProperty(LDSoftwareSourceCode.date_created(), date, context)

    @staticmethod
    def get_licenses(ssc: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return ssc.GetPropertyNodes(LDSoftwareSourceCode.license(), None, graph, context)

    @staticmethod
    def set_licenses(ssc: LDNode, licenses: Array[LDNode], context: LDContext | None=None) -> Any:
        return ssc.SetProperty(LDSoftwareSourceCode.license(), licenses, context)

    @staticmethod
    def try_get_name_as_string(ssc: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = ssc.TryGetPropertyAsSingleton(LDSoftwareSourceCode.name(), context)
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
    def set_name_as_string(ssc: LDNode, name: str, context: LDContext | None=None) -> Any:
        return ssc.SetProperty(LDSoftwareSourceCode.name(), name, context)

    @staticmethod
    def get_programming_languages(ssc: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return ssc.GetPropertyNodes(LDSoftwareSourceCode.programming_language(), None, graph, context)

    @staticmethod
    def set_programming_languages(ssc: LDNode, programming_languages: Array[LDNode], context: LDContext | None=None) -> Any:
        return ssc.SetProperty(LDSoftwareSourceCode.programming_language(), programming_languages, context)

    @staticmethod
    def try_get_sd_publisher(ssc: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = ssc.TryGetPropertyAsSingleNode(LDSoftwareSourceCode.sd_publisher(), graph, context)
        (pattern_matching_result, a_1) = (None, None)
        if match_value is not None:
            def _arrow1793(__unit: None=None) -> bool:
                ld_object: LDNode = match_value
                context_1: LDContext | None = context
                return True if LDPerson.validate(ld_object, context_1) else LDOrganization.validate(ld_object, context_1)

            if _arrow1793():
                pattern_matching_result = 0
                a_1 = match_value

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return a_1

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_sd_publisher(ssc: LDNode, sd_publisher: LDNode, context: LDContext | None=None) -> Any:
        return ssc.SetProperty(LDSoftwareSourceCode.sd_publisher(), sd_publisher, context)

    @staticmethod
    def try_get_url(ssc: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = ssc.TryGetPropertyAsSingleton(LDSoftwareSourceCode.url(), context)
        (pattern_matching_result, u) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                u = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return u

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_url(ssc: LDNode, url: str, context: LDContext | None=None) -> Any:
        return ssc.SetProperty(LDSoftwareSourceCode.url(), url, context)

    @staticmethod
    def try_get_version(ssc: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = ssc.TryGetPropertyAsSingleton(LDSoftwareSourceCode.version(), context)
        (pattern_matching_result, v) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                v = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return v

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_version(ssc: LDNode, version: str, context: LDContext | None=None) -> Any:
        return ssc.SetProperty(LDSoftwareSourceCode.version(), version, context)

    @staticmethod
    def try_get_description(ssc: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = ssc.TryGetPropertyAsSingleton(LDSoftwareSourceCode.description(), context)
        (pattern_matching_result, d) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                d = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return d

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_description(ssc: LDNode, description: str, context: LDContext | None=None) -> Any:
        return ssc.SetProperty(LDSoftwareSourceCode.description(), description, context)

    @staticmethod
    def get_has_part(ssc: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return ssc.GetPropertyNodes(LDSoftwareSourceCode.has_part(), None, graph, context)

    @staticmethod
    def set_has_part(ssc: LDNode, has_parts: FSharpList[str], context: LDContext | None=None) -> Any:
        return ssc.SetProperty(LDSoftwareSourceCode.has_part(), list(has_parts), context)

    @staticmethod
    def get_comments(ssc: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDComment.validate(ld_object, context_1)

        return ssc.GetPropertyNodes(LDSoftwareSourceCode.comment(), filter, graph, context)

    @staticmethod
    def set_comments(ssc: LDNode, comments: Array[LDNode], context: LDContext | None=None) -> Any:
        return ssc.SetProperty(LDSoftwareSourceCode.comment(), comments, context)

    @staticmethod
    def validate(lp: LDNode, context: LDContext | None=None) -> bool:
        return lp.HasType(LDSoftwareSourceCode.schema_type(), context)

    @staticmethod
    def create(id: str | None=None, creator: LDNode | None=None, date_created: str | None=None, licenses: Array[LDNode] | None=None, name: str | None=None, programming_languages: Array[LDNode] | None=None, sd_publisher: LDNode | None=None, url: str | None=None, version: str | None=None, description: str | None=None, has_parts: Array[LDNode] | None=None, comments: Array[LDNode] | None=None, context: LDContext | None=None) -> LDNode:
        ssc: LDNode = LDNode(clean(("#ComputationalWorkflow_" + create_missing_identifier()) + "") if (id is None) else id, [LDSoftwareSourceCode.schema_type()], None, context)
        ssc.SetOptionalProperty(LDSoftwareSourceCode.creator(), creator, context)
        ssc.SetOptionalProperty(LDSoftwareSourceCode.date_created(), date_created, context)
        ssc.SetOptionalProperty(LDSoftwareSourceCode.license(), licenses, context)
        ssc.SetOptionalProperty(LDSoftwareSourceCode.name(), name, context)
        ssc.SetOptionalProperty(LDSoftwareSourceCode.programming_language(), programming_languages, context)
        ssc.SetOptionalProperty(LDSoftwareSourceCode.sd_publisher(), sd_publisher, context)
        ssc.SetOptionalProperty(LDSoftwareSourceCode.url(), url, context)
        ssc.SetOptionalProperty(LDSoftwareSourceCode.version(), version, context)
        ssc.SetOptionalProperty(LDSoftwareSourceCode.description(), description, context)
        ssc.SetOptionalProperty(LDSoftwareSourceCode.has_part(), has_parts, context)
        ssc.SetOptionalProperty(LDSoftwareSourceCode.comment(), comments, context)
        return ssc


LDSoftwareSourceCode_reflection = _expr1794

__all__ = ["LDSoftwareSourceCode_reflection"]

