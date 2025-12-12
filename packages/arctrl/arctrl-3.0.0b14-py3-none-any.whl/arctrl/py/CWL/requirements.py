from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from ..fable_modules.dynamic_obj.dynamic_obj import (DynamicObj, DynamicObj_reflection)
from ..fable_modules.dynamic_obj.dyn_obj import set_optional_property
from ..fable_modules.fable_library.reflection import (TypeInfo, string_type, option_type, class_type, record_type, array_type, float64_type, union_type)
from ..fable_modules.fable_library.types import (Record, FSharpRef, Array, Union)
from .cwltypes import (SchemaDefRequirementType_reflection, SoftwarePackage_reflection, CWLType_reflection)

def _expr505() -> TypeInfo:
    return record_type("ARCtrl.CWL.DockerRequirement", [], DockerRequirement, lambda: [("DockerPull", option_type(string_type)), ("DockerFile", option_type(class_type("Microsoft.FSharp.Collections.FSharpMap`2", [string_type, string_type]))), ("DockerImageId", option_type(string_type))])


@dataclass(eq = False, repr = False, slots = True)
class DockerRequirement(Record):
    DockerPull: str | None
    DockerFile: Any | None
    DockerImageId: str | None

DockerRequirement_reflection = _expr505

def DockerRequirement_create_Z3FC43B23(docker_pull: str | None=None, docker_file: Any | None=None, docker_image_id: str | None=None) -> DockerRequirement:
    return DockerRequirement(docker_pull, docker_file, docker_image_id)


def _expr506() -> TypeInfo:
    return record_type("ARCtrl.CWL.EnvironmentDef", [], EnvironmentDef, lambda: [("EnvName", string_type), ("EnvValue", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class EnvironmentDef(Record):
    EnvName: str
    EnvValue: str

EnvironmentDef_reflection = _expr506

def _expr507() -> TypeInfo:
    return class_type("ARCtrl.CWL.ResourceRequirementInstance", None, ResourceRequirementInstance, DynamicObj_reflection())


class ResourceRequirementInstance(DynamicObj):
    def __init__(self, cores_min: Any | None=None, cores_max: Any | None=None, ram_min: Any | None=None, ram_max: Any | None=None, tmpdir_min: Any | None=None, tmpdir_max: Any | None=None, outdir_min: Any | None=None, outdir_max: Any | None=None) -> None:
        super().__init__()
        this: FSharpRef[ResourceRequirementInstance] = FSharpRef(None)
        this.contents = self
        self.init_004031: int = 1
        set_optional_property("coresMin", cores_min, this.contents)
        set_optional_property("coresMax", cores_max, this.contents)
        set_optional_property("ramMin", ram_min, this.contents)
        set_optional_property("ramMax", ram_max, this.contents)
        set_optional_property("tmpdirMin", tmpdir_min, this.contents)
        set_optional_property("tmpdirMax", tmpdir_max, this.contents)
        set_optional_property("outdirMin", outdir_min, this.contents)
        set_optional_property("outdirMax", outdir_max, this.contents)


ResourceRequirementInstance_reflection = _expr507

def ResourceRequirementInstance__ctor_D76FC00(cores_min: Any | None=None, cores_max: Any | None=None, ram_min: Any | None=None, ram_max: Any | None=None, tmpdir_min: Any | None=None, tmpdir_max: Any | None=None, outdir_min: Any | None=None, outdir_max: Any | None=None) -> ResourceRequirementInstance:
    return ResourceRequirementInstance(cores_min, cores_max, ram_min, ram_max, tmpdir_min, tmpdir_max, outdir_min, outdir_max)


def _expr508() -> TypeInfo:
    return union_type("ARCtrl.CWL.Requirement", [], Requirement, lambda: [[], [("Item", array_type(SchemaDefRequirementType_reflection()))], [("Item", DockerRequirement_reflection())], [("Item", array_type(SoftwarePackage_reflection()))], [("Item", array_type(CWLType_reflection()))], [("Item", array_type(EnvironmentDef_reflection()))], [], [("Item", ResourceRequirementInstance_reflection())], [], [], [], [("Item", float64_type)], [], [], [], []])


class Requirement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["InlineJavascriptRequirement", "SchemaDefRequirement", "DockerRequirement", "SoftwareRequirement", "InitialWorkDirRequirement", "EnvVarRequirement", "ShellCommandRequirement", "ResourceRequirement", "WorkReuseRequirement", "NetworkAccessRequirement", "InplaceUpdateRequirement", "ToolTimeLimitRequirement", "SubworkflowFeatureRequirement", "ScatterFeatureRequirement", "MultipleInputFeatureRequirement", "StepInputExpressionRequirement"]


Requirement_reflection = _expr508

__all__ = ["DockerRequirement_reflection", "DockerRequirement_create_Z3FC43B23", "EnvironmentDef_reflection", "ResourceRequirementInstance_reflection", "Requirement_reflection"]

