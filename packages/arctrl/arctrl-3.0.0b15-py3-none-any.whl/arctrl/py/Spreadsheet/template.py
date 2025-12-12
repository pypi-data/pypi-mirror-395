from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from ..fable_modules.fable_library.date import now
from ..fable_modules.fable_library.guid import parse
from ..fable_modules.fable_library.list import (of_array, FSharpList, empty, map, reverse, append as append_1, of_seq)
from ..fable_modules.fable_library.map_util import add_to_dict
from ..fable_modules.fable_library.option import to_array
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type, string_type, list_type, record_type)
from ..fable_modules.fable_library.seq import (map as map_1, exists, head, append, singleton, delay, to_list, try_find, iterate_indexed, try_pick)
from ..fable_modules.fable_library.seq2 import List_distinct
from ..fable_modules.fable_library.string_ import (starts_with_exact, to_console, printf)
from ..fable_modules.fable_library.types import (FSharpException, Record, to_string, Array)
from ..fable_modules.fable_library.util import (IEnumerable_1, IEnumerator, string_hash, to_enumerable, get_enumerator, ignore)
from ..fable_modules.fs_spreadsheet.fs_row import FsRow
from ..fable_modules.fs_spreadsheet.fs_workbook import FsWorkbook
from ..fable_modules.fs_spreadsheet.fs_worksheet import FsWorksheet
from ..fable_modules.fs_spreadsheet.Tables.fs_table import FsTable
from ..Core.comment import (Remark, Comment, Comment_reflection)
from ..Core.conversion import Person_orcidKey
from ..Core.Helper.identifier import create_missing_identifier
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from ..Core.Table.arc_table import ArcTable
from ..Core.template import (Template, Organisation)
from .AnnotationTable.arc_table import (try_from_fs_worksheet, to_fs_worksheet)
from .Metadata.comment import Comment_fromString
from .Metadata.contacts import (from_rows as from_rows_1, to_rows as to_rows_1)
from .Metadata.ontology_annotation import (from_sparse_table, to_sparse_table, from_rows, to_rows)
from .Metadata.sparse_table import (SparseTable, SparseTable__TryGetValueDefault_5BAE6133, SparseTable_Create_Z2192E64B, SparseTable_FromRows_Z5579EC29, SparseTable_ToRows_759CAFC1, SparseRowModule_tryGetValueAt, SparseRowModule_fromValues, SparseRowModule_writeToSheet, SparseRowModule_fromFsRow, SparseRowModule_getAllValues, SparseRowModule_fromAllValues)

def _expr1621() -> TypeInfo:
    return class_type("ARCtrl.Spreadsheet.TemplateReadError", None, TemplateReadError, class_type("System.Exception"))


class TemplateReadError(FSharpException):
    def __init__(self, Data0: str) -> None:
        super().__init__()
        self.Data0 = Data0


TemplateReadError_reflection = _expr1621

Metadata_ER_labels: FSharpList[str] = of_array(["ER", "ER Term Accession Number", "ER Term Source REF"])

def Metadata_ER_fromSparseTable(matrix: SparseTable) -> FSharpList[OntologyAnnotation]:
    return from_sparse_table("ER", "ER Term Source REF", "ER Term Accession Number", matrix)


def Metadata_ER_toSparseTable(designs: FSharpList[OntologyAnnotation]) -> SparseTable:
    return to_sparse_table("ER", "ER Term Source REF", "ER Term Accession Number", designs)


def Metadata_ER_fromRows(prefix: str | None, rows: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, FSharpList[OntologyAnnotation]]:
    pattern_input: tuple[str | None, int, FSharpList[Remark], FSharpList[OntologyAnnotation]] = from_rows(prefix, "ER", "ER Term Source REF", "ER Term Accession Number", 0, rows)
    return (pattern_input[0], pattern_input[3])


def Metadata_ER_toRows(prefix: str | None, designs: FSharpList[OntologyAnnotation]) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    return to_rows(prefix, "ER", "ER Term Source REF", "ER Term Accession Number", designs)


