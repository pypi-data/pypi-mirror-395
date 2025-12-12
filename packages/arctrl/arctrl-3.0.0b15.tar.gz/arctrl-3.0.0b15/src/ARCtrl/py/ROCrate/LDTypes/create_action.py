from __future__ import annotations
from datetime import datetime
from typing import Any
from ...fable_modules.fable_library.option import (value, default_arg)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import Array
from ...Core.Helper.collections_ import ResizeArray_map
from ...Core.Helper.identifier import create_missing_identifier
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import (LDNode, LDGraph)
from .computational_workflow import LDComputationalWorkflow
from .file import LDFile
from .person import LDPerson
from .sample import LDSample

def _expr1792() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDCreateAction", None, LDCreateAction)


class LDCreateAction:
    @staticmethod
    def schema_type() -> str:
        return "http://schema.org/CreateAction"

    @staticmethod
    def name() -> str:
        return "http://schema.org/name"

    @staticmethod
    def instrument() -> str:
        return "http://schema.org/instrument"

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
    def description() -> str:
        return "http://schema.org/description"

    @staticmethod
    def end_time() -> str:
        return "http://schema.org/endTime"

    @staticmethod
    def disambiguating_description() -> str:
        return "http://schema.org/disambiguatingDescription"

    @staticmethod
    def try_get_name_as_string(ca: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = ca.TryGetPropertyAsSingleton(LDCreateAction.name(), context)
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
    def get_name_as_string(ca: LDNode, context: LDContext | None=None) -> str:
        match_value: Any | None = ca.TryGetPropertyAsSingleton(LDCreateAction.name(), context)
        if match_value is not None:
            if str(type(value(match_value))) == "<class \'str\'>":
                n: str = value(match_value)
                return n

            else: 
                raise Exception(("property `name` of object with @id `" + ca.Id) + "` was not a string")


        else: 
            raise Exception(("Could not access property `name` of object with @id `" + ca.Id) + "`")


    @staticmethod
    def set_name_as_string(ca: LDNode, name: str, context: LDContext | None=None) -> Any:
        return ca.SetProperty(LDCreateAction.name(), name, context)

    @staticmethod
    def get_instruments(ca: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return ca.GetPropertyNodes(LDCreateAction.instrument(), None, graph, context)

    @staticmethod
    def get_instruments_as_computational_workflow(ca: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDComputationalWorkflow.validate(ld_object, context_1)

        return ca.GetPropertyNodes(LDCreateAction.instrument(), filter, graph, context)

    @staticmethod
    def set_instruments(ca: LDNode, instruments: Array[LDNode], context: LDContext | None=None) -> Any:
        return ca.SetProperty(LDCreateAction.instrument(), instruments, context)

    @staticmethod
    def try_get_agent(ca: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode | None:
        match_value: LDNode | None = ca.TryGetPropertyAsSingleNode(LDCreateAction.agent(), graph, context)
        (pattern_matching_result, a_1) = (None, None)
        if match_value is not None:
            def _arrow1790(__unit: None=None) -> bool:
                ld_object: LDNode = match_value
                return LDPerson.validate(ld_object, context)

            if _arrow1790():
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
    def get_agent(ca: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> LDNode:
        match_value: LDNode | None = ca.TryGetPropertyAsSingleNode(LDCreateAction.agent(), graph, context)
        if match_value is not None:
            def _arrow1791(__unit: None=None) -> bool:
                ld_object: LDNode = match_value
                return LDPerson.validate(ld_object, context)

            if _arrow1791():
                a_1: LDNode = match_value
                return a_1

            else: 
                raise Exception(("Property of `agent` of object with @id `" + ca.Id) + "` was not a valid Person")


        else: 
            raise Exception(("Could not access property `agent` of object with @id `" + ca.Id) + "`")


    @staticmethod
    def set_agent(ca: LDNode, agent: LDNode, context: LDContext | None=None) -> Any:
        return ca.SetProperty(LDCreateAction.agent(), agent, context)

    @staticmethod
    def get_objects(ca: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return ca.GetPropertyNodes(LDCreateAction.object_(), None, graph, context)

    @staticmethod
    def get_objects_as_sample(ca: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDSample.validate(ld_object, context_1)

        return ca.GetPropertyNodes(LDCreateAction.object_(), filter, graph, context)

    @staticmethod
    def get_objects_as_data(ca: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDFile.validate(ld_object, context_1)

        return ca.GetPropertyNodes(LDCreateAction.object_(), filter, graph, context)

    @staticmethod
    def set_objects(ca: LDNode, objects: Array[LDNode], context: LDContext | None=None) -> Any:
        return ca.SetProperty(LDCreateAction.object_(), objects, context)

    @staticmethod
    def get_results(ca: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        return ca.GetPropertyNodes(LDCreateAction.result(), None, graph, context)

    @staticmethod
    def get_results_as_sample(ca: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDSample.validate(ld_object, context_1)

        return ca.GetPropertyNodes(LDCreateAction.result(), filter, graph, context)

    @staticmethod
    def get_results_as_data(ca: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> Array[LDNode]:
        def filter(ld_object: LDNode, context_1: LDContext | None=None) -> bool:
            return LDFile.validate(ld_object, context_1)

        return ca.GetPropertyNodes(LDCreateAction.result(), filter, graph, context)

    @staticmethod
    def set_results(ca: LDNode, results: Array[LDNode], context: LDContext | None=None) -> Any:
        return ca.SetProperty(LDCreateAction.result(), results, context)

    @staticmethod
    def try_get_description(ca: LDNode, context: LDContext | None=None) -> str | None:
        match_value: Any | None = ca.TryGetPropertyAsSingleton(LDCreateAction.description(), context)
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
    def set_description(ca: LDNode, description: str, context: LDContext | None=None) -> Any:
        return ca.SetProperty(LDCreateAction.description(), description, context)

    @staticmethod
    def try_get_end_time(ca: LDNode, context: LDContext | None=None) -> Any | None:
        match_value: Any | None = ca.TryGetPropertyAsSingleton(LDCreateAction.end_time(), context)
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
    def set_end_time(ca: LDNode, end_time: Any, context: LDContext | None=None) -> Any:
        return ca.SetProperty(LDCreateAction.end_time(), end_time, context)

    @staticmethod
    def get_disambiguating_descriptions_as_string(ca: LDNode, context: LDContext | None=None) -> Array[str]:
        def f(o_1: Any=None) -> Any:
            return o_1

        def filter(o: Any=None, context_1: LDContext | None=None) -> bool:
            return str(type(o)) == "<class \'str\'>"

        return ResizeArray_map(f, ca.GetPropertyValues(LDCreateAction.disambiguating_description(), filter, context))

    @staticmethod
    def set_disambiguating_descriptions_as_string(ca: LDNode, disambiguating_descriptions: Array[str], context: LDContext | None=None) -> Any:
        return ca.SetProperty(LDCreateAction.disambiguating_description(), disambiguating_descriptions, context)

    @staticmethod
    def validate(ca: LDNode, context: LDContext | None=None) -> bool:
        return ca.HasProperty(LDCreateAction.instrument(), context) if ca.HasType(LDCreateAction.schema_type(), context) else False

    @staticmethod
    def create(name: str, agent: LDNode, instrument: LDNode, objects: Array[LDNode] | None=None, results: Array[LDNode] | None=None, description: str | None=None, id: str | None=None, end_time: Any | None=None, disambiguating_descriptions: Array[str] | None=None, context: LDContext | None=None) -> LDNode:
        id_2: str = clean(("#ComputationalWorkflow_" + create_missing_identifier()) + "") if (id is None) else id
        objects_1: Array[LDNode] = default_arg(objects, [])
        results_1: Array[LDNode] = default_arg(results, [])
        ca: LDNode = LDNode(id_2, [LDCreateAction.schema_type()], None, context)
        ca.SetProperty(LDCreateAction.name(), name, context)
        ca.SetProperty(LDCreateAction.agent(), agent, context)
        ca.SetProperty(LDCreateAction.object_(), objects_1, context)
        ca.SetProperty(LDCreateAction.result(), results_1, context)
        ca.SetProperty(LDCreateAction.instrument(), instrument, context)
        ca.SetOptionalProperty(LDCreateAction.description(), description, context)
        ca.SetOptionalProperty(LDCreateAction.end_time(), end_time, context)
        ca.SetOptionalProperty(LDCreateAction.disambiguating_description(), disambiguating_descriptions, context)
        return ca


LDCreateAction_reflection = _expr1792

__all__ = ["LDCreateAction_reflection"]

