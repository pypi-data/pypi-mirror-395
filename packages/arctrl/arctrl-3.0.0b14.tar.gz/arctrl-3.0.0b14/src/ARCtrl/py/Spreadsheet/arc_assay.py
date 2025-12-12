from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (FSharpList, is_empty, empty, singleton as singleton_1, of_seq)
from ..fable_modules.fable_library.option import (default_arg, to_array)
from ..fable_modules.fable_library.seq import (exists, head, try_head, delay, append, singleton, iterate_indexed, map, try_find, choose, try_pick, is_empty as is_empty_1, iterate)
from ..fable_modules.fable_library.string_ import (starts_with_exact, to_fail, printf, to_console)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (IEnumerable_1, get_enumerator, IEnumerator, to_enumerable)
from ..fable_modules.fs_spreadsheet.fs_row import FsRow
from ..fable_modules.fs_spreadsheet.fs_workbook import FsWorkbook
from ..fable_modules.fs_spreadsheet.fs_worksheet import FsWorksheet
from ..Core.arc_types import ArcAssay
from ..Core.comment import Remark
from ..Core.datamap import Datamap
from ..Core.Helper.identifier import create_missing_identifier
from ..Core.person import Person
from ..Core.Table.arc_table import ArcTable
from .AnnotationTable.arc_table import (try_from_fs_worksheet, to_fs_worksheet as to_fs_worksheet_1)
from .DatamapTable.datamap_table import (try_from_fs_worksheet as try_from_fs_worksheet_1, to_fs_worksheet)
from .Metadata.assays import (from_rows, to_rows)
from .Metadata.contacts import (from_rows as from_rows_1, to_rows as to_rows_1)
from .Metadata.sparse_table import (SparseRowModule_tryGetValueAt, SparseRowModule_fromValues, SparseRowModule_writeToSheet, SparseRowModule_fromFsRow, SparseRowModule_getAllValues, SparseRowModule_fromAllValues)

def ArcAssay_fromRows(rows: IEnumerable_1[IEnumerable_1[tuple[int, str]]]) -> ArcAssay:
    def predicate(row: IEnumerable_1[tuple[int, str]], rows: Any=rows) -> bool:
        return starts_with_exact(head(row)[1], "Assay")

    pattern_input: tuple[str | None, str | None] = (("Assay", "Assay Person")) if exists(predicate, rows) else ((None, None))
    en: IEnumerator[IEnumerable_1[tuple[int, str]]] = get_enumerator(rows)
    def loop(last_row_mut: str | None, assays_mut: FSharpList[ArcAssay], contacts_mut: FSharpList[Person], row_number_mut: int, rows: Any=rows) -> ArcAssay:
        while True:
            (last_row, assays, contacts, row_number) = (last_row_mut, assays_mut, contacts_mut, row_number_mut)
            (pattern_matching_result,) = (None,)
            if last_row is not None:
                def _arrow1587(__unit: None=None, last_row: Any=last_row, assays: Any=assays, contacts: Any=contacts, row_number: Any=row_number) -> bool:
                    prefix: str = last_row
                    return True if (prefix == "ASSAY") else (prefix == "ASSAY METADATA")

                if _arrow1587():
                    pattern_matching_result = 0

                elif last_row == "ASSAY PERFORMERS":
                    pattern_matching_result = 1

                else: 
                    pattern_matching_result = 2


            else: 
                pattern_matching_result = 2

            if pattern_matching_result == 0:
                pattern_input_1: tuple[str | None, int, FSharpList[Remark], FSharpList[ArcAssay]] = from_rows(pattern_input[0], row_number + 1, en)
                last_row_mut = pattern_input_1[0]
                assays_mut = pattern_input_1[3]
                contacts_mut = contacts
                row_number_mut = pattern_input_1[1]
                continue

            elif pattern_matching_result == 1:
                pattern_input_2: tuple[str | None, int, FSharpList[Remark], FSharpList[Person]] = from_rows_1(pattern_input[1], row_number + 1, en)
                last_row_mut = pattern_input_2[0]
                assays_mut = assays
                contacts_mut = pattern_input_2[3]
                row_number_mut = pattern_input_2[1]
                continue

            elif pattern_matching_result == 2:
                (pattern_matching_result_1, assays_2, contacts_2) = (None, None, None)
                if is_empty(assays):
                    if is_empty(contacts):
                        pattern_matching_result_1 = 0

                    else: 
                        pattern_matching_result_1 = 1
                        assays_2 = assays
                        contacts_2 = contacts


                else: 
                    pattern_matching_result_1 = 1
                    assays_2 = assays
                    contacts_2 = contacts

                if pattern_matching_result_1 == 0:
                    return ArcAssay.create(create_missing_identifier())

                elif pattern_matching_result_1 == 1:
                    performers: Array[Person] = list(contacts_2)
                    assay: ArcAssay = default_arg(try_head(assays_2), ArcAssay.create(create_missing_identifier()))
                    return ArcAssay.set_performers(performers, assay)


            break

    if en.System_Collections_IEnumerator_MoveNext():
        return loop(SparseRowModule_tryGetValueAt(0, en.System_Collections_Generic_IEnumerator_1_get_Current()), empty(), empty(), 1)

    else: 
        raise Exception("empty assay metadata sheet")



