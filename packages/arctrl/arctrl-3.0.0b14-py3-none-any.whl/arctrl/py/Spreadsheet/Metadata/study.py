from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from ...fable_modules.fable_library.list import (FSharpList, of_array, map, empty, cons, reverse, append, of_seq)
from ...fable_modules.fable_library.map_util import add_to_dict
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.reflection import (TypeInfo, string_type, list_type, record_type)
from ...fable_modules.fable_library.seq import (collect, delay, append as append_1, singleton)
from ...fable_modules.fable_library.seq2 import List_distinct
from ...fable_modules.fable_library.string_ import starts_with_exact
from ...fable_modules.fable_library.types import (Record, Array)
from ...fable_modules.fable_library.util import (string_hash, IEnumerable_1, IEnumerator, to_enumerable)
from ...Core.arc_types import (ArcStudy, ArcAssay)
from ...Core.comment import (Comment, Comment_reflection, Remark)
from ...Core.conversion import (ARCtrl_ArcTable__ArcTable_GetProtocols, ARCtrl_ArcTable__ArcTable_GetProcesses)
from ...Core.Helper.collections_ import (ResizeArray_iter, Option_fromValueWithDefault)
from ...Core.Helper.identifier import (create_missing_identifier, Study_fileNameFromIdentifier)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.person import Person
from ...Core.Process.factor import Factor
from ...Core.Process.process_sequence import get_factors
from ...Core.Process.protocol import Protocol
from ...Core.publication import Publication
from ...Core.Table.arc_table import ArcTable
from .assays import (from_rows as from_rows_4, to_rows as to_rows_4)
from .comment import (Comment_fromString, Comment_toString)
from .contacts import (from_rows as from_rows_6, to_rows as to_rows_6)
from .design_descriptors import (from_rows as from_rows_1, to_rows as to_rows_1)
from .factors import (from_rows as from_rows_3, to_rows as to_rows_3)
from .protocols import (from_rows as from_rows_5, to_rows as to_rows_5)
from .publication import (from_rows as from_rows_2, to_rows as to_rows_2)
from .sparse_table import (SparseTable__TryGetValueDefault_5BAE6133, SparseTable, SparseTable_Create_Z2192E64B, SparseTable_FromRows_Z5579EC29, SparseTable_ToRows_759CAFC1, SparseRowModule_fromValues)

def _expr1314() -> TypeInfo:
    return record_type("ARCtrl.Spreadsheet.Studies.StudyInfo", [], StudyInfo, lambda: [("Identifier", string_type), ("Title", string_type), ("Description", string_type), ("SubmissionDate", string_type), ("PublicReleaseDate", string_type), ("FileName", string_type), ("Comments", list_type(Comment_reflection()))])


@dataclass(eq = False, repr = False, slots = True)
class StudyInfo(Record):
    Identifier: str
    Title: str
    Description: str
    SubmissionDate: str
    PublicReleaseDate: str
    FileName: str
    Comments: FSharpList[Comment]

StudyInfo_reflection = _expr1314

def StudyInfo_create(identifier: str, title: str, description: str, submission_date: str, public_release_date: str, file_name: str, comments: FSharpList[Comment]) -> StudyInfo:
    return StudyInfo(identifier, title, description, submission_date, public_release_date, file_name, comments)


def StudyInfo_get_Labels(__unit: None=None) -> FSharpList[str]:
    return of_array(["Study Identifier", "Study Title", "Study Description", "Study Submission Date", "Study Public Release Date", "Study File Name"])


def StudyInfo_FromSparseTable_3ECCA699(matrix: SparseTable) -> StudyInfo:
    def mapping(k: str, matrix: Any=matrix) -> Comment:
        return Comment_fromString(k, SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (k, 0)))

    comments: FSharpList[Comment] = map(mapping, matrix.CommentKeys)
    return StudyInfo_create(SparseTable__TryGetValueDefault_5BAE6133(matrix, create_missing_identifier(), ("Study Identifier", 0)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Study Title", 0)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Study Description", 0)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Study Submission Date", 0)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Study Public Release Date", 0)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Study File Name", 0)), comments)


