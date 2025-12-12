from __future__ import annotations
from typing import Any
from ..Core.arc_types import ArcStudy
from ..Core.comment import Comment
from ..Core.datamap import Datamap
from ..Core.Helper.collections_ import (Option_fromSeq, ResizeArray_map, Option_fromValueWithDefault)
from ..Core.person import Person
from ..Core.publication import Publication
from ..Core.Table.arc_tables import ArcTables
from ..FileSystem.file_system import FileSystem
from ..ROCrate.ldcontext import LDContext
from ..ROCrate.ldobject import (LDNode, LDGraph)
from ..ROCrate.LDTypes.dataset import LDDataset
from ..fable_modules.fable_library.date import now
from ..fable_modules.fable_library.list import of_seq
from ..fable_modules.fable_library.option import (bind, map)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.types import Array
from .assay import AssayConversion_getDataFilesFromProcesses_6BABD1B0
from .basic import (BaseTypes_composeComment_Z13201A7E, BaseTypes_decomposeComment_Z2F770004)
from .datamap import (DatamapConversion_composeFragmentDescriptors_Z892BFC3, DatamapConversion_decomposeFragmentDescriptors_Z6E59645F)
from .date_time import (try_from_string, to_string)
from .person import (PersonConversion_composePerson_Z64D846DC, PersonConversion_decomposePerson_Z6839B9E8)
from .scholarly_article import (ScholarlyArticleConversion_composeScholarlyArticle_D324A6D, ScholarlyArticleConversion_decomposeScholarlyArticle_Z6839B9E8)
from .table import (ARCtrl_ArcTables__ArcTables_GetProcesses_5E660E5C, ARCtrl_ArcTables__ArcTables_fromProcesses_Static_Z27F0B586)

def _expr3973() -> TypeInfo:
    return class_type("ARCtrl.Conversion.StudyConversion", None, StudyConversion)


class StudyConversion:
    ...

StudyConversion_reflection = _expr3973

def StudyConversion_composeStudy_ZFE0E38E(study: ArcStudy, fs: FileSystem | None=None) -> LDNode:
    def _arrow3974(s: str, study: Any=study, fs: Any=fs) -> Any | None:
        return try_from_string(s)

    date_created: Any | None = bind(_arrow3974, study.SubmissionDate)
    def _arrow3975(s_1: str, study: Any=study, fs: Any=fs) -> Any | None:
        return try_from_string(s_1)

    date_published: Any | None = bind(_arrow3975, study.PublicReleaseDate)
    date_modified: Any = now()
    def f(p: Publication, study: Any=study, fs: Any=fs) -> LDNode:
        return ScholarlyArticleConversion_composeScholarlyArticle_D324A6D(p)

    publications: Array[LDNode] | None = Option_fromSeq(ResizeArray_map(f, study.Publications))
    def f_1(c: Person, study: Any=study, fs: Any=fs) -> LDNode:
        return PersonConversion_composePerson_Z64D846DC(c)

    creators: Array[LDNode] | None = Option_fromSeq(ResizeArray_map(f_1, study.Contacts))
    process_sequence: Array[LDNode] | None = Option_fromSeq(list(ARCtrl_ArcTables__ArcTables_GetProcesses_5E660E5C(ArcTables(study.Tables), None, study.Identifier, fs)))
    def mapping(datamap: Datamap, study: Any=study, fs: Any=fs) -> Array[LDNode]:
        return DatamapConversion_composeFragmentDescriptors_Z892BFC3(datamap)

    fragment_descriptors: Array[LDNode] | None = map(mapping, study.Datamap)
    def mapping_1(ps: Array[LDNode], study: Any=study, fs: Any=fs) -> Array[LDNode]:
        return AssayConversion_getDataFilesFromProcesses_6BABD1B0(ps, fragment_descriptors)

    data_files: Array[LDNode] | None = map(mapping_1, process_sequence)
    def f_2(c_1: Comment, study: Any=study, fs: Any=fs) -> LDNode:
        return BaseTypes_composeComment_Z13201A7E(c_1)

    comments: Array[LDNode] | None = Option_fromSeq(ResizeArray_map(f_2, study.Comments))
    return LDDataset.create_study(study.Identifier, None, creators, date_created, date_published, date_modified, study.Description, data_files, study.Title, publications, fragment_descriptors, comments, None, process_sequence)


def StudyConversion_decomposeStudy_Z6839B9E8(study: LDNode, graph: LDGraph | None=None, context: LDContext | None=None) -> ArcStudy:
    def _arrow3976(d: Any, study: Any=study, graph: Any=graph, context: Any=context) -> str:
        return to_string(d)

    date_created: str | None = map(_arrow3976, LDDataset.try_get_date_created_as_date_time(study, context))
    def _arrow3977(d_1: Any, study: Any=study, graph: Any=graph, context: Any=context) -> str:
        return to_string(d_1)

    date_published: str | None = map(_arrow3977, LDDataset.try_get_date_published_as_date_time(study, context))
    def f(p: LDNode, study: Any=study, graph: Any=graph, context: Any=context) -> Publication:
        return ScholarlyArticleConversion_decomposeScholarlyArticle_Z6839B9E8(p, graph, context)

    publications: Array[Publication] = ResizeArray_map(f, LDDataset.get_citations(study, graph, context))
    def f_1(c: LDNode, study: Any=study, graph: Any=graph, context: Any=context) -> Person:
        return PersonConversion_decomposePerson_Z6839B9E8(c, graph, context)

    creators: Array[Person] = ResizeArray_map(f_1, LDDataset.get_creators(study, graph, context))
    datamap: Datamap | None
    v: Datamap = DatamapConversion_decomposeFragmentDescriptors_Z6E59645F(LDDataset.get_variable_measured_as_fragment_descriptors(study, graph, context), graph, context)
    datamap = Option_fromValueWithDefault(Datamap.init(), v)
    tables: ArcTables = ARCtrl_ArcTables__ArcTables_fromProcesses_Static_Z27F0B586(of_seq(LDDataset.get_abouts_as_lab_process(study, graph, context)), graph, context)
    def f_2(c_1: LDNode, study: Any=study, graph: Any=graph, context: Any=context) -> Comment:
        return BaseTypes_decomposeComment_Z2F770004(c_1, context)

    comments: Array[Comment] = ResizeArray_map(f_2, LDDataset.get_comments(study, graph, context))
    return ArcStudy.create(LDDataset.get_identifier_as_string(study, context), LDDataset.try_get_name_as_string(study, context), LDDataset.try_get_description_as_string(study, context), date_created, date_published, publications, creators, None, tables.Tables, datamap, None, comments)


__all__ = ["StudyConversion_reflection", "StudyConversion_composeStudy_ZFE0E38E", "StudyConversion_decomposeStudy_Z6839B9E8"]

