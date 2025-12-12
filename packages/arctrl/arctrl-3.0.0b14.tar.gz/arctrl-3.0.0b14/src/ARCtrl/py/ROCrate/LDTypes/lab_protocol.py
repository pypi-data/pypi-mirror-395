from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (append as append_1, singleton, FSharpList, is_empty)
from ...fable_modules.fable_library.option import value
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.seq import (append, to_list, delay, singleton as singleton_1, empty)
from ...fable_modules.fable_library.string_ import join
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import IEnumerable_1
from ...Core.Helper.identifier import create_missing_identifier
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import (LDNode, LDGraph)
from .comment import LDComment
from .defined_term import LDDefinedTerm

def _expr1780() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDLabProtocol", None, LDLabProtocol)


class LDLabProtocol:
    @staticmethod
    def schema_type() -> str:
        return "https://bioschemas.org/LabProtocol"

    @staticmethod
    def description() -> str:
        return "http://schema.org/description"

    @staticmethod
    def name() -> str:
        return "http://schema.org/name"

    @staticmethod
    def computational_tool() -> str:
        return "https://bioschemas.org/properties/computationalTool"

    @staticmethod
    def computational_tool_deprecated() -> str:
        return "https://bioschemas.org/computationalTool"

    @staticmethod
    def lab_equipment() -> str:
        return "https://bioschemas.org/properties/labEquipment"

    @staticmethod
    def lab_equipment_deprecated() -> str:
        return "https://bioschemas.org/labEquipment"

    @staticmethod
    def reagent() -> str:
        return "https://bioschemas.org/properties/reagent"

    @staticmethod
    def reagent_deprecated() -> str:
        return "https://bioschemas.org/reagent"

    @staticmethod
    def intended_use() -> str:
        return "https://bioschemas.org/properties/intendedUse"

    @staticmethod
    def intended_use_deprecated() -> str:
        return "https://bioschemas.org/intendedUse"

    @staticmethod
    def url() -> str:
        return "http://schema.org/url"

    @staticmethod
    def version() -> str:
        return "http://schema.org/version"

    @staticmethod
    def comment() -> str:
        return "http://schema.org/comment"

    @staticmethod
    def try_get_description_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDLabProtocol.description(), context)
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
    def set_description_as_string(lp: LDNode, description: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProtocol.description(), description, context)

    @staticmethod
    def try_get_intended_use_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDLabProtocol.intended_use(), context)
        (pattern_matching_result, iu) = (None, None)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                pattern_matching_result = 0
                iu = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return iu

        elif pattern_matching_result == 1:
            match_value_1: Any | None = lp.TryGetPropertyAsSingleton(LDLabProtocol.intended_use_deprecated(), context)
            (pattern_matching_result_1, iu_1) = (None, None)
            if match_value_1 is not None:
                if str(type(value(match_value_1))) == "<class \'str\'>":
                    pattern_matching_result_1 = 0
                    iu_1 = value(match_value_1)

                else: 
                    pattern_matching_result_1 = 1


            else: 
                pattern_matching_result_1 = 1

            if pattern_matching_result_1 == 0:
                return iu_1

            elif pattern_matching_result_1 == 1:
                return None



    @staticmethod
    def set_intended_use_as_string(lp: LDNode, intended_use: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProtocol.intended_use(), intended_use, context)

    @staticmethod
    def try_get_intended_use_as_defined_term(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDDefinedTerm.validate(ld_object, context_1)

        match_value: LDNode | None = lp.TryGetPropertyAsSingleNode(LDLabProtocol.intended_use(), graph, context)
        (pattern_matching_result, iu_1) = (None, None)
        if match_value is not None:
            if filter(match_value, context):
                pattern_matching_result = 0
                iu_1 = match_value

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return iu_1

        elif pattern_matching_result == 1:
            match_value_1: LDNode | None = lp.TryGetPropertyAsSingleNode(LDLabProtocol.intended_use_deprecated(), graph, context)
            (pattern_matching_result_1, iu_3) = (None, None)
            if match_value_1 is not None:
                if filter(match_value_1, context):
                    pattern_matching_result_1 = 0
                    iu_3 = match_value_1

                else: 
                    pattern_matching_result_1 = 1


            else: 
                pattern_matching_result_1 = 1

            if pattern_matching_result_1 == 0:
                return iu_3

            elif pattern_matching_result_1 == 1:
                return None



    @staticmethod
    def set_intended_use_as_defined_term(lp: LDNode, intended_use: LDNode, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProtocol.intended_use(), intended_use, context)

    @staticmethod
    def try_get_name_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDLabProtocol.name(), context)
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
    def get_name_as_string(lp: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDLabProtocol.name(), context)
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
            raise Exception(("Could not access property `name` of object with @id `" + lp.Id) + "`")


    @staticmethod
    def set_name_as_string(lp: LDNode, name: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProtocol.name(), name, context)

    @staticmethod
    def get_comments(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDComment.validate(ld_object, context_1)

        return lp.GetPropertyNodes(LDLabProtocol.comment(), filter, graph, context)

    @staticmethod
    def set_comments(lp: LDNode, comments: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProtocol.comment(), comments, context)

    @staticmethod
    def get_computational_tools(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        l: Array[LDNode] = lp.GetPropertyNodes(LDLabProtocol.computational_tool(), None, graph, context)
        return lp.GetPropertyNodes(LDLabProtocol.computational_tool_deprecated(), None, graph, context) if (len(l) == 0) else l

    @staticmethod
    def set_computational_tools(lp: LDNode, computational_tools: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProtocol.computational_tool(), computational_tools, context)

    @staticmethod
    def get_lab_equipments(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        l: Array[LDNode] = lp.GetPropertyNodes(LDLabProtocol.lab_equipment(), None, graph, context)
        return lp.GetPropertyNodes(LDLabProtocol.lab_equipment_deprecated(), None, graph, context) if (len(l) == 0) else l

    @staticmethod
    def set_lab_equipments(lp: LDNode, lab_equipments: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProtocol.lab_equipment(), lab_equipments, context)

    @staticmethod
    def get_reagents(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        l: Array[LDNode] = lp.GetPropertyNodes(LDLabProtocol.reagent(), None, graph, context)
        return lp.GetPropertyNodes(LDLabProtocol.reagent_deprecated(), None, graph, context) if (len(l) == 0) else l

    @staticmethod
    def set_reagents(lp: LDNode, reagents: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProtocol.reagent(), reagents, context)

    @staticmethod
    def get_components(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def _arrow1774(__unit: None=None) -> IEnumerable_1[LDNode]:
            source_3: IEnumerable_1[LDNode]
            source_1: Array[LDNode] = LDLabProtocol.get_lab_equipments(lp, graph, context)
            source_3 = append(LDLabProtocol.get_reagents(lp, graph, context), source_1)
            return append(LDLabProtocol.get_computational_tools(lp, graph, context), source_3)

        return list(_arrow1774())

    @staticmethod
    def try_get_url(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDLabProtocol.url(), context)
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
    def set_url(lp: LDNode, url: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProtocol.url(), url, context)

    @staticmethod
    def try_get_version_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDLabProtocol.version(), context)
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
    def set_version_as_string(lp: LDNode, version: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProtocol.version(), version, context)

    @staticmethod
    def validate(lp: LDNode, context: LDContext | None=None) -> bool:
        return lp.HasType(LDLabProtocol.schema_type(), context)

    @staticmethod
    def gen_id(name: str | None=None, process_name: str | None=None, assay_name: str | None=None, study_name: str | None=None) -> str:
        def _arrow1779(__unit: None=None) -> FSharpList[str]:
            def _arrow1778(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1777(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow1776(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow1775(__unit: None=None) -> IEnumerable_1[str]:
                            return singleton_1(value(study_name)) if (study_name is not None) else empty()

                        return append(singleton_1(value(assay_name)) if (assay_name is not None) else empty(), delay(_arrow1775))

                    return append(singleton_1(value(process_name)) if (process_name is not None) else empty(), delay(_arrow1776))

                return append(singleton_1(value(name)) if (name is not None) else empty(), delay(_arrow1777))

            vals: FSharpList[str] = to_list(delay(_arrow1778))
            return singleton(create_missing_identifier()) if is_empty(vals) else vals

        return clean(join("_", append_1(singleton("#Protocol"), _arrow1779())))

    @staticmethod
    def create(id: str, name: str | None=None, description: str | None=None, intended_use: LDNode | None=None, comments: Array[LDNode] | None=None, computational_tools: Array[LDNode] | None=None, lab_equipments: Array[LDNode] | None=None, reagents: Array[LDNode] | None=None, url: str | None=None, version: str | None=None, context: LDContext | None=None) -> LDNode:
        lp: LDNode = LDNode(id, [LDLabProtocol.schema_type()], None, context)
        lp.SetOptionalProperty(LDLabProtocol.name(), name, context)
        lp.SetOptionalProperty(LDLabProtocol.description(), description, context)
        lp.SetOptionalProperty(LDLabProtocol.intended_use(), intended_use, context)
        lp.SetOptionalProperty(LDLabProtocol.comment(), comments, context)
        lp.SetOptionalProperty(LDLabProtocol.computational_tool(), computational_tools, context)
        lp.SetOptionalProperty(LDLabProtocol.lab_equipment(), lab_equipments, context)
        lp.SetOptionalProperty(LDLabProtocol.reagent(), reagents, context)
        lp.SetOptionalProperty(LDLabProtocol.url(), url, context)
        lp.SetOptionalProperty(LDLabProtocol.version(), version, context)
        return lp


LDLabProtocol_reflection = _expr1780

__all__ = ["LDLabProtocol_reflection"]