def StudyInfo_ToSparseTable_1680536E(study: ArcStudy) -> SparseTable:
    matrix: SparseTable = SparseTable_Create_Z2192E64B(None, StudyInfo_get_Labels(), None, 2)
    comment_keys: FSharpList[str] = empty()
    pattern_input: tuple[str, str] = (("", "")) if starts_with_exact(study.Identifier, "MISSING_IDENTIFIER_") else ((study.Identifier, Study_fileNameFromIdentifier(study.Identifier)))
    add_to_dict(matrix.Matrix, ("Study Identifier", 1), pattern_input[0])
    add_to_dict(matrix.Matrix, ("Study Title", 1), default_arg(study.Title, ""))
    add_to_dict(matrix.Matrix, ("Study Description", 1), default_arg(study.Description, ""))
    add_to_dict(matrix.Matrix, ("Study Submission Date", 1), default_arg(study.SubmissionDate, ""))
    add_to_dict(matrix.Matrix, ("Study Public Release Date", 1), default_arg(study.PublicReleaseDate, ""))
    add_to_dict(matrix.Matrix, ("Study File Name", 1), pattern_input[1])
    def f(comment: Comment, study: Any=study) -> None:
        nonlocal comment_keys
        pattern_input_1: tuple[str, str] = Comment_toString(comment)
        n: str = pattern_input_1[0]
        comment_keys = cons(n, comment_keys)
        add_to_dict(matrix.Matrix, (n, 1), pattern_input_1[1])

    ResizeArray_iter(f, study.Comments)
    class ObjectExpr1320:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1319(x: str, y: str) -> bool:
                return x == y

            return _arrow1319

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    return SparseTable(matrix.Matrix, matrix.Keys, reverse(List_distinct(comment_keys, ObjectExpr1320())), matrix.ColumnCount)


def StudyInfo_fromRows(line_number: int, rows: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, int, FSharpList[Remark], StudyInfo]:
    tupled_arg: tuple[str | None, int, FSharpList[Remark], SparseTable] = SparseTable_FromRows_Z5579EC29(rows, StudyInfo_get_Labels(), line_number)
    return (tupled_arg[0], tupled_arg[1], tupled_arg[2], StudyInfo_FromSparseTable_3ECCA699(tupled_arg[3]))


def StudyInfo_toRows_1680536E(study: ArcStudy) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    return SparseTable_ToRows_759CAFC1(StudyInfo_ToSparseTable_1680536E(study))


def from_parts(study_info: StudyInfo, design_descriptors: FSharpList[OntologyAnnotation], publications: FSharpList[Publication], factors: FSharpList[Factor], assays: FSharpList[ArcAssay], protocols: FSharpList[Protocol], contacts: FSharpList[Person]) -> tuple[ArcStudy, FSharpList[ArcAssay]] | None:
    def mapping(assay: ArcAssay, study_info: Any=study_info, design_descriptors: Any=design_descriptors, publications: Any=publications, factors: Any=factors, assays: Any=assays, protocols: Any=protocols, contacts: Any=contacts) -> str:
        return assay.Identifier

    assay_identifiers: FSharpList[str] = map(mapping, assays)
    arcstudy: ArcStudy
    title: str | None = Option_fromValueWithDefault("", study_info.Title)
    description: str | None = Option_fromValueWithDefault("", study_info.Description)
    submission_date: str | None = Option_fromValueWithDefault("", study_info.SubmissionDate)
    public_release_date: str | None = Option_fromValueWithDefault("", study_info.PublicReleaseDate)
    publications_1: Array[Publication] = list(publications)
    contacts_1: Array[Person] = list(contacts)
    study_design_descriptors: Array[OntologyAnnotation] = list(design_descriptors)
    registered_assay_identifiers: Array[str] = list(assay_identifiers)
    comments: Array[Comment] = list(study_info.Comments)
    arcstudy = ArcStudy.make(study_info.Identifier, title, description, submission_date, public_release_date, publications_1, contacts_1, study_design_descriptors, [], None, registered_assay_identifiers, comments)
    if (arcstudy.Identifier == "") if arcstudy.is_empty else False:
        return None

    else: 
        return (arcstudy, assays)



