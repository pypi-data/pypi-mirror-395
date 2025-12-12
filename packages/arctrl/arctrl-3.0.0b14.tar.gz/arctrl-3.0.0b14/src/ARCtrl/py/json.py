from __future__ import annotations
from collections.abc import Callable
from .Core.arc_types import (ArcAssay, ArcStudy, ArcWorkflow, ArcRun, ArcInvestigation)
from .Core.datamap import Datamap
from .Core.ontology_annotation import OntologyAnnotation
from .Core.person import Person
from .ROCrate.ldobject import (LDNode, LDGraph)
from .arc import ARC
from .JsonIO.assay import (ARCtrl_ArcAssay__ArcAssay_fromJsonString_Static_Z721C83C5, ARCtrl_ArcAssay__ArcAssay_fromCompressedJsonString_Static_Z721C83C5, ARCtrl_ArcAssay__ArcAssay_fromISAJsonString_Static_Z721C83C5, ARCtrl_ArcAssay__ArcAssay_fromROCrateJsonString_Static_Z721C83C5, ARCtrl_ArcAssay__ArcAssay_toJsonString_Static_71136F3F, ARCtrl_ArcAssay__ArcAssay_toCompressedJsonString_Static_71136F3F, ARCtrl_ArcAssay__ArcAssay_toISAJsonString_Static_Z3B036AA, ARCtrl_ArcAssay__ArcAssay_toROCrateJsonString_Static_5CABCA47)
from .JsonIO.datamap import (ARCtrl_Datamap__Datamap_fromJsonString_Static_Z721C83C5, ARCtrl_Datamap__Datamap_toJsonString_Static_71136F3F)
from .JsonIO.investigation import (ARCtrl_ArcInvestigation__ArcInvestigation_fromJsonString_Static_Z721C83C5, ARCtrl_ArcInvestigation__ArcInvestigation_fromCompressedJsonString_Static_Z721C83C5, ARCtrl_ArcInvestigation__ArcInvestigation_fromISAJsonString_Static_Z721C83C5, ARCtrl_ArcInvestigation__ArcInvestigation_fromROCrateJsonString_Static_Z721C83C5, ARCtrl_ArcInvestigation__ArcInvestigation_toJsonString_Static_71136F3F, ARCtrl_ArcInvestigation__ArcInvestigation_toCompressedJsonString_Static_71136F3F, ARCtrl_ArcInvestigation__ArcInvestigation_toISAJsonString_Static_Z3B036AA, ARCtrl_ArcInvestigation__ArcInvestigation_toROCrateJsonString_Static_71136F3F)
from .JsonIO.ldobject import (ARCtrl_ROCrate_LDNode__LDNode_fromROCrateJsonString_Static_Z721C83C5, ARCtrl_ROCrate_LDGraph__LDGraph_fromROCrateJsonString_Static_Z721C83C5, ARCtrl_ROCrate_LDGraph__LDGraph_toROCrateJsonString_Static_71136F3F, ARCtrl_ROCrate_LDNode__LDNode_toROCrateJsonString_Static_71136F3F)
from .JsonIO.ontology_annotation import (ARCtrl_OntologyAnnotation__OntologyAnnotation_fromJsonString_Static_Z721C83C5, ARCtrl_OntologyAnnotation__OntologyAnnotation_fromISAJsonString_Static_Z721C83C5, ARCtrl_OntologyAnnotation__OntologyAnnotation_fromROCrateJsonString_Static_Z721C83C5, ARCtrl_OntologyAnnotation__OntologyAnnotation_toJsonString_Static_71136F3F, ARCtrl_OntologyAnnotation__OntologyAnnotation_toISAJsonString_Static_71136F3F, ARCtrl_OntologyAnnotation__OntologyAnnotation_toROCrateJsonString_Static_71136F3F)
from .JsonIO.person import (ARCtrl_Person__Person_fromJsonString_Static_Z721C83C5, ARCtrl_Person__Person_fromISAJsonString_Static_Z721C83C5, ARCtrl_Person__Person_toJsonString_Static_71136F3F, ARCtrl_Person__Person_toISAJsonString_Static_Z3B036AA, ARCtrl_Person__Person_toROCrateJsonString_Static_71136F3F)
from .JsonIO.run import (ARCtrl_ArcRun__ArcRun_fromJsonString_Static_Z721C83C5, ARCtrl_ArcRun__ArcRun_fromCompressedJsonString_Static_Z721C83C5, ARCtrl_ArcRun__ArcRun_toJsonString_Static_71136F3F, ARCtrl_ArcRun__ArcRun_toCompressedJsonString_Static_71136F3F)
from .JsonIO.study import (ARCtrl_ArcStudy__ArcStudy_fromJsonString_Static_Z721C83C5, ARCtrl_ArcStudy__ArcStudy_fromCompressedJsonString_Static_Z721C83C5, ARCtrl_ArcStudy__ArcStudy_fromISAJsonString_Static_Z721C83C5, ARCtrl_ArcStudy__ArcStudy_fromROCrateJsonString_Static_Z721C83C5, ARCtrl_ArcStudy__ArcStudy_toJsonString_Static_71136F3F, ARCtrl_ArcStudy__ArcStudy_toCompressedJsonString_Static_71136F3F, ARCtrl_ArcStudy__ArcStudy_toISAJsonString_Static_Z3FD920F1, ARCtrl_ArcStudy__ArcStudy_toROCrateJsonString_Static_3BA23086)
from .JsonIO.workflow import (ARCtrl_ArcWorkflow__ArcWorkflow_fromJsonString_Static_Z721C83C5, ARCtrl_ArcWorkflow__ArcWorkflow_fromCompressedJsonString_Static_Z721C83C5, ARCtrl_ArcWorkflow__ArcWorkflow_toJsonString_Static_71136F3F, ARCtrl_ArcWorkflow__ArcWorkflow_toCompressedJsonString_Static_71136F3F)
from .fable_modules.fable_library.list import FSharpList
from .fable_modules.fable_library.reflection import (TypeInfo, class_type)

