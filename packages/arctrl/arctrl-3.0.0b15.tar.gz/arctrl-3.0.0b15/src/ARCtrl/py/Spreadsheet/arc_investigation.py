from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from ..fable_modules.fable_library.list import (FSharpList, of_array, map, empty, cons, reverse, append, unzip, concat, of_seq, is_empty as is_empty_1, tail, head)
from ..fable_modules.fable_library.map import (of_list, try_find)
from ..fable_modules.fable_library.map_util import add_to_dict
from ..fable_modules.fable_library.option import (default_arg, value as value_1)
from ..fable_modules.fable_library.reflection import (TypeInfo, string_type, list_type, record_type)
from ..fable_modules.fable_library.seq import (is_empty, delay, append as append_1, singleton, collect, to_list, map as map_1, try_find as try_find_1, iterate_indexed)
from ..fable_modules.fable_library.seq2 import (List_distinct, List_distinctBy)
from ..fable_modules.fable_library.string_ import (to_fail, printf)
from ..fable_modules.fable_library.types import (Record, Array)
from ..fable_modules.fable_library.util import (string_hash, IEnumerable_1, IEnumerator, get_enumerator, ignore, to_enumerable, compare_primitives)
from ..fable_modules.fs_spreadsheet.fs_row import FsRow
from ..fable_modules.fs_spreadsheet.fs_workbook import FsWorkbook
from ..fable_modules.fs_spreadsheet.fs_worksheet import FsWorksheet
from ..Core.arc_types import (ArcInvestigation, ArcStudy, ArcAssay)
from ..Core.comment import (Comment, Comment_reflection, Remark)
from ..Core.Helper.collections_ import (ResizeArray_iter, Option_fromValueWithDefault)
from ..Core.ontology_source_reference import OntologySourceReference
from ..Core.person import Person
from ..Core.publication import Publication
from .Metadata.comment import (Comment_fromString, Comment_toString, Remark_wrapRemark)
from .Metadata.contacts import (from_rows as from_rows_2, to_rows as to_rows_2)
from .Metadata.ontology_source_reference import (from_rows, to_rows)
from .Metadata.publication import (from_rows as from_rows_1, to_rows as to_rows_1)
from .Metadata.sparse_table import (SparseTable__TryGetValueDefault_5BAE6133, SparseTable, SparseTable_Create_Z2192E64B, SparseTable_FromRows_Z5579EC29, SparseTable_ToRows_759CAFC1, SparseRowModule_tryGetValueAt, SparseRowModule_fromValues, SparseRowModule_getAllValues, SparseRowModule_fromAllValues, SparseRowModule_fromFsRow, SparseRowModule_writeToSheet)
from .Metadata.study import (from_rows as from_rows_3, to_rows as to_rows_3)

def _expr1602() -> TypeInfo:
    return record_type("ARCtrl.Spreadsheet.ArcInvestigation.InvestigationInfo", [], ArcInvestigation_InvestigationInfo, lambda: [("Identifier", string_type), ("Title", string_type), ("Description", string_type), ("SubmissionDate", string_type), ("PublicReleaseDate", string_type), ("Comments", list_type(Comment_reflection()))])


@dataclass(eq = False, repr = False, slots = True)
class ArcInvestigation_InvestigationInfo(Record):
    Identifier: str
    Title: str
    Description: str
    SubmissionDate: str
    PublicReleaseDate: str
    Comments: FSharpList[Comment]

ArcInvestigation_InvestigationInfo_reflection = _expr1602

def ArcInvestigation_InvestigationInfo_create(identifier: str, title: str, description: str, submission_date: str, public_release_date: str, comments: FSharpList[Comment]) -> ArcInvestigation_InvestigationInfo:
    return ArcInvestigation_InvestigationInfo(identifier, title, description, submission_date, public_release_date, comments)


def ArcInvestigation_InvestigationInfo_get_Labels(__unit: None=None) -> FSharpList[str]:
    return of_array(["Investigation Identifier", "Investigation Title", "Investigation Description", "Investigation Submission Date", "Investigation Public Release Date"])


