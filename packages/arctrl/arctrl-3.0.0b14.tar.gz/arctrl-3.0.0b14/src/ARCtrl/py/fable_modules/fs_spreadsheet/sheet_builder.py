from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import (Any, Generic, TypeVar)
from ..fable_library.guid import new_guid
from ..fable_library.list import (FSharpList, empty as empty_1, append, singleton, concat, map as map_1, is_empty, iterate)
from ..fable_library.map_util import (try_get_value, add_to_dict)
from ..fable_library.option import (some, to_nullable)
from ..fable_library.reflection import (TypeInfo, lambda_type, list_type, float64_type, option_type, bool_type, string_type, record_type)
from ..fable_library.seq import (indexed, find)
from ..fable_library.types import (FSharpRef, Record)
from ..fable_library.util import (curry2, ignore, get_enumerator, IEnumerable_1, equals)
from .Cells.fs_cell import (FsCell, FsCell_reflection)
from .Cells.fs_cells_collection import FsCellsCollection
from .fs_address import FsAddress
from .fs_row import FsRow
from .fs_workbook import FsWorkbook
from .fs_worksheet import FsWorksheet
from .Ranges.fs_range_address import FsRangeAddress
from .Tables.fs_table import FsTable
from .Tables.fs_table_field import FsTableField

_V = TypeVar("_V")

_T = TypeVar("_T")

def Dictionary_tryGetValue(k: Any, dict_1: Any) -> Any | None:
    pattern_input: tuple[bool, _V]
    out_arg: _V = None
    def _arrow241(__unit: None=None, k: Any=k, dict_1: Any=dict_1) -> _V:
        return out_arg

    def _arrow242(v: _V | None=None, k: Any=k, dict_1: Any=dict_1) -> None:
        nonlocal out_arg
        out_arg = v

    pattern_input = (try_get_value(dict_1, k, FSharpRef(_arrow241, _arrow242)), out_arg)
    if pattern_input[0]:
        return some(pattern_input[1])

    else: 
        return None



def Dictionary_length(dict_1: Any) -> int:
    return len(dict_1)