def from_rows(line_number: int, en: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, int, FSharpList[Remark], tuple[ArcStudy, FSharpList[ArcAssay]] | None]:
    def loop(last_line_mut: str | None, study_info_mut: StudyInfo, design_descriptors_mut: FSharpList[OntologyAnnotation], publications_mut: FSharpList[Publication], factors_mut: FSharpList[Factor], assays_mut: FSharpList[ArcAssay], protocols_mut: FSharpList[Protocol], contacts_mut: FSharpList[Person], remarks_mut: FSharpList[Remark], line_number_1_mut: int, line_number: Any=line_number, en: Any=en) -> tuple[str | None, int, FSharpList[Remark], tuple[ArcStudy, FSharpList[ArcAssay]] | None]:
        while True:
            (last_line, study_info, design_descriptors, publications, factors, assays, protocols, contacts, remarks, line_number_1) = (last_line_mut, study_info_mut, design_descriptors_mut, publications_mut, factors_mut, assays_mut, protocols_mut, contacts_mut, remarks_mut, line_number_1_mut)
            (pattern_matching_result, k_12) = (None, None)
            if last_line is not None:
                if last_line == "STUDY DESIGN DESCRIPTORS":
                    pattern_matching_result = 0

                elif last_line == "STUDY PUBLICATIONS":
                    pattern_matching_result = 1

                elif last_line == "STUDY FACTORS":
                    pattern_matching_result = 2

                elif last_line == "STUDY ASSAYS":
                    pattern_matching_result = 3

                elif last_line == "STUDY PROTOCOLS":
                    pattern_matching_result = 4

                elif last_line == "STUDY CONTACTS":
                    pattern_matching_result = 5

                else: 
                    pattern_matching_result = 6
                    k_12 = last_line


            else: 
                pattern_matching_result = 6
                k_12 = last_line

            if pattern_matching_result == 0:
                pattern_input: tuple[str | None, int, FSharpList[Remark], FSharpList[OntologyAnnotation]] = from_rows_1("Study Design", line_number_1 + 1, en)
                last_line_mut = pattern_input[0]
                study_info_mut = study_info
                design_descriptors_mut = pattern_input[3]
                publications_mut = publications
                factors_mut = factors
                assays_mut = assays
                protocols_mut = protocols
                contacts_mut = contacts
                remarks_mut = append(remarks, pattern_input[2])
                line_number_1_mut = pattern_input[1]
                continue

            elif pattern_matching_result == 1:
                pattern_input_1: tuple[str | None, int, FSharpList[Remark], FSharpList[Publication]] = from_rows_2("Study Publication", line_number_1 + 1, en)
                last_line_mut = pattern_input_1[0]
                study_info_mut = study_info
                design_descriptors_mut = design_descriptors
                publications_mut = pattern_input_1[3]
                factors_mut = factors
                assays_mut = assays
                protocols_mut = protocols
                contacts_mut = contacts
                remarks_mut = append(remarks, pattern_input_1[2])
                line_number_1_mut = pattern_input_1[1]
                continue

            elif pattern_matching_result == 2:
                pattern_input_2: tuple[str | None, int, FSharpList[Remark], FSharpList[Factor]] = from_rows_3("Study Factor", line_number_1 + 1, en)
                last_line_mut = pattern_input_2[0]
                study_info_mut = study_info
                design_descriptors_mut = design_descriptors
                publications_mut = publications
                factors_mut = pattern_input_2[3]
                assays_mut = assays
                protocols_mut = protocols
                contacts_mut = contacts
                remarks_mut = append(remarks, pattern_input_2[2])
                line_number_1_mut = pattern_input_2[1]
                continue

            elif pattern_matching_result == 3:
                pattern_input_3: tuple[str | None, int, FSharpList[Remark], FSharpList[ArcAssay]] = from_rows_4("Study Assay", line_number_1 + 1, en)
                last_line_mut = pattern_input_3[0]
                study_info_mut = study_info
                design_descriptors_mut = design_descriptors
                publications_mut = publications
                factors_mut = factors
                assays_mut = pattern_input_3[3]
                protocols_mut = protocols
                contacts_mut = contacts
                remarks_mut = append(remarks, pattern_input_3[2])
                line_number_1_mut = pattern_input_3[1]
                continue

            elif pattern_matching_result == 4:
                pattern_input_4: tuple[str | None, int, FSharpList[Remark], FSharpList[Protocol]] = from_rows_5("Study Protocol", line_number_1 + 1, en)
                last_line_mut = pattern_input_4[0]
                study_info_mut = study_info
                design_descriptors_mut = design_descriptors
                publications_mut = publications
                factors_mut = factors
                assays_mut = assays
                protocols_mut = pattern_input_4[3]
                contacts_mut = contacts
                remarks_mut = append(remarks, pattern_input_4[2])
                line_number_1_mut = pattern_input_4[1]
                continue

            elif pattern_matching_result == 5:
                pattern_input_5: tuple[str | None, int, FSharpList[Remark], FSharpList[Person]] = from_rows_6("Study Person", line_number_1 + 1, en)
                last_line_mut = pattern_input_5[0]
                study_info_mut = study_info
                design_descriptors_mut = design_descriptors
                publications_mut = publications
                factors_mut = factors
                assays_mut = assays
                protocols_mut = protocols
                contacts_mut = pattern_input_5[3]
                remarks_mut = append(remarks, pattern_input_5[2])
                line_number_1_mut = pattern_input_5[1]
                continue

            elif pattern_matching_result == 6:
                return (k_12, line_number_1, remarks, from_parts(study_info, design_descriptors, publications, factors, assays, protocols, contacts))

            break

    pattern_input_6: tuple[str | None, int, FSharpList[Remark], StudyInfo] = StudyInfo_fromRows(line_number, en)
    return loop(pattern_input_6[0], pattern_input_6[3], empty(), empty(), empty(), empty(), empty(), empty(), pattern_input_6[2], pattern_input_6[1])


