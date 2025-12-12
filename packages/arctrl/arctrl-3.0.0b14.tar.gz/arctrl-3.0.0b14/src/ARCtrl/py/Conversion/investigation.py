from __future__ import annotations
from typing import Any
from ..Core.arc_types import (ArcAssay, ArcStudy, ArcWorkflow, ArcRun, ArcInvestigation)
from ..Core.comment import Comment
from ..Core.Helper.collections_ import (Option_fromSeq, ResizeArray_map, ResizeArray_filter)
from ..Core.person import Person
from ..Core.publication import Publication
from ..FileSystem.file_system import FileSystem
from ..ROCrate.ldcontext import LDContext
from ..ROCrate.ldobject import (LDNode, LDGraph)
from ..ROCrate.LDTypes.dataset import LDDataset
from ..fable_modules.fable_library.date import now
from ..fable_modules.fable_library.option import (bind, default_arg, map)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.seq import (to_list, delay, append)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from .assay import (AssayConversion_composeAssay_Z5C53FD5C, AssayConversion_decomposeAssay_Z6839B9E8)
from .basic import (BaseTypes_composeComment_Z13201A7E, BaseTypes_decomposeComment_Z2F770004)
from .date_time import (try_from_string, to_string)
from .person import (PersonConversion_composePerson_Z64D846DC, PersonConversion_decomposePerson_Z6839B9E8)
from .run import (RunConversion_composeRun_Z8CC08AC, RunConversion_decomposeRun_Z6839B9E8)
from .scholarly_article import (ScholarlyArticleConversion_composeScholarlyArticle_D324A6D, ScholarlyArticleConversion_decomposeScholarlyArticle_Z6839B9E8)
from .study import (StudyConversion_composeStudy_ZFE0E38E, StudyConversion_decomposeStudy_Z6839B9E8)
from .workflow import (WorkflowConversion_composeWorkflow_42450E6E, WorkflowConversion_decomposeWorkflow_Z6839B9E8)

def _expr3984() -> TypeInfo:
    return class_type("ARCtrl.Conversion.InvestigationConversion", None, InvestigationConversion)


class InvestigationConversion:
    ...

InvestigationConversion_reflection = _expr3984

def InvestigationConversion_composeInvestigation_5AEC717D(investigation: ArcInvestigation, fs: FileSystem | None=None) -> LDNode:
    name: str
    match_value: str | None = investigation.Title
    if match_value is None:
        raise Exception("Investigation must have a title")

    else: 
        name = match_value

    def _arrow3985(s: str, investigation: Any=investigation, fs: Any=fs) -> Any | None:
        return try_from_string(s)

    date_created: Any | None = bind(_arrow3985, investigation.SubmissionDate)
    def _arrow3986(s_1: str, investigation: Any=investigation, fs: Any=fs) -> Any | None:
        return try_from_string(s_1)

    date_published: Any = default_arg(bind(_arrow3986, investigation.PublicReleaseDate), now())
    def f(p: Publication, investigation: Any=investigation, fs: Any=fs) -> LDNode:
        return ScholarlyArticleConversion_composeScholarlyArticle_D324A6D(p)

    publications: Array[LDNode] | None = Option_fromSeq(ResizeArray_map(f, investigation.Publications))
    def f_1(c: Person, investigation: Any=investigation, fs: Any=fs) -> LDNode:
        return PersonConversion_composePerson_Z64D846DC(c)

    creators: Array[LDNode] | None = Option_fromSeq(ResizeArray_map(f_1, investigation.Contacts))
    def f_2(c_1: Comment, investigation: Any=investigation, fs: Any=fs) -> LDNode:
        return BaseTypes_composeComment_Z13201A7E(c_1)

    comments: Array[LDNode] | None = Option_fromSeq(ResizeArray_map(f_2, investigation.Comments))
    def _arrow3990(__unit: None=None, investigation: Any=investigation, fs: Any=fs) -> IEnumerable_1[LDNode]:
        def f_3(a_3: ArcAssay) -> LDNode:
            return AssayConversion_composeAssay_Z5C53FD5C(a_3, fs)

        def _arrow3989(__unit: None=None) -> IEnumerable_1[LDNode]:
            def f_4(s_2: ArcStudy) -> LDNode:
                return StudyConversion_composeStudy_ZFE0E38E(s_2, fs)

            def _arrow3988(__unit: None=None) -> IEnumerable_1[LDNode]:
                def f_5(w: ArcWorkflow) -> LDNode:
                    return WorkflowConversion_composeWorkflow_42450E6E(w, fs)

                def _arrow3987(__unit: None=None) -> IEnumerable_1[LDNode]:
                    def f_6(r: ArcRun) -> LDNode:
                        return RunConversion_composeRun_Z8CC08AC(r, fs)

                    return ResizeArray_map(f_6, investigation.Runs)

                return append(ResizeArray_map(f_5, investigation.Workflows), delay(_arrow3987))

            return append(ResizeArray_map(f_4, investigation.Studies), delay(_arrow3988))

        return append(ResizeArray_map(f_3, investigation.Assays), delay(_arrow3989))

    has_parts: Array[LDNode] | None = Option_fromSeq(list(to_list(delay(_arrow3990))))
    mentions: Array[LDNode] | None = Option_fromSeq([])
    return LDDataset.create_investigation(investigation.Identifier, name, None, creators, date_created, date_published, None, investigation.Description, has_parts, publications, comments, mentions)


