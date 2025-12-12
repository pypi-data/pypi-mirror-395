from __future__ import annotations
from collections.abc import Callable
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
from .formal_parameter import LDFormalParameter
from .organization import LDOrganization
from .person import LDPerson

def _expr1789() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDComputationalWorkflow", None, LDComputationalWorkflow)


class LDComputationalWorkflow:
    @staticmethod
    def schema_type() -> str:
        return "https://bioschemas.org/ComputationalWorkflow"

    @staticmethod
    def input() -> str:
        return "https://bioschemas.org/properties/input"

    @staticmethod
    def input_deprecated() -> str:
        return "https://bioschemas.org/input"

    @staticmethod
    def output() -> str:
        return "https://bioschemas.org/properties/output"

    @staticmethod
    def output_deprecated() -> str:
        return "https://bioschemas.org/output"

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
    def additional_type() -> str:
        return "http://schema.org/additionalType"

    @staticmethod
    def comment() -> str:
        return "http://schema.org/comment"

    @staticmethod
    def get_inputs(cw: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        l: Array[LDNode] = cw.GetPropertyNodes(LDComputationalWorkflow.input(), None, graph, context)
        return cw.GetPropertyNodes(LDComputationalWorkflow.input_deprecated(), None, graph, context) if (len(l) == 0) else l

    @staticmethod
    def get_inputs_as_formal_parameters(cw: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDFormalParameter.validate(ld_object, context_1)

        l: Array[LDNode] = cw.GetPropertyNodes(LDComputationalWorkflow.input(), filter, graph, context)
        return cw.GetPropertyNodes(LDComputationalWorkflow.input_deprecated(), filter, graph, context) if (len(l) == 0) else l

    @staticmethod
    def set_inputs(cw: LDNode, inputs: Array[LDNode], context: LDContext | None=None) -> Any:
        return cw.SetProperty(LDComputationalWorkflow.input(), inputs, context)

    @staticmethod
    def get_outputs(cw: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        l: Array[LDNode] = cw.GetPropertyNodes(LDComputationalWorkflow.output(), None, graph, context)
        return cw.GetPropertyNodes(LDComputationalWorkflow.output_deprecated(), None, graph, context) if (len(l) == 0) else l

    @staticmethod
    def get_outputs_as_formal_parameter(cw: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDFormalParameter.validate(ld_object, context_1)

        l: Array[LDNode] = cw.GetPropertyNodes(LDComputationalWorkflow.output(), filter, graph, context)
        return cw.GetPropertyNodes(LDComputationalWorkflow.output_deprecated(), filter, graph, context) if (len(l) == 0) else l

    @staticmethod
    def set_outputs(cw: LDNode, outputs: Array[LDNode], context: LDContext | None=None) -> Any:
        return cw.SetProperty(LDComputationalWorkflow.output(), outputs, context)

    @staticmethod
    def get_creator(cw: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            if LDPerson.validate(ld_object, context_1):
                return True

            else: 
                return LDOrganization.validate(ld_object, context_1)


        return cw.GetPropertyNodes(LDComputationalWorkflow.creator(), filter, graph, context)

    @staticmethod
    def set_creator(cw: LDNode, creator: LDNode, context: LDContext | None=None) -> Any:
        return cw.SetProperty(LDComputationalWorkflow.creator(), creator, context)

    @staticmethod
    def try_get_date_created(cw: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = cw.TryGetPropertyAsSingleton(LDComputationalWorkflow.date_created(), context)
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
    def set_date_created(cw: LDNode, date: str, context: LDContext | None=None) -> Any:
        return cw.SetProperty(LDComputationalWorkflow.date_created(), date, context)

    @staticmethod
    def get_licenses(cw: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return cw.GetPropertyNodes(LDComputationalWorkflow.license(), None, graph, context)

    @staticmethod
    def set_licenses(cw: LDNode, licenses: Array[LDNode], context: LDContext | None=None) -> Any:
        return cw.SetProperty(LDComputationalWorkflow.license(), licenses, context)

    @staticmethod
    def try_get_name_as_string(cw: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = cw.TryGetPropertyAsSingleton(LDComputationalWorkflow.name(), context)
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
    def get_name_as_string(cw: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = cw.TryGetPropertyAsSingleton(LDComputationalWorkflow.name(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                n: str = value(match_value)
                return n

            else: 
                raise Exception(("property `name` of object with @id `" + cw.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `name` of object with @id `" + cw.Id) + "`")


    @staticmethod
    def set_name_as_string(cw: LDNode, name: str, context: LDContext | None=None) -> Any:
        return cw.SetProperty(LDComputationalWorkflow.name(), name, context)

    @staticmethod
    def get_programming_languages(cw: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return cw.GetPropertyNodes(LDComputationalWorkflow.programming_language(), None, graph, context)

    @staticmethod
    def set_programming_languages(cw: LDNode, programming_languages: Array[LDNode], context: LDContext | None=None) -> Any:
        return cw.SetProperty(LDComputationalWorkflow.programming_language(), programming_languages, context)

    @staticmethod
    def try_get_sd_publisher(cw: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = cw.TryGetPropertyAsSingleNode(LDComputationalWorkflow.sd_publisher(), graph, context)
        (pattern_matching_result, a_1) = (None, None)
        if match_value is not None:
            def _arrow1788(__unit: None=None) -> bool:
                ld_object: LDNode = match_value
                context_1: LDContext | None = context
                return True if LDPerson.validate(ld_object, context_1) else LDOrganization.validate(ld_object, context_1)

            if _arrow1788():
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
    def set_sd_publisher(cw: LDNode, sd_publisher: LDNode, context: LDContext | None=None) -> Any:
        return cw.SetProperty(LDComputationalWorkflow.sd_publisher(), sd_publisher, context)

    @staticmethod
    def try_get_url(cw: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = cw.TryGetPropertyAsSingleton(LDComputationalWorkflow.url(), context)
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
    def set_url(cw: LDNode, url: str, context: LDContext | None=None) -> Any:
        return cw.SetProperty(LDComputationalWorkflow.url(), url, context)

    @staticmethod
    def try_get_version(cw: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = cw.TryGetPropertyAsSingleton(LDComputationalWorkflow.version(), context)
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
    def set_version(cw: LDNode, version: str, context: LDContext | None=None) -> Any:
        return cw.SetProperty(LDComputationalWorkflow.version(), version, context)

    @staticmethod
    def try_get_description(cw: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = cw.TryGetPropertyAsSingleton(LDComputationalWorkflow.description(), context)
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
    def set_description(cw: LDNode, description: str, context: LDContext | None=None) -> Any:
        return cw.SetProperty(LDComputationalWorkflow.description(), description, context)

    @staticmethod
    def get_has_part(cw: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return cw.GetPropertyNodes(LDComputationalWorkflow.has_part(), None, graph, context)

    @staticmethod
    def set_has_part(cw: LDNode, has_parts: FSharpList[str], context: LDContext | None=None) -> Any:
        return cw.SetProperty(LDComputationalWorkflow.has_part(), list(has_parts), context)

    @staticmethod
    def try_get_additional_type_as_string(cw: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = cw.TryGetPropertyAsSingleton(LDComputationalWorkflow.additional_type(), context)
        (pattern_matching_result, at) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                at = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return at

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_additional_type_as_string(cw: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = cw.TryGetPropertyAsSingleton(LDComputationalWorkflow.additional_type(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                at: str = value(match_value)
                return at

            else: 
                raise Exception(("property `additionalType` of object with @id `" + cw.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `additionalType` of object with @id `" + cw.Id) + "`")


    @staticmethod
    def set_additional_type_as_string(cw: LDNode, additional_type: str, context: LDContext | None=None) -> Any:
        return cw.SetProperty(LDComputationalWorkflow.additional_type(), additional_type, context)

    @staticmethod
    def get_comments(cw: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDComment.validate(ld_object, context_1)

        return cw.GetPropertyNodes(LDComputationalWorkflow.comment(), filter, graph, context)

    @staticmethod
    def set_comments(cw: LDNode, comments: Array[LDNode], context: LDContext | None=None) -> Any:
        return cw.SetProperty(LDComputationalWorkflow.comment(), comments, context)

    @staticmethod
    def validate(lp: LDNode, context: LDContext | None=None) -> bool:
        return lp.HasType(LDComputationalWorkflow.schema_type(), context)

    @staticmethod
    def create(id: str | None=None, inputs: Array[LDNode] | None=None, outputs: Array[LDNode] | None=None, creator: LDNode | None=None, date_created: str | None=None, licenses: Array[LDNode] | None=None, name: str | None=None, programming_languages: Array[LDNode] | None=None, sd_publisher: LDNode | None=None, url: str | None=None, version: str | None=None, description: str | None=None, has_parts: Array[LDNode] | None=None, comments: Array[LDNode] | None=None, context: LDContext | None=None) -> LDNode:
        cw: LDNode = LDNode(clean(("#ComputationalWorkflow_" + create_missing_identifier()) + "") if (id is None) else id, [LDComputationalWorkflow.schema_type()], None, context)
        cw.SetOptionalProperty(LDComputationalWorkflow.input(), inputs, context)
        cw.SetOptionalProperty(LDComputationalWorkflow.output(), outputs, context)
        cw.SetOptionalProperty(LDComputationalWorkflow.creator(), creator, context)
        cw.SetOptionalProperty(LDComputationalWorkflow.date_created(), date_created, context)
        cw.SetOptionalProperty(LDComputationalWorkflow.license(), licenses, context)
        cw.SetOptionalProperty(LDComputationalWorkflow.name(), name, context)
        cw.SetOptionalProperty(LDComputationalWorkflow.programming_language(), programming_languages, context)
        cw.SetOptionalProperty(LDComputationalWorkflow.sd_publisher(), sd_publisher, context)
        cw.SetOptionalProperty(LDComputationalWorkflow.url(), url, context)
        cw.SetOptionalProperty(LDComputationalWorkflow.version(), version, context)
        cw.SetOptionalProperty(LDComputationalWorkflow.description(), description, context)
        cw.SetOptionalProperty(LDComputationalWorkflow.has_part(), has_parts, context)
        cw.SetOptionalProperty(LDComputationalWorkflow.comment(), comments, context)
        return cw


LDComputationalWorkflow_reflection = _expr1789

__all__ = ["LDComputationalWorkflow_reflection"]

