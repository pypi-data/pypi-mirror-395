from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.dynamic_obj.dynamic_obj import DynamicObj
from ...fable_modules.dynamic_obj.dyn_obj import (try_get_property_value, set_property, set_optional_property)
from ...fable_modules.fable_library.option import (value as value_1, default_arg)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import (FSharpRef, Array)
from ..ldobject import (LDNode, LDNode_reflection)

def _expr1808() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LabProcess", None, LabProcess, LDNode_reflection())


class LabProcess(LDNode):
    def __init__(self, id: str, name: Any=None, agent: Any=None, object: Any=None, result: Any=None, additional_type: Array[str] | None=None, executes_lab_protocol: Any | None=None, parameter_value: Any | None=None, end_time: Any | None=None, disambiguating_description: Any | None=None) -> None:
        super().__init__(id, ["bioschemas.org/LabProcess"], default_arg(additional_type, []))
        this: FSharpRef[LabProcess] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("name", name, this.contents)
        set_property("agent", agent, this.contents)
        set_property("object", object, this.contents)
        set_property("result", result, this.contents)
        set_optional_property("executesLabProtocol", executes_lab_protocol, this.contents)
        set_optional_property("parameterValue", parameter_value, this.contents)
        set_optional_property("endTime", end_time, this.contents)
        set_optional_property("disambiguatingDescription", disambiguating_description, this.contents)

    def GetName(self, __unit: None=None) -> str:
        this: LabProcess = self
        obj: DynamicObj = this
        if try_get_property_value("name", obj) is not None:
            match_value: str | None
            match_value_1: Any | None = obj.TryGetPropertyValue("name")
            if match_value_1 is not None:
                o: Any = value_1(match_value_1)
                match_value = o if (str(type(o)) == "<class \'str\'>") else None

            else: 
                match_value = None

            if match_value is None:
                raise Exception(((((("Property \'" + "name") + "\' is set on this \'") + "LabProcess") + "\' object but cannot be cast to \'") + "String") + "\'")

            else: 
                return match_value


        else: 
            raise Exception(((("No property \'" + "name") + "\' set on this \'") + "LabProcess") + "\' object although it is mandatory. Was it created correctly?")


    @staticmethod
    def get_name() -> Callable[[LabProcess], str]:
        def _arrow1804(lp: LabProcess) -> str:
            return lp.GetName()

        return _arrow1804

    def GetAgent(self, __unit: None=None) -> str:
        this: LabProcess = self
        obj: DynamicObj = this
        if try_get_property_value("agent", obj) is not None:
            match_value: str | None
            match_value_1: Any | None = obj.TryGetPropertyValue("agent")
            if match_value_1 is not None:
                o: Any = value_1(match_value_1)
                match_value = o if (str(type(o)) == "<class \'str\'>") else None

            else: 
                match_value = None

            if match_value is None:
                raise Exception(((((("Property \'" + "agent") + "\' is set on this \'") + "LabProcess") + "\' object but cannot be cast to \'") + "String") + "\'")

            else: 
                return match_value


        else: 
            raise Exception(((("No property \'" + "agent") + "\' set on this \'") + "LabProcess") + "\' object although it is mandatory. Was it created correctly?")


    @staticmethod
    def get_agent() -> Callable[[LabProcess], str]:
        def _arrow1805(lp: LabProcess) -> str:
            return lp.GetAgent()

        return _arrow1805

    def GetObject(self, __unit: None=None) -> str:
        this: LabProcess = self
        obj: DynamicObj = this
        if try_get_property_value("object", obj) is not None:
            match_value: str | None
            match_value_1: Any | None = obj.TryGetPropertyValue("object")
            if match_value_1 is not None:
                o: Any = value_1(match_value_1)
                match_value = o if (str(type(o)) == "<class \'str\'>") else None

            else: 
                match_value = None

            if match_value is None:
                raise Exception(((((("Property \'" + "object") + "\' is set on this \'") + "LabProcess") + "\' object but cannot be cast to \'") + "String") + "\'")

            else: 
                return match_value


        else: 
            raise Exception(((("No property \'" + "object") + "\' set on this \'") + "LabProcess") + "\' object although it is mandatory. Was it created correctly?")


    @staticmethod
    def get_object() -> Callable[[LabProcess], str]:
        def _arrow1806(lp: LabProcess) -> str:
            return lp.GetObject()

        return _arrow1806

    def GetResult(self, __unit: None=None) -> str:
        this: LabProcess = self
        obj: DynamicObj = this
        if try_get_property_value("result", obj) is not None:
            match_value: str | None
            match_value_1: Any | None = obj.TryGetPropertyValue("result")
            if match_value_1 is not None:
                o: Any = value_1(match_value_1)
                match_value = o if (str(type(o)) == "<class \'str\'>") else None

            else: 
                match_value = None

            if match_value is None:
                raise Exception(((((("Property \'" + "result") + "\' is set on this \'") + "LabProcess") + "\' object but cannot be cast to \'") + "String") + "\'")

            else: 
                return match_value


        else: 
            raise Exception(((("No property \'" + "result") + "\' set on this \'") + "LabProcess") + "\' object although it is mandatory. Was it created correctly?")


    @staticmethod
    def get_result() -> Callable[[LabProcess], str]:
        def _arrow1807(lp: LabProcess) -> str:
            return lp.GetResult()

        return _arrow1807


LabProcess_reflection = _expr1808

def LabProcess__ctor_Z43A9BC86(id: str, name: Any=None, agent: Any=None, object: Any=None, result: Any=None, additional_type: Array[str] | None=None, executes_lab_protocol: Any | None=None, parameter_value: Any | None=None, end_time: Any | None=None, disambiguating_description: Any | None=None) -> LabProcess:
    return LabProcess(id, name, agent, object, result, additional_type, executes_lab_protocol, parameter_value, end_time, disambiguating_description)


__all__ = ["LabProcess_reflection"]

