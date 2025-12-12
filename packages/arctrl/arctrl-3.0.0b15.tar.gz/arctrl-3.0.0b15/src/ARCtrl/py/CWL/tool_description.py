from __future__ import annotations
from ..fable_modules.dynamic_obj.dynamic_obj import (DynamicObj, DynamicObj_reflection)
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.types import Array
from .inputs import CWLInput
from .outputs import CWLOutput
from .requirements import Requirement

def _expr517() -> TypeInfo:
    return class_type("ARCtrl.CWL.CWLToolDescription", None, CWLToolDescription, DynamicObj_reflection())


class CWLToolDescription(DynamicObj):
    def __init__(self, outputs: Array[CWLOutput], cwl_version: str | None=None, base_command: Array[str] | None=None, requirements: Array[Requirement] | None=None, hints: Array[Requirement] | None=None, inputs: Array[CWLInput] | None=None, metadata: DynamicObj | None=None) -> None:
        super().__init__()
        self._cwlVersion: str = default_arg(cwl_version, "v1.2")
        self._outputs: Array[CWLOutput] = outputs
        self._baseCommand: Array[str] | None = base_command
        self._requirements: Array[Requirement] | None = requirements
        self._hints: Array[Requirement] | None = hints
        self._inputs: Array[CWLInput] | None = inputs
        self._metadata: DynamicObj | None = metadata

    @property
    def CWLVersion(self, __unit: None=None) -> str:
        this: CWLToolDescription = self
        return this._cwlVersion

    @CWLVersion.setter
    def CWLVersion(self, version: str) -> None:
        this: CWLToolDescription = self
        this._cwlVersion = version

    @property
    def Outputs(self, __unit: None=None) -> Array[CWLOutput]:
        this: CWLToolDescription = self
        return this._outputs

    @Outputs.setter
    def Outputs(self, outputs: Array[CWLOutput]) -> None:
        this: CWLToolDescription = self
        this._outputs = outputs

    @property
    def BaseCommand(self, __unit: None=None) -> Array[str] | None:
        this: CWLToolDescription = self
        return this._baseCommand

    @BaseCommand.setter
    def BaseCommand(self, base_command: Array[str] | None=None) -> None:
        this: CWLToolDescription = self
        this._baseCommand = base_command

    @property
    def Requirements(self, __unit: None=None) -> Array[Requirement] | None:
        this: CWLToolDescription = self
        return this._requirements

    @Requirements.setter
    def Requirements(self, requirements: Array[Requirement] | None=None) -> None:
        this: CWLToolDescription = self
        this._requirements = requirements

    @property
    def Hints(self, __unit: None=None) -> Array[Requirement] | None:
        this: CWLToolDescription = self
        return this._hints

    @Hints.setter
    def Hints(self, hints: Array[Requirement] | None=None) -> None:
        this: CWLToolDescription = self
        this._hints = hints

    @property
    def Inputs(self, __unit: None=None) -> Array[CWLInput] | None:
        this: CWLToolDescription = self
        return this._inputs

    @Inputs.setter
    def Inputs(self, inputs: Array[CWLInput] | None=None) -> None:
        this: CWLToolDescription = self
        this._inputs = inputs

    @property
    def Metadata(self, __unit: None=None) -> DynamicObj | None:
        this: CWLToolDescription = self
        return this._metadata

    @Metadata.setter
    def Metadata(self, metadata: DynamicObj | None=None) -> None:
        this: CWLToolDescription = self
        this._metadata = metadata


CWLToolDescription_reflection = _expr517

def CWLToolDescription__ctor_Z3224DB85(outputs: Array[CWLOutput], cwl_version: str | None=None, base_command: Array[str] | None=None, requirements: Array[Requirement] | None=None, hints: Array[Requirement] | None=None, inputs: Array[CWLInput] | None=None, metadata: DynamicObj | None=None) -> CWLToolDescription:
    return CWLToolDescription(outputs, cwl_version, base_command, requirements, hints, inputs, metadata)


__all__ = ["CWLToolDescription_reflection"]