def ArcAssay_toRows(assay: ArcAssay) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    def _arrow1591(__unit: None=None, assay: Any=assay) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
        def _arrow1590(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
            def _arrow1589(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                def _arrow1588(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                    return to_rows_1("Assay Person", of_seq(assay.Performers))

                return append(singleton(SparseRowModule_fromValues(to_enumerable(["ASSAY PERFORMERS"]))), delay(_arrow1588))

            return append(to_rows("Assay", singleton_1(assay)), delay(_arrow1589))

        return append(singleton(SparseRowModule_fromValues(to_enumerable(["ASSAY"]))), delay(_arrow1590))

    return delay(_arrow1591)


def ArcAssay_toMetadataSheet(assay: ArcAssay) -> FsWorksheet:
    sheet: FsWorksheet = FsWorksheet("isa_assay")
    def action(row_i: int, r: IEnumerable_1[tuple[int, str]], assay: Any=assay) -> None:
        SparseRowModule_writeToSheet(row_i + 1, r, sheet)

    iterate_indexed(action, ArcAssay_toRows(assay))
    return sheet


def ArcAssay_fromMetadataSheet(sheet: FsWorksheet) -> ArcAssay:
    try: 
        rows: IEnumerable_1[IEnumerable_1[tuple[int, str]]] = map(SparseRowModule_fromFsRow, sheet.Rows)
        def predicate(row: IEnumerable_1[tuple[int, str]]) -> bool:
            return starts_with_exact(head(row)[1], "Assay")

        has_prefix: bool = exists(predicate, rows)
        return ArcAssay_fromRows(rows)

    except Exception as err:
        arg: str = str(err)
        return to_fail(printf("Failed while parsing metadatasheet: %s"))(arg)



def ArcAssay_toMetadataCollection(assay: ArcAssay) -> IEnumerable_1[IEnumerable_1[str | None]]:
    def mapping(row: IEnumerable_1[tuple[int, str]], assay: Any=assay) -> IEnumerable_1[str | None]:
        return SparseRowModule_getAllValues(row)

    return map(mapping, ArcAssay_toRows(assay))


def ArcAssay_fromMetadataCollection(collection: IEnumerable_1[IEnumerable_1[str | None]]) -> ArcAssay:
    try: 
        return ArcAssay_fromRows(map(SparseRowModule_fromAllValues, collection))

    except Exception as err:
        arg: str = str(err)
        return to_fail(printf("Failed while parsing metadatasheet: %s"))(arg)



def ArcAssay_isMetadataSheetName(name: str) -> bool:
    if name == "isa_assay":
        return True

    else: 
        return name == "Assay"



def ArcAssay_isMetadataSheet(sheet: FsWorksheet) -> bool:
    return ArcAssay_isMetadataSheetName(sheet.Name)


def ArcAssay_tryGetMetadataSheet(doc: FsWorkbook) -> FsWorksheet | None:
    def predicate(sheet: FsWorksheet, doc: Any=doc) -> bool:
        return ArcAssay_isMetadataSheet(sheet)

    return try_find(predicate, doc.GetWorksheets())


def ARCtrl_ArcAssay__ArcAssay_fromFsWorkbook_Static_32154C9D(doc: FsWorkbook) -> ArcAssay:
    try: 
        assay_metadata: ArcAssay
        match_value: FsWorksheet | None = ArcAssay_tryGetMetadataSheet(doc)
        if match_value is None:
            to_console(printf("Cannot retrieve metadata: Assay file does not contain \"%s\" or \"%s\" sheet."))("isa_assay")("Assay")
            assay_metadata = ArcAssay.create(create_missing_identifier())

        else: 
            assay_metadata = ArcAssay_fromMetadataSheet(match_value)

        sheets: Array[FsWorksheet] = doc.GetWorksheets()
        annotation_tables: IEnumerable_1[ArcTable] = choose(try_from_fs_worksheet, sheets)
        datamap_sheet: Datamap | None = try_pick(try_from_fs_worksheet_1, sheets)
        if not is_empty_1(annotation_tables):
            assay_metadata.Tables = list(annotation_tables)

        assay_metadata.Datamap = datamap_sheet
        return assay_metadata

    except Exception as err:
        arg_2: str = str(err)
        return to_fail(printf("Could not parse assay: \n%s"))(arg_2)



def ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F(assay: ArcAssay, datamap_sheet: bool | None=None) -> FsWorkbook:
    datamap_sheet_1: bool = default_arg(datamap_sheet, True)
    doc: FsWorkbook = FsWorkbook()
    metadata_sheet: FsWorksheet = ArcAssay_toMetadataSheet(assay)
    doc.AddWorksheet(metadata_sheet)
    if datamap_sheet_1:
        def action(arg: Datamap, assay: Any=assay, datamap_sheet: Any=datamap_sheet) -> None:
            sheet: FsWorksheet = to_fs_worksheet(arg)
            doc.AddWorksheet(sheet)

        iterate(action, to_array(assay.Datamap))

    def action_1(i: int, arg_1: ArcTable, assay: Any=assay, datamap_sheet: Any=datamap_sheet) -> None:
        sheet_1: FsWorksheet = to_fs_worksheet_1(i, arg_1)
        doc.AddWorksheet(sheet_1)

    iterate_indexed(action_1, assay.Tables)
    return doc


def ARCtrl_ArcAssay__ArcAssay_ToFsWorkbook_6FCE9E49(this: ArcAssay, datamap_sheet: bool | None=None) -> FsWorkbook:
    return ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F(this, datamap_sheet)


__all__ = ["ArcAssay_fromRows", "ArcAssay_toRows", "ArcAssay_toMetadataSheet", "ArcAssay_fromMetadataSheet", "ArcAssay_toMetadataCollection", "ArcAssay_fromMetadataCollection", "ArcAssay_isMetadataSheetName", "ArcAssay_isMetadataSheet", "ArcAssay_tryGetMetadataSheet", "ARCtrl_ArcAssay__ArcAssay_fromFsWorkbook_Static_32154C9D", "ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F", "ARCtrl_ArcAssay__ArcAssay_ToFsWorkbook_6FCE9E49"]

