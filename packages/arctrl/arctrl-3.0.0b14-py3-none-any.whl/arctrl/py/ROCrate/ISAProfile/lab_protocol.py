from __future__ import annotations
from typing import Any
from ...fable_modules.dynamic_obj.dyn_obj import set_optional_property
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import (FSharpRef, Array)
from ..ldobject import (LDNode, LDNode_reflection)

def _expr1809() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LabProtocol", None, LabProtocol, LDNode_reflection())


class LabProtocol(LDNode):
    def __init__(self, id: str, additional_type: Array[str] | None=None, name: Any | None=None, intended_use: Any | None=None, description: Any | None=None, url: Any | None=None, comment: Any | None=None, version: Any | None=None, lab_equipment: Any | None=None, reagent: Any | None=None, computational_tool: Any | None=None) -> None:
        super().__init__(id, ["bioschemas.org/LabProtocol"], default_arg(additional_type, []))
        this: FSharpRef[LabProtocol] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_optional_property("name", name, this.contents)
        set_optional_property("intendedUse", intended_use, this.contents)
        set_optional_property("description", description, this.contents)
        set_optional_property("url", url, this.contents)
        set_optional_property("comment", comment, this.contents)
        set_optional_property("version", version, this.contents)
        set_optional_property("labEquipment", lab_equipment, this.contents)
        set_optional_property("reagent", reagent, this.contents)
        set_optional_property("computationalTool", computational_tool, this.contents)


LabProtocol_reflection = _expr1809

def LabProtocol__ctor_Z6F48851E(id: str, additional_type: Array[str] | None=None, name: Any | None=None, intended_use: Any | None=None, description: Any | None=None, url: Any | None=None, comment: Any | None=None, version: Any | None=None, lab_equipment: Any | None=None, reagent: Any | None=None, computational_tool: Any | None=None) -> LabProtocol:
    return LabProtocol(id, additional_type, name, intended_use, description, url, comment, version, lab_equipment, reagent, computational_tool)


__all__ = ["LabProtocol_reflection"]