def to_rows(study: ArcStudy, assays: FSharpList[ArcAssay] | None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    def mapping(p: ArcTable, study: Any=study, assays: Any=assays) -> FSharpList[Protocol]:
        return ARCtrl_ArcTable__ArcTable_GetProtocols(p)

    protocols: FSharpList[Protocol] = of_seq(collect(mapping, study.Tables))
    def mapping_1(f: ArcTable, study: Any=study, assays: Any=assays) -> FSharpList[Factor]:
        return get_factors(ARCtrl_ArcTable__ArcTable_GetProcesses(f))

    factors: FSharpList[Factor] = of_seq(collect(mapping_1, study.Tables))
    assays_1: FSharpList[ArcAssay] = default_arg(assays, of_seq(study.GetRegisteredAssaysOrIdentifier()))
    def _arrow1342(__unit: None=None, study: Any=study, assays: Any=assays) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
        def _arrow1341(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
            def _arrow1340(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                def _arrow1339(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                    def _arrow1338(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                        def _arrow1337(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                            def _arrow1336(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                def _arrow1335(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                    def _arrow1334(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                        def _arrow1333(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                            def _arrow1332(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                                def _arrow1331(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                                    def _arrow1330(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                                        return to_rows_6("Study Person", of_seq(study.Contacts))

                                                    return append_1(singleton(SparseRowModule_fromValues(to_enumerable(["STUDY CONTACTS"]))), delay(_arrow1330))

                                                return append_1(to_rows_5("Study Protocol", protocols), delay(_arrow1331))

                                            return append_1(singleton(SparseRowModule_fromValues(to_enumerable(["STUDY PROTOCOLS"]))), delay(_arrow1332))

                                        return append_1(to_rows_4("Study Assay", assays_1), delay(_arrow1333))

                                    return append_1(singleton(SparseRowModule_fromValues(to_enumerable(["STUDY ASSAYS"]))), delay(_arrow1334))

                                return append_1(to_rows_3("Study Factor", factors), delay(_arrow1335))

                            return append_1(singleton(SparseRowModule_fromValues(to_enumerable(["STUDY FACTORS"]))), delay(_arrow1336))

                        return append_1(to_rows_2("Study Publication", of_seq(study.Publications)), delay(_arrow1337))

                    return append_1(singleton(SparseRowModule_fromValues(to_enumerable(["STUDY PUBLICATIONS"]))), delay(_arrow1338))

                return append_1(to_rows_1("Study Design", of_seq(study.StudyDesignDescriptors)), delay(_arrow1339))

            return append_1(singleton(SparseRowModule_fromValues(to_enumerable(["STUDY DESIGN DESCRIPTORS"]))), delay(_arrow1340))

        return append_1(StudyInfo_toRows_1680536E(study), delay(_arrow1341))

    return delay(_arrow1342)


__all__ = ["StudyInfo_reflection", "StudyInfo_create", "StudyInfo_get_Labels", "StudyInfo_FromSparseTable_3ECCA699", "StudyInfo_ToSparseTable_1680536E", "StudyInfo_fromRows", "StudyInfo_toRows_1680536E", "from_parts", "from_rows", "to_rows"]

