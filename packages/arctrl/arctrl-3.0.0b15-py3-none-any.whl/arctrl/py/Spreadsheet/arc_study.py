from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.list import (FSharpList, empty)
from ..fable_modules.fable_library.option import (default_arg, to_array)
from ..fable_modules.fable_library.seq import (iterate_indexed, append, map, try_find, try_pick, iterate)
from ..fable_modules.fable_library.string_ import (to_fail, printf, to_console)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (IEnumerable_1, to_enumerable, get_enumerator, IEnumerator, ignore)
from ..fable_modules.fs_spreadsheet.fs_row import FsRow
from ..fable_modules.fs_spreadsheet.fs_workbook import FsWorkbook
from ..fable_modules.fs_spreadsheet.fs_worksheet import FsWorksheet
from ..Core.arc_types import (ArcStudy, ArcAssay)
from ..Core.datamap import Datamap
from ..Core.Helper.collections_ import (ResizeArray_choose, ResizeArray_isEmpty)
from ..Core.Helper.identifier import create_missing_identifier
from ..Core.Table.arc_table import ArcTable
from .AnnotationTable.arc_table import (try_from_fs_worksheet, to_fs_worksheet as to_fs_worksheet_1)
from .DatamapTable.datamap_table import (try_from_fs_worksheet as try_from_fs_worksheet_1, to_fs_worksheet)
from .Metadata.sparse_table import (SparseRowModule_writeToSheet, SparseRowModule_fromValues, SparseRowModule_fromFsRow, SparseRowModule_getAllValues, SparseRowModule_fromAllValues)
from .Metadata.study import (to_rows, from_rows)

def ArcStudy_toMetadataSheet(study: ArcStudy, assays: FSharpList[ArcAssay] | None=None) -> FsWorksheet:
    sheet: FsWorksheet = FsWorksheet("isa_study")
    def action(row_i: int, r: IEnumerable_1[tuple[int, str]], study: Any=study, assays: Any=assays) -> None:
        SparseRowModule_writeToSheet(row_i + 1, r, sheet)

    def _arrow1592(__unit: None=None, study: Any=study, assays: Any=assays) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
        source_1: IEnumerable_1[IEnumerable_1[tuple[int, str]]] = to_rows(study, assays)
        return append(to_enumerable([SparseRowModule_fromValues(to_enumerable(["STUDY"]))]), source_1)

    iterate_indexed(action, _arrow1592())
    return sheet


def ArcStudy_fromRows(rows: IEnumerable_1[IEnumerable_1[tuple[int, str]]]) -> tuple[ArcStudy, FSharpList[ArcAssay]] | None:
    en: IEnumerator[IEnumerable_1[tuple[int, str]]] = get_enumerator(rows)
    ignore(en.System_Collections_IEnumerator_MoveNext())
    return from_rows(2, en)[3]


def ArcStudy_fromMetadataSheet(sheet: FsWorksheet) -> tuple[ArcStudy, FSharpList[ArcAssay]]:
    try: 
        return default_arg(ArcStudy_fromRows(map(SparseRowModule_fromFsRow, sheet.Rows)), (ArcStudy.create(create_missing_identifier()), empty()))

    except Exception as err:
        arg: str = str(err)
        return to_fail(printf("Failed while parsing metadatasheet: %s"))(arg)



def ArcStudy_toMetadataCollection(study: ArcStudy, assays: FSharpList[ArcAssay] | None=None) -> IEnumerable_1[IEnumerable_1[str | None]]:
    def mapping(row: IEnumerable_1[tuple[int, str]], study: Any=study, assays: Any=assays) -> IEnumerable_1[str | None]:
        return SparseRowModule_getAllValues(row)

    def _arrow1593(__unit: None=None, study: Any=study, assays: Any=assays) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
        source_1: IEnumerable_1[IEnumerable_1[tuple[int, str]]] = to_rows(study, assays)
        return append(to_enumerable([SparseRowModule_fromValues(to_enumerable(["STUDY"]))]), source_1)

    return map(mapping, _arrow1593())