def _expr4082() -> TypeInfo:
    return class_type("ARCtrl.JsonHelper.OntologyAnnotationJson", None, JsonHelper_OntologyAnnotationJson)


class JsonHelper_OntologyAnnotationJson:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_json_string(self, s: str) -> OntologyAnnotation:
        return ARCtrl_OntologyAnnotation__OntologyAnnotation_fromJsonString_Static_Z721C83C5(s)

    def from_isajson_string(self, s: str) -> OntologyAnnotation:
        return ARCtrl_OntologyAnnotation__OntologyAnnotation_fromISAJsonString_Static_Z721C83C5(s)

    def from_rocrate_json_string(self, s: str) -> OntologyAnnotation:
        return ARCtrl_OntologyAnnotation__OntologyAnnotation_fromROCrateJsonString_Static_Z721C83C5(s)

    def to_json_string(self, oa: OntologyAnnotation, spaces: int | None=None) -> str:
        return ARCtrl_OntologyAnnotation__OntologyAnnotation_toJsonString_Static_71136F3F(spaces)(oa)

    def to_isajson_string(self, oa: OntologyAnnotation, spaces: int | None=None) -> str:
        return ARCtrl_OntologyAnnotation__OntologyAnnotation_toISAJsonString_Static_71136F3F(spaces)(oa)

    def to_rocrate_json_string(self, oa: OntologyAnnotation, spaces: int | None=None) -> str:
        return ARCtrl_OntologyAnnotation__OntologyAnnotation_toROCrateJsonString_Static_71136F3F(spaces)(oa)


JsonHelper_OntologyAnnotationJson_reflection = _expr4082

