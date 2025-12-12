from typing import Any
from ..fable_modules.fable_library.reflection import (TypeInfo, union_type)
from ..fable_modules.fable_library.types import (Array, Union)
from .tool_description import CWLToolDescription_reflection
from .workflow_description import CWLWorkflowDescription_reflection

def _expr518() -> TypeInfo:
    return union_type("ARCtrl.CWL.CWLProcessingUnit", [], CWLProcessingUnit, lambda: [[("Item", CWLToolDescription_reflection())], [("Item", CWLWorkflowDescription_reflection())]])


class CWLProcessingUnit(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["CommandLineTool", "Workflow"]


CWLProcessingUnit_reflection = _expr518

__all__ = ["CWLProcessingUnit_reflection"]