def ArcStudy_fromMetadataCollection(collection: IEnumerable_1[IEnumerable_1[str | None]]) -> tuple[ArcStudy, FSharpList[ArcAssay]]:
    try: 
        return default_arg(ArcStudy_fromRows(map(SparseRowModule_fromAllValues, collection)), (ArcStudy.create(create_missing_identifier()), empty()))

    except Exception as err:
        arg: str = str(err)
        return to_fail(printf("Failed while parsing metadatasheet: %s"))(arg)



def ArcStudy_isMetadataSheetName(name: str) -> bool:
    if name == "isa_study":
        return True

    else: 
        return name == "Study"



def ArcStudy_isMetadataSheet(sheet: FsWorksheet) -> bool:
    return ArcStudy_isMetadataSheetName(sheet.Name)


def ArcStudy_tryGetMetadataSheet(doc: FsWorkbook) -> FsWorksheet | None:
    def predicate(sheet: FsWorksheet, doc: Any=doc) -> bool:
        return ArcStudy_isMetadataSheet(sheet)

    return try_find(predicate, doc.GetWorksheets())


def ARCtrl_ArcStudy__ArcStudy_fromFsWorkbook_Static_32154C9D(doc: FsWorkbook) -> tuple[ArcStudy, FSharpList[ArcAssay]]:
    try: 
        pattern_input: tuple[ArcStudy, FSharpList[ArcAssay]]
        match_value: FsWorksheet | None = ArcStudy_tryGetMetadataSheet(doc)
        if match_value is None:
            to_console(printf("Cannot retrieve metadata: Study file does not contain \"%s\" or \"%s\" sheet."))("isa_study")("Study")
            pattern_input = (ArcStudy.create(create_missing_identifier()), empty())

        else: 
            pattern_input = ArcStudy_fromMetadataSheet(match_value)

        study_metadata: ArcStudy = pattern_input[0]
        sheets: Array[FsWorksheet] = doc.GetWorksheets()
        annotation_tables: Array[ArcTable] = ResizeArray_choose(try_from_fs_worksheet, sheets)
        datamap_sheet: Datamap | None = try_pick(try_from_fs_worksheet_1, sheets)
        if not ResizeArray_isEmpty(annotation_tables):
            study_metadata.Tables = annotation_tables

        study_metadata.Datamap = datamap_sheet
        return (study_metadata, pattern_input[1])

    except Exception as err:
        arg_2: str = str(err)
        return to_fail(printf("Could not parse study: \n%s"))(arg_2)



def ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522(study: ArcStudy, assays: FSharpList[ArcAssay] | None=None, datamap_sheet: bool | None=None) -> FsWorkbook:
    datamap_sheet_1: bool = default_arg(datamap_sheet, True)
    doc: FsWorkbook = FsWorkbook()
    metadata_sheet: FsWorksheet = ArcStudy_toMetadataSheet(study, assays)
    doc.AddWorksheet(metadata_sheet)
    if datamap_sheet_1:
        def action(arg: Datamap, study: Any=study, assays: Any=assays, datamap_sheet: Any=datamap_sheet) -> None:
            sheet: FsWorksheet = to_fs_worksheet(arg)
            doc.AddWorksheet(sheet)

        iterate(action, to_array(study.Datamap))

    def action_1(i: int, arg_1: ArcTable, study: Any=study, assays: Any=assays, datamap_sheet: Any=datamap_sheet) -> None:
        sheet_1: FsWorksheet = to_fs_worksheet_1(i, arg_1)
        doc.AddWorksheet(sheet_1)

    iterate_indexed(action_1, study.Tables)
    return doc


def ARCtrl_ArcStudy__ArcStudy_ToFsWorkbook_257FC1F0(this: ArcStudy, assays: FSharpList[ArcAssay] | None=None, datamap_sheet: bool | None=None) -> FsWorkbook:
    return ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522(this, assays, datamap_sheet)


__all__ = ["ArcStudy_toMetadataSheet", "ArcStudy_fromRows", "ArcStudy_fromMetadataSheet", "ArcStudy_toMetadataCollection", "ArcStudy_fromMetadataCollection", "ArcStudy_isMetadataSheetName", "ArcStudy_isMetadataSheet", "ArcStudy_tryGetMetadataSheet", "ARCtrl_ArcStudy__ArcStudy_fromFsWorkbook_Static_32154C9D", "ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522", "ARCtrl_ArcStudy__ArcStudy_ToFsWorkbook_257FC1F0"]

