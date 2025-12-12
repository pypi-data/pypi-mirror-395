from __future__ import annotations
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import Array
from ...Core.Helper.identifier import create_missing_identifier
from ..helper import clean
from ..ldcontext import LDContext
from ..ldobject import LDNode
from .computational_workflow import LDComputationalWorkflow
from .file import LDFile
from .lab_protocol import LDLabProtocol
from .software_source_code import LDSoftwareSourceCode

def _expr1795() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDWorkflowProtocol", None, LDWorkflowProtocol)


class LDWorkflowProtocol:
    @staticmethod
    def schema_type() -> Array[str]:
        return [LDFile.schema_type(), LDComputationalWorkflow.schema_type(), LDSoftwareSourceCode.schema_type(), LDLabProtocol.schema_type()]

    @staticmethod
    def validate(wp: LDNode, context: LDContext | None=None) -> bool:
        return LDLabProtocol.validate(wp, context) if (LDSoftwareSourceCode.validate(wp, context) if LDComputationalWorkflow.validate(wp, context) else False) else False

    @staticmethod
    def create(id: str | None=None, inputs: Array[LDNode] | None=None, outputs: Array[LDNode] | None=None, creator: LDNode | None=None, date_created: str | None=None, licenses: Array[LDNode] | None=None, name: str | None=None, programming_languages: Array[LDNode] | None=None, sd_publisher: LDNode | None=None, url: str | None=None, version: str | None=None, description: str | None=None, has_parts: Array[LDNode] | None=None, intended_use: LDNode | None=None, comments: Array[LDNode] | None=None, computational_tools: Array[LDNode] | None=None, additional_type: Array[str] | None=None, context: LDContext | None=None) -> LDNode:
        at: Array[str] = ["WorkflowProtocol"]
        wp: LDNode = LDNode(clean(("#ComputationalWorkflow_" + create_missing_identifier()) + "") if (id is None) else id, LDWorkflowProtocol.schema_type(), at, context)
        wp.SetOptionalProperty(LDComputationalWorkflow.input(), inputs, context)
        wp.SetOptionalProperty(LDComputationalWorkflow.output(), outputs, context)
        wp.SetOptionalProperty(LDComputationalWorkflow.creator(), creator, context)
        wp.SetOptionalProperty(LDComputationalWorkflow.date_created(), date_created, context)
        wp.SetOptionalProperty(LDComputationalWorkflow.license(), licenses, context)
        wp.SetOptionalProperty(LDComputationalWorkflow.name(), name, context)
        wp.SetOptionalProperty(LDComputationalWorkflow.programming_language(), programming_languages, context)
        wp.SetOptionalProperty(LDComputationalWorkflow.sd_publisher(), sd_publisher, context)
        wp.SetOptionalProperty(LDComputationalWorkflow.url(), url, context)
        wp.SetOptionalProperty(LDComputationalWorkflow.version(), version, context)
        wp.SetOptionalProperty(LDComputationalWorkflow.description(), description, context)
        wp.SetOptionalProperty(LDComputationalWorkflow.has_part(), has_parts, context)
        wp.SetOptionalProperty(LDLabProtocol.intended_use(), intended_use, context)
        wp.SetOptionalProperty(LDLabProtocol.computational_tool(), computational_tools, context)
        wp.SetOptionalProperty(LDComputationalWorkflow.additional_type(), additional_type, context)
        wp.SetOptionalProperty(LDComputationalWorkflow.comment(), comments, context)
        return wp


LDWorkflowProtocol_reflection = _expr1795

__all__ = ["LDWorkflowProtocol_reflection"]

