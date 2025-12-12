from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (FSharpList, empty, of_seq)
from ..fable_modules.fable_library.seq import (delay, append, singleton, iterate_indexed, map, try_find, try_pick)
from ..fable_modules.fable_library.string_ import (to_fail, printf, to_console)
from ..fable_modules.fable_library.util import (get_enumerator, IEnumerable_1, IEnumerator, to_enumerable)
from ..fable_modules.fs_spreadsheet.fs_row import FsRow
from ..fable_modules.fs_spreadsheet.fs_workbook import FsWorkbook
from ..fable_modules.fs_spreadsheet.fs_worksheet import FsWorksheet
from ..Core.arc_types import ArcWorkflow
from ..Core.comment import Remark
from ..Core.datamap import Datamap
from ..Core.Helper.identifier import create_missing_identifier
from ..Core.person import Person
from .DatamapTable.datamap_table import try_from_fs_worksheet
from .Metadata.contacts import (from_rows as from_rows_1, to_rows as to_rows_1)
from .Metadata.sparse_table import (SparseRowModule_tryGetValueAt, SparseRowModule_fromValues, SparseRowModule_writeToSheet, SparseRowModule_fromFsRow, SparseRowModule_getAllValues, SparseRowModule_fromAllValues)
from .Metadata.workflow import (from_rows, to_rows)

def ArcWorkflow_fromRows(rows: IEnumerable_1[IEnumerable_1[tuple[int, str]]]) -> ArcWorkflow:
    en: IEnumerator[IEnumerable_1[tuple[int, str]]] = get_enumerator(rows)
    def loop(last_row_mut: str | None, workflow_mut: ArcWorkflow | None, contacts_mut: FSharpList[Person], row_number_mut: int, rows: Any=rows) -> ArcWorkflow:
        while True:
            (last_row, workflow, contacts, row_number) = (last_row_mut, workflow_mut, contacts_mut, row_number_mut)
            (pattern_matching_result,) = (None,)
            if last_row is not None:
                if last_row == "WORKFLOW":
                    pattern_matching_result = 0

                elif last_row == "WORKFLOW CONTACTS":
                    pattern_matching_result = 1

                else: 
                    pattern_matching_result = 2


            else: 
                pattern_matching_result = 2

            if pattern_matching_result == 0:
                pattern_input: tuple[str | None, int, FSharpList[Remark], ArcWorkflow] = from_rows(row_number + 1, en)
                last_row_mut = pattern_input[0]
                workflow_mut = pattern_input[3]
                contacts_mut = contacts
                row_number_mut = pattern_input[1]
                continue

            elif pattern_matching_result == 1:
                pattern_input_1: tuple[str | None, int, FSharpList[Remark], FSharpList[Person]] = from_rows_1("Workflow Person", row_number + 1, en)
                last_row_mut = pattern_input_1[0]
                workflow_mut = workflow
                contacts_mut = pattern_input_1[3]
                row_number_mut = pattern_input_1[1]
                continue

            elif pattern_matching_result == 2:
                if workflow is not None:
                    workflow_2: ArcWorkflow = workflow
                    workflow_2.Contacts = list(contacts)
                    return workflow_2

                else: 
                    return ArcWorkflow.create(create_missing_identifier(), None, None, None, None, None, None, None, None, None, list(contacts))


            break

    if en.System_Collections_IEnumerator_MoveNext():
        return loop(SparseRowModule_tryGetValueAt(0, en.System_Collections_Generic_IEnumerator_1_get_Current()), None, empty(), 1)

    else: 
        raise Exception("empty workflow metadata sheet")



