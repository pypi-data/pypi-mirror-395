from __future__ import annotations
from dataclasses import dataclass
from ..fable_modules.dynamic_obj.dynamic_obj import (DynamicObj, DynamicObj_reflection)
from ..fable_modules.fable_library.reflection import (TypeInfo, string_type, option_type, record_type, array_type, class_type)
from ..fable_modules.fable_library.types import (Record, Array)
from .requirements import Requirement

def _expr513() -> TypeInfo:
    return record_type("ARCtrl.CWL.StepInput", [], StepInput, lambda: [("Id", string_type), ("Source", option_type(string_type)), ("DefaultValue", option_type(string_type)), ("ValueFrom", option_type(string_type))])


@dataclass(eq = False, repr = False, slots = True)
class StepInput(Record):
    Id: str
    Source: str | None
    DefaultValue: str | None
    ValueFrom: str | None
    @staticmethod
    def create(id: str, source: str | None=None, default_value: str | None=None, value_from: str | None=None) -> StepInput:
        return StepInput(id, source, default_value, value_from)


StepInput_reflection = _expr513

def _expr514() -> TypeInfo:
    return record_type("ARCtrl.CWL.StepOutput", [], StepOutput, lambda: [("Id", array_type(string_type))])


@dataclass(eq = False, repr = False, slots = True)
class StepOutput(Record):
    Id: Array[str]
    @staticmethod
    def create(id: Array[str]) -> StepOutput:
        return StepOutput(id)


StepOutput_reflection = _expr514

def _expr515() -> TypeInfo:
    return class_type("ARCtrl.CWL.WorkflowStep", None, WorkflowStep, DynamicObj_reflection())


class WorkflowStep(DynamicObj):
    def __init__(self, id: str, in_: Array[StepInput], out_: StepOutput, run: str, requirements: Array[Requirement] | None=None, hints: Array[Requirement] | None=None) -> None:
        super().__init__()
        self._id: str = id
        self._in: Array[StepInput] = in_
        self._out: StepOutput = out_
        self._run: str = run
        self._requirements: Array[Requirement] | None = requirements
        self._hints: Array[Requirement] | None = hints

    @property
    def Id(self, __unit: None=None) -> str:
        this: WorkflowStep = self
        return this._id

    @Id.setter
    def Id(self, id: str) -> None:
        this: WorkflowStep = self
        this._id = id

    @property
    def In(self, __unit: None=None) -> Array[StepInput]:
        this: WorkflowStep = self
        return this._in

    @In.setter
    def In(self, in_: Array[StepInput]) -> None:
        this: WorkflowStep = self
        this._in = in_

    @property
    def Out(self, __unit: None=None) -> StepOutput:
        this: WorkflowStep = self
        return this._out

    @Out.setter
    def Out(self, out_: StepOutput) -> None:
        this: WorkflowStep = self
        this._out = out_

    @property
    def Run(self, __unit: None=None) -> str:
        this: WorkflowStep = self
        return this._run

    @Run.setter
    def Run(self, run: str) -> None:
        this: WorkflowStep = self
        this._run = run

    @property
    def Requirements(self, __unit: None=None) -> Array[Requirement] | None:
        this: WorkflowStep = self
        return this._requirements

    @Requirements.setter
    def Requirements(self, requirements: Array[Requirement] | None=None) -> None:
        this: WorkflowStep = self
        this._requirements = requirements

    @property
    def Hints(self, __unit: None=None) -> Array[Requirement] | None:
        this: WorkflowStep = self
        return this._hints

    @Hints.setter
    def Hints(self, hints: Array[Requirement] | None=None) -> None:
        this: WorkflowStep = self
        this._hints = hints


WorkflowStep_reflection = _expr515

def WorkflowStep__ctor_4159DCB0(id: str, in_: Array[StepInput], out_: StepOutput, run: str, requirements: Array[Requirement] | None=None, hints: Array[Requirement] | None=None) -> WorkflowStep:
    return WorkflowStep(id, in_, out_, run, requirements, hints)


__all__ = ["StepInput_reflection", "StepOutput_reflection", "WorkflowStep_reflection"]