Metadata_Tags_labels: FSharpList[str] = of_array(["Tags", "Tags Term Accession Number", "Tags Term Source REF"])

def Metadata_Tags_fromSparseTable(matrix: SparseTable) -> FSharpList[OntologyAnnotation]:
    return from_sparse_table("Tags", "Tags Term Source REF", "Tags Term Accession Number", matrix)


def Metadata_Tags_toSparseTable(designs: FSharpList[OntologyAnnotation]) -> SparseTable:
    return to_sparse_table("Tags", "Tags Term Source REF", "Tags Term Accession Number", designs)


def Metadata_Tags_fromRows(prefix: str | None, rows: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, FSharpList[OntologyAnnotation]]:
    pattern_input: tuple[str | None, int, FSharpList[Remark], FSharpList[OntologyAnnotation]] = from_rows(prefix, "Tags", "Tags Term Source REF", "Tags Term Accession Number", 0, rows)
    return (pattern_input[0], pattern_input[3])


def Metadata_Tags_toRows(prefix: str | None, designs: FSharpList[OntologyAnnotation]) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    return to_rows(prefix, "Tags", "Tags Term Source REF", "Tags Term Accession Number", designs)


def _expr1622() -> TypeInfo:
    return record_type("ARCtrl.Spreadsheet.Metadata.Template.TemplateInfo", [], Metadata_Template_TemplateInfo, lambda: [("Id", string_type), ("Name", string_type), ("Version", string_type), ("Description", string_type), ("Organisation", string_type), ("Table", string_type), ("Comments", list_type(Comment_reflection()))])


@dataclass(eq = False, repr = False, slots = True)
class Metadata_Template_TemplateInfo(Record):
    Id: str
    Name: str
    Version: str
    Description: str
    Organisation: str
    Table: str
    Comments: FSharpList[Comment]

Metadata_Template_TemplateInfo_reflection = _expr1622

def Metadata_Template_TemplateInfo_create(id: str, name: str, version: str, description: str, organisation: str, table: str, comments: FSharpList[Comment]) -> Metadata_Template_TemplateInfo:
    return Metadata_Template_TemplateInfo(id, name, version, description, organisation, table, comments)


def Metadata_Template_TemplateInfo_get_empty(__unit: None=None) -> Metadata_Template_TemplateInfo:
    return Metadata_Template_TemplateInfo_create("", "", "", "", "", "", empty())


def Metadata_Template_TemplateInfo_get_Labels(__unit: None=None) -> FSharpList[str]:
    return of_array(["Id", "Name", "Version", "Description", "Organisation", "Table"])


def Metadata_Template_TemplateInfo_FromSparseTable_3ECCA699(matrix: SparseTable) -> Metadata_Template_TemplateInfo:
    def mapping(k: str, matrix: Any=matrix) -> Comment:
        return Comment_fromString(k, SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (k, 0)))

    comments: FSharpList[Comment] = map(mapping, matrix.CommentKeys)
    return Metadata_Template_TemplateInfo_create(SparseTable__TryGetValueDefault_5BAE6133(matrix, create_missing_identifier(), ("Id", 0)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Name", 0)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Version", 0)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Description", 0)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Organisation", 0)), SparseTable__TryGetValueDefault_5BAE6133(matrix, "", ("Table", 0)), comments)


