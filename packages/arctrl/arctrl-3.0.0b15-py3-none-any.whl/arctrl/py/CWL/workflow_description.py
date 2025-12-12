from __future__ import annotations
from ..fable_modules.dynamic_obj.dynamic_obj import (DynamicObj, DynamicObj_reflection)
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.types import Array
from .inputs import CWLInput
from .outputs import CWLOutput
from .requirements import Requirement
from .workflow_steps import WorkflowStep

def _expr519() -> TypeInfo:
    return class_type("ARCtrl.CWL.CWLWorkflowDescription", None, CWLWorkflowDescription, DynamicObj_reflection())


class CWLWorkflowDescription(DynamicObj):
    def __init__(self, steps: Array[WorkflowStep], inputs: Array[CWLInput], outputs: Array[CWLOutput], cwl_version: str | None=None, requirements: Array[Requirement] | None=None, hints: Array[Requirement] | None=None, metadata: DynamicObj | None=None) -> None:
        super().__init__()
        self._cwlVersion: str = default_arg(cwl_version, "v1.2")
        self._steps: Array[WorkflowStep] = steps
        self._inputs: Array[CWLInput] = inputs
        self._outputs: Array[CWLOutput] = outputs
        self._requirements: Array[Requirement] | None = requirements
        self._hints: Array[Requirement] | None = hints
        self._metadata: DynamicObj | None = metadata

    @property
    def CWLVersion(self, __unit: None=None) -> str:
        this: CWLWorkflowDescription = self
        return this._cwlVersion

    @CWLVersion.setter
    def CWLVersion(self, version: str) -> None:
        this: CWLWorkflowDescription = self
        this._cwlVersion = version

    @property
    def Steps(self, __unit: None=None) -> Array[WorkflowStep]:
        this: CWLWorkflowDescription = self
        return this._steps

    @Steps.setter
    def Steps(self, steps: Array[WorkflowStep]) -> None:
        this: CWLWorkflowDescription = self
        this._steps = steps

    @property
    def Inputs(self, __unit: None=None) -> Array[CWLInput]:
        this: CWLWorkflowDescription = self
        return this._inputs

    @Inputs.setter
    def Inputs(self, inputs: Array[CWLInput]) -> None:
        this: CWLWorkflowDescription = self
        this._inputs = inputs

    @property
    def Outputs(self, __unit: None=None) -> Array[CWLOutput]:
        this: CWLWorkflowDescription = self
        return this._outputs

    @Outputs.setter
    def Outputs(self, outputs: Array[CWLOutput]) -> None:
        this: CWLWorkflowDescription = self
        this._outputs = outputs

    @property
    def Requirements(self, __unit: None=None) -> Array[Requirement] | None:
        this: CWLWorkflowDescription = self
        return this._requirements

    @Requirements.setter
    def Requirements(self, requirements: Array[Requirement] | None=None) -> None:
        this: CWLWorkflowDescription = self
        this._requirements = requirements

    @property
    def Hints(self, __unit: None=None) -> Array[Requirement] | None:
        this: CWLWorkflowDescription = self
        return this._hints

    @Hints.setter
    def Hints(self, hints: Array[Requirement] | None=None) -> None:
        this: CWLWorkflowDescription = self
        this._hints = hints

    @property
    def Metadata(self, __unit: None=None) -> DynamicObj | None:
        this: CWLWorkflowDescription = self
        return this._metadata

    @Metadata.setter
    def Metadata(self, metadata: DynamicObj | None=None) -> None:
        this: CWLWorkflowDescription = self
        this._metadata = metadata


CWLWorkflowDescription_reflection = _expr519

def CWLWorkflowDescription__ctor_704BBD06(steps: Array[WorkflowStep], inputs: Array[CWLInput], outputs: Array[CWLOutput], cwl_version: str | None=None, requirements: Array[Requirement] | None=None, hints: Array[Requirement] | None=None, metadata: DynamicObj | None=None) -> CWLWorkflowDescription:
    return CWLWorkflowDescription(steps, inputs, outputs, cwl_version, requirements, hints, metadata)


__all__ = ["CWLWorkflowDescription_reflection"]