def ArcWorkflow_toRows(workflow: ArcWorkflow) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    def _arrow1597(__unit: None=None, workflow: Any=workflow) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
        def _arrow1596(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
            def _arrow1595(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                def _arrow1594(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
                    return to_rows_1("Workflow Person", of_seq(workflow.Contacts))

                return append(singleton(SparseRowModule_fromValues(to_enumerable(["WORKFLOW CONTACTS"]))), delay(_arrow1594))

            return append(to_rows(workflow), delay(_arrow1595))

        return append(singleton(SparseRowModule_fromValues(to_enumerable(["WORKFLOW"]))), delay(_arrow1596))

    return delay(_arrow1597)


def ArcWorkflow_toMetadataSheet(workflow: ArcWorkflow) -> FsWorksheet:
    sheet: FsWorksheet = FsWorksheet("isa_workflow")
    def action(row_i: int, r: IEnumerable_1[tuple[int, str]], workflow: Any=workflow) -> None:
        SparseRowModule_writeToSheet(row_i + 1, r, sheet)

    iterate_indexed(action, ArcWorkflow_toRows(workflow))
    return sheet


def ArcWorkflow_fromMetadataSheet(sheet: FsWorksheet) -> ArcWorkflow:
    try: 
        return ArcWorkflow_fromRows(map(SparseRowModule_fromFsRow, sheet.Rows))

    except Exception as err:
        arg: str = str(err)
        return to_fail(printf("Failed while parsing metadatasheet: %s"))(arg)



def ArcWorkflow_toMetadataCollection(workflow: ArcWorkflow) -> IEnumerable_1[IEnumerable_1[str | None]]:
    def mapping(row: IEnumerable_1[tuple[int, str]], workflow: Any=workflow) -> IEnumerable_1[str | None]:
        return SparseRowModule_getAllValues(row)

    return map(mapping, ArcWorkflow_toRows(workflow))


def ArcWorkflow_fromMetadataCollection(collection: IEnumerable_1[IEnumerable_1[str | None]]) -> ArcWorkflow:
    try: 
        return ArcWorkflow_fromRows(map(SparseRowModule_fromAllValues, collection))

    except Exception as err:
        arg: str = str(err)
        return to_fail(printf("Failed while parsing metadatasheet: %s"))(arg)



def ArcWorkflow_isMetadataSheetName(name: str) -> bool:
    return name == "isa_workflow"


def ArcWorkflow_isMetadataSheet(sheet: FsWorksheet) -> bool:
    return ArcWorkflow_isMetadataSheetName(sheet.Name)


def ArcWorkflow_tryGetMetadataSheet(doc: FsWorkbook) -> FsWorksheet | None:
    def predicate(sheet: FsWorksheet, doc: Any=doc) -> bool:
        return ArcWorkflow_isMetadataSheet(sheet)

    return try_find(predicate, doc.GetWorksheets())


def ARCtrl_ArcWorkflow__ArcWorkflow_fromFsWorkbook_Static_32154C9D(doc: FsWorkbook) -> ArcWorkflow:
    try: 
        workflow_metadata: ArcWorkflow
        match_value: FsWorksheet | None = ArcWorkflow_tryGetMetadataSheet(doc)
        if match_value is None:
            to_console(printf("Cannot retrieve metadata: Workflow file does not contain \"%s\" sheet."))("isa_workflow")
            workflow_metadata = ArcWorkflow.create(create_missing_identifier())

        else: 
            workflow_metadata = ArcWorkflow_fromMetadataSheet(match_value)

        datamap_sheet: Datamap | None = try_pick(try_from_fs_worksheet, doc.GetWorksheets())
        workflow_metadata.Datamap = datamap_sheet
        return workflow_metadata

    except Exception as err:
        arg_1: str = str(err)
        return to_fail(printf("Could not parse assay: \n%s"))(arg_1)



def ARCtrl_ArcWorkflow__ArcWorkflow_toFsWorkbook_Static_Z1C75CB0E(workflow: ArcWorkflow) -> FsWorkbook:
    doc: FsWorkbook = FsWorkbook()
    metadata_sheet: FsWorksheet = ArcWorkflow_toMetadataSheet(workflow)
    doc.AddWorksheet(metadata_sheet)
    return doc


def ARCtrl_ArcWorkflow__ArcWorkflow_ToFsWorkbook(this: ArcWorkflow) -> FsWorkbook:
    return ARCtrl_ArcWorkflow__ArcWorkflow_toFsWorkbook_Static_Z1C75CB0E(this)


__all__ = ["ArcWorkflow_fromRows", "ArcWorkflow_toRows", "ArcWorkflow_toMetadataSheet", "ArcWorkflow_fromMetadataSheet", "ArcWorkflow_toMetadataCollection", "ArcWorkflow_fromMetadataCollection", "ArcWorkflow_isMetadataSheetName", "ArcWorkflow_isMetadataSheet", "ArcWorkflow_tryGetMetadataSheet", "ARCtrl_ArcWorkflow__ArcWorkflow_fromFsWorkbook_Static_32154C9D", "ARCtrl_ArcWorkflow__ArcWorkflow_toFsWorkbook_Static_Z1C75CB0E", "ARCtrl_ArcWorkflow__ArcWorkflow_ToFsWorkbook"]