def Metadata_Template_TemplateInfo_ToSparseTable_48C39BE1(template: Template) -> SparseTable:
    matrix: SparseTable = SparseTable_Create_Z2192E64B(None, Metadata_Template_TemplateInfo_get_Labels(), None, 2)
    comment_keys: FSharpList[str] = empty()
    def _arrow1623(__unit: None=None, template: Any=template) -> str:
        copy_of_struct: str = template.Id
        return str(copy_of_struct)

    def _arrow1624(__unit: None=None, template: Any=template) -> str:
        copy_of_struct_1: str = template.Id
        return str(copy_of_struct_1)

    add_to_dict(matrix.Matrix, ("Id", 1), "" if starts_with_exact(_arrow1623(), "MISSING_IDENTIFIER_") else _arrow1624())
    add_to_dict(matrix.Matrix, ("Name", 1), template.Name)
    add_to_dict(matrix.Matrix, ("Version", 1), template.Version)
    add_to_dict(matrix.Matrix, ("Description", 1), template.Description)
    add_to_dict(matrix.Matrix, ("Organisation", 1), to_string(template.Organisation))
    add_to_dict(matrix.Matrix, ("Table", 1), template.Table.Name)
    class ObjectExpr1626:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1625(x: str, y: str) -> bool:
                return x == y

            return _arrow1625

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    return SparseTable(matrix.Matrix, matrix.Keys, reverse(List_distinct(comment_keys, ObjectExpr1626())), matrix.ColumnCount)


def Metadata_Template_TemplateInfo_fromRows_9F97F2A(rows: IEnumerator[IEnumerable_1[tuple[int, str]]]) -> tuple[str | None, Metadata_Template_TemplateInfo]:
    tupled_arg: tuple[str | None, int, FSharpList[Remark], SparseTable] = SparseTable_FromRows_Z5579EC29(rows, Metadata_Template_TemplateInfo_get_Labels(), 0)
    return (tupled_arg[0], Metadata_Template_TemplateInfo_FromSparseTable_3ECCA699(tupled_arg[3]))


def Metadata_Template_TemplateInfo_toRows_48C39BE1(template: Template) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    return SparseTable_ToRows_759CAFC1(Metadata_Template_TemplateInfo_ToSparseTable_48C39BE1(template))


def Metadata_Template_mapDeprecatedKeys(rows: IEnumerable_1[IEnumerable_1[tuple[int, str]]]) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    def mapping_1(r: IEnumerable_1[tuple[int, str]], rows: Any=rows) -> IEnumerable_1[tuple[int, str]]:
        def mapping(tupled_arg: tuple[int, str], r: Any=r) -> tuple[int, str]:
            k: int = tupled_arg[0] or 0
            v: str = tupled_arg[1]
            if k == 0:
                if v == "#AUTHORS list":
                    return (k, "AUTHORS")

                elif v == "#ER list":
                    return (k, "ERS")

                elif v == "#TAGS list":
                    return (k, "TAGS")

                elif v == "Authors ORCID":
                    return (k, ("Comment[" + Person_orcidKey) + "]")

                elif v == "Authors Last Name":
                    return (k, "Author Last Name")

                elif v == "Authors First Name":
                    return (k, "Author First Name")

                elif v == "Authors Mid Initials":
                    return (k, "Author Mid Initials")

                elif v == "Authors Email":
                    return (k, "Author Email")

                elif v == "Authors Phone":
                    return (k, "Author Phone")

                elif v == "Authors Fax":
                    return (k, "Author Fax")

                elif v == "Authors Address":
                    return (k, "Author Address")

                elif v == "Authors Affiliation":
                    return (k, "Author Affiliation")

                elif v == "Authors Role":
                    return (k, "Author Roles")

                elif v == "Authors Role Term Accession Number":
                    return (k, "Author Roles Term Accession Number")

                elif v == "Authors Role Term Source REF":
                    return (k, "Author Roles Term Source REF")

                else: 
                    return (k, v)


            else: 
                return (k, v)


        return map_1(mapping, r)

    s: IEnumerable_1[IEnumerable_1[tuple[int, str]]] = map_1(mapping_1, rows)
    def predicate(v_32: str, rows: Any=rows) -> bool:
        return v_32 == "TEMPLATE"

    if exists(predicate, to_array(SparseRowModule_tryGetValueAt(0, head(s)))):
        return s

    else: 
        return append(singleton(SparseRowModule_fromValues(to_enumerable(["TEMPLATE"]))), s)



