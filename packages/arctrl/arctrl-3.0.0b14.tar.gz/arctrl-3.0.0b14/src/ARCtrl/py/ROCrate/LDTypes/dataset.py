from __future__ import annotations
from collections.abc import Callable
from datetime import datetime
from typing import Any
from ...fable_modules.fable_library.array_ import contains
from ...fable_modules.fable_library.option import value as value_1
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.resize_array import exists
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import string_hash
from ...Core.Helper.collections_ import ResizeArray_tryPick
from ..ldcontext import LDContext
from ..ldobject import (LDNode, LDGraph)
from .comment import LDComment
from .creative_work import LDCreativeWork
from .defined_term import LDDefinedTerm
from .file import LDFile
from .lab_process import LDLabProcess
from .person import LDPerson
from .property_value import LDPropertyValue
from .scholarly_article import LDScholarlyArticle
from .workflow_invocation import LDWorkflowInvocation
from .workflow_protocol import LDWorkflowProtocol

def _expr1832() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDDataset", None, LDDataset)


class LDDataset:
    @staticmethod
    def schema_type() -> str:
        return "http://schema.org/Dataset"

    @staticmethod
    def identifier() -> str:
        return "http://schema.org/identifier"

    @staticmethod
    def creator() -> str:
        return "http://schema.org/creator"

    @staticmethod
    def date_created() -> str:
        return "http://schema.org/dateCreated"

    @staticmethod
    def date_published() -> str:
        return "http://schema.org/datePublished"

    @staticmethod
    def sd_date_published() -> str:
        return "http://schema.org/datePublished"

    @staticmethod
    def license() -> str:
        return "http://schema.org/license"

    @staticmethod
    def date_modified() -> str:
        return "http://schema.org/dateModified"

    @staticmethod
    def description() -> str:
        return "http://schema.org/description"

    @staticmethod
    def has_part() -> str:
        return "http://schema.org/hasPart"

    @staticmethod
    def headline() -> str:
        return "http://schema.org/headline"

    @staticmethod
    def name() -> str:
        return "http://schema.org/name"

    @staticmethod
    def citation() -> str:
        return "http://schema.org/citation"

    @staticmethod
    def comment() -> str:
        return "http://schema.org/comment"

    @staticmethod
    def mentions() -> str:
        return "http://schema.org/mentions"

    @staticmethod
    def url() -> str:
        return "http://schema.org/url"

    @staticmethod
    def about() -> str:
        return "http://schema.org/about"

    @staticmethod
    def measurement_method() -> str:
        return "http://schema.org/measurementMethod"

    @staticmethod
    def measurement_technique() -> str:
        return "http://schema.org/measurementTechnique"

    @staticmethod
    def variable_measured() -> str:
        return "http://schema.org/variableMeasured"

    @staticmethod
    def main_entity() -> str:
        return "http://schema.org/mainEntity"

    @staticmethod
    def try_get_identifier_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.identifier(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_identifier_as_string(lp: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.identifier(), context)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                n: str = value_1(match_value)
                return n

            else: 
                raise Exception(("property `identifier` of object with @id `" + lp.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `identifier` of object with @id `" + lp.Id) + "`")


    @staticmethod
    def set_identifier_as_string(lp: LDNode, identifier: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.identifier(), identifier, context)

    @staticmethod
    def get_creators(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(p: LDNode, ctx: LDContext | None=None) -> bool:
            return LDPerson.validate(p, ctx)

        return lp.GetPropertyNodes(LDDataset.creator(), filter, graph, context)

    @staticmethod
    def set_creators(lp: LDNode, creators: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.creator(), creators, context)

    @staticmethod
    def try_get_date_created_as_date_time(lp: LDNode, context: LDContext | None=None) -> Any | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.date_created(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if isinstance(value_1(match_value), datetime):
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_date_created_as_date_time(lp: LDNode, date_created: Any, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.date_created(), date_created, context)

    @staticmethod
    def try_get_date_published_as_date_time(lp: LDNode, context: LDContext | None=None) -> Any | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.date_published(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if isinstance(value_1(match_value), datetime):
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_date_published_as_date_time(lp: LDNode, date_published: Any, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.date_published(), date_published, context)

    @staticmethod
    def try_get_sddate_published_as_date_time(lp: LDNode, context: LDContext | None=None) -> Any | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.sd_date_published(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if isinstance(value_1(match_value), datetime):
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_sddate_published_as_date_time(lp: LDNode, sd_date_published: Any, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.sd_date_published(), sd_date_published, context)

    @staticmethod
    def try_get_license_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.license(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def try_get_license_as_creative_work(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = lp.TryGetPropertyAsSingleNode(LDDataset.license(), graph, context)
        (pattern_matching_result, n_1) = (None, None)
        if match_value is not None:
            def _arrow1811(__unit: None=None) -> bool:
                n: LDNode = match_value
                return LDCreativeWork.validate(n, context)

            if _arrow1811():
                pattern_matching_result = 0
                n_1 = match_value

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n_1

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_license_as_string(lp: LDNode, license: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.license(), license, context)

    @staticmethod
    def set_license_as_creative_work(lp: LDNode, license: Any=None, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.license(), license, context)

    @staticmethod
    def try_get_date_modified_as_date_time(lp: LDNode, context: LDContext | None=None) -> Any | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.date_modified(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if isinstance(value_1(match_value), datetime):
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_date_modified_as_date_time(lp: LDNode, date_modified: Any, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.date_modified(), date_modified, context)

    @staticmethod
    def try_get_description_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.description(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_description_as_string(lp: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.description(), context)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                n: str = value_1(match_value)
                return n

            else: 
                raise Exception(("property `description` of object with @id `" + lp.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `description` of object with @id `" + lp.Id) + "`")


    @staticmethod
    def set_description_as_string(lp: LDNode, description: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.description(), description, context)

    @staticmethod
    def get_has_parts(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return lp.GetPropertyNodes(LDDataset.has_part(), None, graph, context)

    @staticmethod
    def get_has_parts_as_dataset(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ldnode: LDNode, context_1: LDContext | None=None) -> bool:
            return LDDataset.validate(ldnode, context_1)

        return lp.GetPropertyNodes(LDDataset.has_part(), filter, graph, context)

    @staticmethod
    def get_has_parts_as_file(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ldnode: LDNode, context_1: LDContext | None=None) -> bool:
            return LDFile.validate(ldnode, context_1)

        return lp.GetPropertyNodes(LDDataset.has_part(), filter, graph, context)

    @staticmethod
    def set_has_parts(lp: LDNode, has_parts: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.has_part(), has_parts, context)

    @staticmethod
    def try_get_headline_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.headline(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def try_get_name_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.name(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_name_as_string(lp: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.name(), context)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                n: str = value_1(match_value)
                return n

            else: 
                raise Exception(("property `name` of object with @id `" + lp.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `name` of object with @id `" + lp.Id) + "`")


    @staticmethod
    def set_name_as_string(lp: LDNode, name: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.name(), name, context)

    @staticmethod
    def get_citations(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ldnode: LDNode, context_1: LDContext | None=None) -> bool:
            return LDScholarlyArticle.validate(ldnode, context_1)

        return lp.GetPropertyNodes(LDDataset.citation(), filter, graph, context)

    @staticmethod
    def set_citations(lp: LDNode, citations: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.citation(), citations, context)

    @staticmethod
    def get_comments(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ldnode: LDNode, context_1: LDContext | None=None) -> bool:
            return LDComment.validate(ldnode, context_1)

        return lp.GetPropertyNodes(LDDataset.comment(), filter, graph, context)

    @staticmethod
    def set_comments(lp: LDNode, comments: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.comment(), comments, context)

    @staticmethod
    def try_get_url_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.url(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def get_url_as_string(lp: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.url(), context)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                n: str = value_1(match_value)
                return n

            else: 
                raise Exception(("property `url` of object with @id `" + lp.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `url` of object with @id `" + lp.Id) + "`")


    @staticmethod
    def set_url_as_string(lp: LDNode, url: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.url(), url, context)

    @staticmethod
    def get_abouts(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return lp.GetPropertyNodes(LDDataset.about(), None, graph, context)

    @staticmethod
    def get_abouts_as_lab_process(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ldnode: LDNode, context_1: LDContext | None=None) -> bool:
            return LDLabProcess.validate(ldnode, context_1)

        return lp.GetPropertyNodes(LDDataset.about(), filter, graph, context)

    @staticmethod
    def get_abouts_as_workflow_invocation(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ldnode: LDNode, context_1: LDContext | None=None) -> bool:
            return LDWorkflowInvocation.validate(ldnode, context_1)

        return lp.GetPropertyNodes(LDDataset.about(), filter, graph, context)

    @staticmethod
    def set_abouts(lp: LDNode, abouts: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.about(), abouts, context)

    @staticmethod
    def try_get_measurement_method_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.measurement_method(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def try_get_measurement_method_as_defined_term(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = lp.TryGetPropertyAsSingleNode(LDDataset.measurement_method(), graph, context)
        (pattern_matching_result, n_1) = (None, None)
        if match_value is not None:
            def _arrow1813(__unit: None=None) -> bool:
                n: LDNode = match_value
                return LDDefinedTerm.validate(n, context)

            if _arrow1813():
                pattern_matching_result = 0
                n_1 = match_value

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n_1

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_measurement_method_as_string(lp: LDNode, measurement_method: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.measurement_method(), measurement_method, context)

    @staticmethod
    def set_measurement_method_as_defined_term(lp: LDNode, measurement_method: LDNode, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.measurement_method(), measurement_method, context)

    @staticmethod
    def try_get_measurement_technique_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.measurement_technique(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def try_get_measurement_technique_as_defined_term(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = lp.TryGetPropertyAsSingleNode(LDDataset.measurement_technique(), graph, context)
        (pattern_matching_result, n_1) = (None, None)
        if match_value is not None:
            def _arrow1815(__unit: None=None) -> bool:
                n: LDNode = match_value
                return LDDefinedTerm.validate(n, context)

            if _arrow1815():
                pattern_matching_result = 0
                n_1 = match_value

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n_1

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_measurement_technique_as_string(lp: LDNode, measurement_technique: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.measurement_technique(), measurement_technique, context)

    @staticmethod
    def set_measurement_technique_as_defined_term(lp: LDNode, measurement_technique: LDNode, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.measurement_technique(), measurement_technique, context)

    @staticmethod
    def try_get_variable_measured_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDDataset.variable_measured(), context)
        (pattern_matching_result, n) = (None, None)
        if match_value is not None:
            if str(type(value_1(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                n = value_1(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def try_get_variable_measured_as_property_value(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = lp.TryGetPropertyAsSingleNode(LDDataset.variable_measured(), graph, context)
        (pattern_matching_result, n_1) = (None, None)
        if match_value is not None:
            def _arrow1817(__unit: None=None) -> bool:
                n: LDNode = match_value
                return LDPropertyValue.validate(n, context)

            if _arrow1817():
                pattern_matching_result = 0
                n_1 = match_value

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return n_1

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def try_get_variable_measured_as_measurement_type(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        def f(n: LDNode) -> LDNode | None:
            if not LDPropertyValue.validate_fragment_descriptor(n, context):
                return n

            else: 
                return None


        return ResizeArray_tryPick(f, lp.GetPropertyNodes(LDDataset.variable_measured(), None, graph, context))

    @staticmethod
    def get_variable_measured_as_fragment_descriptors(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ldnode: LDNode, context_1: LDContext | None=None) -> bool:
            return LDPropertyValue.validate_fragment_descriptor(ldnode, context_1)

        return lp.GetPropertyNodes(LDDataset.variable_measured(), filter, graph, context)

    @staticmethod
    def set_variable_measured_as_string(lp: LDNode, variable_measured: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.variable_measured(), variable_measured, context)

    @staticmethod
    def set_variable_measured_as_property_value(lp: LDNode, variable_measured: LDNode, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.variable_measured(), variable_measured, context)

    @staticmethod
    def set_variable_measured_as_property_values(lp: LDNode, variable_measured: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.variable_measured(), variable_measured, context)

    @staticmethod
    def get_main_entities(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return lp.GetPropertyNodes(LDDataset.main_entity(), None, graph, context)

    @staticmethod
    def set_main_entities(lp: LDNode, main_entities: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDDataset.main_entity(), main_entities, context)

    @staticmethod
    def gen_idinvesigation(__unit: None=None) -> str:
        return "./"

    @staticmethod
    def gen_idstudy(identifier: str) -> str:
        return ("studies/" + identifier) + "/"

    @staticmethod
    def gen_idassay(identifier: str) -> str:
        return ("assays/" + identifier) + "/"

    @staticmethod
    def gen_idarcworkflow(identifier: str) -> str:
        return ("workflows/" + identifier) + "/"

    @staticmethod
    def gen_idarcrun(identifier: str) -> str:
        return ("runs/" + identifier) + "/"

    @staticmethod
    def validate(lp: LDNode, context: LDContext | None=None) -> bool:
        return lp.HasType(LDDataset.schema_type(), context)

    @staticmethod
    def validate_investigation(lp: LDNode, context: LDContext | None=None) -> bool:
        class ObjectExpr1819:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1818(x: str, y: str) -> bool:
                    return x == y

                return _arrow1818

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        return contains("Investigation", lp.AdditionalType, ObjectExpr1819()) if LDDataset.validate(lp, context) else False

    @staticmethod
    def validate_study(lp: LDNode, context: LDContext | None=None) -> bool:
        class ObjectExpr1821:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1820(x: str, y: str) -> bool:
                    return x == y

                return _arrow1820

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        return contains("Study", lp.AdditionalType, ObjectExpr1821()) if LDDataset.validate(lp, context) else False

    @staticmethod
    def validate_assay(lp: LDNode, context: LDContext | None=None) -> bool:
        class ObjectExpr1823:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1822(x: str, y: str) -> bool:
                    return x == y

                return _arrow1822

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        return contains("Assay", lp.AdditionalType, ObjectExpr1823()) if LDDataset.validate(lp, context) else False

    @staticmethod
    def validate_arcworkflow(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> bool:
        class ObjectExpr1825:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1824(x: str, y: str) -> bool:
                    return x == y

                return _arrow1824

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        def _arrow1826(ld_0027: LDNode) -> bool:
            return LDWorkflowProtocol.validate(ld_0027, context)

        return exists(_arrow1826, LDDataset.get_main_entities(lp, graph, context)) if (contains("Workflow", lp.AdditionalType, ObjectExpr1825()) if LDDataset.validate(lp, context) else False) else False

    @staticmethod
    def validate_arcrun(lp: LDNode, context: LDContext | None=None) -> bool:
        class ObjectExpr1828:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1827(x: str, y: str) -> bool:
                    return x == y

                return _arrow1827

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        return contains("Run", lp.AdditionalType, ObjectExpr1828()) if LDDataset.validate(lp, context) else False

    @staticmethod
    def create(id: str, identier: str | None=None, creators: Array[LDNode] | None=None, date_created: Any | None=None, date_published: Any | None=None, date_modified: Any | None=None, description: str | None=None, has_parts: Array[LDNode] | None=None, name: str | None=None, citations: Array[LDNode] | None=None, comments: Array[LDNode] | None=None, mentions: Array[LDNode] | None=None, url: str | None=None, abouts: Array[LDNode] | None=None, measurement_method: LDNode | None=None, measurement_technique: LDNode | None=None, variable_measureds: Array[LDNode] | None=None, context: LDContext | None=None) -> LDNode:
        s: LDNode = LDNode(id, [LDDataset.schema_type()], None, context)
        s.SetOptionalProperty(LDDataset.identifier(), identier, context)
        s.SetOptionalProperty(LDDataset.creator(), creators, context)
        s.SetOptionalProperty(LDDataset.date_created(), date_created, context)
        s.SetOptionalProperty(LDDataset.date_published(), date_published, context)
        s.SetOptionalProperty(LDDataset.date_modified(), date_modified, context)
        s.SetOptionalProperty(LDDataset.description(), description, context)
        s.SetOptionalProperty(LDDataset.has_part(), has_parts, context)
        s.SetOptionalProperty(LDDataset.name(), name, context)
        s.SetOptionalProperty(LDDataset.citation(), citations, context)
        s.SetOptionalProperty(LDDataset.comment(), comments, context)
        s.SetOptionalProperty(LDDataset.mentions(), mentions, context)
        s.SetOptionalProperty(LDDataset.url(), url, context)
        s.SetOptionalProperty(LDDataset.about(), abouts, context)
        s.SetOptionalProperty(LDDataset.measurement_method(), measurement_method, context)
        s.SetOptionalProperty(LDDataset.measurement_technique(), measurement_technique, context)
        s.SetOptionalProperty(LDDataset.variable_measured(), variable_measureds, context)
        return s

    @staticmethod
    def create_investigation(identifier: str, name: str, id: str | None=None, creators: Array[LDNode] | None=None, date_created: Any | None=None, date_published: Any | None=None, date_modified: Any | None=None, description: str | None=None, has_parts: Array[LDNode] | None=None, citations: Array[LDNode] | None=None, comments: Array[LDNode] | None=None, mentions: Array[LDNode] | None=None, url: str | None=None, context: LDContext | None=None) -> LDNode:
        id_1: str = LDDataset.gen_idinvesigation() if (id is None) else id
        s: LDNode = LDDataset.create(id_1, identifier, creators, date_created, date_published, date_modified, description, has_parts, name, citations, comments, mentions, url, None, None, None, None, context)
        s.AdditionalType = ["Investigation"]
        return s

    @staticmethod
    def create_study(identifier: str, id: str | None=None, creators: Array[LDNode] | None=None, date_created: Any | None=None, date_published: Any | None=None, date_modified: Any | None=None, description: str | None=None, has_parts: Array[LDNode] | None=None, name: str | None=None, citations: Array[LDNode] | None=None, variable_measureds: Array[LDNode] | None=None, comments: Array[LDNode] | None=None, url: str | None=None, abouts: Array[LDNode] | None=None, context: LDContext | None=None) -> LDNode:
        id_1: str = LDDataset.gen_idstudy(identifier) if (id is None) else id
        s: LDNode = LDDataset.create(id_1, identifier, creators, date_created, date_published, date_modified, description, has_parts, name, citations, comments, None, url, abouts, None, None, variable_measureds, context)
        s.AdditionalType = ["Study"]
        return s

    @staticmethod
    def create_assay(identifier: str, id: str | None=None, name: str | None=None, description: str | None=None, creators: Array[LDNode] | None=None, has_parts: Array[LDNode] | None=None, measurement_method: LDNode | None=None, measurement_technique: LDNode | None=None, variable_measureds: Array[LDNode] | None=None, abouts: Array[LDNode] | None=None, comments: Array[LDNode] | None=None, context: LDContext | None=None) -> LDNode:
        id_1: str = LDDataset.gen_idassay(identifier) if (id is None) else id
        s: LDNode = LDDataset.create(id_1, identifier, creators, None, None, None, description, has_parts, name, None, comments, None, None, abouts, measurement_method, measurement_technique, variable_measureds, context)
        s.AdditionalType = ["Assay"]
        return s

    @staticmethod
    def create_arcworkflow(identifier: str, main_entities: Array[LDNode], id: str | None=None, name: str | None=None, description: str | None=None, creators: Array[LDNode] | None=None, has_parts: Array[LDNode] | None=None, comments: Array[LDNode] | None=None, context: LDContext | None=None) -> LDNode:
        id_1: str = LDDataset.gen_idarcworkflow(identifier) if (id is None) else id
        s: LDNode = LDDataset.create(id_1, identifier, creators, None, None, None, description, has_parts, name, None, comments, None, None, None, None, None, None, context)
        s.AdditionalType = ["Workflow"]
        s.SetProperty(LDDataset.main_entity(), main_entities, context)
        return s

    @staticmethod
    def create_arcrun(identifier: str, id: str | None=None, name: str | None=None, description: str | None=None, creators: Array[LDNode] | None=None, has_parts: Array[LDNode] | None=None, measurement_method: LDNode | None=None, measurement_technique: LDNode | None=None, variable_measureds: Array[LDNode] | None=None, abouts: Array[LDNode] | None=None, mentions: Array[LDNode] | None=None, comments: Array[LDNode] | None=None, context: LDContext | None=None) -> LDNode:
        id_1: str = LDDataset.gen_idarcrun(identifier) if (id is None) else id
        s: LDNode = LDDataset.create(id_1, identifier, creators, None, None, None, description, has_parts, name, None, comments, mentions, None, abouts, measurement_method, measurement_technique, variable_measureds, context)
        s.AdditionalType = ["Run"]
        return s


LDDataset_reflection = _expr1832

__all__ = ["LDDataset_reflection"]

