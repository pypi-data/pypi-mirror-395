from __future__ import annotations
from .Core.arc_types import (ArcAssay, ArcStudy, ArcWorkflow, ArcRun, ArcInvestigation)
from .FileSystem.file_system import FileSystem
from .ROCrate.ldcontext import LDContext
from .ROCrate.ldobject import (LDNode, LDGraph)
from .Conversion.assay import (AssayConversion_composeAssay_Z5C53FD5C, AssayConversion_decomposeAssay_Z6839B9E8)
from .Conversion.investigation import (InvestigationConversion_composeInvestigation_5AEC717D, InvestigationConversion_decomposeInvestigation_Z6839B9E8)
from .Conversion.run import (RunConversion_composeRun_Z8CC08AC, RunConversion_decomposeRun_Z6839B9E8)
from .Conversion.study import (StudyConversion_composeStudy_ZFE0E38E, StudyConversion_decomposeStudy_Z6839B9E8)
from .Conversion.workflow import (WorkflowConversion_composeWorkflow_42450E6E, WorkflowConversion_decomposeWorkflow_Z6839B9E8)
from .fable_modules.fable_library.reflection import (TypeInfo, class_type)

def ARCtrl_ArcAssay__ArcAssay_ToROCrateAssay_1695DD5C(this: ArcAssay, fs: FileSystem | None=None) -> LDNode:
    return AssayConversion_composeAssay_Z5C53FD5C(this, fs)