def Metadata_Template_fromRows(rows: IEnumerable_1[IEnumerable_1[tuple[int, str]]]) -> tuple[Metadata_Template_TemplateInfo, FSharpList[OntologyAnnotation], FSharpList[OntologyAnnotation], FSharpList[Person]]:
    def loop(en_mut: IEnumerator[IEnumerable_1[tuple[int, str]]], last_line_mut: str | None, template_info_mut: Metadata_Template_TemplateInfo, ers_mut: FSharpList[OntologyAnnotation], tags_mut: FSharpList[OntologyAnnotation], authors_mut: FSharpList[Person], rows: Any=rows) -> tuple[Metadata_Template_TemplateInfo, FSharpList[OntologyAnnotation], FSharpList[OntologyAnnotation], FSharpList[Person]]:
        while True:
            (en, last_line, template_info, ers, tags, authors) = (en_mut, last_line_mut, template_info_mut, ers_mut, tags_mut, authors_mut)
            (pattern_matching_result,) = (None,)
            if last_line is not None:
                if last_line == "ERS":
                    pattern_matching_result = 0

                elif last_line == "TAGS":
                    pattern_matching_result = 1

                elif last_line == "AUTHORS":
                    pattern_matching_result = 2

                else: 
                    pattern_matching_result = 3


            else: 
                pattern_matching_result = 3

            if pattern_matching_result == 0:
                pattern_input: tuple[str | None, FSharpList[OntologyAnnotation]] = Metadata_ER_fromRows(None, en)
                en_mut = en
                last_line_mut = pattern_input[0]
                template_info_mut = template_info
                ers_mut = append_1(ers, pattern_input[1])
                tags_mut = tags
                authors_mut = authors
                continue

            elif pattern_matching_result == 1:
                pattern_input_1: tuple[str | None, FSharpList[OntologyAnnotation]] = Metadata_Tags_fromRows(None, en)
                en_mut = en
                last_line_mut = pattern_input_1[0]
                template_info_mut = template_info
                ers_mut = ers
                tags_mut = append_1(tags, pattern_input_1[1])
                authors_mut = authors
                continue

            elif pattern_matching_result == 2:
                pattern_input_2: tuple[str | None, int, FSharpList[Remark], FSharpList[Person]] = from_rows_1("Author", 0, en)
                en_mut = en
                last_line_mut = pattern_input_2[0]
                template_info_mut = template_info
                ers_mut = ers
                tags_mut = tags
                authors_mut = append_1(authors, pattern_input_2[3])
                continue

            elif pattern_matching_result == 3:
                return (template_info, ers, tags, authors)

            break

    en_1: IEnumerator[IEnumerable_1[tuple[int, str]]] = get_enumerator(Metadata_Template_mapDeprecatedKeys(rows))
    ignore(en_1.System_Collections_IEnumerator_MoveNext())
    pattern_input_3: tuple[str | None, Metadata_Template_TemplateInfo] = Metadata_Template_TemplateInfo_fromRows_9F97F2A(en_1)
    return loop(en_1, pattern_input_3[0], pattern_input_3[1], empty(), empty(), empty())