def _expr243(gen0: TypeInfo) -> TypeInfo:
    return record_type("FsSpreadsheet.SheetBuilder.FieldMap`1", [gen0], FieldMap_1, lambda: [("CellTransformers", list_type(lambda_type(gen0, lambda_type(FsCell_reflection(), FsCell_reflection())))), ("HeaderTransformers", list_type(lambda_type(gen0, lambda_type(FsCell_reflection(), FsCell_reflection())))), ("ColumnWidth", option_type(float64_type)), ("RowHeight", option_type(lambda_type(gen0, option_type(float64_type)))), ("AdjustToContents", bool_type), ("Hash", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class FieldMap_1(Record, Generic[_T]):
    CellTransformers: FSharpList[Callable[[_T, FsCell], FsCell]]
    HeaderTransformers: FSharpList[Callable[[_T, FsCell], FsCell]]
    ColumnWidth: float | None
    RowHeight: Callable[[_T], float | None] | None
    AdjustToContents: bool
    Hash: str

FieldMap_1_reflection = _expr243

def FieldMap_1_empty(__unit: None=None) -> FieldMap_1[Any]:
    def _arrow244(__unit: None=None) -> str:
        copy_of_struct: str = new_guid()
        return str(copy_of_struct)

    return FieldMap_1(empty_1(), empty_1(), None, None, False, _arrow244())


def FieldMap_1_create_Z3BCCB7EB(map_row: Callable[[_T, FsCell], FsCell]) -> FieldMap_1[Any]:
    empty: FieldMap_1[_T] = FieldMap_1_empty()
    return FieldMap_1(append(empty.CellTransformers, singleton(curry2(map_row))), empty.HeaderTransformers, empty.ColumnWidth, empty.RowHeight, empty.AdjustToContents, empty.Hash)


def FieldMap_1__header_Z721C83C5(self_1: FieldMap_1[Any], name: str) -> FieldMap_1[Any]:
    def transformer(_arg: _T | None=None, self_1: Any=self_1, name: Any=name) -> Callable[[FsCell], FsCell]:
        def _arrow245(cell: FsCell, _arg: Any=_arg) -> FsCell:
            cell.SetValueAs(name)
            return cell

        return _arrow245

    return FieldMap_1(self_1.CellTransformers, append(self_1.HeaderTransformers, singleton(transformer)), self_1.ColumnWidth, self_1.RowHeight, self_1.AdjustToContents, self_1.Hash)


def FieldMap_1__header_54F19B58(self_1: FieldMap_1[Any], map_header: Callable[[_T], str]) -> FieldMap_1[Any]:
    def transformer(value: _T | None=None, self_1: Any=self_1, map_header: Any=map_header) -> Callable[[FsCell], FsCell]:
        def _arrow246(cell: FsCell, value: Any=value) -> FsCell:
            cell.SetValueAs(map_header(value))
            return cell

        return _arrow246

    return FieldMap_1(self_1.CellTransformers, append(self_1.HeaderTransformers, singleton(transformer)), self_1.ColumnWidth, self_1.RowHeight, self_1.AdjustToContents, self_1.Hash)


def FieldMap_1__adjustToContents(self_1: FieldMap_1[Any]) -> FieldMap_1[Any]:
    return FieldMap_1(self_1.CellTransformers, self_1.HeaderTransformers, self_1.ColumnWidth, self_1.RowHeight, True, self_1.Hash)


def FieldMap_1_field_Z5C94BCA1(map: Callable[[_T], int]) -> FieldMap_1[Any]:
    def _arrow247(row: Any, cell: FsCell, map: Any=map) -> FsCell:
        cell.SetValueAs(map(row))
        return cell

    return FieldMap_1_create_Z3BCCB7EB(_arrow247)


def FieldMap_1_field_54F19B58(map: Callable[[_T], str]) -> FieldMap_1[Any]:
    def _arrow248(row: Any, cell: FsCell, map: Any=map) -> FsCell:
        cell.SetValueAs(map(row))
        return cell

    return FieldMap_1_create_Z3BCCB7EB(_arrow248)


def FieldMap_1_field_477D79EC(map: Callable[[_T], Any]) -> FieldMap_1[Any]:
    def _arrow249(row: Any, cell: FsCell, map: Any=map) -> FsCell:
        cell.SetValueAs(map(row))
        return cell

    return FieldMap_1_create_Z3BCCB7EB(_arrow249)


def FieldMap_1_field_Z1D55A0D7(map: Callable[[_T], bool]) -> FieldMap_1[Any]:
    def _arrow250(row: Any, cell: FsCell, map: Any=map) -> FsCell:
        cell.SetValueAs(map(row))
        return cell

    return FieldMap_1_create_Z3BCCB7EB(_arrow250)


def FieldMap_1_field_298D8758(map: Callable[[_T], float]) -> FieldMap_1[Any]:
    def _arrow251(row: Any, cell: FsCell, map: Any=map) -> FsCell:
        cell.SetValueAs(map(row))
        return cell

    return FieldMap_1_create_Z3BCCB7EB(_arrow251)


def FieldMap_1_field_Z78848E24(map: Callable[[_T], int | None]) -> FieldMap_1[Any]:
    def _arrow252(row: Any, cell: FsCell, map: Any=map) -> FsCell:
        cell.SetValueAs(to_nullable(map(row)))
        return cell

    return FieldMap_1_create_Z3BCCB7EB(_arrow252)


def FieldMap_1_field_4C14CE8F(map: Callable[[_T], Any | None]) -> FieldMap_1[Any]:
    def _arrow253(row: Any, cell: FsCell, map: Any=map) -> FsCell:
        cell.SetValueAs(to_nullable(map(row)))
        return cell

    return FieldMap_1_create_Z3BCCB7EB(_arrow253)


def FieldMap_1_field_Z404517D6(map: Callable[[_T], bool | None]) -> FieldMap_1[Any]:
    def _arrow254(row: Any, cell: FsCell, map: Any=map) -> FsCell:
        cell.SetValueAs(to_nullable(map(row)))
        return cell

    return FieldMap_1_create_Z3BCCB7EB(_arrow254)


def FieldMap_1_field_Z14464045(map: Callable[[_T], float | None]) -> FieldMap_1[Any]:
    def _arrow255(row: Any, cell: FsCell, map: Any=map) -> FsCell:
        cell.SetValueAs(to_nullable(map(row)))
        return cell

    return FieldMap_1_create_Z3BCCB7EB(_arrow255)


def FieldMap_1_field_33F53BB(map: Callable[[_T], str | None]) -> FieldMap_1[Any]:
    def _arrow257(row: Any, cell: FsCell, map: Any=map) -> FsCell:
        match_value: str | None = map(row)
        if match_value is not None:
            text: str = match_value
            cell.SetValueAs(text)
            return cell

        else: 
            return cell


    return FieldMap_1_create_Z3BCCB7EB(_arrow257)


def FsSpreadsheet_FsTable__FsTable_Populate_526F9CF7(self_1: FsTable, cells: FsCellsCollection, data: IEnumerable_1[Any], fields: FSharpList[FieldMap_1[Any]]) -> None:
    def mapping(field: FieldMap_1[_T], self_1: Any=self_1, cells: Any=cells, data: Any=data, fields: Any=fields) -> FSharpList[Callable[[_T, FsCell], FsCell]]:
        return field.HeaderTransformers

    headers_available: bool = not is_empty(concat(map_1(mapping, fields)))
    if (self_1.ShowHeaderRow == False) if headers_available else False:
        self_1.ShowHeaderRow = headers_available

    start_address: FsAddress = self_1.RangeAddress.FirstAddress
    start_row_index: int = ((start_address.RowNumber + 1) if headers_available else start_address.RowNumber) or 0
    with get_enumerator(indexed(data)) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            for_loop_var: tuple[int, _T] = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            row: _T = for_loop_var[1]
            active_row_index: int = (for_loop_var[0] + start_row_index) or 0
            with get_enumerator(fields) as enumerator_1:
                while enumerator_1.System_Collections_IEnumerator_MoveNext():
                    field_1: FieldMap_1[_T] = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                    header_cell: FsCell = FsCell.create_empty()
                    with get_enumerator(field_1.HeaderTransformers) as enumerator_2:
                        while enumerator_2.System_Collections_IEnumerator_MoveNext():
                            ignore(enumerator_2.System_Collections_Generic_IEnumerator_1_get_Current()(row)(header_cell))
                    header_string: str = field_1.Hash if (header_cell.ValueAsString() == "") else header_cell.ValueAsString()
                    table_field: FsTableField = self_1.Field(header_string, cells)
                    active_cell: FsCell = table_field.Column.Cell(active_row_index, cells)
                    with get_enumerator(field_1.CellTransformers) as enumerator_3:
                        while enumerator_3.System_Collections_IEnumerator_MoveNext():
                            ignore(enumerator_3.System_Collections_Generic_IEnumerator_1_get_Current()(row)(active_cell))


def FsSpreadsheet_FsTable__FsTable_populate_Static_Z735E4C44(table: FsTable, cells: FsCellsCollection, data: IEnumerable_1[Any], fields: FSharpList[FieldMap_1[Any]]) -> None:
    FsSpreadsheet_FsTable__FsTable_Populate_526F9CF7(table, cells, data, fields)


def FsSpreadsheet_FsWorksheet__FsWorksheet_Populate_Z2A1350BF(self_1: FsWorksheet, data: IEnumerable_1[Any], fields: FSharpList[FieldMap_1[Any]]) -> None:
    def mapping(field: FieldMap_1[_T], self_1: Any=self_1, data: Any=data, fields: Any=fields) -> FSharpList[Callable[[_T, FsCell], FsCell]]:
        return field.HeaderTransformers

    headers_available: bool = not is_empty(concat(map_1(mapping, fields)))
    headers: Any = dict([])
    with get_enumerator(indexed(data)) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            for_loop_var: tuple[int, _T] = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            row: _T = for_loop_var[1]
            start_row_index: int = (2 if headers_available else 1) or 0
            active_row: FsRow = self_1.Row(for_loop_var[0] + start_row_index)
            with get_enumerator(fields) as enumerator_1:
                while enumerator_1.System_Collections_IEnumerator_MoveNext():
                    field_1: FieldMap_1[_T] = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                    header_cell: FsCell = FsCell.create_empty()
                    with get_enumerator(field_1.HeaderTransformers) as enumerator_2:
                        while enumerator_2.System_Collections_IEnumerator_MoveNext():
                            ignore(enumerator_2.System_Collections_Generic_IEnumerator_1_get_Current()(row)(header_cell))
                    index: int
                    pattern_input: tuple[bool, str] = ((False, field_1.Hash)) if equals(header_cell.Value, "") else ((True, header_cell.ValueAsString()))
                    header_string: str = pattern_input[1]
                    match_value: int | None = Dictionary_tryGetValue(header_string, headers)
                    if match_value is None:
                        i: int = (len(headers) + 1) or 0
                        add_to_dict(headers, header_string, i)
                        if pattern_input[0]:
                            value: None = self_1.Row(1).Item(i).CopyFrom(header_cell)
                            ignore(None)

                        index = i

                    else: 
                        index = match_value

                    active_cell: FsCell = active_row.Item(index)
                    with get_enumerator(field_1.CellTransformers) as enumerator_3:
                        while enumerator_3.System_Collections_IEnumerator_MoveNext():
                            ignore(enumerator_3.System_Collections_Generic_IEnumerator_1_get_Current()(row)(active_cell))
    self_1.SortRows()


def FsSpreadsheet_FsWorksheet__FsWorksheet_populate_Static_Z2578A106(sheet: FsWorksheet, data: IEnumerable_1[Any], fields: FSharpList[FieldMap_1[Any]]) -> None:
    FsSpreadsheet_FsWorksheet__FsWorksheet_Populate_Z2A1350BF(sheet, data, fields)


def FsSpreadsheet_FsWorksheet__FsWorksheet_createFrom_Static_Z2DEFA746(name: str, data: IEnumerable_1[Any], fields: FSharpList[FieldMap_1[Any]]) -> FsWorksheet:
    sheet: FsWorksheet = FsWorksheet(name)
    FsSpreadsheet_FsWorksheet__FsWorksheet_populate_Static_Z2578A106(sheet, data, fields)
    return sheet


def FsSpreadsheet_FsWorksheet__FsWorksheet_createFrom_Static_Z2A1350BF(data: IEnumerable_1[Any], fields: FSharpList[FieldMap_1[Any]]) -> FsWorksheet:
    return FsSpreadsheet_FsWorksheet__FsWorksheet_createFrom_Static_Z2DEFA746("Sheet1", data, fields)


def FsSpreadsheet_FsWorksheet__FsWorksheet_PopulateTable_59F260F9(self_1: FsWorksheet, table_name: str, start_address: FsAddress, data: IEnumerable_1[Any], fields: FSharpList[FieldMap_1[Any]]) -> None:
    def mapping(field: FieldMap_1[_T], self_1: Any=self_1, table_name: Any=table_name, start_address: Any=start_address, data: Any=data, fields: Any=fields) -> FSharpList[Callable[[_T, FsCell], FsCell]]:
        return field.HeaderTransformers

    headers_available: bool = not is_empty(concat(map_1(mapping, fields)))
    FsSpreadsheet_FsTable__FsTable_Populate_526F9CF7(self_1.Table(table_name, FsRangeAddress(start_address, start_address), headers_available), self_1.CellCollection, data, fields)
    self_1.SortRows()


def FsSpreadsheet_FsWorksheet__FsWorksheet_createTableFrom_Static_30234BE1(name: str, table_name: str, data: IEnumerable_1[Any], fields: FSharpList[FieldMap_1[Any]]) -> FsWorksheet:
    sheet: FsWorksheet = FsWorksheet(name)
    FsSpreadsheet_FsWorksheet__FsWorksheet_PopulateTable_59F260F9(sheet, table_name, FsAddress(1, 1), data, fields)
    return sheet


def FsSpreadsheet_FsWorkbook__FsWorkbook_Populate_Z2DEFA746(self_1: FsWorkbook, name: str, data: IEnumerable_1[Any], fields: FSharpList[FieldMap_1[Any]]) -> None:
    ignore(self_1.InitWorksheet(name))
    def predicate(s: FsWorksheet, self_1: Any=self_1, name: Any=name, data: Any=data, fields: Any=fields) -> bool:
        return s.Name == name

    FsSpreadsheet_FsWorksheet__FsWorksheet_populate_Static_Z2578A106(find(predicate, self_1.GetWorksheets()), data, fields)


def FsSpreadsheet_FsWorkbook__FsWorkbook_populate_Static_Z7163EB39(workbook: FsWorkbook, name: str, data: IEnumerable_1[Any], fields: FSharpList[FieldMap_1[Any]]) -> None:
    FsSpreadsheet_FsWorkbook__FsWorkbook_Populate_Z2DEFA746(workbook, name, data, fields)


def FsSpreadsheet_FsWorkbook__FsWorkbook_createFrom_Static_Z2DEFA746(name: str, data: IEnumerable_1[Any], fields: FSharpList[FieldMap_1[Any]]) -> FsWorkbook:
    workbook: FsWorkbook = FsWorkbook()
    FsSpreadsheet_FsWorkbook__FsWorkbook_populate_Static_Z7163EB39(workbook, name, data, fields)
    return workbook


def FsSpreadsheet_FsWorkbook__FsWorkbook_createFrom_Static_Z2A1350BF(data: IEnumerable_1[Any], fields: FSharpList[FieldMap_1[Any]]) -> FsWorkbook:
    return FsSpreadsheet_FsWorkbook__FsWorkbook_createFrom_Static_Z2DEFA746("Sheet1", data, fields)


def FsSpreadsheet_FsWorkbook__FsWorkbook_createFrom_Static_Z2E36FAE7(sheets: FSharpList[FsWorksheet]) -> FsWorkbook:
    workbook: FsWorkbook = FsWorkbook()
    def action(sheet: FsWorksheet, sheets: Any=sheets) -> None:
        value: None = workbook.AddWorksheet(sheet)
        ignore(None)

    iterate(action, sheets)
    return workbook


__all__ = ["Dictionary_tryGetValue", "Dictionary_length", "FieldMap_1_reflection", "FieldMap_1_empty", "FieldMap_1_create_Z3BCCB7EB", "FieldMap_1__header_Z721C83C5", "FieldMap_1__header_54F19B58", "FieldMap_1__adjustToContents", "FieldMap_1_field_Z5C94BCA1", "FieldMap_1_field_54F19B58", "FieldMap_1_field_477D79EC", "FieldMap_1_field_Z1D55A0D7", "FieldMap_1_field_298D8758", "FieldMap_1_field_Z78848E24", "FieldMap_1_field_4C14CE8F", "FieldMap_1_field_Z404517D6", "FieldMap_1_field_Z14464045", "FieldMap_1_field_33F53BB", "FsSpreadsheet_FsTable__FsTable_Populate_526F9CF7", "FsSpreadsheet_FsTable__FsTable_populate_Static_Z735E4C44", "FsSpreadsheet_FsWorksheet__FsWorksheet_Populate_Z2A1350BF", "FsSpreadsheet_FsWorksheet__FsWorksheet_populate_Static_Z2578A106", "FsSpreadsheet_FsWorksheet__FsWorksheet_createFrom_Static_Z2DEFA746", "FsSpreadsheet_FsWorksheet__FsWorksheet_createFrom_Static_Z2A1350BF", "FsSpreadsheet_FsWorksheet__FsWorksheet_PopulateTable_59F260F9", "FsSpreadsheet_FsWorksheet__FsWorksheet_createTableFrom_Static_30234BE1", "FsSpreadsheet_FsWorkbook__FsWorkbook_Populate_Z2DEFA746", "FsSpreadsheet_FsWorkbook__FsWorkbook_populate_Static_Z7163EB39", "FsSpreadsheet_FsWorkbook__FsWorkbook_createFrom_Static_Z2DEFA746", "FsSpreadsheet_FsWorkbook__FsWorkbook_createFrom_Static_Z2A1350BF", "FsSpreadsheet_FsWorkbook__FsWorkbook_createFrom_Static_Z2E36FAE7"]