def InvestigationConversion_decomposeInvestigation_Z6839B9E8(investigation: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcInvestigation:
    title: str | None
    match_value: str | None = LDDataset.try_get_name_as_string(investigation, context)
    title = LDDataset.try_get_headline_as_string(investigation, context) if (match_value is None) else match_value
    def _arrow3991(d: Any, investigation: Any=investigation, graph: Any=graph, context: Any=context) -> str:
        return to_string(d)

    date_created: str | None = map(_arrow3991, LDDataset.try_get_date_created_as_date_time(investigation, context))
    def _arrow3992(d_1: Any, investigation: Any=investigation, graph: Any=graph, context: Any=context) -> str:
        return to_string(d_1)

    date_published: str | None = map(_arrow3992, LDDataset.try_get_date_published_as_date_time(investigation, context))
    def f(p: LDNode, investigation: Any=investigation, graph: Any=graph, context: Any=context) -> Publication:
        return ScholarlyArticleConversion_decomposeScholarlyArticle_Z6839B9E8(p, graph, context)

    publications: Array[Publication] = ResizeArray_map(f, LDDataset.get_citations(investigation, graph, context))
    def f_1(c: LDNode, investigation: Any=investigation, graph: Any=graph, context: Any=context) -> Person:
        return PersonConversion_decomposePerson_Z6839B9E8(c, graph, context)

    creators: Array[Person] = ResizeArray_map(f_1, LDDataset.get_creators(investigation, graph, context))
    datasets: Array[LDNode] = LDDataset.get_has_parts_as_dataset(investigation, graph, context)
    def f_3(d_3: LDNode, investigation: Any=investigation, graph: Any=graph, context: Any=context) -> ArcStudy:
        return StudyConversion_decomposeStudy_Z6839B9E8(d_3, graph, context)

    def f_2(d_2: LDNode, investigation: Any=investigation, graph: Any=graph, context: Any=context) -> bool:
        return LDDataset.validate_study(d_2, context)

    studies: Array[ArcStudy] = ResizeArray_map(f_3, ResizeArray_filter(f_2, datasets))
    def f_5(d_5: LDNode, investigation: Any=investigation, graph: Any=graph, context: Any=context) -> ArcAssay:
        return AssayConversion_decomposeAssay_Z6839B9E8(d_5, graph, context)

    def f_4(d_4: LDNode, investigation: Any=investigation, graph: Any=graph, context: Any=context) -> bool:
        return LDDataset.validate_assay(d_4, context)

    assays: Array[ArcAssay] = ResizeArray_map(f_5, ResizeArray_filter(f_4, datasets))
    def f_7(d_7: LDNode, investigation: Any=investigation, graph: Any=graph, context: Any=context) -> ArcWorkflow:
        return WorkflowConversion_decomposeWorkflow_Z6839B9E8(d_7, graph, context)

    def f_6(d_6: LDNode, investigation: Any=investigation, graph: Any=graph, context: Any=context) -> bool:
        return LDDataset.validate_arcworkflow(d_6, graph, context)

    workflows: Array[ArcWorkflow] = ResizeArray_map(f_7, ResizeArray_filter(f_6, datasets))
    def f_9(d_9: LDNode, investigation: Any=investigation, graph: Any=graph, context: Any=context) -> ArcRun:
        return RunConversion_decomposeRun_Z6839B9E8(d_9, graph, context)

    def f_8(d_8: LDNode, investigation: Any=investigation, graph: Any=graph, context: Any=context) -> bool:
        return LDDataset.validate_arcrun(d_8, context)

    runs: Array[ArcRun] = ResizeArray_map(f_9, ResizeArray_filter(f_8, datasets))
    def f_10(c_1: LDNode, investigation: Any=investigation, graph: Any=graph, context: Any=context) -> Comment:
        return BaseTypes_decomposeComment_Z2F770004(c_1, context)

    comments: Array[Comment] = ResizeArray_map(f_10, LDDataset.get_comments(investigation, graph, context))
    return ArcInvestigation.create(LDDataset.get_identifier_as_string(investigation, context), title, LDDataset.try_get_description_as_string(investigation, context), date_created, date_published, None, publications, creators, assays, studies, workflows, runs, None, comments)


__all__ = ["InvestigationConversion_reflection", "InvestigationConversion_composeInvestigation_5AEC717D", "InvestigationConversion_decomposeInvestigation_Z6839B9E8"]