def Metadata_Template_toRows(template: Template) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    def _arrow1634(__unit: None=None, template: Any=template) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
        def _arrow1633(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
            def _arrow1632(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                def _arrow1631(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                    def _arrow1630(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                        def _arrow1629(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                            def _arrow1628(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                def _arrow1627(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                                    return to_rows_1("Author", of_seq(template.Authors))

                                return append(singleton(SparseRowModule_fromValues(to_enumerable(["AUTHORS"]))), delay(_arrow1627))

                            return append(Metadata_Tags_toRows(None, to_list(template.Tags)), delay(_arrow1628))

                        return append(singleton(SparseRowModule_fromValues(to_enumerable(["TAGS"]))), delay(_arrow1629))

                    return append(Metadata_ER_toRows(None, to_list(template.EndpointRepositories)), delay(_arrow1630))

                return append(singleton(SparseRowModule_fromValues(to_enumerable(["ERS"]))), delay(_arrow1631))

            return append(Metadata_Template_TemplateInfo_toRows_48C39BE1(template), delay(_arrow1632))

        return append(singleton(SparseRowModule_fromValues(to_enumerable(["TEMPLATE"]))), delay(_arrow1633))

    return delay(_arrow1634)


Template_metadataSheetName: str = "isa_template"

Template_obsoleteMetadataSheetName: str = "SwateTemplateMetadata"

def Template_fromParts(template_info: Metadata_Template_TemplateInfo, ers: FSharpList[OntologyAnnotation], tags: FSharpList[OntologyAnnotation], authors: FSharpList[Person], table: ArcTable, last_updated: Any) -> Template:
    id: str = parse(template_info.Id)
    organisation: Organisation = Organisation.of_string(template_info.Organisation)
    authors_1: Array[Person] = list(authors)
    repos: Array[OntologyAnnotation] = list(ers)
    tags_1: Array[OntologyAnnotation] = list(tags)
    return Template.make(id, table, template_info.Name, template_info.Description, organisation, template_info.Version, authors_1, repos, tags_1, last_updated)


def Template_isMetadataSheetName(name: str) -> bool:
    if name == Template_metadataSheetName:
        return True

    else: 
        return name == Template_obsoleteMetadataSheetName



def Template_isMetadataSheet(sheet: FsWorksheet) -> bool:
    return Template_isMetadataSheetName(sheet.Name)


def Template_tryGetMetadataSheet(doc: FsWorkbook) -> FsWorksheet | None:
    def predicate(sheet: FsWorksheet, doc: Any=doc) -> bool:
        return Template_isMetadataSheet(sheet)

    return try_find(predicate, doc.GetWorksheets())


def Template_toMetadataSheet(template: Template) -> FsWorksheet:
    sheet: FsWorksheet = FsWorksheet(Template_metadataSheetName)
    def action(row_i: int, r: IEnumerable_1[tuple[int, str]], template: Any=template) -> None:
        SparseRowModule_writeToSheet(row_i + 1, r, sheet)

    iterate_indexed(action, Metadata_Template_toRows(template))
    return sheet


def Template_fromMetadataSheet(sheet: FsWorksheet) -> tuple[Metadata_Template_TemplateInfo, FSharpList[OntologyAnnotation], FSharpList[OntologyAnnotation], FSharpList[Person]]:
    def mapping(r: FsRow, sheet: Any=sheet) -> IEnumerable_1[tuple[int, str]]:
        return SparseRowModule_fromFsRow(r)

    return Metadata_Template_fromRows(map_1(mapping, sheet.Rows))


def Template_toMetadataCollection(template: Template) -> IEnumerable_1[IEnumerable_1[str | None]]:
    def mapping(row: IEnumerable_1[tuple[int, str]], template: Any=template) -> IEnumerable_1[str | None]:
        return SparseRowModule_getAllValues(row)

    return map_1(mapping, Metadata_Template_toRows(template))


def Template_fromMetadataCollection(collection: IEnumerable_1[IEnumerable_1[str | None]]) -> tuple[Metadata_Template_TemplateInfo, FSharpList[OntologyAnnotation], FSharpList[OntologyAnnotation], FSharpList[Person]]:
    def mapping(v: IEnumerable_1[str | None], collection: Any=collection) -> IEnumerable_1[tuple[int, str]]:
        return SparseRowModule_fromAllValues(v)

    return Metadata_Template_fromRows(map_1(mapping, collection))


def Template_fromFsWorkbook(doc: FsWorkbook) -> Template:
    pattern_input: tuple[Metadata_Template_TemplateInfo, FSharpList[OntologyAnnotation], FSharpList[OntologyAnnotation], FSharpList[Person]]
    match_value: FsWorksheet | None = Template_tryGetMetadataSheet(doc)
    if match_value is None:
        to_console(printf("Could not find metadata sheet with sheetname \"isa_template\" or deprecated sheetname \"Template\""))
        pattern_input = (Metadata_Template_TemplateInfo_get_empty(), empty(), empty(), empty())

    else: 
        pattern_input = Template_fromMetadataSheet(match_value)

    template_info: Metadata_Template_TemplateInfo = pattern_input[0]
    sheets: Array[FsWorksheet] = doc.GetWorksheets()
    def _arrow1635(__unit: None=None, doc: Any=doc) -> ArcTable:
        def try_table_name_matches(ws: FsWorksheet) -> FsWorksheet | None:
            def predicate(t: FsTable, ws: Any=ws) -> bool:
                return t.Name == template_info.Table

            if exists(predicate, ws.Tables):
                return ws

            else: 
                return None


        match_value_1: FsWorksheet | None = try_pick(try_table_name_matches, sheets)
        if match_value_1 is None:
            def try_wsname_matches(ws_1: FsWorksheet) -> FsWorksheet | None:
                if ws_1.Name == template_info.Table:
                    return ws_1

                else: 
                    return None


            match_value_3: FsWorksheet | None = try_pick(try_wsname_matches, sheets)
            if match_value_3 is None:
                raise TemplateReadError(("No worksheet or table with name `" + template_info.Table) + "` found")

            else: 
                ws_3: FsWorksheet = match_value_3
                match_value_4: ArcTable | None = try_from_fs_worksheet(ws_3)
                if match_value_4 is None:
                    raise TemplateReadError(("Ws with name `" + ws_3.Name) + "` could not be converted to a table")

                else: 
                    return match_value_4



        else: 
            ws_2: FsWorksheet = match_value_1
            match_value_2: ArcTable | None = try_from_fs_worksheet(ws_2)
            if match_value_2 is None:
                raise TemplateReadError(("Ws with name `" + ws_2.Name) + "` could not be converted to a table")

            else: 
                return match_value_2



    return Template_fromParts(template_info, pattern_input[1], pattern_input[2], pattern_input[3], _arrow1635(), now())


def Template_toFsWorkbook(template: Template) -> FsWorkbook:
    doc: FsWorkbook = FsWorkbook()
    meta_data_sheet: FsWorksheet = Template_toMetadataSheet(template)
    doc.AddWorksheet(meta_data_sheet)
    sheet: FsWorksheet = to_fs_worksheet(None, template.Table)
    doc.AddWorksheet(sheet)
    return doc


__all__ = ["TemplateReadError_reflection", "Metadata_ER_labels", "Metadata_ER_fromSparseTable", "Metadata_ER_toSparseTable", "Metadata_ER_fromRows", "Metadata_ER_toRows", "Metadata_Tags_labels", "Metadata_Tags_fromSparseTable", "Metadata_Tags_toSparseTable", "Metadata_Tags_fromRows", "Metadata_Tags_toRows", "Metadata_Template_TemplateInfo_reflection", "Metadata_Template_TemplateInfo_create", "Metadata_Template_TemplateInfo_get_empty", "Metadata_Template_TemplateInfo_get_Labels", "Metadata_Template_TemplateInfo_FromSparseTable_3ECCA699", "Metadata_Template_TemplateInfo_ToSparseTable_48C39BE1", "Metadata_Template_TemplateInfo_fromRows_9F97F2A", "Metadata_Template_TemplateInfo_toRows_48C39BE1", "Metadata_Template_mapDeprecatedKeys", "Metadata_Template_fromRows", "Metadata_Template_toRows", "Template_metadataSheetName", "Template_obsoleteMetadataSheetName", "Template_fromParts", "Template_isMetadataSheetName", "Template_isMetadataSheet", "Template_tryGetMetadataSheet", "Template_toMetadataSheet", "Template_fromMetadataSheet", "Template_toMetadataCollection", "Template_fromMetadataCollection", "Template_fromFsWorkbook", "Template_toFsWorkbook"]

