from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import Array
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import LDNode
from .create_action import LDCreateAction
from .lab_process import LDLabProcess

def _expr1796() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDWorkflowInvocation", None, LDWorkflowInvocation)


class LDWorkflowInvocation:
    @staticmethod
    def schema_type() -> Array[str]:
        return [LDCreateAction.schema_type(), LDLabProcess.schema_type()]

    @staticmethod
    def gen_id(name: str, run_name: str | None=None) -> str:
        return clean(("#WorkflowInvocation_" + name) + "") if (run_name is None) else clean(((("#WorkflowInvocation_R_" + run_name) + "_") + name) + "")

    @staticmethod
    def validate(wp: LDNode, context: LDContext | None=None) -> bool:
        return LDLabProcess.validate(wp, context) if LDCreateAction.validate(wp, context) else False

    @staticmethod
    def create(name: str, instrument: LDNode, objects: Array[LDNode] | None=None, results: Array[LDNode] | None=None, description: str | None=None, agents: Array[LDNode] | None=None, id: str | None=None, end_time: Any | None=None, disambiguating_descriptions: Array[str] | None=None, executes_lab_protocol: LDNode | None=None, parameter_values: Array[LDNode] | None=None, context: LDContext | None=None) -> LDNode:
        at: Array[str] = ["WorkflowInvocation"]
        ca: LDNode = LDNode(LDWorkflowInvocation.gen_id(name) if (id is None) else id, LDWorkflowInvocation.schema_type(), at, context)
        ca.SetProperty(LDCreateAction.name(), name, context)
        ca.SetOptionalProperty(LDCreateAction.object_(), objects, context)
        ca.SetOptionalProperty(LDCreateAction.result(), results, context)
        ca.SetProperty(LDCreateAction.instrument(), instrument, context)
        ca.SetOptionalProperty(LDCreateAction.agent(), agents, context)
        ca.SetOptionalProperty(LDCreateAction.description(), description, context)
        ca.SetOptionalProperty(LDCreateAction.end_time(), end_time, context)
        ca.SetOptionalProperty(LDCreateAction.disambiguating_description(), disambiguating_descriptions, context)
        ca.SetOptionalProperty(LDLabProcess.executes_lab_protocol(), executes_lab_protocol, context)
        ca.SetOptionalProperty(LDLabProcess.parameter_value(), parameter_values, context)
        return ca


LDWorkflowInvocation_reflection = _expr1796

__all__ = ["LDWorkflowInvocation_reflection"]