def JsonHelper_OntologyAnnotationJson__ctor(__unit: None=None) -> JsonHelper_OntologyAnnotationJson:
    return JsonHelper_OntologyAnnotationJson(__unit)


def _expr4083() -> TypeInfo:
    return class_type("ARCtrl.JsonHelper.PersonJson", None, JsonHelper_PersonJson)


class JsonHelper_PersonJson:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_json_string(self, s: str) -> Person:
        return ARCtrl_Person__Person_fromJsonString_Static_Z721C83C5(s)

    def from_isajson_string(self, s: str) -> Person:
        return ARCtrl_Person__Person_fromISAJsonString_Static_Z721C83C5(s)

    def from_rocrate_json_string(self, s: str) -> LDNode:
        return ARCtrl_ROCrate_LDNode__LDNode_fromROCrateJsonString_Static_Z721C83C5(s)

    def to_json_string(self, person: Person, spaces: int | None=None) -> str:
        return ARCtrl_Person__Person_toJsonString_Static_71136F3F(spaces)(person)

    def to_isajson_string(self, person: Person, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
        return ARCtrl_Person__Person_toISAJsonString_Static_Z3B036AA(spaces, use_idreferencing)(person)

    def to_rocrate_json_string(self, person: Person, spaces: int | None=None) -> str:
        return ARCtrl_Person__Person_toROCrateJsonString_Static_71136F3F(spaces)(person)


JsonHelper_PersonJson_reflection = _expr4083

def JsonHelper_PersonJson__ctor(__unit: None=None) -> JsonHelper_PersonJson:
    return JsonHelper_PersonJson(__unit)


def _expr4084() -> TypeInfo:
    return class_type("ARCtrl.JsonHelper.DatamapJson", None, JsonHelper_DatamapJson)


class JsonHelper_DatamapJson:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_json_string(self, s: str) -> Datamap:
        return ARCtrl_Datamap__Datamap_fromJsonString_Static_Z721C83C5(s)

    def to_json_string(self, datamap: Datamap, spaces: int | None=None) -> str:
        return ARCtrl_Datamap__Datamap_toJsonString_Static_71136F3F(spaces)(datamap)


JsonHelper_DatamapJson_reflection = _expr4084

def JsonHelper_DatamapJson__ctor(__unit: None=None) -> JsonHelper_DatamapJson:
    return JsonHelper_DatamapJson(__unit)


def _expr4085() -> TypeInfo:
    return class_type("ARCtrl.JsonHelper.AssayJson", None, JsonHelper_AssayJson)


class JsonHelper_AssayJson:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_json_string(self, s: str) -> ArcAssay:
        return ARCtrl_ArcAssay__ArcAssay_fromJsonString_Static_Z721C83C5(s)

    def from_compressed_json_string(self, s: str) -> ArcAssay:
        return ARCtrl_ArcAssay__ArcAssay_fromCompressedJsonString_Static_Z721C83C5(s)

    def from_isajson_string(self, s: str) -> ArcAssay:
        return ARCtrl_ArcAssay__ArcAssay_fromISAJsonString_Static_Z721C83C5(s)

    def from_rocrate_json_string(self, s: str) -> ArcAssay:
        return ARCtrl_ArcAssay__ArcAssay_fromROCrateJsonString_Static_Z721C83C5(s)

    def to_json_string(self, assay: ArcAssay, spaces: int | None=None) -> str:
        return ARCtrl_ArcAssay__ArcAssay_toJsonString_Static_71136F3F(spaces)(assay)

    def to_compressed_json_string(self, assay: ArcAssay, spaces: int | None=None) -> str:
        return ARCtrl_ArcAssay__ArcAssay_toCompressedJsonString_Static_71136F3F(spaces)(assay)

    def to_isajson_string(self, assay: ArcAssay, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
        return ARCtrl_ArcAssay__ArcAssay_toISAJsonString_Static_Z3B036AA(spaces, use_idreferencing)(assay)

    def to_rocrate_json_string(self, assay: ArcAssay, study_name: str, spaces: int | None=None) -> str:
        return ARCtrl_ArcAssay__ArcAssay_toROCrateJsonString_Static_5CABCA47(study_name, spaces)(assay)


JsonHelper_AssayJson_reflection = _expr4085

def JsonHelper_AssayJson__ctor(__unit: None=None) -> JsonHelper_AssayJson:
    return JsonHelper_AssayJson(__unit)


def _expr4086() -> TypeInfo:
    return class_type("ARCtrl.JsonHelper.StudyJson", None, JsonHelper_StudyJson)


class JsonHelper_StudyJson:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_json_string(self, s: str) -> ArcStudy:
        return ARCtrl_ArcStudy__ArcStudy_fromJsonString_Static_Z721C83C5(s)

    def from_compressed_json_string(self, s: str) -> ArcStudy:
        return ARCtrl_ArcStudy__ArcStudy_fromCompressedJsonString_Static_Z721C83C5(s)

    def from_isajson_string(self, s: str) -> tuple[ArcStudy, FSharpList[ArcAssay]]:
        return ARCtrl_ArcStudy__ArcStudy_fromISAJsonString_Static_Z721C83C5(s)

    def from_rocrate_json_string(self, s: str) -> tuple[ArcStudy, FSharpList[ArcAssay]]:
        return ARCtrl_ArcStudy__ArcStudy_fromROCrateJsonString_Static_Z721C83C5(s)

    def to_json_string(self, study: ArcStudy, spaces: int | None=None) -> str:
        return ARCtrl_ArcStudy__ArcStudy_toJsonString_Static_71136F3F(spaces)(study)

    def to_compressed_json_string(self, study: ArcStudy, spaces: int | None=None) -> str:
        return ARCtrl_ArcStudy__ArcStudy_toCompressedJsonString_Static_71136F3F(spaces)(study)

    def to_isajson_string(self, study: ArcStudy, assays: FSharpList[ArcAssay] | None=None, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
        return ARCtrl_ArcStudy__ArcStudy_toISAJsonString_Static_Z3FD920F1(assays, spaces, use_idreferencing)(study)

    def to_rocrate_json_string(self, study: ArcStudy, assays: FSharpList[ArcAssay] | None=None, spaces: int | None=None) -> str:
        return ARCtrl_ArcStudy__ArcStudy_toROCrateJsonString_Static_3BA23086(assays, spaces)(study)


JsonHelper_StudyJson_reflection = _expr4086

def JsonHelper_StudyJson__ctor(__unit: None=None) -> JsonHelper_StudyJson:
    return JsonHelper_StudyJson(__unit)


def _expr4087() -> TypeInfo:
    return class_type("ARCtrl.JsonHelper.WorkflowJson", None, JsonHelper_WorkflowJson)


class JsonHelper_WorkflowJson:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_json_string(self, s: str) -> ArcWorkflow:
        return ARCtrl_ArcWorkflow__ArcWorkflow_fromJsonString_Static_Z721C83C5(s)

    def from_compressed_json_string(self, s: str) -> ArcWorkflow:
        return ARCtrl_ArcWorkflow__ArcWorkflow_fromCompressedJsonString_Static_Z721C83C5(s)

    def to_json_string(self, workflow: ArcWorkflow, spaces: int | None=None) -> str:
        return ARCtrl_ArcWorkflow__ArcWorkflow_toJsonString_Static_71136F3F(spaces)(workflow)

    def to_compressed_json_string(self, workflow: ArcWorkflow, spaces: int | None=None) -> str:
        return ARCtrl_ArcWorkflow__ArcWorkflow_toCompressedJsonString_Static_71136F3F(spaces)(workflow)


JsonHelper_WorkflowJson_reflection = _expr4087

def JsonHelper_WorkflowJson__ctor(__unit: None=None) -> JsonHelper_WorkflowJson:
    return JsonHelper_WorkflowJson(__unit)


def _expr4088() -> TypeInfo:
    return class_type("ARCtrl.JsonHelper.RunJson", None, JsonHelper_RunJson)


class JsonHelper_RunJson:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_json_string(self, s: str) -> ArcRun:
        return ARCtrl_ArcRun__ArcRun_fromJsonString_Static_Z721C83C5(s)

    def from_compressed_json_string(self, s: str) -> ArcRun:
        return ARCtrl_ArcRun__ArcRun_fromCompressedJsonString_Static_Z721C83C5(s)

    def to_json_string(self, run: ArcRun, spaces: int | None=None) -> str:
        return ARCtrl_ArcRun__ArcRun_toJsonString_Static_71136F3F(spaces)(run)

    def to_compressed_json_string(self, run: ArcRun, spaces: int | None=None) -> str:
        return ARCtrl_ArcRun__ArcRun_toCompressedJsonString_Static_71136F3F(spaces)(run)


JsonHelper_RunJson_reflection = _expr4088

def JsonHelper_RunJson__ctor(__unit: None=None) -> JsonHelper_RunJson:
    return JsonHelper_RunJson(__unit)


def _expr4089() -> TypeInfo:
    return class_type("ARCtrl.JsonHelper.InvestigationJson", None, JsonHelper_InvestigationJson)


class JsonHelper_InvestigationJson:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_json_string(self, s: str) -> ArcInvestigation:
        return ARCtrl_ArcInvestigation__ArcInvestigation_fromJsonString_Static_Z721C83C5(s)

    def from_compressed_json_string(self, s: str) -> ArcInvestigation:
        return ARCtrl_ArcInvestigation__ArcInvestigation_fromCompressedJsonString_Static_Z721C83C5(s)

    def from_isajson_string(self, s: str) -> ArcInvestigation:
        return ARCtrl_ArcInvestigation__ArcInvestigation_fromISAJsonString_Static_Z721C83C5(s)

    def from_rocrate_json_string(self, s: str) -> ArcInvestigation:
        return ARCtrl_ArcInvestigation__ArcInvestigation_fromROCrateJsonString_Static_Z721C83C5(s)

    def to_json_string(self, investigation: ArcInvestigation, spaces: int | None=None) -> str:
        return ARCtrl_ArcInvestigation__ArcInvestigation_toJsonString_Static_71136F3F(spaces)(investigation)

    def to_compressed_json_string(self, investigation: ArcInvestigation, spaces: int | None=None) -> str:
        return ARCtrl_ArcInvestigation__ArcInvestigation_toCompressedJsonString_Static_71136F3F(spaces)(investigation)

    def to_isajson_string(self, investigation: ArcInvestigation, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
        return ARCtrl_ArcInvestigation__ArcInvestigation_toISAJsonString_Static_Z3B036AA(spaces, use_idreferencing)(investigation)

    def to_rocrate_json_string(self, investigation: ArcInvestigation, spaces: int | None=None) -> str:
        return ARCtrl_ArcInvestigation__ArcInvestigation_toROCrateJsonString_Static_71136F3F(spaces)(investigation)


JsonHelper_InvestigationJson_reflection = _expr4089

def JsonHelper_InvestigationJson__ctor(__unit: None=None) -> JsonHelper_InvestigationJson:
    return JsonHelper_InvestigationJson(__unit)


def _expr4090() -> TypeInfo:
    return class_type("ARCtrl.JsonHelper.ARCJson", None, JsonHelper_ARCJson)


class JsonHelper_ARCJson:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_rocrate_json_string(self, s: str) -> ARC:
        return ARC.from_rocrate_json_string(s)

    def to_rocrate_json_string(self, spaces: int | None=None) -> Callable[[ARC], str]:
        return ARC.to_rocrate_json_string(spaces)


JsonHelper_ARCJson_reflection = _expr4090

def JsonHelper_ARCJson__ctor(__unit: None=None) -> JsonHelper_ARCJson:
    return JsonHelper_ARCJson(__unit)


def _expr4091() -> TypeInfo:
    return class_type("ARCtrl.JsonHelper.LDGraphJson", None, JsonHelper_LDGraphJson)


class JsonHelper_LDGraphJson:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_rocrate_json_string(self, s: str) -> LDGraph:
        return ARCtrl_ROCrate_LDGraph__LDGraph_fromROCrateJsonString_Static_Z721C83C5(s)

    def to_rocrate_json_string(self, spaces: int | None=None) -> Callable[[LDGraph], str]:
        return ARCtrl_ROCrate_LDGraph__LDGraph_toROCrateJsonString_Static_71136F3F(spaces)


JsonHelper_LDGraphJson_reflection = _expr4091

def JsonHelper_LDGraphJson__ctor(__unit: None=None) -> JsonHelper_LDGraphJson:
    return JsonHelper_LDGraphJson(__unit)


def _expr4092() -> TypeInfo:
    return class_type("ARCtrl.JsonHelper.LDNodeJson", None, JsonHelper_LDNodeJson)


class JsonHelper_LDNodeJson:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_rocrate_json_string(self, s: str) -> LDNode:
        return ARCtrl_ROCrate_LDNode__LDNode_fromROCrateJsonString_Static_Z721C83C5(s)

    def to_rocrate_json_string(self, spaces: int | None=None) -> Callable[[LDNode], str]:
        return ARCtrl_ROCrate_LDNode__LDNode_toROCrateJsonString_Static_71136F3F(spaces)


JsonHelper_LDNodeJson_reflection = _expr4092

def JsonHelper_LDNodeJson__ctor(__unit: None=None) -> JsonHelper_LDNodeJson:
    return JsonHelper_LDNodeJson(__unit)


def _expr4093() -> TypeInfo:
    return class_type("ARCtrl.JsonController", None, JsonController)


class JsonController:
    @staticmethod
    def OntologyAnnotation() -> JsonHelper_OntologyAnnotationJson:
        return JsonHelper_OntologyAnnotationJson()

    @staticmethod
    def Person() -> JsonHelper_PersonJson:
        return JsonHelper_PersonJson()

    @staticmethod
    def Datamap() -> JsonHelper_DatamapJson:
        return JsonHelper_DatamapJson()

    @staticmethod
    def Assay() -> JsonHelper_AssayJson:
        return JsonHelper_AssayJson()

    @staticmethod
    def Study() -> JsonHelper_StudyJson:
        return JsonHelper_StudyJson()

    @staticmethod
    def Workflow() -> JsonHelper_WorkflowJson:
        return JsonHelper_WorkflowJson()

    @staticmethod
    def Run() -> JsonHelper_RunJson:
        return JsonHelper_RunJson()

    @staticmethod
    def Investigation() -> JsonHelper_InvestigationJson:
        return JsonHelper_InvestigationJson()

    @staticmethod
    def ARC() -> JsonHelper_ARCJson:
        return JsonHelper_ARCJson()

    @staticmethod
    def LDGraph() -> JsonHelper_LDGraphJson:
        return JsonHelper_LDGraphJson()

    @staticmethod
    def LDNode() -> JsonHelper_LDNodeJson:
        return JsonHelper_LDNodeJson()


JsonController_reflection = _expr4093

__all__ = ["JsonHelper_OntologyAnnotationJson_reflection", "JsonHelper_PersonJson_reflection", "JsonHelper_DatamapJson_reflection", "JsonHelper_AssayJson_reflection", "JsonHelper_StudyJson_reflection", "JsonHelper_WorkflowJson_reflection", "JsonHelper_RunJson_reflection", "JsonHelper_InvestigationJson_reflection", "JsonHelper_ARCJson_reflection", "JsonHelper_LDGraphJson_reflection", "JsonHelper_LDNodeJson_reflection", "JsonController_reflection"]