def ArcInvestigation_InvestigationInfo_FromSparseTable_3ECCA699(matrix: SparseTable) -> ArcInvestigation_InvestigationInfo:
    def mapping(k: str, matrix: Any=matrix) -> Comment:
        return Comment_fromString(k, SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (k, 0)))

    comments: FSharpList[Comment] = map(mapping, matrix.CommentKeys)
    return ArcInvestigation_InvestigationInfo_create(SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Investigation Identifier", 0)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Investigation Title", 0)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Investigation Description", 0)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Investigation Submission Date", 0)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Investigation Public Release Date", 0)), comments)


def ArcInvestigation_InvestigationInfo_ToSparseTable_Z720BD3FF(investigation: ArcInvestigation) -> SparseTable:
    matrix: SparseTable = SparseTable_Create_Z2192E64B(None, ArcInvestigation_InvestigationInfo_get_Labels(), None, 2)
    comment_keys: FSharpList[str] = empty()
    add_to_dict(matrix.Matrix, ("Investigation Identifier", 1), investigation.Identifier)
    add_to_dict(matrix.Matrix, ("Investigation Title", 1), default_arg(investigation.Title, ""))
    add_to_dict(matrix.Matrix, ("Investigation Description", 1), default_arg(investigation.Description, ""))
    add_to_dict(matrix.Matrix, ("Investigation Submission Date", 1), default_arg(investigation.SubmissionDate, ""))
    add_to_dict(matrix.Matrix, ("Investigation Public Release Date", 1), default_arg(investigation.PublicReleaseDate, ""))
    def f(comment: Comment, investigation: Any=investigation) -> None:
        nonlocal comment_keys
        pattern_input: tuple[str, str] = Comment_toString(comment)
        n: str = pattern_input[0]
        comment_keys = cons(n, comment_keys)
        add_to_dict(matrix.Matrix, (n, 1), pattern_input[1])

    ResizeArray_iter(f, investigation.Comments)
    class ObjectExpr1604:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1603(x: str, y: str) -> bool:
                return x == y

            return _arrow1603

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    return SparseTable(matrix.Matrix, matrix.Keys, reverse(List_distinct(comment_keys, ObjectExpr1604())), matrix.ColumnCount)


def ArcInvestigation_InvestigationInfo_fromRows(line_number: int, rows: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, int, FSharpList[Remark], ArcInvestigation_InvestigationInfo]:
    tupled_arg: tuple[str | None, int, FSharpList[Remark], SparseTable] = SparseTable_FromRows_Z5579EC29(rows, ArcInvestigation_InvestigationInfo_get_Labels(), line_number)
    return (tupled_arg[0], tupled_arg[1], tupled_arg[2], ArcInvestigation_InvestigationInfo_FromSparseTable_3ECCA699(tupled_arg[3]))


def ArcInvestigation_InvestigationInfo_toRows_Z720BD3FF(investigation: ArcInvestigation) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    return SparseTable_ToRows_759CAFC1(ArcInvestigation_InvestigationInfo_ToSparseTable_Z720BD3FF(investigation))


def ArcInvestigation_fromParts(investigation_info: ArcInvestigation_InvestigationInfo, ontology_source_reference: FSharpList[OntologySourceReference], publications: FSharpList[Publication], contacts: FSharpList[Person], studies: FSharpList[ArcStudy], assays: FSharpList[ArcAssay], remarks: FSharpList[Remark]) -> ArcInvestigation:
    def mapping(s: ArcStudy, investigation_info: Any=investigation_info, ontology_source_reference: Any=ontology_source_reference, publications: Any=publications, contacts: Any=contacts, studies: Any=studies, assays: Any=assays, remarks: Any=remarks) -> str:
        return s.Identifier

    study_identifiers: FSharpList[str] = map(mapping, studies)
    title: str | None = Option_fromValueWithDefault("", investigation_info.Title)
    description: str | None = Option_fromValueWithDefault("", investigation_info.Description)
    submission_date: str | None = Option_fromValueWithDefault("", investigation_info.SubmissionDate)
    public_release_date: str | None = Option_fromValueWithDefault("", investigation_info.PublicReleaseDate)
    ontology_source_references: Array[OntologySourceReference] = list(ontology_source_reference)
    publications_1: Array[Publication] = list(publications)
    contacts_1: Array[Person] = list(contacts)
    assays_1: Array[ArcAssay] = list(assays)
    studies_1: Array[ArcStudy] = list(studies)
    registered_study_identifiers: Array[str] = list(study_identifiers)
    comments: Array[Comment] = list(investigation_info.Comments)
    remarks_1: Array[Remark] = list(remarks)
    return ArcInvestigation.make(investigation_info.Identifier, title, description, submission_date, public_release_date, ontology_source_references, publications_1, contacts_1, assays_1, studies_1, [], [], registered_study_identifiers, comments, remarks_1)


