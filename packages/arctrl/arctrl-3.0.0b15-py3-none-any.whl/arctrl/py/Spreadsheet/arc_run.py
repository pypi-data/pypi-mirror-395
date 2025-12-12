from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (FSharpList, empty, of_seq)
from ..fable_modules.fable_library.seq import (delay, append, singleton, iterate_indexed, map, try_find, choose, try_pick, is_empty)
from ..fable_modules.fable_library.string_ import (to_fail, printf, to_console)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (get_enumerator, IEnumerable_1, IEnumerator, to_enumerable)
from ..fable_modules.fs_spreadsheet.fs_row import FsRow
from ..fable_modules.fs_spreadsheet.fs_workbook import FsWorkbook
from ..fable_modules.fs_spreadsheet.fs_worksheet import FsWorksheet
from ..Core.arc_types import ArcRun
from ..Core.comment import Remark
from ..Core.datamap import Datamap
from ..Core.Helper.identifier import create_missing_identifier
from ..Core.person import Person
from ..Core.Table.arc_table import ArcTable
from .AnnotationTable.arc_table import (try_from_fs_worksheet, to_fs_worksheet)
from .DatamapTable.datamap_table import try_from_fs_worksheet as try_from_fs_worksheet_1
from .Metadata.contacts import (from_rows as from_rows_1, to_rows as to_rows_1)
from .Metadata.run import (from_rows, to_rows)
from .Metadata.sparse_table import (SparseRowModule_tryGetValueAt, SparseRowModule_fromValues, SparseRowModule_writeToSheet, SparseRowModule_fromFsRow, SparseRowModule_getAllValues, SparseRowModule_fromAllValues)

def ArcRun_fromRows(rows: IEnumerable_1[IEnumerable_1[tuple[int, str]]]) -> ArcRun:
    en: IEnumerator[IEnumerable_1[tuple[int, str]]] = get_enumerator(rows)
    def loop(last_row_mut: str | None, run_mut: ArcRun | None, performers_mut: FSharpList[Person], row_number_mut: int, rows: Any=rows) -> ArcRun:
        while True:
            (last_row, run, performers, row_number) = (last_row_mut, run_mut, performers_mut, row_number_mut)
            (pattern_matching_result,) = (None,)
            if last_row is not None:
                if last_row == "RUN":
                    pattern_matching_result = 0

                elif last_row == "RUN PERFORMERS":
                    pattern_matching_result = 1

                else: 
                    pattern_matching_result = 2


            else: 
                pattern_matching_result = 2

            if pattern_matching_result == 0:
                pattern_input: tuple[str | None, int, FSharpList[Remark], ArcRun] = from_rows(row_number + 1, en)
                last_row_mut = pattern_input[0]
                run_mut = pattern_input[3]
                performers_mut = performers
                row_number_mut = pattern_input[1]
                continue

            elif pattern_matching_result == 1:
                pattern_input_1: tuple[str | None, int, FSharpList[Remark], FSharpList[Person]] = from_rows_1("Run Person", row_number + 1, en)
                last_row_mut = pattern_input_1[0]
                run_mut = run
                performers_mut = pattern_input_1[3]
                row_number_mut = pattern_input_1[1]
                continue

            elif pattern_matching_result == 2:
                if run is not None:
                    run_2: ArcRun = run
                    run_2.Performers = list(performers)
                    return run_2

                else: 
                    return ArcRun.create(create_missing_identifier(), None, None, None, None, None, None, None, None, list(performers))


            break

    if en.System_Collections_IEnumerator_MoveNext():
        return loop(SparseRowModule_tryGetValueAt(0, en.System_Collections_Generic_IEnumerator_1_get_Current()), None, empty(), 1)

    else: 
        raise Exception("empty run metadata sheet")