def ARCtrl_ArcAssay__ArcAssay_fromROCrateAssay_Static_Z6839B9E8(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcAssay:
    return AssayConversion_decomposeAssay_Z6839B9E8(a, graph, context)


def ARCtrl_ArcStudy__ArcStudy_ToROCrateStudy_1695DD5C(this: ArcStudy, fs: FileSystem | None=None) -> LDNode:
    return StudyConversion_composeStudy_ZFE0E38E(this, fs)


def ARCtrl_ArcStudy__ArcStudy_fromROCrateStudy_Static_Z6839B9E8(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcStudy:
    return StudyConversion_decomposeStudy_Z6839B9E8(a, graph, context)


def ARCtrl_ArcWorkflow__ArcWorkflow_ToROCrateWorkflow_1695DD5C(this: ArcWorkflow, fs: FileSystem | None=None) -> LDNode:
    return WorkflowConversion_composeWorkflow_42450E6E(this, fs)


def ARCtrl_ArcWorkflow__ArcWorkflow_fromROCrateWorkflow_Static_Z6839B9E8(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcWorkflow:
    return WorkflowConversion_decomposeWorkflow_Z6839B9E8(a, graph, context)


def ARCtrl_ArcRun__ArcRun_ToROCrateRun_1695DD5C(this: ArcRun, fs: FileSystem | None=None) -> LDNode:
    return RunConversion_composeRun_Z8CC08AC(this, fs)


def ARCtrl_ArcRun__ArcRun_fromROCrateRun_Static_Z6839B9E8(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcRun:
    return RunConversion_decomposeRun_Z6839B9E8(a, graph, context)


def ARCtrl_ArcInvestigation__ArcInvestigation_ToROCrateInvestigation_1695DD5C(this: ArcInvestigation, fs: FileSystem | None=None) -> LDNode:
    return InvestigationConversion_composeInvestigation_5AEC717D(this, fs)


def ARCtrl_ArcInvestigation__ArcInvestigation_fromROCrateInvestigation_Static_Z6839B9E8(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcInvestigation:
    return InvestigationConversion_decomposeInvestigation_Z6839B9E8(a, graph, context)


def ARCtrl_ROCrate_Dataset__Dataset_toArcAssay_Static_Z6839B9E8(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcAssay:
    return AssayConversion_decomposeAssay_Z6839B9E8(a, graph, context)


def ARCtrl_ROCrate_Dataset__Dataset_fromArcAssay_Static_1501C0F8(a: ArcAssay) -> LDNode:
    return AssayConversion_composeAssay_Z5C53FD5C(a)


def ARCtrl_ROCrate_Dataset__Dataset_toArcStudy_Static_Z6839B9E8(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcStudy:
    return StudyConversion_decomposeStudy_Z6839B9E8(a, graph, context)


def ARCtrl_ROCrate_Dataset__Dataset_fromArcStudy_Static_1680536E(a: ArcStudy) -> LDNode:
    return StudyConversion_composeStudy_ZFE0E38E(a)


def ARCtrl_ROCrate_Dataset__Dataset_toArcWorkflow_Static_Z6839B9E8(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcWorkflow:
    return WorkflowConversion_decomposeWorkflow_Z6839B9E8(a, graph, context)


def ARCtrl_ROCrate_Dataset__Dataset_fromArcWorkflow_Static_Z1C75CB0E(a: ArcWorkflow) -> LDNode:
    return WorkflowConversion_composeWorkflow_42450E6E(a)


def ARCtrl_ROCrate_Dataset__Dataset_toArcRun_Static_Z6839B9E8(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcRun:
    return RunConversion_decomposeRun_Z6839B9E8(a, graph, context)


def ARCtrl_ROCrate_Dataset__Dataset_fromArcRun_Static_Z3EFAF6F8(a: ArcRun) -> LDNode:
    return RunConversion_composeRun_Z8CC08AC(a)


def ARCtrl_ROCrate_Dataset__Dataset_toArcInvestigation_Static_Z6839B9E8(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcInvestigation:
    return InvestigationConversion_decomposeInvestigation_Z6839B9E8(a, graph, context)


def ARCtrl_ROCrate_Dataset__Dataset_fromArcInvestigation_Static_Z720BD3FF(a: ArcInvestigation) -> LDNode:
    return InvestigationConversion_composeInvestigation_5AEC717D(a)


def _expr3993() -> TypeInfo:
    return class_type("ARCtrl.Conversion.TypeExtensions.Conversion", None, Conversion)


class Conversion:
    @staticmethod
    def arc_assay_to_dataset(a: ArcAssay, fs: FileSystem | None=None) -> LDNode:
        return ARCtrl_ArcAssay__ArcAssay_ToROCrateAssay_1695DD5C(a, fs)

    @staticmethod
    def dataset_to_arc_assay(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcAssay:
        return ARCtrl_ArcAssay__ArcAssay_fromROCrateAssay_Static_Z6839B9E8(a, graph, context)

    @staticmethod
    def arc_study_to_dataset(a: ArcStudy, fs: FileSystem | None=None) -> LDNode:
        return ARCtrl_ArcStudy__ArcStudy_ToROCrateStudy_1695DD5C(a, fs)

    @staticmethod
    def dataset_to_arc_study(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcStudy:
        return ARCtrl_ArcStudy__ArcStudy_fromROCrateStudy_Static_Z6839B9E8(a, graph, context)

    @staticmethod
    def arc_workflow_to_dataset(a: ArcWorkflow, fs: FileSystem | None=None) -> LDNode:
        return ARCtrl_ArcWorkflow__ArcWorkflow_ToROCrateWorkflow_1695DD5C(a, fs)

    @staticmethod
    def dataset_to_arc_workflow(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcWorkflow:
        return ARCtrl_ArcWorkflow__ArcWorkflow_fromROCrateWorkflow_Static_Z6839B9E8(a, graph, context)

    @staticmethod
    def arc_run_to_dataset(a: ArcRun, fs: FileSystem | None=None) -> LDNode:
        return ARCtrl_ArcRun__ArcRun_ToROCrateRun_1695DD5C(a, fs)

    @staticmethod
    def dataset_to_arc_run(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcRun:
        return ARCtrl_ArcRun__ArcRun_fromROCrateRun_Static_Z6839B9E8(a, graph, context)

    @staticmethod
    def arc_investigation_to_dataset(a: ArcInvestigation, fs: FileSystem | None=None) -> LDNode:
        return ARCtrl_ArcInvestigation__ArcInvestigation_ToROCrateInvestigation_1695DD5C(a, fs)

    @staticmethod
    def dataset_to_arc_investigation(a: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcInvestigation:
        return ARCtrl_ArcInvestigation__ArcInvestigation_fromROCrateInvestigation_Static_Z6839B9E8(a, graph, context)


Conversion_reflection = _expr3993

__all__ = ["ARCtrl_ArcAssay__ArcAssay_ToROCrateAssay_1695DD5C", "ARCtrl_ArcAssay__ArcAssay_fromROCrateAssay_Static_Z6839B9E8", "ARCtrl_ArcStudy__ArcStudy_ToROCrateStudy_1695DD5C", "ARCtrl_ArcStudy__ArcStudy_fromROCrateStudy_Static_Z6839B9E8", "ARCtrl_ArcWorkflow__ArcWorkflow_ToROCrateWorkflow_1695DD5C", "ARCtrl_ArcWorkflow__ArcWorkflow_fromROCrateWorkflow_Static_Z6839B9E8", "ARCtrl_ArcRun__ArcRun_ToROCrateRun_1695DD5C", "ARCtrl_ArcRun__ArcRun_fromROCrateRun_Static_Z6839B9E8", "ARCtrl_ArcInvestigation__ArcInvestigation_ToROCrateInvestigation_1695DD5C", "ARCtrl_ArcInvestigation__ArcInvestigation_fromROCrateInvestigation_Static_Z6839B9E8", "ARCtrl_ROCrate_Dataset__Dataset_toArcAssay_Static_Z6839B9E8", "ARCtrl_ROCrate_Dataset__Dataset_fromArcAssay_Static_1501C0F8", "ARCtrl_ROCrate_Dataset__Dataset_toArcStudy_Static_Z6839B9E8", "ARCtrl_ROCrate_Dataset__Dataset_fromArcStudy_Static_1680536E", "ARCtrl_ROCrate_Dataset__Dataset_toArcWorkflow_Static_Z6839B9E8", "ARCtrl_ROCrate_Dataset__Dataset_fromArcWorkflow_Static_Z1C75CB0E", "ARCtrl_ROCrate_Dataset__Dataset_toArcRun_Static_Z6839B9E8", "ARCtrl_ROCrate_Dataset__Dataset_fromArcRun_Static_Z3EFAF6F8", "ARCtrl_ROCrate_Dataset__Dataset_toArcInvestigation_Static_Z6839B9E8", "ARCtrl_ROCrate_Dataset__Dataset_fromArcInvestigation_Static_Z720BD3FF", "Conversion_reflection"]