def ArcInvestigation_fromRows(rows: IEnumerable_1[IEnumerable_1[tuple[int, str]]]) -> ArcInvestigation:
    if is_empty(rows):
        raise Exception("isa_investigation sheet in Investigation file is empty")

    en: IEnumerator[IEnumerable_1[tuple[int, str]]] = get_enumerator(rows)
    empty_investigation_info: ArcInvestigation_InvestigationInfo = ArcInvestigation_InvestigationInfo_create("", "", "", "", "", empty())
    def loop(last_line_mut: str | None, ontology_source_references_mut: FSharpList[OntologySourceReference], investigation_info_mut: ArcInvestigation_InvestigationInfo, publications_mut: FSharpList[Publication], contacts_mut: FSharpList[Person], studies_mut: FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]], remarks_mut: FSharpList[Remark], line_number_mut: int, rows: Any=rows) -> ArcInvestigation:
        while True:
            (last_line, ontology_source_references, investigation_info, publications, contacts, studies, remarks, line_number) = (last_line_mut, ontology_source_references_mut, investigation_info_mut, publications_mut, contacts_mut, studies_mut, remarks_mut, line_number_mut)
            (pattern_matching_result,) = (None,)
            if last_line is not None:
                if last_line == "ONTOLOGY SOURCE REFERENCE":
                    pattern_matching_result = 0

                elif last_line == "INVESTIGATION":
                    pattern_matching_result = 1

                elif last_line == "INVESTIGATION PUBLICATIONS":
                    pattern_matching_result = 2

                elif last_line == "INVESTIGATION CONTACTS":
                    pattern_matching_result = 3

                elif last_line == "STUDY":
                    pattern_matching_result = 4

                else: 
                    pattern_matching_result = 5


            else: 
                pattern_matching_result = 5

            if pattern_matching_result == 0:
                pattern_input: tuple[str | None, int, FSharpList[Remark], FSharpList[OntologySourceReference]] = from_rows(line_number + 1, en)
                last_line_mut = pattern_input[0]
                ontology_source_references_mut = pattern_input[3]
                investigation_info_mut = investigation_info
                publications_mut = publications
                contacts_mut = contacts
                studies_mut = studies
                remarks_mut = append(remarks, pattern_input[2])
                line_number_mut = pattern_input[1]
                continue

            elif pattern_matching_result == 1:
                pattern_input_1: tuple[str | None, int, FSharpList[Remark], ArcInvestigation_InvestigationInfo] = ArcInvestigation_InvestigationInfo_fromRows(line_number + 1, en)
                last_line_mut = pattern_input_1[0]
                ontology_source_references_mut = ontology_source_references
                investigation_info_mut = pattern_input_1[3]
                publications_mut = publications
                contacts_mut = contacts
                studies_mut = studies
                remarks_mut = append(remarks, pattern_input_1[2])
                line_number_mut = pattern_input_1[1]
                continue

            elif pattern_matching_result == 2:
                pattern_input_2: tuple[str | None, int, FSharpList[Remark], FSharpList[Publication]] = from_rows_1("Investigation Publication", line_number + 1, en)
                last_line_mut = pattern_input_2[0]
                ontology_source_references_mut = ontology_source_references
                investigation_info_mut = investigation_info
                publications_mut = pattern_input_2[3]
                contacts_mut = contacts
                studies_mut = studies
                remarks_mut = append(remarks, pattern_input_2[2])
                line_number_mut = pattern_input_2[1]
                continue

            elif pattern_matching_result == 3:
                pattern_input_3: tuple[str | None, int, FSharpList[Remark], FSharpList[Person]] = from_rows_2("Investigation Person", line_number + 1, en)
                last_line_mut = pattern_input_3[0]
                ontology_source_references_mut = ontology_source_references
                investigation_info_mut = investigation_info
                publications_mut = publications
                contacts_mut = pattern_input_3[3]
                studies_mut = studies
                remarks_mut = append(remarks, pattern_input_3[2])
                line_number_mut = pattern_input_3[1]
                continue

            elif pattern_matching_result == 4:
                pattern_input_4: tuple[str | None, int, FSharpList[Remark], tuple[ArcStudy, FSharpList[ArcAssay]] | None] = from_rows_3(line_number + 1, en)
                study: tuple[ArcStudy, FSharpList[ArcAssay]] | None = pattern_input_4[3]
                new_remarks_4: FSharpList[Remark] = pattern_input_4[2]
                line_number_6: int = pattern_input_4[1] or 0
                current_line_4: str | None = pattern_input_4[0]
                if study is not None:
                    last_line_mut = current_line_4
                    ontology_source_references_mut = ontology_source_references
                    investigation_info_mut = investigation_info
                    publications_mut = publications
                    contacts_mut = contacts
                    studies_mut = cons(value_1(study), studies)
                    remarks_mut = append(remarks, new_remarks_4)
                    line_number_mut = line_number_6
                    continue

                else: 
                    last_line_mut = current_line_4
                    ontology_source_references_mut = ontology_source_references
                    investigation_info_mut = investigation_info
                    publications_mut = publications
                    contacts_mut = contacts
                    studies_mut = studies
                    remarks_mut = append(remarks, new_remarks_4)
                    line_number_mut = line_number_6
                    continue


            elif pattern_matching_result == 5:
                if en.System_Collections_IEnumerator_MoveNext():
                    last_line_mut = SparseRowModule_tryGetValueAt(0, en.System_Collections_Generic_IEnumerator_1_get_Current())
                    ontology_source_references_mut = ontology_source_references
                    investigation_info_mut = investigation_info
                    publications_mut = publications
                    contacts_mut = contacts
                    studies_mut = studies
                    remarks_mut = remarks
                    line_number_mut = line_number
                    continue

                else: 
                    pattern_input_5: tuple[FSharpList[ArcStudy], FSharpList[ArcAssay]]
                    tupled_arg: tuple[FSharpList[ArcStudy], FSharpList[FSharpList[ArcAssay]]] = unzip(studies)
                    def projection(a_1: ArcAssay, last_line: Any=last_line, ontology_source_references: Any=ontology_source_references, investigation_info: Any=investigation_info, publications: Any=publications, contacts: Any=contacts, studies: Any=studies, remarks: Any=remarks, line_number: Any=line_number) -> str:
                        return a_1.Identifier

                    class ObjectExpr1606:
                        @property
                        def Equals(self) -> Callable[[str, str], bool]:
                            def _arrow1605(x: str, y: str) -> bool:
                                return x == y

                            return _arrow1605

                        @property
                        def GetHashCode(self) -> Callable[[str], int]:
                            return string_hash

                    pattern_input_5 = (reverse(tupled_arg[0]), List_distinctBy(projection, concat(tupled_arg[1]), ObjectExpr1606()))
                    return ArcInvestigation_fromParts(investigation_info, ontology_source_references, publications, contacts, pattern_input_5[0], pattern_input_5[1], remarks)


            break

    arc_investigation: ArcInvestigation
    ignore(en.System_Collections_IEnumerator_MoveNext())
    arc_investigation = loop(SparseRowModule_tryGetValueAt(0, en.System_Collections_Generic_IEnumerator_1_get_Current()), empty(), empty_investigation_info, empty(), empty(), empty(), empty(), 1)
    if arc_investigation.Identifier == "":
        raise Exception("Mandatory Investigation identifier is not present")

    return arc_investigation