def ArcRun_toRows(run: ArcRun) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    def _arrow1601(__unit: None=None, run: Any=run) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
        def _arrow1600(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
            def _arrow1599(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                def _arrow1598(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                    return to_rows_1("Run Person", of_seq(run.Performers))

                return append(singleton(SparseRowModule_fromValues(to_enumerable(["RUN PERFORMERS"]))), delay(_arrow1598))

            return append(to_rows(run), delay(_arrow1599))

        return append(singleton(SparseRowModule_fromValues(to_enumerable(["RUN"]))), delay(_arrow1600))

    return delay(_arrow1601)


def ArcRun_toMetadataSheet(run: ArcRun) -> FsWorksheet:
    sheet: FsWorksheet = FsWorksheet("isa_run")
    def action(row_i: int, r: IEnumerable_1[tuple[int, str]], run: Any=run) -> None:
        SparseRowModule_writeToSheet(row_i + 1, r, sheet)

    iterate_indexed(action, ArcRun_toRows(run))
    return sheet


def ArcRun_fromMetadataSheet(sheet: FsWorksheet) -> ArcRun:
    try: 
        return ArcRun_fromRows(map(SparseRowModule_fromFsRow, sheet.Rows))

    except Exception as err:
        arg: str = str(err)
        return to_fail(printf("Failed while parsing metadatasheet: %s"))(arg)



def ArcRun_toMetadataCollection(run: ArcRun) -> IEnumerable_1[IEnumerable_1[str | None]]:
    def mapping(row: IEnumerable_1[tuple[int, str]], run: Any=run) -> IEnumerable_1[str | None]:
        return SparseRowModule_getAllValues(row)

    return map(mapping, ArcRun_toRows(run))


def ArcRun_fromMetadataCollection(collection: IEnumerable_1[IEnumerable_1[str | None]]) -> ArcRun:
    try: 
        return ArcRun_fromRows(map(SparseRowModule_fromAllValues, collection))

    except Exception as err:
        arg: str = str(err)
        return to_fail(printf("Failed while parsing metadatasheet: %s"))(arg)



def ArcRun_isMetadataSheetName(name: str) -> bool:
    return name == "isa_run"


def ArcRun_isMetadataSheet(sheet: FsWorksheet) -> bool:
    return ArcRun_isMetadataSheetName(sheet.Name)


def ArcRun_tryGetMetadataSheet(doc: FsWorkbook) -> FsWorksheet | None:
    def predicate(sheet: FsWorksheet, doc: Any=doc) -> bool:
        return ArcRun_isMetadataSheet(sheet)

    return try_find(predicate, doc.GetWorksheets())


def ARCtrl_ArcRun__ArcRun_fromFsWorkbook_Static_32154C9D(doc: FsWorkbook) -> ArcRun:
    try: 
        run_metadata: ArcRun
        match_value: FsWorksheet | None = ArcRun_tryGetMetadataSheet(doc)
        if match_value is None:
            to_console(printf("Cannot retrieve metadata: Run file does not contain \"%s\" sheet."))("isa_run")
            run_metadata = ArcRun.create(create_missing_identifier())

        else: 
            run_metadata = ArcRun_fromMetadataSheet(match_value)

        sheets: Array[FsWorksheet] = doc.GetWorksheets()
        annotation_tables: IEnumerable_1[ArcTable] = choose(try_from_fs_worksheet, sheets)
        datamap_sheet: Datamap | None = try_pick(try_from_fs_worksheet_1, sheets)
        run_metadata.Datamap = datamap_sheet
        if not is_empty(annotation_tables):
            run_metadata.Tables = list(annotation_tables)

        return run_metadata

    except Exception as err:
        arg_1: str = str(err)
        return to_fail(printf("Could not parse assay: \n%s"))(arg_1)



def ARCtrl_ArcRun__ArcRun_toFsWorkbook_Static_Z3EFAF6F8(run: ArcRun) -> FsWorkbook:
    doc: FsWorkbook = FsWorkbook()
    metadata_sheet: FsWorksheet = ArcRun_toMetadataSheet(run)
    doc.AddWorksheet(metadata_sheet)
    def action(i: int, arg: ArcTable, run: Any=run) -> None:
        sheet: FsWorksheet = to_fs_worksheet(i, arg)
        doc.AddWorksheet(sheet)

    iterate_indexed(action, run.Tables)
    return doc


def ARCtrl_ArcRun__ArcRun_ToFsWorkbook(this: ArcRun) -> FsWorkbook:
    return ARCtrl_ArcRun__ArcRun_toFsWorkbook_Static_Z3EFAF6F8(this)


__all__ = ["ArcRun_fromRows", "ArcRun_toRows", "ArcRun_toMetadataSheet", "ArcRun_fromMetadataSheet", "ArcRun_toMetadataCollection", "ArcRun_fromMetadataCollection", "ArcRun_isMetadataSheetName", "ArcRun_isMetadataSheet", "ArcRun_tryGetMetadataSheet", "ARCtrl_ArcRun__ArcRun_fromFsWorkbook_Static_32154C9D", "ARCtrl_ArcRun__ArcRun_toFsWorkbook_Static_Z3EFAF6F8", "ARCtrl_ArcRun__ArcRun_ToFsWorkbook"]

