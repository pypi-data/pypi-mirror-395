from __future__ import annotations
from collections.abc import Callable
from datetime import datetime
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.option import (value, default_arg)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import Array
from ...Core.Helper.collections_ import ResizeArray_map
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import (LDNode, LDGraph)
from .file import LDFile
from .lab_protocol import LDLabProtocol
from .person import LDPerson
from .property_value import LDPropertyValue
from .sample import LDSample

__C = TypeVar("__C")

__B = TypeVar("__B")

def _expr1786() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDLabProcess", None, LDLabProcess)


class LDLabProcess:
    @staticmethod
    def schema_type() -> str:
        return "https://bioschemas.org/LabProcess"

    @staticmethod
    def name() -> str:
        return "http://schema.org/name"

    @staticmethod
    def agent() -> str:
        return "http://schema.org/agent"

    @staticmethod
    def object_() -> str:
        return "http://schema.org/object"

    @staticmethod
    def result() -> str:
        return "http://schema.org/result"

    @staticmethod
    def executes_lab_protocol() -> str:
        return "https://bioschemas.org/properties/executesLabProtocol"

    @staticmethod
    def executes_lab_protocol_deprecated() -> str:
        return "https://bioschemas.org/executesLabProtocol"

    @staticmethod
    def parameter_value() -> str:
        return "https://bioschemas.org/properties/parameterValue"

    @staticmethod
    def parameter_value_deprecated() -> str:
        return "https://bioschemas.org/parameterValue"

    @staticmethod
    def end_time() -> str:
        return "http://schema.org/endTime"

    @staticmethod
    def disambiguating_description() -> str:
        return "http://schema.org/disambiguatingDescription"

    @staticmethod
    def try_get_name_as_string(lp: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDLabProcess.name(), context)
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
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDLabProcess.name(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                n: str = value(match_value)
                return n

            else: 
                raise Exception(("property `name` of object with @id `" + lp.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `name` of object with @id `" + lp.Id) + "`")


    @staticmethod
    def set_name_as_string(lp: LDNode, name: str, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProcess.name(), name, context)

    @staticmethod
    def try_get_agent(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = lp.TryGetPropertyAsSingleNode(LDLabProcess.agent(), graph, context)
        (pattern_matching_result, a_1) = (None, None)
        if match_value is not None:
            def _arrow1781(__unit: None=None) -> bool:
                ld_object: LDNode = match_value
                return LDPerson.validate(ld_object, context)

            if _arrow1781():
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
    def get_agent(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode:
        match_value: LDNode | None = lp.TryGetPropertyAsSingleNode(LDLabProcess.agent(), graph, context)
        if match_value is not None:
            def _arrow1782(__unit: None=None) -> bool:
                ld_object: LDNode = match_value
                return LDPerson.validate(ld_object, context)

            if _arrow1782():
                a_1: LDNode = match_value
                return a_1

            else: 
                raise Exception(("Property of `agent` of object with @id `" + lp.Id) + "` was not a valid Person")


        else: 
            raise Exception(("Could not access property `agent` of object with @id `" + lp.Id) + "`")


    @staticmethod
    def set_agent(lp: LDNode, agent: LDNode, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProcess.agent(), agent, context)

    @staticmethod
    def get_objects(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return lp.GetPropertyNodes(LDLabProcess.object_(), None, graph, context)

    @staticmethod
    def get_objects_as_sample(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDSample.validate(ld_object, context_1)

        return lp.GetPropertyNodes(LDLabProcess.object_(), filter, graph, context)

    @staticmethod
    def get_objects_as_data(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDFile.validate(ld_object, context_1)

        return lp.GetPropertyNodes(LDLabProcess.object_(), filter, graph, context)

    @staticmethod
    def set_objects(lp: LDNode, objects: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProcess.object_(), objects, context)

    @staticmethod
    def get_results(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return lp.GetPropertyNodes(LDLabProcess.result(), None, graph, context)

    @staticmethod
    def get_results_as_sample(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDSample.validate(ld_object, context_1)

        return lp.GetPropertyNodes(LDLabProcess.result(), filter, graph, context)

    @staticmethod
    def get_results_as_data(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDFile.validate(ld_object, context_1)

        return lp.GetPropertyNodes(LDLabProcess.result(), filter, graph, context)

    @staticmethod
    def set_results(lp: LDNode, results: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProcess.result(), results, context)

    @staticmethod
    def try_get_executes_lab_protocol(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDLabProtocol.validate(ld_object, context_1)

        match_value: LDNode | None = lp.TryGetPropertyAsSingleNode(LDLabProcess.executes_lab_protocol(), graph, context)
        (pattern_matching_result, l_1) = (None, None)
        if match_value is not None:
            if filter(match_value, context):
                pattern_matching_result = 0
                l_1 = match_value

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return l_1

        elif pattern_matching_result == 1:
            match_value_1: LDNode | None = lp.TryGetPropertyAsSingleNode(LDLabProcess.executes_lab_protocol_deprecated(), graph, context)
            (pattern_matching_result_1, l_3) = (None, None)
            if match_value_1 is not None:
                if filter(match_value_1, context):
                    pattern_matching_result_1 = 0
                    l_3 = match_value_1

                else: 
                    pattern_matching_result_1 = 1


            else: 
                pattern_matching_result_1 = 1

            if pattern_matching_result_1 == 0:
                return l_3

            elif pattern_matching_result_1 == 1:
                return None



    @staticmethod
    def set_executes_lab_protocol(lp: LDNode, executes_lab_protocol: LDNode, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProcess.executes_lab_protocol(), executes_lab_protocol, context)

    @staticmethod
    def get_parameter_values(lp: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDPropertyValue.validate(ld_object, context_1)

        l: Array[LDNode] = lp.GetPropertyNodes(LDLabProcess.parameter_value(), filter, graph, context)
        return lp.GetPropertyNodes(LDLabProcess.parameter_value_deprecated(), filter, graph, context) if (len(l) == 0) else l

    @staticmethod
    def set_parameter_values(lp: LDNode, parameter_values: Array[LDNode], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProcess.parameter_value(), parameter_values, context)

    @staticmethod
    def try_get_end_time(lp: LDNode, context: LDContext | None=None) -> Any | None:
        match_value: Any | None = lp.TryGetPropertyAsSingleton(LDLabProcess.end_time(), context)
        (pattern_matching_result, et) = (None, None)
        if match_value is not None:
            if isinstance(value(match_value), datetime):
                pattern_matching_result = 0
                et = value(match_value)

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            return et

        elif pattern_matching_result == 1:
            return None


    @staticmethod
    def set_end_time(lp: LDNode, end_time: Any, context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProcess.end_time(), end_time, context)

    @staticmethod
    def get_disambiguating_descriptions_as_string(lp: LDNode, context: LDContext | None=None) -> Array[str]:
        def f(o_1: Any=None) -> Any:
            return o_1

        def filter(o: Any=None, context_1: LDContext | None=None) -> bool:
            return str(type(o)) == "<class \'str\'>"

        return ResizeArray_map(f, lp.GetPropertyValues(LDLabProcess.disambiguating_description(), filter, context))

    @staticmethod
    def set_disambiguating_descriptions_as_string(lp: LDNode, disambiguating_descriptions: Array[str], context: LDContext | None=None) -> Any:
        return lp.SetProperty(LDLabProcess.disambiguating_description(), disambiguating_descriptions, context)

    @staticmethod
    def validate(lp: LDNode, context: LDContext | None=None) -> bool:
        return lp.HasProperty(LDLabProcess.name(), context) if lp.HasType(LDLabProcess.schema_type(), context) else False

    @staticmethod
    def gen_id(name: Any, assay_name: Any | None=None, study_name: Any | None=None) -> str:
        def _arrow1783(__unit: None=None) -> str:
            study_1: __C = value(study_name)
            return ((("#Process_S_" + str(study_1)) + "_") + str(name)) + ""

        def _arrow1784(__unit: None=None) -> str:
            assay_1: __B = value(assay_name)
            return ((("#Process_A_" + str(assay_1)) + "_") + str(name)) + ""

        def _arrow1785(__unit: None=None) -> str:
            assay: __B = value(assay_name)
            study: __C = value(study_name)
            return ((((("#Process_S_" + str(study)) + "_A_") + str(assay)) + "_") + str(name)) + ""

        return clean((_arrow1783() if (study_name is not None) else (("#Process_" + str(name)) + "")) if (assay_name is None) else (_arrow1784() if (study_name is None) else _arrow1785()))

    @staticmethod
    def create(name: str, objects: Array[LDNode] | None=None, results: Array[LDNode] | None=None, id: str | None=None, agent: LDNode | None=None, executes_lab_protocol: LDNode | None=None, parameter_values: Array[LDNode] | None=None, end_time: Any | None=None, disambiguating_descriptions: Array[str] | None=None, context: LDContext | None=None) -> LDNode:
        id_1: str = LDLabProcess.gen_id(name) if (id is None) else id
        objects_1: Array[LDNode] = default_arg(objects, [])
        results_1: Array[LDNode] = default_arg(results, [])
        lp: LDNode = LDNode(id_1, [LDLabProcess.schema_type()], None, context)
        lp.SetProperty(LDLabProcess.name(), name, context)
        lp.SetOptionalProperty(LDLabProcess.agent(), agent, context)
        lp.SetProperty(LDLabProcess.object_(), objects_1, context)
        lp.SetProperty(LDLabProcess.result(), results_1, context)
        lp.SetOptionalProperty(LDLabProcess.executes_lab_protocol(), executes_lab_protocol, context)
        lp.SetOptionalProperty(LDLabProcess.parameter_value(), parameter_values, context)
        lp.SetOptionalProperty(LDLabProcess.end_time(), end_time, context)
        lp.SetOptionalProperty(LDLabProcess.disambiguating_description(), disambiguating_descriptions, context)
        return lp


LDLabProcess_reflection = _expr1786

__all__ = ["LDLabProcess_reflection"]