def ArcInvestigation_toRows(investigation: ArcInvestigation) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    def _arrow1619(__unit: None=None, investigation: Any=investigation) -> FSharpList[IEnumerable_1[tuple[int, str]]]:
        remarks: FSharpList[Remark] = of_seq(investigation.Remarks)
        def _arrow1617(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
            def _arrow1616(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                def _arrow1615(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                    def _arrow1614(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                        def _arrow1613(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                            def _arrow1612(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                def _arrow1611(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                    def _arrow1610(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                        def _arrow1609(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                            def _arrow1608(study_identifier: str) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                                study: ArcStudy = default_arg(investigation.TryGetStudy(study_identifier), ArcStudy(study_identifier))
                                                def _arrow1607(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                                    return to_rows_3(study, None)

                                                return append_1(singleton(SparseRowModule_fromValues(to_enumerable(["STUDY"]))), delay(_arrow1607))

                                            return collect(_arrow1608, investigation.RegisteredStudyIdentifiers)

                                        return append_1(to_rows_2("Investigation Person", of_seq(investigation.Contacts)), delay(_arrow1609))

                                    return append_1(singleton(SparseRowModule_fromValues(to_enumerable(["INVESTIGATION CONTACTS"]))), delay(_arrow1610))

                                return append_1(to_rows_1("Investigation Publication", of_seq(investigation.Publications)), delay(_arrow1611))

                            return append_1(singleton(SparseRowModule_fromValues(to_enumerable(["INVESTIGATION PUBLICATIONS"]))), delay(_arrow1612))

                        return append_1(ArcInvestigation_InvestigationInfo_toRows_Z720BD3FF(investigation), delay(_arrow1613))

                    return append_1(singleton(SparseRowModule_fromValues(to_enumerable(["INVESTIGATION"]))), delay(_arrow1614))

                return append_1(to_rows(of_seq(investigation.OntologySourceReferences)), delay(_arrow1615))

            return append_1(singleton(SparseRowModule_fromValues(to_enumerable(["ONTOLOGY SOURCE REFERENCE"]))), delay(_arrow1616))

        rows: IEnumerable_1[IEnumerable_1[tuple[int, str]]] = delay(_arrow1617)
        try: 
            def mapping(remark: Remark) -> tuple[int, str]:
                return Remark.to_tuple(remark)

            class ObjectExpr1618:
                @property
                def Compare(self) -> Callable[[int, int], int]:
                    return compare_primitives

            rm: Any = of_list(map(mapping, remarks), ObjectExpr1618())
            def loop(i_mut: int, l_mut: FSharpList[IEnumerable_1[tuple[int, str]]], nl_mut: FSharpList[IEnumerable_1[tuple[int, str]]]) -> FSharpList[IEnumerable_1[tuple[int, str]]]:
                while True:
                    (i, l, nl) = (i_mut, l_mut, nl_mut)
                    match_value: str | None = try_find(i, rm)
                    if match_value is None:
                        if not is_empty_1(l):
                            i_mut = i + 1
                            l_mut = tail(l)
                            nl_mut = cons(head(l), nl)
                            continue

                        else: 
                            return nl


                    else: 
                        remark_1: str = match_value
                        i_mut = i + 1
                        l_mut = l
                        nl_mut = cons(SparseRowModule_fromValues(to_enumerable([Remark_wrapRemark(remark_1)])), nl)
                        continue

                    break

            return reverse(loop(1, of_seq(rows), empty()))

        except Exception as match_value_1:
            return to_list(rows)


    return _arrow1619()


def ArcInvestigation_toMetadataCollection(investigation: ArcInvestigation) -> IEnumerable_1[IEnumerable_1[str | None]]:
    def mapping(row: IEnumerable_1[tuple[int, str]], investigation: Any=investigation) -> IEnumerable_1[str | None]:
        return SparseRowModule_getAllValues(row)

    return map_1(mapping, ArcInvestigation_toRows(investigation))


def ArcInvestigation_fromMetadataCollection(collection: IEnumerable_1[IEnumerable_1[str | None]]) -> ArcInvestigation:
    def mapping(v: IEnumerable_1[str | None], collection: Any=collection) -> IEnumerable_1[tuple[int, str]]:
        return SparseRowModule_fromAllValues(v)

    return ArcInvestigation_fromRows(map_1(mapping, collection))


def ArcInvestigation_isMetadataSheetName(name: str) -> bool:
    if name == "isa_investigation":
        return True

    else: 
        return name == "Investigation"



def ArcInvestigation_isMetadataSheet(sheet: FsWorksheet) -> bool:
    return ArcInvestigation_isMetadataSheetName(sheet.Name)


def ArcInvestigation_tryGetMetadataSheet(doc: FsWorkbook) -> FsWorksheet | None:
    def predicate(sheet: FsWorksheet, doc: Any=doc) -> bool:
        return ArcInvestigation_isMetadataSheet(sheet)

    return try_find_1(predicate, doc.GetWorksheets())


def ARCtrl_ArcInvestigation__ArcInvestigation_fromFsWorkbook_Static_32154C9D(doc: FsWorkbook) -> ArcInvestigation:
    try: 
        def _arrow1620(__unit: None=None) -> Array[FsRow]:
            sheet_1: FsWorksheet
            match_value: FsWorksheet | None = ArcInvestigation_tryGetMetadataSheet(doc)
            if match_value is None:
                raise Exception("Could not find metadata sheet with sheetname \"isa_investigation\" or deprecated sheetname \"Investigation\"")

            else: 
                sheet_1 = match_value

            return FsWorksheet.get_rows(sheet_1)

        return ArcInvestigation_fromRows(map_1(SparseRowModule_fromFsRow, _arrow1620()))

    except Exception as err:
        arg: str = str(err)
        return to_fail(printf("Could not read investigation from spreadsheet: %s"))(arg)



def ARCtrl_ArcInvestigation__ArcInvestigation_toFsWorkbook_Static_Z720BD3FF(investigation: ArcInvestigation) -> FsWorkbook:
    try: 
        wb: FsWorkbook = FsWorkbook()
        sheet: FsWorksheet = FsWorksheet("isa_investigation")
        def action(row_i: int, r: IEnumerable_1[tuple[int, str]]) -> None:
            SparseRowModule_writeToSheet(row_i + 1, r, sheet)

        iterate_indexed(action, ArcInvestigation_toRows(investigation))
        wb.AddWorksheet(sheet)
        return wb

    except Exception as err:
        arg: str = str(err)
        return to_fail(printf("Could not write investigation to spreadsheet: %s"))(arg)



def ARCtrl_ArcInvestigation__ArcInvestigation_ToFsWorkbook(this: ArcInvestigation) -> FsWorkbook:
    return ARCtrl_ArcInvestigation__ArcInvestigation_toFsWorkbook_Static_Z720BD3FF(this)


__all__ = ["ArcInvestigation_InvestigationInfo_reflection", "ArcInvestigation_InvestigationInfo_create", "ArcInvestigation_InvestigationInfo_get_Labels", "ArcInvestigation_InvestigationInfo_FromSparseTable_3ECCA699", "ArcInvestigation_InvestigationInfo_ToSparseTable_Z720BD3FF", "ArcInvestigation_InvestigationInfo_fromRows", "ArcInvestigation_InvestigationInfo_toRows_Z720BD3FF", "ArcInvestigation_fromParts", "ArcInvestigation_fromRows", "ArcInvestigation_toRows", "ArcInvestigation_toMetadataCollection", "ArcInvestigation_fromMetadataCollection", "ArcInvestigation_isMetadataSheetName", "ArcInvestigation_isMetadataSheet", "ArcInvestigation_tryGetMetadataSheet", "ARCtrl_ArcInvestigation__ArcInvestigation_fromFsWorkbook_Static_32154C9D", "ARCtrl_ArcInvestigation__ArcInvestigation_toFsWorkbook_Static_Z720BD3FF", "ARCtrl_ArcInvestigation__ArcInvestigation_ToFsWorkbook"]

