from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.option import value
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import Array
from ...Core.Helper.identifier import create_missing_identifier
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import (LDNode, LDGraph)

def _expr1723() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDFormalParameter", None, LDFormalParameter)


class LDFormalParameter:
    @staticmethod
    def schema_type() -> str:
        return "https://bioschemas.org/FormalParameter"

    @staticmethod
    def encoding_format() -> str:
        return "http://schema.org/encodingFormat"

    @staticmethod
    def name() -> str:
        return "http://schema.org/name"

    @staticmethod
    def same_as() -> str:
        return "http://schema.org/sameAs"

    @staticmethod
    def description() -> str:
        return "http://schema.org/description"

    @staticmethod
    def work_example() -> str:
        return "http://schema.org/workExample"

    @staticmethod
    def default_value() -> str:
        return "http://schema.org/defaultValue"

    @staticmethod
    def value_required() -> str:
        return "http://schema.org/valueRequired"

    @staticmethod
    def identifier() -> str:
        return "http://schema.org/identifier"

    @staticmethod
    def image() -> str:
        return "http://schema.org/image"

    @staticmethod
    def main_entity_of_page() -> str:
        return "http://schema.org/mainEntityOfPage"

    @staticmethod
    def potential_action() -> str:
        return "http://schema.org/potentialAction"

    @staticmethod
    def subject_of() -> str:
        return "http://schema.org/subjectOf"

    @staticmethod
    def url() -> str:
        return "http://schema.org/url"

    @staticmethod
    def alternate_name() -> str:
        return "http://schema.org/alternateName"

    @staticmethod
    def disambiguating_description() -> str:
        return "http://schema.org/disambiguatingDescription"

    @staticmethod
    def get_encoding_formats(fp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return fp.GetPropertyNodes(LDFormalParameter.encoding_format(), None, graph, context)

    @staticmethod
    def set_encoding_formats(fp: LDNode, encoding_formats: Array[LDNode], context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.encoding_format(), encoding_formats, context)

    @staticmethod
    def try_get_name_as_string(fp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = fp.TryGetPropertyAsSingleton(LDFormalParameter.name(), context)
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
    def get_name_as_string(fp: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = fp.TryGetPropertyAsSingleton(LDFormalParameter.name(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                n: str = value(match_value)
                return n

            else: 
                raise Exception(("Property of `name` of object with @id `" + fp.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `name` of object with @id `" + fp.Id) + "`")


    @staticmethod
    def set_name_as_string(fp: LDNode, name: str, context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.name(), name, context)

    @staticmethod
    def get_same_as(fp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return fp.GetPropertyNodes(LDFormalParameter.same_as(), None, graph, context)

    @staticmethod
    def set_same_as(fp: LDNode, sames: Array[LDNode], context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.same_as(), sames, context)

    @staticmethod
    def try_get_description_as_string(fp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = fp.TryGetPropertyAsSingleton(LDFormalParameter.description(), context)
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
    def set_description_as_string(fp: LDNode, description: str, context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.description(), description, context)

    @staticmethod
    def try_get_work_example_as_string(fp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = fp.TryGetPropertyAsSingleton(LDFormalParameter.work_example(), context)
        (pattern_matching_result, we) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                we = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return we

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_work_example_as_string(fp: LDNode, work_example: str, context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.work_example(), work_example, context)

    @staticmethod
    def try_get_default_value_as_string(fp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = fp.TryGetPropertyAsSingleton(LDFormalParameter.default_value(), context)
        (pattern_matching_result, dv) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                dv = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return dv

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_default_value_as_string(fp: LDNode, default_value: str, context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.default_value(), default_value, context)

    @staticmethod
    def try_get_value_required_as_boolean(fp: LDNode, context: LDContext | None=None) -> bool | None:
        match_value: Any | None = fp.TryGetPropertyAsSingleton(LDFormalParameter.value_required(), context)
        (pattern_matching_result, vr) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'bool\'>":
                pattern_matching_result = 0
                vr = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return vr

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_value_required_as_boolean(fp: LDNode, value_required: bool, context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.value_required(), value_required, context)

    @staticmethod
    def get_identifiers(fp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return fp.GetPropertyNodes(LDFormalParameter.identifier(), None, graph, context)

    @staticmethod
    def set_identifiers(fp: LDNode, identifiers: Array[LDNode], context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.identifier(), identifiers, context)

    @staticmethod
    def try_get_image_as_string(fp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = fp.TryGetPropertyAsSingleton(LDFormalParameter.image(), context)
        (pattern_matching_result, img) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                img = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return img

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_image_as_string(fp: LDNode, image: str, context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.image(), image, context)

    @staticmethod
    def try_get_main_entity_of_page_as_string(fp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = fp.TryGetPropertyAsSingleton(LDFormalParameter.main_entity_of_page(), context)
        (pattern_matching_result, meop) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                meop = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return meop

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_main_entity_of_page_as_string(fp: LDNode, main_entity_of_page: str, context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.main_entity_of_page(), main_entity_of_page, context)

    @staticmethod
    def get_potential_actions(fp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return fp.GetPropertyNodes(LDFormalParameter.potential_action(), None, graph, context)

    @staticmethod
    def set_potential_actions(fp: LDNode, potential_actions: Array[LDNode], context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.potential_action(), potential_actions, context)

    @staticmethod
    def get_subject_ofs(fp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return fp.GetPropertyNodes(LDFormalParameter.subject_of(), None, graph, context)

    @staticmethod
    def set_subject_ofs(fp: LDNode, subject_ofs: Array[LDNode], context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.subject_of(), subject_ofs, context)

    @staticmethod
    def try_get_url_as_string(fp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = fp.TryGetPropertyAsSingleton(LDFormalParameter.url(), context)
        (pattern_matching_result, url) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                url = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return url

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_url_as_string(fp: LDNode, url: str, context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.url(), url, context)

    @staticmethod
    def get_alternate_names(fp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return fp.GetPropertyNodes(LDFormalParameter.alternate_name(), None, graph, context)

    @staticmethod
    def set_alternate_names(fp: LDNode, alternate_names: Array[LDNode], context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.alternate_name(), alternate_names, context)

    @staticmethod
    def try_get_disambiguating_description_as_string(fp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = fp.TryGetPropertyAsSingleton(LDFormalParameter.disambiguating_description(), context)
        (pattern_matching_result, desc) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                desc = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return desc

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_disambiguating_description_as_string(fp: LDNode, disambiguating_description: str, context: LDContext | None=None) -> Any:
        return fp.SetProperty(LDFormalParameter.disambiguating_description(), disambiguating_description, context)

    @staticmethod
    def gen_id(name: str, workflow_name: str | None=None, run_name: str | None=None) -> str:
        def _arrow1720(__unit: None=None) -> str:
            run_1: str = run_name
            return ((("#FormalParameter_R_" + run_1) + "_") + name) + ""

        def _arrow1721(__unit: None=None) -> str:
            workflow_1: str = workflow_name
            return ((("#FormalParameter_W_" + workflow_1) + "_") + name) + ""

        def _arrow1722(__unit: None=None) -> str:
            run: str = run_name
            workflow: str = workflow_name
            return ((((("#FormalParameter_W_" + workflow) + "_R_") + run) + "_") + name) + ""

        return clean((_arrow1720() if (run_name is not None) else (((("#FormalParameter_" + name) + "_") + create_missing_identifier()) + "")) if (workflow_name is None) else (_arrow1721() if (run_name is None) else _arrow1722()))

    @staticmethod
    def validate(fp: LDNode, context: LDContext | None=None) -> bool:
        return (len(fp.AdditionalType) > 0) if fp.HasType(LDFormalParameter.schema_type(), context) else False

    @staticmethod
    def create(additional_type: str, id: str | None=None, encoding_formats: Array[LDNode] | None=None, name: str | None=None, same_as: Array[LDNode] | None=None, description: str | None=None, work_example: str | None=None, default_value: str | None=None, value_required: bool | None=None, identifiers: Array[LDNode] | None=None, image: str | None=None, subject_ofs: Array[LDNode] | None=None, url: str | None=None, alternate_names: Array[LDNode] | None=None, disambiguating_description: str | None=None, context: LDContext | None=None) -> LDNode:
        fp: LDNode = LDNode(clean(("#FormalParameter_" + create_missing_identifier()) + "") if (id is None) else id, [LDFormalParameter.schema_type()], None, context)
        fp.AdditionalType = [additional_type]
        fp.SetOptionalProperty(LDFormalParameter.encoding_format(), encoding_formats, context)
        fp.SetOptionalProperty(LDFormalParameter.name(), name, context)
        fp.SetOptionalProperty(LDFormalParameter.same_as(), same_as, context)
        fp.SetOptionalProperty(LDFormalParameter.description(), description, context)
        fp.SetOptionalProperty(LDFormalParameter.work_example(), work_example, context)
        fp.SetOptionalProperty(LDFormalParameter.default_value(), default_value, context)
        fp.SetOptionalProperty(LDFormalParameter.value_required(), value_required, context)
        fp.SetOptionalProperty(LDFormalParameter.identifier(), identifiers, context)
        fp.SetOptionalProperty(LDFormalParameter.image(), image, context)
        fp.SetOptionalProperty(LDFormalParameter.subject_of(), subject_ofs, context)
        fp.SetOptionalProperty(LDFormalParameter.url(), url, context)
        fp.SetOptionalProperty(LDFormalParameter.alternate_name(), alternate_names, context)
        fp.SetOptionalProperty(LDFormalParameter.disambiguating_description(), disambiguating_description, context)
        return fp


LDFormalParameter_reflection = _expr1723

__all__ = ["LDFormalParameter_reflection"]

